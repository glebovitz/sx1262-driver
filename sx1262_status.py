from base import BaseLoRa
import spidev
import RPi.GPIO
import time

class SX1262Status:
### WAIT, OPERATION STATUS, AND PACKET STATUS METHODS ###

    def wait(self, timeout: int = 0) -> bool :

        # immediately return when currently not waiting transmit or receive process
        if self._statusIrq :
            return True

        # wait transmit or receive process finish by checking IRQ status
        irqStat = 0x0000
        t = time.time()
        while irqStat == 0x0000 and self._statusIrq == 0x0000 :
            # only check IRQ status register for non interrupt operation
            if self._irq == -1 : irqStat = self.getIrqStatus()
            # return when timeout reached
            if (time.time() - t) > timeout and timeout > 0 : return False

        if self._statusIrq :
            # immediately return when interrupt signal hit
            return True
        elif self._statusWait == self.STATUS_TX_WAIT :
            # for transmit, calculate transmit time and set back txen pin to previous state
            self._transmitTime = time.time() - self._transmitTime
            if self._txen != -1 :
                self.gpio.output(self._txen, self._txState)
        elif self._statusWait == self.STATUS_RX_WAIT :
            # for receive, get received payload length and buffer index and set back txen pin to previous state
            (self._payloadTxRx, self._bufferIndex) = self.getRxBufferStatus()
            if self._txen != -1 :
                self.gpio.output(self._txen, self._txState)
            self._fixRxTimeout()
        elif self._statusWait == self.STATUS_RX_CONTINUOUS :
            # for receive continuous, get received payload length and buffer index and clear IRQ status
            (self._payloadTxRx, self._bufferIndex) = self.getRxBufferStatus()
            self.clearIrqStatus(0x03FF)

        # store IRQ status
        self._statusIrq = irqStat
        return True

    def status(self) -> int :

        # set back status IRQ for RX continuous operation
        statusIrq = self._statusIrq
        if self._statusWait == self.STATUS_RX_CONTINUOUS :
            self._statusIrq = 0x0000

        # get status for transmit and receive operation based on status IRQ
        if statusIrq & self.IRQ_TIMEOUT :
            if self._statusWait == self.STATUS_TX_WAIT : return self.STATUS_TX_TIMEOUT
            else : return self.STATUS_RX_TIMEOUT
        elif statusIrq & self.IRQ_HEADER_ERR : return self.STATUS_HEADER_ERR
        elif statusIrq & self.IRQ_CRC_ERR : return self.STATUS_CRC_ERR
        elif statusIrq & self.IRQ_TX_DONE : return self.STATUS_TX_DONE
        elif statusIrq & self.IRQ_RX_DONE : return self.STATUS_RX_DONE

        # return TX or RX wait status
        return self._statusWait

    def transmitTime(self) -> float :

        # get transmit time in millisecond (ms)
        return self._transmitTime * 1000

    def dataRate(self) -> float :

        # get data rate last transmitted package in kbps
        return self._payloadTxRx / self._transmitTime

    def packetRssi(self) -> float :

        # get relative signal strength index (RSSI) of last incoming package
        (rssiPkt, snrPkt, signalRssiPkt) = self.getPacketStatus()
        return rssiPkt / -2.0

    def snr(self) -> float :

        # get signal to noise ratio (SNR) of last incoming package
        (rssiPkt, snrPkt, signalRssiPkt) = self.getPacketStatus()
        if snrPkt > 127 : snrPkt = snrPkt - 256
        return snrPkt / 4.0

    def signalRssi(self) -> float :

        (rssiPkt, snrPkt, signalRssiPkt) = self.getPacketStatus()
        return signalRssiPkt / -2.0

    def rssiInst(self) -> float :

        return self.getRssiInst() / -2.0

    def getError(self) -> int :
        error = self.getDeviceErrors()
        self.clearDeviceErrors()
        return error