# Spartan-6 XC6SLX9-2TQG144 (U1), all 144 pins

Generated from the KiCad netlist of `GottFA_SLX16_Module.kicad_sch` (see `tools/`), so it is exact by construction. `U1.n` = Spartan-6 pin (with its ISE name), `ESP GPIOn` = the real ESP32-S3 GPIO (never the module pad number). Power nets list no members.

The constraint file that actually builds the bitstream is [`GottFA80_SLX9.ucf`](https://github.com/Vapi27/GottFA80_PLuS/blob/spartan6-feasibility/GottFA80_SLX9.ucf) in the FPGA repository; this table is the schematic side.

| pin | ISE name | net | also on |
|---|---|---|---|
| 1 | IO_L83N_VREF_3_1 | `U6_PB[0]` | P3.3 |
| 2 | IO_L83P_3_2 | `U6_PA[4]` | P3.4 |
| 3 | GND_3 | `GND` |  |
| 4 | VCCO_3_4 | `VCC3.3` |  |
| 5 | IO_L52N_3_5 | `U6_PA[7]` | P3.5 |
| 6 | IO_L52P_3_6 | `U6_PA[5]` | P3.6 |
| 7 | IO_L51N_3_7 | `U4_PB[0]` | P3.7 |
| 8 | IO_L51P_3_8 | `U5_PB_7` | P3.8 |
| 9 | IO_L50N_3_9 | `U4_PB[2]` | P3.9 |
| 10 | IO_L50P_3_10 | `U4_PB[1]` | P3.10 |
| 11 | IO_L49N_3_11 | `U4_PB[4]` | P3.11 |
| 12 | IO_L49P_3_12 | `U4_PB[3]` | P3.12 |
| 13 | GND_13 | `GND` |  |
| 14 | IO_L44N_GCLK20_3_14 | `U4_PB[6]` | P3.13 |
| 15 | IO_L44P_GCLK21_3_15 | `U4_PB[5]` | P3.14 |
| 16 | IO_L43N_GCLK22_IRDY2_3_16 | `U4_PA[0]` | P3.15 |
| 17 | IO_L43P_GCLK23_3_17 | `U4_PB[7]` | P3.16 |
| 18 | VCCO_3_18 | `VCC3.3` |  |
| 19 | VCCINT_19 | `VCC1.2` |  |
| 20 | VCCAUX_20 | `VCC3.3` |  |
| 21 | IO_L42N_GCLK24_3_21 | `U4_PA[2]` | P3.17 |
| 22 | IO_L42P_GCLK25_TRDY2_3_22 | `U4_PA[1]` | P3.18 |
| 23 | IO_L41N_GCLK26_3_23 | `U4_PA[4]` | P3.19 |
| 24 | IO_L41P_GCLK27_3_24 | `U4_PA[3]` | P3.20 |
| 25 | GND_25 | `GND` |  |
| 26 | IO_L37N_3_26 | `U4_PA[6]` | P3.21 |
| 27 | IO_L37P_3_27 | `U4_PA[5]` | P3.22 |
| 28 | VCCINT_28 | `VCC1.2` |  |
| 29 | IO_L36N_3_29 | `DIP_Strobe[0]` | P3.23 |
| 30 | IO_L36P_3_30 | `U4_PA[7]` | P3.24 |
| 31 | VCCO_3_31 | `VCC3.3` |  |
| 32 | IO_L2N_3_32 | `reset_sw` | P3.25 |
| 33 | IO_L2P_3_33 | `—` |  |
| 34 | IO_L1N_VREF_3_34 | `—` |  |
| 35 | IO_L1P_3_35 | `NOR_CS_FPGA` | JP1.1 |
| 36 | VCCAUX_36 | `VCC3.3` |  |
| 37 | PROGRAM_B_2_37 | `PROGRAM_B` |  |
| 38 | IO_L65N_CSO_B_2_38 | `CFG_CS` | U5.1 ~{CS}_1 |
| 39 | IO_L65P_INIT_B_2_39 | `INIT_B` |  |
| 40 | IO_L64N_D9_2_40 | `LED_ON` | P4.3 |
| 41 | IO_L64P_D8_2_41 | `Audio_RX` | P4.4, ESP GPIO43 (TXD0) |
| 42 | VCCO_2_42 | `VCC3.3` |  |
| 43 | IO_L62N_D6_2_43 | `LED_SDcard` | P4.5 |
| 44 | IO_L62P_D5_2_44 | `Sound` | P4.6 |
| 45 | IO_L49N_D4_2_45 | `LED_Int` | P4.7 |
| 46 | IO_L49P_D3_2_46 | `Debug` | P4.11, ESP GPIO44 (RXD0) |
| 47 | IO_L48N_RDWR_B_VREF_2_47 | `—` |  |
| 48 | IO_L48P_D7_2_48 | `DIP_Return[0]` | P4.12 |
| 49 | GND_49 | `GND` |  |
| 50 | IO_L31N_GCLK30_D15_2_50 | `DIP_Return[2]` | P4.13 |
| 51 | IO_L31P_GCLK31_D14_2_51 | `clk_50` |  |
| 52 | VCCINT_52 | `VCC1.2` |  |
| 53 | VCCAUX_53 | `VCC3.3` |  |
| 54 | GND_54 | `GND` |  |
| 55 | IO_L30N_GCLK0_USERCCLK_2_55 | `DIP_Return[1]` | P4.14 |
| 56 | IO_L30P_GCLK1_D13_2_56 | `CS_SDcard` | P4.15 |
| 57 | IO_L14N_D12_2_57 | `DIP_Strobe[3]` | P4.16 |
| 58 | IO_L14P_D11_2_58 | `DIP_Strobe[2]` | P4.17 |
| 59 | IO_L13N_D10_2_59 | `DIP_Strobe[1]` | P4.18 |
| 60 | IO_L13P_M1_2_60 | `M1` |  |
| 61 | IO_L12N_D2_MISO3_2_61 | `CS_EEprom` | P4.21 |
| 62 | IO_L12P_D1_MISO2_2_62 | `MISO` | P4.22, U6.2 DO/IO_{1}_2, ESP GPIO16 |
| 63 | VCCO_2_63 | `VCC3.3` |  |
| 64 | IO_L3N_MOSI_CSI_B_MISO0_2_64 | `CFG_DI_MOSI` | U5.5 DI/IO_{0}_5 |
| 65 | IO_L3P_D0_DIN_MISO_MISO1_2_65 | `CFG_DO_MISO` | U5.2 DO/IO_{1}_2 |
| 66 | IO_L2N_CMPMOSI_2_66 | `MOSI` | P4.23, U6.5 DI/IO_{0}_5, ESP GPIO13 |
| 67 | IO_L2P_CMPCLK_2_67 | `CLK` | P4.24, U6.6 CLK_6, ESP GPIO14 |
| 68 | GND_68 | `GND` |  |
| 69 | IO_L1N_M0_CMPMISO_2_69 | `M0` |  |
| 70 | IO_L1P_CCLK_2_70 | `CFG_CCLK` | U5.6 CLK_6 |
| 71 | DONE_2_71 | `DONE` |  |
| 72 | CMPCS_B_2_72 | `CMPCS_B` |  |
| 73 | SUSPEND_73 | `GND` |  |
| 74 | IO_L74N_DOUT_BUSY_1_74 | `disp_segments[1]` | P1.1 |
| 75 | IO_L74P_AWAKE_1_75 | `disp_segments[2]` | P1.2 |
| 76 | VCCO_1_76 | `VCC3.3` |  |
| 77 | GND_77 | `GND` |  |
| 78 | IO_L47N_1_78 | `disp_segments[3]` | P1.3 |
| 79 | IO_L47P_1_79 | `disp_segments[4]` | P1.4 |
| 80 | IO_L46N_1_80 | `disp_segments[6]` | P1.5 |
| 81 | IO_L46P_1_81 | `disp_segments[7]` | P1.6 |
| 82 | IO_L45N_1_82 | `disp_segments[5]` | P1.7 |
| 83 | IO_L45P_1_83 | `disp_segments[8]` | P1.8 |
| 84 | IO_L43N_GCLK4_1_84 | `disp_segments[9]` | P1.9 |
| 85 | IO_L43P_GCLK5_1_85 | `disp_segments[10]` | P1.10 |
| 86 | VCCO_1_86 | `VCC3.3` |  |
| 87 | IO_L42N_GCLK6_TRDY1_1_87 | `disp_segments[11]` | P1.11 |
| 88 | IO_L42P_GCLK7_1_88 | `disp_segments[12]` | P1.12 |
| 89 | VCCINT_89 | `VCC1.2` |  |
| 90 | VCCAUX_90 | `VCC3.3` |  |
| 91 | GND_91 | `GND` |  |
| 92 | IO_L41N_GCLK8_1_92 | `disp_segments[13]` | P1.13 |
| 93 | IO_L41P_GCLK9_IRDY1_1_93 | `disp_segments[14]` | P1.14 |
| 94 | IO_L40N_GCLK10_1_94 | `disp_segments[15]` | P1.15 |
| 95 | IO_L40P_GCLK11_1_95 | `disp_segments[16]` | P1.16 |
| 96 | GND_96 | `GND` |  |
| 97 | IO_L34N_1_97 | `disp_segments[17]` | P1.17 |
| 98 | IO_L34P_1_98 | `disp_segments[18]` | P1.18 |
| 99 | IO_L33N_1_99 | `disp_segments[19]` | P1.19 |
| 100 | IO_L33P_1_100 | `disp_segments[20]` | P1.20 |
| 101 | IO_L32N_1_101 | `disp_segments[21]` | P1.21 |
| 102 | IO_L32P_1_102 | `disp_segments[22]` | P1.22 |
| 103 | VCCO_1_103 | `VCC3.3` |  |
| 104 | IO_L1N_VREF_1_104 | `disp_segments[23]` | P1.23 |
| 105 | IO_L1P_1_105 | `disp_segments[24]` | P1.24 |
| 106 | TDO_106 | `TDO` | P5.5 |
| 107 | TMS_107 | `TMS` | P5.9 |
| 108 | GND_108 | `GND` |  |
| 109 | TCK_109 | `TCK` | P5.3 |
| 110 | TDI_110 | `TDI` | P5.7 |
| 111 | IO_L66N_SCP0_0_111 | `U5_PA[0]` | P2.4 |
| 112 | IO_L66P_SCP1_0_112 | `U5_PA[1]` | P2.5 |
| 113 | GND_113 | `GND` |  |
| 114 | IO_L65N_SCP2_0_114 | `U5_PA[2]` | P2.6 |
| 115 | IO_L65P_SCP3_0_115 | `U5_PA[3]` | P2.7 |
| 116 | IO_L64N_SCP4_0_116 | `SPARE_IO_1` | P2.8 |
| 117 | IO_L64P_SCP5_0_117 | `SPARE_IO_2` | P2.9 |
| 118 | IO_L63N_SCP6_0_118 | `U6_PB[2]` | P2.10 |
| 119 | IO_L63P_SCP7_0_119 | `U6_PB[1]` | P2.11 |
| 120 | IO_L62N_VREF_0_120 | `DIP_Return[3]` | P2.12 |
| 121 | IO_L62P_0_121 | `SPARE_IO_3` | P2.13 |
| 122 | VCCO_0_122 | `VCC3.3` |  |
| 123 | IO_L37N_GCLK12_0_123 | `myTest` | P2.14 |
| 124 | IO_L37P_GCLK13_0_124 | `U5_PA_7` | P2.15 |
| 125 | VCCO_0_125 | `VCC3.3` |  |
| 126 | IO_L36N_GCLK14_0_126 | `U6_PB[3]` | P2.16 |
| 127 | IO_L36P_GCLK15_0_127 | `U6_PB[4]` | P2.17 |
| 128 | VCCINT_128 | `VCC1.2` |  |
| 129 | VCCAUX_129 | `VCC3.3` |  |
| 130 | GND_130 | `GND` |  |
| 131 | IO_L35N_GCLK16_0_131 | `U6_PB[5]` | P2.18 |
| 132 | IO_L35P_GCLK17_0_132 | `U6_PB[6]` | P2.19 |
| 133 | IO_L34N_GCLK18_0_133 | `U6_PB[7]` | P2.20 |
| 134 | IO_L34P_GCLK19_0_134 | `U6_PA[3]` | P2.21 |
| 135 | VCCO_0_135 | `VCC3.3` |  |
| 136 | GND_136 | `GND` |  |
| 137 | IO_L4N_0_137 | `U6_PA[1]` | P2.22 |
| 138 | IO_L4P_0_138 | `U6_PA[2]` | P2.23 |
| 139 | IO_L3N_0_139 | `U6_PA[0]` | P2.24 |
| 140 | IO_L3P_0_140 | `U6_PA[6]` | P2.25 |
| 141 | IO_L2N_0_141 | `FA_CTRL_REQ` | ESP GPIO21 |
| 142 | IO_L2P_0_142 | `ESP32_RX` | ESP GPIO18 |
| 143 | IO_L1N_VREF_0_143 | `ESP32_TX` | ESP GPIO47 |
| 144 | IO_L1P_HSWAPEN_0_144 | `HSWAPEN` |  |

## FPGA I/O pins that reach neither a connector nor a part

U1.33 (IO_L2P_3_33), U1.34 (IO_L1N_VREF_3_34), U1.47 (IO_L48N_RDWR_B_VREF_2_47)
