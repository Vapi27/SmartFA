# Carrier connectors P1–P4, pin by pin

Generated from the KiCad netlist of `GottFA_SLX16_Module.kicad_sch` (see `tools/`), so it is exact by construction. `U1.n` = Spartan-6 pin (with its ISE name), `ESP GPIOn` = the real ESP32-S3 GPIO (never the module pad number). Power nets list no members.

Four 2×14 headers, 2.54 mm, the geometry of bontango's 10CL006 devboard.

## P1 — P1 - afficheur

| pin | net | also on |
|---|---|---|
| 1 | `disp_segments[1]` | U1.74 (IO_L74N_DOUT_BUSY_1_74) |
| 2 | `disp_segments[2]` | U1.75 (IO_L74P_AWAKE_1_75) |
| 3 | `disp_segments[3]` | U1.78 (IO_L47N_1_78) |
| 4 | `disp_segments[4]` | U1.79 (IO_L47P_1_79) |
| 5 | `disp_segments[6]` | U1.80 (IO_L46N_1_80) |
| 6 | `disp_segments[7]` | U1.81 (IO_L46P_1_81) |
| 7 | `disp_segments[5]` | U1.82 (IO_L45N_1_82) |
| 8 | `disp_segments[8]` | U1.83 (IO_L45P_1_83) |
| 9 | `disp_segments[9]` | U1.84 (IO_L43N_GCLK4_1_84) |
| 10 | `disp_segments[10]` | U1.85 (IO_L43P_GCLK5_1_85) |
| 11 | `disp_segments[11]` | U1.87 (IO_L42N_GCLK6_TRDY1_1_87) |
| 12 | `disp_segments[12]` | U1.88 (IO_L42P_GCLK7_1_88) |
| 13 | `disp_segments[13]` | U1.92 (IO_L41N_GCLK8_1_92) |
| 14 | `disp_segments[14]` | U1.93 (IO_L41P_GCLK9_IRDY1_1_93) |
| 15 | `disp_segments[15]` | U1.94 (IO_L40N_GCLK10_1_94) |
| 16 | `disp_segments[16]` | U1.95 (IO_L40P_GCLK11_1_95) |
| 17 | `disp_segments[17]` | U1.97 (IO_L34N_1_97) |
| 18 | `disp_segments[18]` | U1.98 (IO_L34P_1_98) |
| 19 | `disp_segments[19]` | U1.99 (IO_L33N_1_99) |
| 20 | `disp_segments[20]` | U1.100 (IO_L33P_1_100) |
| 21 | `disp_segments[21]` | U1.101 (IO_L32N_1_101) |
| 22 | `disp_segments[22]` | U1.102 (IO_L32P_1_102) |
| 23 | `disp_segments[23]` | U1.104 (IO_L1N_VREF_1_104) |
| 24 | `disp_segments[24]` | U1.105 (IO_L1P_1_105) |
| 25 | `GND` |  |
| 26 | `GND` |  |
| 27 | `VCC3.3` |  |
| 28 | `VCC3.3` |  |

## P2 — P2 - U5/U6 PA-PB

| pin | net | also on |
|---|---|---|
| 1 | `GND` |  |
| 2 | `GND` |  |
| 3 | `—` |  |
| 4 | `U5_PA[0]` | U1.111 (IO_L66N_SCP0_0_111) |
| 5 | `U5_PA[1]` | U1.112 (IO_L66P_SCP1_0_112) |
| 6 | `U5_PA[2]` | U1.114 (IO_L65N_SCP2_0_114) |
| 7 | `U5_PA[3]` | U1.115 (IO_L65P_SCP3_0_115) |
| 8 | `SPARE_IO_1` | U1.116 (IO_L64N_SCP4_0_116) |
| 9 | `SPARE_IO_2` | U1.117 (IO_L64P_SCP5_0_117) |
| 10 | `U6_PB[2]` | U1.118 (IO_L63N_SCP6_0_118) |
| 11 | `U6_PB[1]` | U1.119 (IO_L63P_SCP7_0_119) |
| 12 | `DIP_Return[3]` | U1.120 (IO_L62N_VREF_0_120) |
| 13 | `SPARE_IO_3` | U1.121 (IO_L62P_0_121) |
| 14 | `myTest` | U1.123 (IO_L37N_GCLK12_0_123) |
| 15 | `U5_PA_7` | U1.124 (IO_L37P_GCLK13_0_124) |
| 16 | `U6_PB[3]` | U1.126 (IO_L36N_GCLK14_0_126) |
| 17 | `U6_PB[4]` | U1.127 (IO_L36P_GCLK15_0_127) |
| 18 | `U6_PB[5]` | U1.131 (IO_L35N_GCLK16_0_131) |
| 19 | `U6_PB[6]` | U1.132 (IO_L35P_GCLK17_0_132) |
| 20 | `U6_PB[7]` | U1.133 (IO_L34N_GCLK18_0_133) |
| 21 | `U6_PA[3]` | U1.134 (IO_L34P_GCLK19_0_134) |
| 22 | `U6_PA[1]` | U1.137 (IO_L4N_0_137) |
| 23 | `U6_PA[2]` | U1.138 (IO_L4P_0_138) |
| 24 | `U6_PA[0]` | U1.139 (IO_L3N_0_139) |
| 25 | `U6_PA[6]` | U1.140 (IO_L3P_0_140) |
| 26 | `GND` |  |
| 27 | `GND` |  |
| 28 | `VCC3.3` |  |

