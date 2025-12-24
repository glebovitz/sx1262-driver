from base import BaseLoRa
import spidev
import RPi.GPIO
import time
from sx1262_constants import *

class SX1262Receive:
### RECEIVE RELATED METHODS ###

    def request(self, timeout: int = RX_SINGLE) -> bool :

        # skip to enter RX mode when previous RX operation incomplete
        if self.getMode() == STATUS_MODE_RX : return False

        # clear previous interrupt and set RX done, RX timeout, header error, and CRC error as interrupt source
        self._irqSetup(IRQ_RX_DONE | IRQ_TIMEOUT | IRQ_HEADER_ERR | IRQ_CRC_ERR)

        # set status to RX wait or RX continuous wait
        self._statusWait = STATUS_RX_WAIT
        self._statusIrq = 0x0000
        # calculate RX timeout config
        rxTimeout = timeout << 6
        if rxTimeout > 0x00FFFFFF : rxTimeout = RX_SINGLE
        if timeout == RX_CONTINUOUS :
            rxTimeout = RX_CONTINUOUS
            self._statusWait = STATUS_RX_CONTINUOUS

        # save current txen pin state and set txen pin to high
        if self._txen != -1 :
            self._txState = self.gpio.input(self._txen)
            self.gpio.output(self._txen, self.gpio.HIGH)

        # set device to receive mode with configured timeout, single, or continuous operation
        self.setRx(rxTimeout)

        # set operation status to wait and attach RX interrupt handler
        if self._irq != -1 :
            self.gpio.remove_event_detect(self._irq)
            print("IRQ pin:", self._irq)
            print("IRQ mode:", self.gpio.gpio_function(self._irq))
            print("IRQ level:", self.gpio.input(self._irq))

            self.gpio.remove_event_detect(16)
            if timeout == RX_CONTINUOUS :
                self.gpio.add_event_detect(self._irq, self.gpio.RISING, callback=self._interruptRxContinuous, bouncetime=10)
            else :
                self.gpio.add_event_detect(self._irq, self.gpio.RISING, callback=self._interruptRx, bouncetime=10)
        return True

    def listen(self, rxPeriod: int, sleepPeriod: int) -> bool :

        # skip to enter RX mode when previous RX operation incomplete
        if self.getMode() == STATUS_MODE_RX : return False

        # clear previous interrupt and set RX done, RX timeout, header error, and CRC error as interrupt source
        self._irqSetup(IRQ_RX_DONE | IRQ_TIMEOUT | IRQ_HEADER_ERR | IRQ_CRC_ERR)

        # set status to RX wait or RX continuous wait
        self._statusWait = STATUS_RX_WAIT
        self._statusIrq = 0x0000
        # calculate RX period and sleep period config
        rxPeriod = rxPeriod << 6
        sleepPeriod = sleepPeriod << 6
        if rxPeriod > 0x00FFFFFF : rxPeriod = 0x00FFFFFF
        if sleepPeriod > 0x00FFFFFF : sleepPeriod = 0x00FFFFFF

        # save current txen pin state and set txen pin to high
        if self._txen != -1 :
            self._txState = self.gpio.input(self._txen)
            self.gpio.output(self._txen, self.gpio.HIGH)

        # set device to receive mode with configured receive and sleep period
        self.setRxDutyCycle(rxPeriod, sleepPeriod)

        # set operation status to wait and attach RX interrupt handler
        if self._irq != -1 :
            self.gpio.remove_event_detect(self._irq)
            self.gpio.add_event_detect(self._irq, self.gpio.RISING, callback=self._interruptRx, bouncetime=10)
        return True

    def available(self) -> int :

        # get size of package still available to read
        return self._payloadTxRx

    def read(self, length: int = 0) :

        # single or multiple bytes read
        single = False
        if length == 0 :
            length = 1
            single = True
        # read data from buffer and update buffer index and payload
        buf = self.readBuffer(self._bufferIndex, length)
        self._bufferIndex = (self._bufferIndex + length) % 256
        if self._payloadTxRx > length :
            self._payloadTxRx -= length
        else :
            self._payloadTxRx = 0
        # return single byte or tuple
        if single : return buf[0]
        else : return buf

    def get(self, length: int = 1) -> bytes :

        # read data from buffer and update buffer index and payload
        buf = self.readBuffer(self._bufferIndex, length)
        self._bufferIndex = (self._bufferIndex + length) % 256
        if self._payloadTxRx > length :
            self._payloadTxRx -= length
        else :
            self._payloadTxRx = 0
        # return array of bytes
        return bytes(buf)

    def purge(self, length: int = 0) :

        # subtract or reset received payload length
        if self._bufferIndex > length :
            self._payloadTxRx = self._payloadTxRx - length
        else :
            self._payloadTxRx = 0
        self._bufferIndex += self._payloadTxRx
