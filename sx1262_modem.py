from base import BaseLoRa
import spidev
import RPi.GPIO
import time

class SX1262Modem:
### MODEM, MODULATION PARAMETER, AND PACKET PARAMETER SETUP METHODS ###

    def setModem(self, modem) :

        self._modem = modem
        self.setStandby(self.STANDBY_RC)
        self.setPacketType(modem)

    def setFrequency(self, frequency: int) :

        # perform image calibration before set frequency
        if frequency < 446000000 :
            calFreqMin = self.CAL_IMG_430
            calFreqMax = self.CAL_IMG_440
        elif frequency < 734000000 :
            calFreqMin = self.CAL_IMG_470
            calFreqMax = self.CAL_IMG_510
        elif frequency < 828000000 :
            calFreqMin = self.CAL_IMG_779
            calFreqMax = self.CAL_IMG_787
        elif frequency < 877000000 :
            calFreqMin = self.CAL_IMG_863
            calFreqMax = self.CAL_IMG_870
        else :
            calFreqMin = self.CAL_IMG_902
            calFreqMax = self.CAL_IMG_928
        self.calibrateImage(calFreqMin, calFreqMax)

        # calculate frequency and set frequency setting
        rfFreq = int(frequency * 33554432 / 32000000)
        self.setRfFrequency(rfFreq)

    def setTxPower(self, txPower: int, version = TX_POWER_SX1262) :

        #  maximum TX power is 22 dBm and 15 dBm for SX1261
        if txPower > 22 : txPower = 22
        elif txPower > 15 and version == self.TX_POWER_SX1261 : txPower = 15

        paDutyCycle = 0x00
        hpMax = 0x00
        deviceSel = 0x00
        power = 0x0E
        if version == self.TX_POWER_SX1261 : deviceSel = 0x01
        # set parameters for PA config and TX params configuration
        if txPower == 22 :
            paDutyCycle = 0x04
            hpMax = 0x07
            power = 0x16
        elif txPower >= 20 :
            paDutyCycle = 0x03
            hpMax = 0x05
            power = 0x16
        elif txPower >= 17 :
            paDutyCycle = 0x02
            hpMax = 0x03
            power = 0x16
        elif txPower >= 14 and version == self.TX_POWER_SX1261 :
            paDutyCycle = 0x04
            hpMax = 0x00
            power = 0x0E
        elif txPower >= 14 and version == self.TX_POWER_SX1262 :
            paDutyCycle = 0x02
            hpMax = 0x02
            power = 0x16
        elif txPower >= 14 and version == self.TX_POWER_SX1268 :
            paDutyCycle = 0x04
            hpMax = 0x06
            power = 0x0F
        elif txPower >= 10 and version == self.TX_POWER_SX1261 :
            paDutyCycle = 0x01
            hpMax = 0x00
            power = 0x0D
        elif txPower >= 10 and version == self.TX_POWER_SX1268 :
            paDutyCycle = 0x00
            hpMax = 0x03
            power = 0x0F
        else : return

        # set power amplifier and TX power configuration
        self.setPaConfig(paDutyCycle, hpMax, deviceSel, 0x01)
        self.setTxParams(power, self.PA_RAMP_800U)

    def setRxGain(self, rxGain) :

        # set power saving or boosted gain in register
        gain = self.POWER_SAVING_GAIN
        if rxGain == self.RX_GAIN_BOOSTED :
            gain = self.BOOSTED_GAIN
            # set certain register to retain configuration after wake from sleep mode
            self.writeRegister(self.REG_RX_GAIN, (gain,), 1)
            self.writeRegister(0x029F, (0x01, 0x08, 0xAC), 3)
        else :
            self.writeRegister(self.REG_RX_GAIN, (gain,), 1)

    def setLoRaModulation(self, sf: int, bw: int, cr: int, ldro: bool = False) :

        self._sf = sf
        self._bw = bw
        self._cr = cr
        self._ldro = ldro

        # valid spreading factor is between 5 and 12
        if sf > 12 : sf = 12
        elif sf < 5 : sf = 5
        # select bandwidth options
        if bw < 9100 : bw = self.BW_7800
        elif bw < 13000 : bw = self.BW_10400
        elif bw < 18200 : bw = self.BW_15600
        elif bw < 26000 : bw = self.BW_20800
        elif bw < 36500 : bw = self.BW_31250
        elif bw < 52100 : bw = self.BW_41700
        elif bw < 93800 : bw = self.BW_62500
        elif bw < 187500 : bw = self.BW_125000
        elif bw < 375000 : bw = self.BW_250000
        else : bw = self.BW_500000
        # valid code rate denominator is between 4 and 8
        cr = cr - 4
        if cr > 4 : cr = 0
        # set low data rate option
        if ldro : ldro = self.LDRO_ON
        else : ldro = self.LDRO_OFF

        self.setModulationParamsLoRa(sf, bw, cr, ldro)

    def setLoRaPacket(self, headerType, preambleLength: int, payloadLength: int, crcType: bool = False, invertIq: bool = False) :

        self._headerType = headerType
        self._preambleLength = preambleLength
        self._payloadLength = payloadLength
        self._crcType = crcType
        self._invertIq = invertIq

        # filter valid header type config
        if headerType != self.HEADER_IMPLICIT : headerType = self.HEADER_EXPLICIT
        # set CRC and invert IQ option
        if crcType : crcType = self.CRC_ON
        else : crcType = self.CRC_OFF
        if invertIq : invertIq = self.IQ_INVERTED
        else : invertIq = self.IQ_STANDARD

        self.setPacketParamsLoRa(preambleLength, headerType, payloadLength, crcType, invertIq)
        self._fixInvertedIq(invertIq)

    def setSpreadingFactor(self, sf: int) :

        self.setLoRaModulation(sf, self._bw, self._cr, self._ldro)

    def setBandwidth(self, bw: int) :

        self.setLoRaModulation(self._sf, bw, self._cr, self._ldro)

    def setCodeRate(self, cr: int) :

        self.setLoRaModulation(self._sf, self._bw, cr, self._ldro)

    def setLdroEnable(self, ldro: bool = True) :

        self.setLoRaModulation(self._sf, self._bw, self._cr, ldro)

    def setHeaderType(self, headerType) :

        self.setLoRaPacket(self._preambleLength, headerType, self._payloadLength, self._crcType, self._invertIq)

    def setPreambleLength(self, preambleLength: int) :

        self.setLoRaPacket(preambleLength, self._headerType, self._payloadLength, self._crcType, self._invertIq)

    def setPayloadLength(self, payloadLength: int) :

        self.setLoRaPacket(self._preambleLength, self._headerType, payloadLength, self._crcType, self._invertIq)

    def setCrcEnable(self, crcType: bool = True) :

        self.setLoRaPacket(self._preambleLength, self._headerType, self._payloadLength, crcType, self._invertIq)

    def setInvertIq(self, invertIq: bool = True) :

        self.setLoRaPacket(self._preambleLength, self._headerType, self._payloadLength, self._crcType, invertIq)

    def setSyncWord(self, syncWord: int) :

        buf = (
            (syncWord >> 8) & 0xFF,
            syncWord & 0xFF
        )
        if syncWord <= 0xFF :
            buf = (
                (syncWord & 0xF0) | 0x04,
                (syncWord << 4) | 0x04
            )
        self.writeRegister(self.REG_LORA_SYNC_WORD_MSB, buf, 2)

    def setFskModulation(self, br: int, pulseShape: int, bandwidth: int, fdev: int) :

        self.setModulationParamsFsk(br, pulseShape, bandwidth, fdev)

    def setFskPacket(self, preambleLength: int, preambleDetector: int, syncWordLength: int, addrComp: int, packetType: int, payloadLength: int, crcType: int, whitening: int) :

        self.setPacketParamsFsk(preambleLength, preambleDetector, syncWordLength, addrComp, packetType, payloadLength, crcType, whitening)

    def setFskSyncWord(self, sw: tuple, swLen: int) :

        self.writeRegister(self.REG_FSK_SYNC_WORD_0, sw, swLen)

    def setFskAddress(self, nodeAddr: int, broadcastAddr: int) :

        self.writeRegister(self.REG_FSK_NODE_ADDRESS, (nodeAddr, broadcastAddr), 2)

    def setFskCrc(self, crcInit: int, crcPolynom: int) :

        buf = (crcInit >> 8, crcInit & 0xFF, crcPolynom >> 8, crcPolynom & 0xFF)
        self.writeRegister(self.REG_FSK_CRC_INITIAL_MSB, buf, 4)

    def setFskWhitening(self, whitening: int) :

        self.writeRegister(self.REG_FSK_WHITENING_INITIAL_MSB, (whitening >> 8, whitening & 0xFF), 2)
