from base import BaseLoRa
import spidev
import RPi.GPIO
import time

### COMMON OPERATIONAL METHODS ###
class SX1262Common:
    def begin(self, bus: int = _bus, cs: int = _cs, reset: int = _reset, busy: int = _busy, irq: int = _irq, txen: int = _txen, rxen: int = _rxen, wake: int = _wake) :
        print(f"pins: bus: {bus} cs:{cs} reset:{reset} irq: {irq} busy: {busy}")
        # set spi and gpio pins
        self.setSpi(bus, cs)
        self.setPins(reset, busy, irq, txen, rxen, wake)
        # perform device reset
        self.reset()

        # check if device connect and set modem to LoRa
        self.setStandby(self.STANDBY_RC)
        if self.getMode() != self.STATUS_MODE_STDBY_RC :
            return False
        self.setPacketType(self.LORA_MODEM)
        self._fixResistanceAntenna()
        return True

    def end(self) :

        self.sleep(self.SLEEP_COLD_START)
        self.spi.close()
        self.gpio.cleanup()

    def getStatus(self):
        resp = self._readBytes(0xC0, 1)
        if not resp:
            return None
        return resp[0]

    def reset(self) -> bool :

        # put reset pin to low then wait busy pin to low
        self.gpio.output(self._reset, self.gpio.LOW)
        time.sleep(0.001)
        self.gpio.output(self._reset, self.gpio.HIGH)
        return not self.busyCheck()

    def sleep(self, option = SLEEP_WARM_START) :

        # put device in sleep mode, wait for 500 us to enter sleep mode
        self.standby()
        self.setSleep(option)
        time.sleep(0.0005)

    def wake(self) :

        # wake device by set wake pin (cs pin) to low before spi transaction and put device in standby mode
        if (self._wake != -1) :
            self.gpio.setup(self._wake, self.gpio.OUT)
            self.gpio.output(self._wake, self.gpio.LOW)
            time.sleep(0.0005)
        self.setStandby(self.STANDBY_RC)
        self._fixResistanceAntenna()

    def standby(self, option = STANDBY_RC) :

        self.setStandby(option)

    def busyCheck(self, timeout: int = _busyTimeout) :

        # wait for busy pin to LOW or timeout reached
        t = time.time()
        while self.gpio.input(self._busy) == self.gpio.HIGH :
            if (time.time() - t) > (timeout / 1000) : return True
        return False

    def setFallbackMode(self, fallbackMode) :

        self.setRxTxFallbackMode(fallbackMode)

    def getMode(self) -> int :

        return self.getStatus() & 0x70