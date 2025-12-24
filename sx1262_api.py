from base import BaseLoRa
import spidev
import RPi.GPIO
import time

class SX1262Api:
    ### SX126X API: OPERATIONAL MODES COMMANDS ###

    def setSleep(self, sleepConfig: int) :
        self._writeBytes(0x84, (sleepConfig,), 1)

    def setStandby(self, stbyConfig: int) :
        self._writeBytes(0x80, (stbyConfig,), 1)

    def setFs(self) :
        self._writeBytes(0xC1, (), 0)

    def setTx(self, timeout: int) :
        buf = (
            (timeout >> 16) & 0xFF,
            (timeout >> 8) & 0xFF,
            timeout & 0xFF
        )
        self._writeBytes(0x83, buf, 3)

    def setRx(self, timeout: int) :
        buf = (
            (timeout >> 16) & 0xFF,
            (timeout >> 8) & 0xFF,
            timeout & 0xFF
        )
        self._writeBytes(0x82, buf, 3)

    def setTimerOnPreamble(self, enable: int) :
        self._writeBytes(0x9F, (enable,), 1)

    def setRxDutyCycle(self, rxPeriod: int, sleepPeriod: int) :
        buf = (
            (rxPeriod >> 16) & 0xFF,
            (rxPeriod >> 8) & 0xFF,
            rxPeriod & 0xFF,
            (sleepPeriod >> 16) & 0xFF,
            (sleepPeriod >> 8) & 0xFF,
            sleepPeriod & 0xFF
        )
        self._writeBytes(0x94, buf, 6)

    def setCad(self) :
        self._writeBytes(0xC5, (), 0)

    def setTxContinuousWave(self) :
        self._writeBytes(0xD1, (), 0)

    def setTxInfinitePreamble(self) :
        self._writeBytes(0xD2, (), 0)

    def setRegulatorMode(self, modeParam: int) :
        self._writeBytes(0x96, (modeParam,), 1)

    def calibrate(self, calibParam: int) :
        self._writeBytes(0x89, (calibParam,), 1)

    def calibrateImage(self, freq1: int, freq2: int) :
        buf = (freq1, freq2)
        self._writeBytes(0x98, buf, 2)

    def setPaConfig(self, paDutyCycle: int, hpMax: int, deviceSel: int, paLut: int) :
        buf = (paDutyCycle, hpMax, deviceSel, paLut)
        self._writeBytes(0x95, buf, 4)

    def setRxTxFallbackMode(self, fallbackMode: int) :
        self._writeBytes(0x93, (fallbackMode,), 1)

### SX126X API: REGISTER AND BUFFER ACCESS COMMANDS ###

    def writeRegister(self, address: int, data: tuple, nData: int) :
        buf = (
            (address >> 8) & 0xFF, 
            address & 0xFF
        ) + tuple(data)
        self._writeBytes(0x0D, buf, nData+2)

    def readRegister(self, address: int, nData: int) -> tuple :
        addr = (
            (address >> 8) & 0xFF,
            address & 0xFF
        )
        buf = self._readBytes(0x1D, nData+1, addr, 2)
        return buf[1:]

    def writeBuffer(self, offset: int, data: tuple, nData: int) :
        buf = (offset,) + tuple(data)
        self._writeBytes(0x0E, buf, nData+1)

    def readBuffer(self, offset: int, nData: int) -> tuple :
        buf = self._readBytes(0x1E, nData+1, (offset,), 1)
        return buf[1:]

