# ESP32-S3-WROOM-1-N8R8 (U7), every connected pad

Generated from the KiCad netlist of `GottFA_SLX16_Module.kicad_sch` (see `tools/`), so it is exact by construction. `U1.n` = Spartan-6 pin (with its ISE name), `ESP GPIOn` = the real ESP32-S3 GPIO (never the module pad number). Power nets list no members.

| pad | GPIO | net | also on |
|---|---|---|---|
| 1 | GND | `GND` |  |
| 2 | 3V3 | `VCC3.3` |  |
| 3 | EN | `ESP_EN` |  |
| 4 | GPIO4 | `ESP_TCK` |  |
| 5 | GPIO5 | `ESP_TMS` |  |
| 6 | GPIO6 | `ESP_TDI` |  |
| 7 | GPIO7 | `ESP_TDO` |  |
| 8 | GPIO15 | `NOR_CS` | JP1.2, U6.1 ~{CS}_1 |
| 9 | GPIO16 | `MISO` | P4.22, U1.62 (IO_L12P_D1_MISO2_2_62), U6.2 DO/IO_{1}_2 |
| 10 | GPIO17 | `—` |  |
| 11 | GPIO18 | `ESP32_RX` | U1.142 (IO_L2P_0_142) |
| 12 | GPIO8 | `LED_RED` |  |
| 13 | USB_D- | `USB_D_N` |  |
| 14 | USB_D+ | `USB_D_P` |  |
| 15 | GPIO3 | `—` |  |
| 16 | GPIO46 | `—` |  |
| 17 | GPIO9 | `OLED_SCL` | P7.3 |
| 18 | GPIO10 | `OLED_SDA` | P7.4 |
| 19 | GPIO11 | `LED_GREEN` |  |
| 20 | GPIO12 | `LED_BLUE` |  |
| 21 | GPIO13 | `MOSI` | P4.23, U1.66 (IO_L2N_CMPMOSI_2_66), U6.5 DI/IO_{0}_5 |
| 22 | GPIO14 | `CLK` | P4.24, U1.67 (IO_L2P_CMPCLK_2_67), U6.6 CLK_6 |
| 23 | GPIO21 | `FA_CTRL_REQ` | U1.141 (IO_L2N_0_141) |
| 24 | GPIO47 | `ESP32_TX` | U1.143 (IO_L1N_VREF_0_143) |
| 25 | GPIO48 | `—` |  |
| 26 | GPIO45 | `—` |  |
| 27 | GPIO0 | `ESP_BOOT` |  |
| 28 | GPIO35 | `—` |  |
| 29 | GPIO36 | `—` |  |
| 30 | GPIO37 | `—` |  |
| 31 | GPIO38 | `—` |  |
| 32 | GPIO39 | `—` |  |
| 33 | GPIO40 | `—` |  |
| 34 | GPIO41 | `—` |  |
| 35 | GPIO42 | `—` |  |
| 36 | GPIO44 (RXD0) | `Debug` | P4.11, U1.46 (IO_L49P_D3_2_46) |
| 37 | GPIO43 (TXD0) | `Audio_RX` | P4.4, U1.41 (IO_L64P_D8_2_41) |
| 38 | GPIO2 | `—` |  |
| 39 | GPIO1 | `—` |  |
| 40 | GND | `GND` |  |
| 41 | GND | `GND` |  |
