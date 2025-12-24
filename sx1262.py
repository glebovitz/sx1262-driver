from base import BaseLoRa
import spidev
import RPi.GPIO
import time
from sx1262_constants import SX1262Constants
from sx1262_api import SX1262Api
from sx1262_common import SX1262Common 
from sx1262_hardware import  SX1262Hardware
from sx1262_modem import SX1262Modem
from sx1262_receive import SX1262Receive
from sx1262_transmit import SX1262Transmit
from sx1262_status import SX1262Status
from sx1262_interrupt import SX1262Interrupt

class SX1262 (
    SX1262Constants,
    SX1262Api,
    SX1262Common,
    SX1262Hardware,
    SX1262Modem,
    SX1262Receive,
    SX1262Transmit,
    SX1262Status,
    SX1262Interrupt
):
    def __init__(self):
        super().__init__()
        self.spi = spidev.SpiDev()
        self.gpio = RPi.GPIO
        self.gpio.setmode(RPi.GPIO.BCM)
        self.gpio.setwarnings(False)