### SX126X API: DIO AND IRQ CONTROL ###

    def setDioIrqParams(self, irqMask: int, dio1Mask: int, dio2Mask: int, dio3Mask: int) :
        buf = (
            (irqMask >> 8) & 0xFF,
            irqMask & 0xFF,
            (dio1Mask >> 8) & 0xFF,
            dio1Mask & 0xFF,
            (dio2Mask >> 8) & 0xFF,
            dio2Mask & 0xFF,
            (dio3Mask >> 8) & 0xFF,
            dio3Mask & 0xFF
        )
        self._writeBytes(0x08, buf, 8)

    def getIrqStatus(self) -> int :
        buf = self._readBytes(0x12, 3)
        return (buf[1] << 8) | buf[2]

    def clearIrqStatus(self, clearIrqParam: int) :
        buf = (
            (clearIrqParam >> 8) & 0xFF,
            clearIrqParam & 0xFF
        )
        self._writeBytes(0x02, buf, 2)

    def setDio2AsRfSwitchCtrl(self, enable: int) :
        self._writeBytes(0x9D, (enable,), 1)

    def setDio3AsTcxoCtrl(self, tcxoVoltage: int, delay: int) :
        buf = (
            tcxoVoltage & 0xFF,
            (delay >> 16) & 0xFF,
            (delay >> 8) & 0xFF,
            delay & 0xFF
        )
        self._writeBytes(0x97, buf, 4)

### SX126X API: RF, MODULATION, AND PACKET COMMANDS ###

    def setRfFrequency(self, rfFreq: int) :
        buf = (
            (rfFreq >> 24) & 0xFF,
            (rfFreq >> 16) & 0xFF,
            (rfFreq >> 8) & 0xFF,
            rfFreq & 0xFF
        )
        self._writeBytes(0x86, buf, 4)

    def setPacketType(self, packetType: int) :
        self._writeBytes(0x8A, (packetType,), 1)

    def getPakcetType(self) -> int :
        buf = self._readBytes(0x11, 2)
        return buf[1]

    def setTxParams(self, power: int, rampTime: int) :
        buf = (power, rampTime)
        self._writeBytes(0x8E, buf, 2)

    def setModulationParamsLoRa(self, sf: int, bw: int, cr: int, ldro: int) :
        buf = (sf, bw, cr, ldro, 0, 0, 0, 0)
        self._writeBytes(0x8B, buf, 8)

    def setModulationParamsFsk(self, br: int, pulseShape: int, bandwidth: int, Fdev: int) :
        buf = (
            (br >> 16) & 0xFF,
            (br >> 8) & 0xFF,
            br & 0xFF,
            pulseShape,
            bandwidth,
            (br >> 16) & 0xFF,
            (br >> 8) & 0xFF,
            Fdev & 0xFF
        )
        self._writeBytes(0x8B, buf, 8)

    def setPacketParamsLoRa(self, preambleLength: int, headerType: int, payloadLength: int, crcType: int, invertIq: int) :
        buf = (
            (preambleLength >> 8) & 0xFF,
            preambleLength & 0xFF,
            headerType,
            payloadLength,
            crcType,
            invertIq,
            0,
            0,
            0
        )
        self._writeBytes(0x8C, buf, 9)

    def setPacketParamsFsk(self, preambleLength: int, preambleDetector: int, syncWordLength: int, addrComp: int, packetType: int, payloadLength: int, crcType: int, whitening: int) :
        buf = (
            (preambleLength >> 8) & 0xFF,
            preambleLength & 0xFF,
            preambleDetector,
            syncWordLength,
            addrComp,
            packetType,
            payloadLength,
            crcType,
            whitening
        )
        self._writeBytes(0x8C, buf, 9)

    def setCadParams(self, cadSymbolNum: int, cadDetPeak: int, cadDetMin: int, cadExitMode: int, cadTimeout: int) :
        buf = (
            cadSymbolNum,
            cadDetPeak,
            cadDetMin,
            cadExitMode,
            (cadTimeout >> 16) & 0xFF,
            (cadTimeout >> 8) & 0xFF,
            cadTimeout & 0xFF
        )
        self._writeBytes(0x88, buf, 7)

    def setBufferBaseAddress(self, txBaseAddress: int, rxBaseAddress: int) :
        buf = (txBaseAddress, rxBaseAddress)
        self._writeBytes(0x8F, buf, 2)

    def setLoRaSymbNumTimeout(self, symbnum: int) :
        self._writeBytes(0xA0, (symbnum,), 1)