## P3 — P3 - U4/U6 PA-PB

| pin | net | also on |
|---|---|---|
| 1 | `GND` |  |
| 2 | `GND` |  |
| 3 | `U6_PB[0]` | U1.1 (IO_L83N_VREF_3_1) |
| 4 | `U6_PA[4]` | U1.2 (IO_L83P_3_2) |
| 5 | `U6_PA[7]` | U1.5 (IO_L52N_3_5) |
| 6 | `U6_PA[5]` | U1.6 (IO_L52P_3_6) |
| 7 | `U4_PB[0]` | U1.7 (IO_L51N_3_7) |
| 8 | `U5_PB_7` | U1.8 (IO_L51P_3_8) |
| 9 | `U4_PB[2]` | U1.9 (IO_L50N_3_9) |
| 10 | `U4_PB[1]` | U1.10 (IO_L50P_3_10) |
| 11 | `U4_PB[4]` | U1.11 (IO_L49N_3_11) |
| 12 | `U4_PB[3]` | U1.12 (IO_L49P_3_12) |
| 13 | `U4_PB[6]` | U1.14 (IO_L44N_GCLK20_3_14) |
| 14 | `U4_PB[5]` | U1.15 (IO_L44P_GCLK21_3_15) |
| 15 | `U4_PA[0]` | U1.16 (IO_L43N_GCLK22_IRDY2_3_16) |
| 16 | `U4_PB[7]` | U1.17 (IO_L43P_GCLK23_3_17) |
| 17 | `U4_PA[2]` | U1.21 (IO_L42N_GCLK24_3_21) |
| 18 | `U4_PA[1]` | U1.22 (IO_L42P_GCLK25_TRDY2_3_22) |
| 19 | `U4_PA[4]` | U1.23 (IO_L41N_GCLK26_3_23) |
| 20 | `U4_PA[3]` | U1.24 (IO_L41P_GCLK27_3_24) |
| 21 | `U4_PA[6]` | U1.26 (IO_L37N_3_26) |
| 22 | `U4_PA[5]` | U1.27 (IO_L37P_3_27) |
| 23 | `DIP_Strobe[0]` | U1.29 (IO_L36N_3_29) |
| 24 | `U4_PA[7]` | U1.30 (IO_L36P_3_30) |
| 25 | `reset_sw` | U1.32 (IO_L2N_3_32) |
| 26 | `GND` |  |
| 27 | `GND` |  |
| 28 | `VCC3.3` |  |

## P4 — P4 - LED/son/SPI

| pin | net | also on |
|---|---|---|
| 1 | `GND` |  |
| 2 | `GND` |  |
| 3 | `LED_ON` | U1.40 (IO_L64N_D9_2_40) |
| 4 | `Audio_RX` | U1.41 (IO_L64P_D8_2_41), ESP GPIO43 (TXD0) |
| 5 | `LED_SDcard` | U1.43 (IO_L62N_D6_2_43) |
| 6 | `Sound` | U1.44 (IO_L62P_D5_2_44) |
| 7 | `LED_Int` | U1.45 (IO_L49N_D4_2_45) |
| 8 | `GND` |  |
| 9 | `GND` |  |
| 10 | `GND` |  |
| 11 | `Debug` | U1.46 (IO_L49P_D3_2_46), ESP GPIO44 (RXD0) |
| 12 | `DIP_Return[0]` | U1.48 (IO_L48P_D7_2_48) |
| 13 | `DIP_Return[2]` | U1.50 (IO_L31N_GCLK30_D15_2_50) |
| 14 | `DIP_Return[1]` | U1.55 (IO_L30N_GCLK0_USERCCLK_2_55) |
| 15 | `CS_SDcard` | U1.56 (IO_L30P_GCLK1_D13_2_56) |
| 16 | `DIP_Strobe[3]` | U1.57 (IO_L14N_D12_2_57) |
| 17 | `DIP_Strobe[2]` | U1.58 (IO_L14P_D11_2_58) |
| 18 | `DIP_Strobe[1]` | U1.59 (IO_L13N_D10_2_59) |
| 19 | `VCC1.2` |  |
| 20 | `VCC1.2` |  |
| 21 | `CS_EEprom` | U1.61 (IO_L12N_D2_MISO3_2_61) |
| 22 | `MISO` | U1.62 (IO_L12P_D1_MISO2_2_62), U6.2 DO/IO_{1}_2, ESP GPIO16 |
| 23 | `MOSI` | U1.66 (IO_L2N_CMPMOSI_2_66), U6.5 DI/IO_{0}_5, ESP GPIO13 |
| 24 | `CLK` | U1.67 (IO_L2P_CMPCLK_2_67), U6.6 CLK_6, ESP GPIO14 |
| 25 | `GND` |  |
| 26 | `GND` |  |
| 27 | `VCC3.3` |  |
| 28 | `VCC3.3` |  |

## Positions with nothing behind them on this module

P2.3

P2.8, P2.9 and P2.13 carry `SPARE_IO_1/2/3` (U1.116, U1.117, U1.121): FPGA I/Os that reach the connector but are not used by the current design (not constrained in the `.ucf`).
