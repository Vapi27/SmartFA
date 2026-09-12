# Internal parts: config flash U5, game NOR U6, JP1, JTAG P5, power P6, USB J1, OLED P7

Generated from the KiCad netlist of `GottFA_SLX16_Module.kicad_sch` (see `tools/`), so it is exact by construction. `U1.n` = Spartan-6 pin (with its ISE name), `ESP GPIOn` = the real ESP32-S3 GPIO (never the module pad number). Power nets list no members.

## U5 — W25Q32JVSNIQ - flash de config

| pin | net | also on |
|---|---|---|
| 1 | `CFG_CS` | U1.38 (IO_L65N_CSO_B_2_38) |
| 2 | `CFG_DO_MISO` | U1.65 (IO_L3P_D0_DIN_MISO_MISO1_2_65) |
| 3 | `VCC3.3` |  |
| 4 | `GND` |  |
| 5 | `CFG_DI_MOSI` | U1.64 (IO_L3N_MOSI_CSI_B_MISO0_2_64) |
| 6 | `CFG_CCLK` | U1.70 (IO_L1P_CCLK_2_70) |
| 7 | `VCC3.3` |  |
| 8 | `VCC3.3` |  |

## U6 — W25Q32JVSNIQ - NOR jeux

| pin | net | also on |
|---|---|---|
| 1 | `NOR_CS` | JP1.2, ESP GPIO15 |
| 2 | `MISO` | P4.22, U1.62 (IO_L12P_D1_MISO2_2_62), ESP GPIO16 |
| 3 | `VCC3.3` |  |
| 4 | `GND` |  |
| 5 | `MOSI` | P4.23, U1.66 (IO_L2N_CMPMOSI_2_66), ESP GPIO13 |
| 6 | `CLK` | P4.24, U1.67 (IO_L2P_CMPCLK_2_67), ESP GPIO14 |
| 7 | `VCC3.3` |  |
| 8 | `VCC3.3` |  |

## JP1 — Bridged

| pin | net | also on |
|---|---|---|
| 1 | `NOR_CS_FPGA` | U1.35 (IO_L1P_3_35) |
| 2 | `NOR_CS` | U6.1 ~{CS}_1, ESP GPIO15 |

## P5 — JTAG

| pin | net | also on |
|---|---|---|
| 1 | `VCC3.3` |  |
| 2 | `GND` |  |
| 3 | `TCK` | U1.109 (TCK_109) |
| 4 | `GND` |  |
| 5 | `TDO` | U1.106 (TDO_106) |
| 6 | `GND` |  |
| 7 | `TDI` | U1.110 (TDI_110) |
| 8 | `GND` |  |
| 9 | `TMS` | U1.107 (TMS_107) |
| 10 | `GND` |  |

## P6 — 5V IN machine

| pin | net | also on |
|---|---|---|
| 1 | `+5V` |  |
| 2 | `GND` |  |

## J1 — USB-C 16P

| pin | net | also on |
|---|---|---|
| SH | `GND` |  |
| A1 | `GND` |  |
| B1 | `GND` |  |
| A4 | `+5V` |  |
| B4 | `+5V` |  |
| A5 | `CC1` |  |
| B5 | `CC2` |  |
| A6 | `USBC_D_P` |  |
| B6 | `USBC_D_P` |  |
| A7 | `USBC_D_N` |  |
| B7 | `USBC_D_N` |  |
| A9 | `+5V` |  |
| B9 | `+5V` |  |
| A12 | `GND` |  |
| B12 | `GND` |  |

## P7 — OLED 0.91 I2C

| pin | net | also on |
|---|---|---|
| 1 | `GND` |  |
| 2 | `VCC3.3` |  |
| 3 | `OLED_SCL` | ESP GPIO9 |
| 4 | `OLED_SDA` | ESP GPIO10 |
