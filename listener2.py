#!/usr/bin/env python3
import threading
import time

from sx1262_driver.sx1262_constants import *
from sx1262_driver.sx1262 import SX1262 as SX126x  # adjust if your driver file has a different name

# ------------------------------------------------------------
# Pin mapping (BCM) — confirmed by your continuity testing
# ------------------------------------------------------------
BUSY_PIN = 20    # Physical Pin 38
IRQ_PIN = 16     # Physical Pin 36 (DIO1)  (unused here; we poll IRQ status)
RESET_PIN = 18   # Physical Pin 12
NSS_PIN = 21     # Physical Pin 40 (manual CS, mapped as CS_DEFINE in constants)
SPI_BUS = 0
SPI_DEV = 0

# ------------------------------------------------------------
# Radio parameters
# ------------------------------------------------------------
FREQUENCY_HZ = 910_525_000   # 910.525 MHz
BANDWIDTH_HZ = 62_500        # 62.5 kHz
SPREADING_FACTOR = 7
CODING_RATE = 5              # 4/5
PREAMBLE_LENGTH = 12
PAYLOAD_LENGTH = 32
CRC_ENABLED = True
INVERT_IQ = False


def start_background_rssi(driver, interval=5):
    """
    driver.rssi_inst() returns instantaneous RSSI in dBm.
    Runs forever in a daemon thread.
    """

    def loop():
        while True:
            try:
                rssi = driver.rssi_inst()
                print("RSSI:", rssi)

                # Flush the SPI bus / status
                mode = driver.get_mode()
                print("Raw mode bits from GET_STATUS:", hex(mode) if mode is not None else "None")

            except Exception as e:
                print("RSSI monitor error:", e)
            time.sleep(interval)

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def start_irq_polling(driver, interval=0.01):
    """
    Poll the IRQ status register and, if non-zero, invoke
    the driver's internal RX interrupt handler.
    """

    def loop():
        while True:
            irq = driver.get_irq_status()
            if irq:
                # Let the driver decode the IRQ and call on_rx()
                driver._interrupt_rx(None)
            time.sleep(interval)

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def on_rx():
    status = radio.status()

    if (status == STATUS_RX_DONE)
        handle_rx_done(payload_length=radio.available(), buffer_index=None, irq_status=None)
    elif status == STATUS_CRC_ERR:
        handle_crc_error(irq_status=None)
    elif status == STATUS_HEADER_ERR:
        handle_header_error(irq_status=None)
    elif status == STATUS_RX_TIMEOUT:
        handle_timeout(irq_status=None)
    else:
        print("Nada")

    irq = radio.get_irq_status()
    radio.clear_irq_status(irq)

def handle_rx_done(payload_length=None, buffer_index=None, irq_status=None):
    data = radio.get(payload_length)
    rssi = radio.packet_rssi()
    snr = radio.snr()

    print("\n--- PACKET RECEIVED ---")
    print(f"Bytes: {payload_length}")
    print(f"Data:  {data.hex(' ')}")
    print(f"RSSI:  {rssi:.1f} dBm")
    print(f"SNR:   {snr:.1f} dB")
    print("------------------------")


def handle_crc_error(irq_status=None):
    print("CRC error")


def handle_header_error(irq_status=None):
    print("Header error")


def handle_timeout(irq_status=None):
    print("RX timeout (unexpected in continuous mode)")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    global radio

    print("Initializing SX1262…")

    radio = SX126x()

    ok = radio.begin(
        bus=SPI_BUS,
        cs=SPI_DEV,
        reset=RESET_PIN,
        busy=BUSY_PIN,
        irq=-1,
        txen=-1,
        rxen=-1,
        wake=-1,
    )

    if not ok:
        raise RuntimeError("SX1262 failed to enter STDBY_RC. Check BUSY, RESET, NSS wiring.")

    print("Configuring radio…")

    # Optional: background RSSI monitor
    # start_background_rssi(radio, interval=5)

    # Poll IRQ status in a background thread instead of GPIO edge callbacks
    start_irq_polling(radio)

    # Sync word (public network)
    radio.set_sync_word(LORA_SYNC_WORD_PUBLIC)

    # Frequency
    radio.set_frequency(FREQUENCY_HZ)

    # LoRa modulation
    radio.set_lora_modulation(
        sf=SPREADING_FACTOR,
        bw=BANDWIDTH_HZ,
        cr=CODING_RATE,
        ldro=False,
    )

    # Packet parameters
    radio.set_lora_packet(
        header_type=HEADER_EXPLICIT,
        preamble_length=PREAMBLE_LENGTH,
        payload_length=PAYLOAD_LENGTH,
        crc_type=CRC_ENABLED,
        invert_iq=INVERT_IQ,
    )

    # Optional: boosted gain
    radio.set_rx_gain(RX_GAIN_BOOSTED)

    # Register callback
    radio.on_receive(on_rx)

    print(f"Starting continuous receive at {FREQUENCY_HZ/1e6:.6f} MHz…")
    print("Waiting for packets…")

    ok = radio.request(RX_CONTINUOUS)
    if not ok:
        raise RuntimeError("Failed to enter RX_CONTINUOUS mode.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down…")
        radio.end()


if __name__ == "__main__":
    main()
