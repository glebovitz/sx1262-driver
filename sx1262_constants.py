# SX126X register map
class SX1262Constants:
    def __init__(self):
        self.REG_FSK_WHITENING_INITIAL_MSB          = 0x06B8
        self.REG_FSK_CRC_INITIAL_MSB                = 0x06BC
        self.REG_FSK_SYNC_WORD_0                    = 0x06C0
        self.REG_FSK_NODE_ADDRESS                   = 0x06CD
        self.REG_IQ_POLARITY_SETUP                  = 0x0736
        self.REG_LORA_SYNC_WORD_MSB                 = 0x0740
        self.REG_TX_MODULATION                      = 0x0889
        self.REG_RX_GAIN                            = 0x08AC
        self.REG_TX_CLAMP_CONFIG                    = 0x08D8
        self.REG_OCP_CONFIGURATION                  = 0x08E7
        self.REG_RTC_CONTROL                        = 0x0902
        self.REG_XTA_TRIM                           = 0x0911
        self.REG_XTB_TRIM                           = 0x0912
        self.REG_EVENT_MASK                         = 0x0944

        # SetSleep
        self.SLEEP_COLD_START                       = 0x00        # sleep mode: cold start, configuration is lost (default)
        self.SLEEP_WARM_START                       = 0x04        #             warm start, configuration is retained
        self.SLEEP_COLD_START_RTC                   = 0x01        #             cold start and wake on RTC timeout
        self.SLEEP_WARM_START_RTC                   = 0x05        #             warm start and wake on RTC timeout

        # SetStandby
        self.STANDBY_RC                             = 0x00        # standby mode: using 13 MHz RC oscillator
        self.STANDBY_XOSC                           = 0x01        #               using 32 MHz crystal oscillator

        # SetTx
        self.TX_SINGLE                              = 0x000000    # Tx timeout duration: no timeout (Rx single mode)

        # SetRx
        self.RX_SINGLE                              = 0x000000    # Rx timeout duration: no timeout (Rx single mode)
        self.RX_CONTINUOUS                          = 0xFFFFFF    #                      infinite (Rx continuous mode)

        # SetRegulatorMode
        self.REGULATOR_LDO                          = 0x00        # set regulator mode: LDO (default)
        self.REGULATOR_DC_DC                        = 0x01        #                     DC-DC

        # CalibrateImage
        self.CAL_IMG_430                            = 0x6B        # ISM band: 430-440 Mhz
        self.CAL_IMG_440                            = 0x6F
        self.CAL_IMG_470                            = 0x75        #           470-510 Mhz
        self.CAL_IMG_510                            = 0x81
        self.CAL_IMG_779                            = 0xC1        #           779-787 Mhz
        self.CAL_IMG_787                            = 0xC5
        self.CAL_IMG_863                            = 0xD7        #           863-870 Mhz
        self.CAL_IMG_870                            = 0xDB
        self.CAL_IMG_902                            = 0xE1        #           902-928 Mhz
        self.CAL_IMG_928                            = 0xE9

        # SetPaConfig
        self.TX_POWER_SX1261                        = 0x01        # device version for TX power: SX1261
        self.TX_POWER_SX1262                        = 0x02        #                              SX1262
        self.TX_POWER_SX1268                        = 0x08        #                              SX1268

        # SetRxTxFallbackMode
        self.FALLBACK_FS                            = 0x40        # after Rx/Tx go to: FS mode
        self.FALLBACK_STDBY_XOSC                    = 0x30        #                    standby mode with crystal oscillator
        self.FALLBACK_STDBY_RC                      = 0x20        #                    standby mode with RC oscillator (default)

        # SetDioIrqParams
        self.IRQ_TX_DONE                            = 0x0001      # packet transmission completed
        self.IRQ_RX_DONE                            = 0x0002      # packet received
        self.IRQ_PREAMBLE_DETECTED                  = 0x0004      # preamble detected
        self.IRQ_SYNC_WORD_VALID                    = 0x0008      # valid sync word detected
        self.IRQ_HEADER_VALID                       = 0x0010      # valid LoRa header received
        self.IRQ_HEADER_ERR                         = 0x0020      # LoRa header CRC error
        self.IRQ_CRC_ERR                            = 0x0040      # wrong CRC received
        self.IRQ_CAD_DONE                           = 0x0080      # channel activity detection finished
        self.IRQ_CAD_DETECTED                       = 0x0100      # channel activity detected
        self.IRQ_TIMEOUT                            = 0x0200      # Rx or Tx timeout
        self.IRQ_ALL                                = 0x03FF      # all interrupts
        self.IRQ_NONE                               = 0x0000      # no interrupts

        # SetDio2AsRfSwitch
        self.DIO2_AS_IRQ                            = 0x00        # DIO2 configuration: IRQ
        self.DIO2_AS_RF_SWITCH                      = 0x01        #                     RF switch control

        # SetDio3AsTcxoCtrl
        self.DIO3_OUTPUT_1_6                        = 0x00        # DIO3 voltage output for TCXO: 1.6 V
        self.DIO3_OUTPUT_1_7                        = 0x01        #                               1.7 V
        self.DIO3_OUTPUT_1_8                        = 0x02        #                               1.8 V
        self.DIO3_OUTPUT_2_2                        = 0x03        #                               2.2 V
        self.DIO3_OUTPUT_2_4                        = 0x04        #                               2.4 V
        self.DIO3_OUTPUT_2_7                        = 0x05        #                               2.7 V
        self.DIO3_OUTPUT_3_0                        = 0x06        #                               3.0 V
        self.DIO3_OUTPUT_3_3                        = 0x07        #                               3.3 V
        self.TCXO_DELAY_2_5                         = 0x0140      # TCXO delay time: 2.5 ms
        self.TCXO_DELAY_5                           = 0x0280      #                  5 ms
        self.TCXO_DELAY_10                          = 0x0560      #                  10 ms

        # SetRfFrequency
        self.RF_FREQUENCY_XTAL                      = 32000000    # XTAL frequency used for RF frequency calculation
        self.RF_FREQUENCY_NOM                       = 33554432    # used for RF frequency calculation

        # SetPacketType
        self.FSK_MODEM                              = 0x00        # GFSK packet type
        self.LORA_MODEM                             = 0x01        # LoRa packet type

        # SetTxParams
        self.PA_RAMP_10U                            = 0x00        # ramp time: 10 us
        self.PA_RAMP_20U                            = 0x01        #            20 us
        self.PA_RAMP_40U                            = 0x02        #            40 us
        self.PA_RAMP_80U                            = 0x03        #            80 us
        self.PA_RAMP_200U                           = 0x04        #            200 us
        self.PA_RAMP_800U                           = 0x05        #            800 us
        self.PA_RAMP_1700U                          = 0x06        #            1700 us
        self.PA_RAMP_3400U                          = 0x07        #            3400 us

        # SetModulationParams
        self.BW_7800                                = 0x00        # LoRa bandwidth: 7.8 kHz
        self.BW_10400                               = 0x08        #                 10.4 kHz
        self.BW_15600                               = 0x01        #                 15.6 kHz
        self.BW_20800                               = 0x09        #                 20.8 kHz
        self.BW_31250                               = 0x02        #                 31.25 kHz
        self.BW_41700                               = 0x0A        #                 41.7 kHz
        self.BW_62500                               = 0x03        #                 62.5 kHz
        self.BW_125000                              = 0x04        #                 125.0 kHz
        self.BW_250000                              = 0x05        #                 250.0 kHz
        self.BW_500000                              = 0x06        #                 500.0 kHz
        self.CR_4_4                                 = 0x00        # LoRa coding rate: 4/4 (no coding rate)
        self.CR_4_5                                 = 0x01        #                   4/5
        self.CR_4_6                                 = 0x01        #                   4/6
        self.CR_4_7                                 = 0x01        #                   4/7
        self.CR_4_8                                 = 0x01        #                   4/8
        self.LDRO_OFF                               = 0x00        # LoRa low data rate optimization: disabled
        self.LDRO_ON                                = 0x01        #                                  enabled

        # SetModulationParams for FSK packet type
        self.PULSE_NO_FILTER                        = 0x00        # FSK pulse shape: no filter applied
        self.PULSE_GAUSSIAN_BT_0_3                  = 0x08        #                  Gaussian BT 0.3
        self.PULSE_GAUSSIAN_BT_0_5                  = 0x09        #                  Gaussian BT 0.5
        self.PULSE_GAUSSIAN_BT_0_7                  = 0x0A        #                  Gaussian BT 0.7
        self.PULSE_GAUSSIAN_BT_1                    = 0x0B        #                  Gaussian BT 1
        self.BW_4800                                = 0x1F        # FSK bandwidth: 4.8 kHz DSB
        self.BW_5800                                = 0x17        #                5.8 kHz DSB
        self.BW_7300                                = 0x0F        #                7.3 kHz DSB
        self.BW_9700                                = 0x1E        #                9.7 kHz DSB
        self.BW_11700                               = 0x16        #                11.7 kHz DSB
        self.BW_14600                               = 0x0E        #                14.6 kHz DSB
        self.BW_19500                               = 0x1D        #                19.5 kHz DSB
        self.BW_23400                               = 0x15        #                23.4 kHz DSB
        self.BW_29300                               = 0x0D        #                29.3 kHz DSB
        self.BW_39000                               = 0x1C        #                39 kHz DSB
        self.BW_46900                               = 0x14        #                46.9 kHz DSB
        self.BW_58600                               = 0x0C        #                58.6 kHz DSB
        self.BW_78200                               = 0x1B        #                78.2 kHz DSB
        self.BW_93800                               = 0x13        #                93.8 kHz DSB
        self.BW_117300                              = 0x0B        #                117.3 kHz DSB
        self.BW_156200                              = 0x1A        #                156.2 kHz DSB
        self.BW_187200                              = 0x12        #                187.2 kHz DSB
        self.BW_234300                              = 0x0A        #                232.3 kHz DSB
        self.BW_312000                              = 0x19        #                312 kHz DSB
        self.BW_373600                              = 0x11        #                373.6 kHz DSB
        self.BW_467000                              = 0x09        #                476 kHz DSB

        # SetPacketParams
        self.HEADER_EXPLICIT                        = 0x00        # LoRa header mode: explicit
        self.HEADER_IMPLICIT                        = 0x01        #                   implicit
        self.CRC_OFF                                = 0x00        # LoRa CRC mode: disabled
        self.CRC_ON                                 = 0x01        #                enabled
        self.IQ_STANDARD                            = 0x00        # LoRa IQ setup: standard
        self.IQ_INVERTED                            = 0x01        #                inverted

        # SetPacketParams for FSK packet type
        self.PREAMBLE_DET_LEN_OFF                   = 0x00        # FSK preamble detector length: off
        self.PREAMBLE_DET_LEN_8                     = 0x04        #                               8-bit
        self.PREAMBLE_DET_LEN_16                    = 0x05        #                               16-bit
        self.PREAMBLE_DET_LEN_24                    = 0x06        #                               24-bit
        self.PREAMBLE_DET_LEN_32                    = 0x07        #                               32-bit
        self.ADDR_COMP_OFF                          = 0x00        # FSK address filtering: off
        self.ADDR_COMP_NODE                         = 0x01        #                        filtering on node address
        self.ADDR_COMP_ALL                          = 0x02        #                        filtering on node and broadcast address
        self.PACKET_KNOWN                           = 0x00        # FSK packet type: the packet length known on both side
        self.PACKET_VARIABLE                        = 0x01        #                  the packet length on variable size
        self.CRC_0                                  = 0x01        # FSK CRC type: no CRC
        self.CRC_1                                  = 0x00        #               CRC computed on 1 byte
        self.CRC_2                                  = 0x02        #               CRC computed on 2 byte
        self.CRC_1_INV                              = 0x04        #               CRC computed on 1 byte and inverted
        self.CRC_2_INV                              = 0x06        #               CRC computed on 2 byte and inverted
        self.WHITENING_OFF                          = 0x00        # FSK whitening: no encoding
        self.WHITENING_ON                           = 0x01        #                whitening enable

        # SetCadParams
        self.CAD_ON_1_SYMB                          = 0x00        # number of symbols used for CAD: 1
        self.CAD_ON_2_SYMB                          = 0x01        #                                 2
        self.CAD_ON_4_SYMB                          = 0x02        #                                 4
        self.CAD_ON_8_SYMB                          = 0x03        #                                 8
        self.CAD_ON_16_SYMB                         = 0x04        #                                 16
        self.CAD_EXIT_STDBY                         = 0x00        # after CAD is done, always exit to STDBY_RC mode
        self.CAD_EXIT_RX                            = 0x01        # after CAD is done, exit to Rx mode if activity is detected

        # GetStatus
        self.STATUS_DATA_AVAILABLE                  = 0x04        # command status: packet received and data can be retrieved
        self.STATUS_CMD_TIMEOUT                     = 0x06        #                 SPI command timed out
        self.STATUS_CMD_ERROR                       = 0x08        #                 invalid SPI command
        self.STATUS_CMD_FAILED                      = 0x0A        #                 SPI command failed to execute
        self.STATUS_CMD_TX_DONE                     = 0x0C        #                 packet transmission done
        self.STATUS_MODE_STDBY_RC                   = 0x20        # current chip mode: STDBY_RC
        self.STATUS_MODE_STDBY_XOSC                 = 0x30        #                    STDBY_XOSC
        self.STATUS_MODE_FS                         = 0x40        #                    FS
        self.STATUS_MODE_RX                         = 0x50        #                    RX
        self.STATUS_MODE_TX                         = 0x60        #                    TX

        # GetDeviceErrors
        self.RC64K_CALIB_ERR                        = 0x0001      # device errors: RC64K calibration failed
        self.RC13M_CALIB_ERR                        = 0x0002      #                RC13M calibration failed
        self.PLL_CALIB_ERR                          = 0x0004      #                PLL calibration failed
        self.ADC_CALIB_ERR                          = 0x0008      #                ADC calibration failed
        self.IMG_CALIB_ERR                          = 0x0010      #                image calibration failed
        self.XOSC_START_ERR                         = 0x0020      #                crystal oscillator failed to start
        self.PLL_LOCK_ERR                           = 0x0040      #                PLL failed to lock
        self.PA_RAMP_ERR                            = 0x0100      #                PA ramping failed

        # LoraSyncWord
        self.LORA_SYNC_WORD_PUBLIC                  = 0x3444      # LoRa SyncWord for public network
        self.LORA_SYNC_WORD_PRIVATE                 = 0x0741      # LoRa SyncWord for private network (default)

        # RxGain
        self.RX_GAIN_POWER_SAVING                   = 0x00        # gain used in Rx mode: power saving gain (default)
        self.RX_GAIN_BOOSTED                        = 0x01        #                       boosted gain
        self.POWER_SAVING_GAIN                      = 0x94        # power saving gain register value
        self.BOOSTED_GAIN                           = 0x96        # boosted gain register value

        # TX and RX operation status 
        self.STATUS_DEFAULT                         = 0           # default status (false)
        self.STATUS_TX_WAIT                         = 1
        self.STATUS_TX_TIMEOUT                      = 2
        self.STATUS_TX_DONE                         = 3
        self.STATUS_RX_WAIT                         = 4
        self.STATUS_RX_CONTINUOUS                   = 5
        self.STATUS_RX_TIMEOUT                      = 6
        self.STATUS_RX_DONE                         = 7
        self.STATUS_HEADER_ERR                      = 8
        self.STATUS_CRC_ERR                         = 9
        self.STATUS_CAD_WAIT                        = 10
        self.STATUS_CAD_DETECTED                    = 11
        self.STATUS_CAD_DONE                        = 12

        # SPI and GPIO pin setting
        self._bus = 0
        self._cs = 0
        self._reset = 22
        self._busy = 23
        self._cs_define = 21
        self._irq = -1
        self._txen = -1
        self._rxen = -1
        self._wake = -1
        self._busyTimeout = 5000
        self._spiSpeed = 7800000
        self._txState = self.gpio.LOW
        self._rxState = self.gpio.LOW

        # LoRa setting
        self._dio = 1
        self._modem = self.LORA_MODEM
        self._sf = 7
        self._bw = 125000
        self._cr = 5
        self._ldro = False
        self._headerType = self.HEADER_EXPLICIT
        self._preambleLength = 12
        self._payloadLength = 32
        self._crcType = False
        self._invertIq = False

        # Operation properties
        self._bufferIndex = 0
        self._payloadTxRx = 32
        self._statusWait = self.STATUS_DEFAULT
        self._statusIrq = self.STATUS_DEFAULT
        self._transmitTime = 0.0

        # callback functions
        self._onTransmit = None
        self._onReceive = None