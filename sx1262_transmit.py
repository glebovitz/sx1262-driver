from base import BaseLoRa
import spidev
import RPi.GPIO
import time
from sx1262_constants import *

class SX1262Transmit:
### TRANSMIT RELATED METHODS ###

    def beginPacket(self) :

        # reset payload length and buffer index
        self._payloadTxRx = 0
        self.setBufferBaseAddress(self._bufferIndex, (self._bufferIndex + 0xFF) % 0xFF)

        # save current txen pin state and set txen pin to LOW
        if self._txen != -1 :
            self._txState = self.gpio.input(self._txen)
            self.gpio.output(self._txen, self.gpio.LOW)
        self._fixLoRaBw500(self._bw)

    def endPacket(self, timeout: int = TX_SINGLE) -> bool :

        # skip to enter TX mode when previous TX operation incomplete
        if self.getMode == STATUS_MODE_TX : return False

        # clear previous interrupt and set TX done, and TX timeout as interrupt source
        self._irqSetup(IRQ_TX_DONE | IRQ_TIMEOUT)
        # set packet payload length
        self.setPacketParamsLoRa(self._preambleLength, self._headerType, self._payloadTxRx, self._crcType, self._invertIq)

        # set status to TX wait
        self._statusWait = STATUS_TX_WAIT
        self._statusIrq = 0x0000
        # calculate TX timeout config
        txTimeout = timeout << 6
        if txTimeout > 0x00FFFFFF : txTimeout = TX_SINGLE

        # set device to transmit mode with configured timeout or single operation
        self.setTx(txTimeout)
        self._transmitTime = time.time()

        # set operation status to wait and attach TX interrupt handler
        if self._irq != -1 :
            self.gpio.remove_event_detect(self._irq)
            self.gpio.add_event_detect(self._irq, self.gpio.RISING, callback=self._interruptTx, bouncetime=10)
        return True

    def write(self, data, length: int = 0) :

        # prepare data and data length to be transmitted
        if type(data) is list or type(data) is tuple :
            if length == 0 or length > len(data) : length = len(data)
        elif type(data) is int or type(data) is float :
            length = 1
            data = (int(data),)
        else :
            raise TypeError("input data must be list, tuple, integer or float")
        # write data to buffer and update buffer index and payload
        self.writeBuffer(self._bufferIndex, data, length)
        self._bufferIndex = (self._bufferIndex + length) % 256
        self._payloadTxRx += length

    def put(self, data) :

        # prepare bytes or bytearray to be transmitted
        if type(data) is bytes or type(data) is bytearray :
            dataList = tuple(data)
            length = len(dataList)
        else : raise TypeError("input data must be bytes or bytearray")
        # write data to buffer and update buffer index and payload
        self.writeBuffer(self._bufferIndex, dataList, length)
        self._bufferIndex = (self._bufferIndex + length) % 256
        self._payloadTxRx += length
    