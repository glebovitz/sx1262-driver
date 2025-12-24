from base import BaseLoRa
import spidev
import RPi.GPIO
import time
from sx1262_constants import *

class SX1262Interrupt:
### INTERRUPT HANDLER METHODS ###

    def _irqSetup(self, irqMask) :

        # clear IRQ status of previous transmit or receive operation
        self.clearIrqStatus(0x03FF)
        # set selected interrupt source
        dio1Mask = 0x0000
        dio2Mask = 0x0000
        dio3Mask = 0x0000
        if self._dio == 2 : dio2Mask = irqMask
        elif self._dio == 3 : dio3Mask = irqMask
        else : dio1Mask = irqMask
        self.setDioIrqParams(irqMask, dio1Mask, dio2Mask, dio3Mask)

    def _interruptTx(self, channel) :

        # calculate transmit time
        self._transmitTime = time.time() - self._transmitTime
        # set back txen pin to previous state
        if self._txen != -1 :
            self.gpio.output(self._txen, self._txState)
        # store IRQ status
        self._statusIrq = self.getIrqStatus()

        # call onTransmit function
        if callable(self._onTransmit) :
            self._onTransmit()

    def _interruptRx(self, channel) :

        # set back txen pin to previous state
        if self._txen != -1 :
            self.gpio.output(self._txen, self._txState)
        self._fixRxTimeout()
        # store IRQ status
        self._statusIrq = self.getIrqStatus()
        # get received payload length and buffer index
        (self._payloadTxRx, self._bufferIndex) = self.getRxBufferStatus()

        # call onReceive function
        if callable(self._onReceive) :
            self._onReceive()

    def _interruptRxContinuous(self, channel) :

        # store IRQ status
        self._statusIrq = self.getIrqStatus()
        # clear IRQ status
        self.clearIrqStatus(0x03FF)
        # get received payload length and buffer index
        (self._payloadTxRx, self._bufferIndex) = self.getRxBufferStatus()

        # call onReceive function
        if callable(self._onReceive) :
            self._onReceive()

    def onTransmit(self, callback) :

        # register onTransmit function to call every transmit done
        self._onTransmit = callback

    def onReceive(self, callback) :

        # register onReceive function to call every receive done
        self._onReceive = callback
