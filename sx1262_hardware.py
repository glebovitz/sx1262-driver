from base import BaseLoRa
import spidev
import RPi.GPIO
import time

class SX1262Hardware:
### HARDWARE CONFIGURATION METHODS ###

    def setSpi(self, bus: int, cs: int, speed: int = _spiSpeed) :

        self._bus = bus
        self._cs = cs
        self._spiSpeed = speed
        # open spi line and set bus id, chip select, and spi speed
        self.spi.open(bus, cs)
        self.spi.max_speed_hz = speed
        self.spi.lsbfirst = False
        self.spi.mode = 0

    def setPins(self, reset: int, busy: int, irq: int = -1, txen: int = -1, rxen: int = -1, wake: int = -1) :

        self._reset = reset
        self._busy = busy
        self._irq = irq
        self._txen = txen
        self._rxen = rxen
        self._wake = wake
        # set pins as input or output
        self.gpio.setup(reset, self.gpio.OUT)
        self.gpio.setup(busy, self.gpio.IN)
        self.gpio.setup(self._cs_define, self.gpio.OUT)
        if irq != -1 : self.gpio.setup(irq, self.gpio.IN)
        if txen != -1 : self.gpio.setup(txen, self.gpio.OUT)
        # if rxen != -1 : self.gpio.setup(rxen, self.gpio.OUT)

    def setRfIrqPin(self, dioPinSelect: int) :

        if dioPinSelect == 2 or dioPinSelect == 3 : self._dio = dioPinSelect
        else : self._dio = 1

    def setDio2RfSwitch(self, enable: bool = True) :

        if enable : self.setDio2AsRfSwitchCtrl(self.DIO2_AS_RF_SWITCH)
        else : self.setDio2AsRfSwitchCtrl(self.DIO2_AS_IRQ)

    def setDio3TcxoCtrl(self, tcxoVoltage, delayTime) :

        self.setDio3AsTcxoCtrl(tcxoVoltage, delayTime)
        self.setStandby(self.STANDBY_RC)
        self.calibrate(0xFF)

    def setXtalCap(self, xtalA, xtalB) :

        self.setStandby(self.STANDBY_XOSC)
        self.writeRegister(self.REG_XTA_TRIM, (xtalA, xtalB), 2)
        self.setStandby(self.STANDBY_RC)
        self.calibrate(0xFF)

    def setRegulator(self, regMode) :

        self.setRegulatorMode(regMode)

    def setCurrentProtection(self, level) :
        #avoid wrap-around of OCP register, which has 6bits
        if level > 63 : level = 63
        self.writeRegister(self.REG_OCP_CONFIGURATION, (level,), 1)
