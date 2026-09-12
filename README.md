# Smart FA — the GottFA_SLX16 module

A drop-in FPGA module for bontango's **FA pinball boards** — the four 2×14 headers of the
10CL006 devboard — built around a **Xilinx Spartan-6 XC6SLX9** and an **ESP32-S3**, with
the game ROM images in an on-module SPI NOR and no SD card. Made by Pstore
([pinballs.store](https://pinballs.store)) as the replacement CPU board for **Gottlieb
System 80 / 80A / 80B** machines, on bontango's GPL [GottFA80](https://github.com/bontango/GottFA80).

This repository is the **hardware documentation**: schematics, pin tables generated from
the netlist, the ESP↔FPGA link, and what the next revision changes. The code lives next door:

| | |
|---|---|
| FPGA design (VHDL, GPL-3) | [Vapi27/GottFA80_PLuS](https://github.com/Vapi27/GottFA80_PLuS), branch `spartan6-feasibility` — bontango's GottFA80_PLuS ported to this module |
| ESP32-S3 companion firmware (GPL-3) | [Vapi27/gottfa-esp32](https://github.com/Vapi27/gottfa-esp32) — WiFi, web UI, LISYcontrol diagnostics, speech engine, XVC JTAG |
| `FA_Control` (Pstore) | production and workshop firmware, a fork of bontango's [FA_Control](https://github.com/bontango/FA_Control) ported to this module; not published yet (upstream carries no licence file) |

## What is on the board

| | |
|---|---|
| FPGA | Xilinx Spartan-6 **XC6SLX9-2TQG144C** (U1), 50 MHz crystal (Y2), configured in Master-SPI mode from U5 |
| MCU | **ESP32-S3-WROOM-1-N8R8** (U7): 8 MB flash, 8 MB PSRAM, WiFi. Native USB on the USB-C **J1** (ESD: SRV05-4) |
| Flash | **U5** W25Q32: FPGA configuration. **U6** W25Q32: game ROM images, one 16 KB slot per game number (the GottFA SD-card numbering), written by the ESP over WiFi |
| Power | +5 V in on **P6** or the USB-C; AMS1085 3.3 V (U3), AMS1117 1.2 V core (U2). LEDs: D1 3V3, D3 +5V, **D5 DONE** (off = FPGA configured), D6 RGB status |
| Carrier interface | **P1–P4**, four 2×14 headers, 2.54 mm: the geometry and the pin contract of bontango's 10CL006 devboard, so the module plugs into the same FA carriers |
| Also | **P5** JTAG (2×5), **P7** I2C OLED header (1×4), **JP1** solder jumper bridging the NOR chip select between the ESP and the FPGA |

## Read this before powering a V1.0 board

1. **P6 polarity.** On the first batch (V1.0) the 5 V input **P6 is reversed relative to the
   LISY convention**: the square pad P6.1 is **+5 V**, P6.2 is GND. There is **no
   reverse-polarity protection** — +5 V goes straight into the 3.3 V regulator. Cross the two
   wires of the P6 cable and mark it. The pre-series revision adds ideal-diode ORing
   (LM66100) and silkscreen.
2. **Never feed the USB-C and P6 at the same time** on V1.0: same +5 V node, no diode.
3. **Solenoid power off during any FPGA configuration or U5 write.** HSWAPEN is grounded, so
   the I/Os pull up while the FPGA configures; the carrier's coil drivers are active-high.
   Logic 5 V is all a burn needs.
4. P1–P4 only carry 3.3 V and 1.2 V *outputs*. Plugging the module onto a carrier does not
   power it; +5 V enters through P6 or the USB-C only.

## Schematics

| File | |
|---|---|
| [`schematic/SmartFA_schematic_sheet.pdf`](schematic/SmartFA_schematic_sheet.pdf) | **one A3 sheet**, drawn in the style of the 10CL006 devboard schematic: the FPGA in the centre with function and number on all 144 pins, one connector per side, wires fanned to every pin, side blocks for the ESP (real GPIOs), the flashes, JP1, JTAG, P6 and the crystal |
| [`schematic/SmartFA_wiring.pdf`](schematic/SmartFA_wiring.pdf) | **7 pages**: bus overview with the FA-board compatibility points, then one connector per page with one wire per pin and the other parts on the net, then the internal links |
| [`schematic/GottFA_SLX16_Module_schematic.pdf`](schematic/GottFA_SLX16_Module_schematic.pdf) | the KiCad schematic itself (six label-based sheets), exported with `kicad-cli` |

The first two are **generated from the netlist** by the scripts in [`tools/`](tools/README.md),
so they are exact by construction — the same source KiCad uses.

## Pin tables (generated from the netlist)

- [`pinout/connectors.md`](pinout/connectors.md) — P1–P4, pin by pin: net, FPGA pin, ESP GPIO, other parts on the net
- [`pinout/esp32.md`](pinout/esp32.md) — every connected pad of the ESP32-S3 module with its real GPIO
- [`pinout/fpga.md`](pinout/fpga.md) — all 144 Spartan-6 pins; the three I/Os that reach nothing are U1.33, U1.34, U1.47
- [`pinout/internal.md`](pinout/internal.md) — U5, U6, JP1, P5, P6, J1, P7

The constraint file that builds the bitstream is
[`GottFA80_SLX9.ucf`](https://github.com/Vapi27/GottFA80_PLuS/blob/spartan6-feasibility/GottFA80_SLX9.ucf)
in the FPGA repository.

## The ESP ↔ FPGA link

Five wires, all on the module (details and protocols: [`docs/esp-fpga-link.md`](docs/esp-fpga-link.md)):

| ESP GPIO | net | FPGA | carries |
|---|---|---|---|
| 18 | `ESP32_RX` | U1.142 | FPGA → ESP: status beacon, sound commands, telemetry (115 200 8N1) |
| 47 | `ESP32_TX` | U1.143 | ESP → FPGA: 14-bit audio samples (441 000 baud) and display injection |
| 21 | `FA_CTRL_REQ` | U1.141 | ESP → FPGA, active low: control/request line (hold the 6502, take the SPI bus) |
| 44 (RXD0) | `Debug` | U1.46 | also carrier P4.11 |
| 43 (TXD0) | `Audio_RX` | U1.41 | also carrier P4.4 |

## The shared SPI bus

`CLK` / `MOSI` / `MISO` join the FPGA (U1.67 / U1.66 / U1.62), the game NOR U6, the ESP
(GPIO14 / 13 / 16) and the carrier (P4.24 / P4.23 / P4.22). Chip selects: `NOR_CS` from ESP
GPIO15, bridged by **JP1** to `NOR_CS_FPGA` (U1.35); `CS_EEprom` on P4.21 (U1.61) for the
carrier's NVRAM; `CS_SDcard` on P4.15 (U1.56), unused — the module has no SD socket. The FPGA
owns the bus while the game runs and hands it to the ESP on request.

Because the SPI position differs from one FA board to the next, the NOR moves **inside** the
module in the next revision — see [`docs/next-revision.md`](docs/next-revision.md), which also
covers bontango's proposal for a universal ESP↔FPGA link on three connector positions.

## Status

- **V1.0**: first batch, September 2026. Boots the game from the NOR and plays in real machines
  (Volcano, System 80; Hot Shots, System 80B), with GOSOF80 sound effects from the FPGA and
  speech from the ESP summed into the carrier's audio stage.
- **Pre-series revision** (decided 2026-09-02): +5 V ideal-diode ORing and protection, 0 Ω
  series positions on the shared SPI bus, DONE LED rewired, extra decoupling at the ESP.

## Regenerating the PDFs and tables

[`tools/README.md`](tools/README.md). `tools/smartfa_nets.json` is the netlist the generators
consume, exported from the KiCad schematic on 2026-09-12 (153 nets, 512 nodes).

## Licence

See [`NOTICE`](NOTICE). Copyright © 2026 Valère Pillet / Pstore.
