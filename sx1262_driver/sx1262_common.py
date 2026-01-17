import time

from sx1262_constants import *

import lgpio # type: ignore - pi only


class SX1262Common:
    def __init__(self):
        super().__init__()

    def begin(
        self,
        bus: int = BUS,
        cs: int = CS,
        reset: int = RESET,
        busy: int = BUSY,
        irq: int = IRQ,
        txen: int = TXEN,
        rxen: int = RXEN,
        wake: int = WAKE,
    ) -> bool:
        print(f"pins: bus: {bus} cs:{cs} reset:{reset} irq:{irq} busy:{busy}")

        self.set_spi(bus, cs)
        self.set_pins(reset, busy, irq, txen, rxen, wake)

        self.reset()

        self.set_standby(STANDBY_RC)
        if self.get_mode() != STATUS_MODE_STDBY_RC:
            return False

        self.set_packet_type(LORA_MODEM)
        self._fix_resistance_antenna()
        self._start_recv_loop()
        return True

    def end(self):
        self.sleep(SLEEP_COLD_START)
        self._stop_recv_loop()
        self.spi.close()
        # close gpio chip handle
        lgpio.gpiochip_close(self.gpio_chip)

    def get_status(self):
        resp = self._read_bytes(0xC0, 1)
        if not resp:
            return None
        return resp[0]

    def reset(self) -> bool:
        lgpio.gpio_write(self.gpio_chip, self._reset, 0)
        time.sleep(0.001)
        lgpio.gpio_write(self.gpio_chip, self._reset, 1)
        return not self.busy_check()

    def sleep(self, option=SLEEP_WARM_START):
        self.standby()
        self.set_sleep(option)
        time.sleep(0.0005)

    def wake(self):
        if self._wake != -1:
            lgpio.gpio_claim_output(self.gpio_chip, self._wake)
            lgpio.gpio_write(self.gpio_chip, self._wake, 0)
            time.sleep(0.0005)

        self.set_standby(STANDBY_RC)
        self._fix_resistance_antenna()

    def standby(self, option=STANDBY_RC):
        self.set_standby(option)

    def busy_check(self, timeout: int = BUSY_TIMEOUT) -> bool:
        start = time.time()
        while lgpio.gpio_read(self.gpio_chip, self._busy) == 1:
            if (time.time() - start) > (timeout / 1000.0):
                return True
        return False

    def set_fallback_mode(self, fallback_mode):
        self.set_rx_tx_fallback_mode(fallback_mode)

    def get_mode(self) -> int:
        status = self.get_status()
        if status is None:
            return 0
        return status & 0x70

    def get_mode_and_status(self) -> int:
        status = self.get_status()
        if status is None:
            return 0
        return status & 0x7E
    
    def recover_from_rx_fault(self, irq_bits):
        """
        Recover the SX1262 from TIMEOUT, CRC_ERR, or HEADER_ERR.
        This handles the SX1262 'RX deadlock' where SetRx() is ignored
        unless the chip is forced through STDBY_RC first.
        """

        # 1. Clear only the IRQ bits that actually fired
        self.clear_irq_status(irq_bits)

        # 2. Force chip into STDBY_RC (required after timeout/error)
        self.set_standby(STANDBY_RC)

        # 3. Wait for BUSY to go low
        print("busy check", self.busy_check())

        # 4. Small settling delay (SX1262 errata)
        time.sleep(0.001)

        # 5. Re-enter continuous RX
        self.set_rx(RX_CONTINUOUS)

        # 6. Optional: verify
        mode = self.get_mode_and_status()
        print("Recovery complete, mode =", hex(mode))

