from sx1262_constants import * 

# SX126X register map
class SX1262Vars:
    def __init__(self):

        # SPI and GPIO pin setting
        self._bus = Bus
        self._cs = Cs
        self._reset = Reset
        self._busy = Busy
        self._cs_define = Cs_define
        self._irq = Irq
        self._txen = Txen
        self._rxen = Rxen
        self._wake = Wake
        self._busyTimeout = BusyTimeout
        self._spiSpeed = SpiSpeed
        self._txState = TxState
        self._rxState = RxState

        # LoRa setting
        self._dio = Dio
        self._modem = Modem
        self._sf = Sf
        self._bw = Bw
        self._cr = Cr
        self._ldro = Ldro
        self._headerType = HeaderType
        self._preambleLength = PreambleLength
        self._payloadLength = PayloadLength
        self._crcType = CrcType
        self._invertIq = InvertIq

        # Operation properties
        self._bufferIndex = BufferIndex
        self._payloadTxRx = PayloadTxRx
        self._statusWait = StatusWait
        self._statusIrq = StatusIrq
        self._transmitTime = TransmitTime

        # callback functions
        self._onTransmit = OnTransmit
        self._onReceive = OnReceive