### SX126X API: STATUS COMMANDS ###

    def getStatus(self) -> int :
        buf = self._readBytes(0xC0, 1)
        return buf[0]

    def getChipStatus(self):
        # 0xC0 = GET_STATUS
        # Transaction: send opcode, then 1 dummy to clock out status
        if self.busyCheck():
            return None  # chip is busy, no status

        self.gpio.output(self._cs_define, self.gpio.LOW)
        resp = self.spi.xfer2([0xC0, 0])  # [undefined, status]
        self.gpio.output(self._cs_define, self.gpio.HIGH)

        # resp[0] is garbage during opcode; resp[1] is the status byte
        return resp


    def getRxBufferStatus(self) -> tuple :
        buf = self._readBytes(0x13, 3)
        return buf[1:3]

    def getPacketStatus(self) -> tuple :
        buf = self._readBytes(0x14, 4)
        return buf[1:4]

    def getRssiInst(self) -> int :
        buf = self._readBytes(0x15, 2)
        return buf[1]

    def getFullRssiInst(self):
        resp = self._readBytes(0x15, 4)
        status = resp[0]
        rssi_raw = resp[1]

        # Convert raw RSSI to dBm
        rssi_dbm = -rssi_raw / 2.0

        return status, rssi_dbm

    def decode_status(self, status):
        mode = status & 0x07
        modes = {
            1: "STBY_RC",
            2: "STBY_XOSC",
            3: "FS",
            4: "RX",
            5: "TX"
        }
        return modes.get(mode, "UNKNOWN")

    def getStats(self) -> tuple :
        buf = self._readBytes(0x10, 7)
        return (
            (buf[1] >> 8) | buf[2],
            (buf[3] >> 8) | buf[4],
            (buf[5] >> 8) | buf[6]
        )

    def resetStats(self) :
        buf = (0, 0, 0, 0, 0, 0)
        self._writeBytes(0x00, buf, 6)

    def getDeviceErrors(self) -> int :
        buf = self._readBytes(0x17, 2)
        return buf[1]

    def clearDeviceErrors(self) :
        buf = (0, 0)
        self._writeBytes(0x07, buf, 2)

### SX126X API: WORKAROUND FUNCTIONS ###

    def _fixLoRaBw500(self, bw: int) :
        packetType = self.getPakcetType()
        buf = self.readRegister(self.REG_TX_MODULATION, 1)
        value = buf[0] | 0x04
        if packetType == self.LORA_MODEM and bw == self.BW_500000 :
            value = buf[0] & 0xFB
        self.writeRegister(self.REG_TX_MODULATION, (value,), 1)

    def _fixResistanceAntenna(self) :
        buf = self.readRegister(self.REG_TX_CLAMP_CONFIG, 1)
        value = buf[0] | 0x1E
        self.writeRegister(self.REG_TX_CLAMP_CONFIG, (value,), 1)

    def _fixRxTimeout(self) :
        self.writeRegister(self.REG_RTC_CONTROL, (0,), 1)
        buf = self.readRegister(self.REG_EVENT_MASK, 1)
        value = buf[0] | 0x02
        self.writeRegister(self.REG_EVENT_MASK, (value,), 1)

    def _fixInvertedIq(self, invertIq: bool) :
        buf = self.readRegister(self.REG_IQ_POLARITY_SETUP, 1)
        value = buf[0] & 0xFB
        if invertIq :
            value = buf[0] | 0x04
        self.writeRegister(self.REG_IQ_POLARITY_SETUP, (value,), 1)

### SX126X API: UTILITIES ###

    def _writeBytes(self, opCode: int, data: tuple, nBytes: int) :
        if self.busyCheck() : return
        self.gpio.output(self._cs_define, self.gpio.LOW)
        buf = [opCode]
        for i in range(nBytes) : buf.append(data[i])
        self.spi.xfer2(buf)
        self.gpio.output(self._cs_define, self.gpio.HIGH)

    def _readBytes(self, opCode: int, nBytes: int, address: tuple = (), nAddress: int = 0) -> tuple :
        if self.busyCheck() : return ()
        self.gpio.output(self._cs_define, self.gpio.LOW)
        buf = [opCode]
        for i in range(nAddress) : buf.append(address[i])
        for i in range(nBytes) : buf.append(0x00)
        feedback = self.spi.xfer2(buf)
        self.gpio.output(self._cs_define, self.gpio.HIGH)
        return tuple(feedback[nAddress+1:])
