# Next revision — what changes and why

## 1. A universal ESP ↔ FPGA link on the carrier connector (bontango's proposal, 2026-09-07)

Ralf Thelen (bontango) pointed out that three positions of the FA-board interface are unused
on **every** FA board: absent on the Cyclone II and Cyclone 10 boards (NU), and PIN_75/84/85
on the Cyclone IV board, never assigned. His proposal: *"if you use these three pins to
communicate between ESP32 and FPGA (e.g. via serial protocol) it would fit to all FA
boards."* He names them **P2.59, P2.64, P2.65**.

Our reading of that numbering — to be confirmed with him — is positions **3, 8 and 9 of the
P2 header** (1–28 numbering). On the Smart FA V1.0 netlist
([`../pinout/connectors.md`](../pinout/connectors.md)):

| position | V1.0 | note |
|---|---|---|
| P2.3 | not connected | needs a PCB change |
| P2.8 | `SPARE_IO_1` → U1.116 | FPGA I/O already there, unused by the design |
| P2.9 | `SPARE_IO_2` → U1.117 | FPGA I/O already there, unused by the design |

So a **two-wire serial link (FPGA TX / RX) on P2.8 and P2.9 is possible on the V1.0 boards
with a bitstream change only**; the third position needs the next PCB. Our own link uses three
signals internally (`ESP32_RX`, `ESP32_TX`, `FA_CTRL_REQ` — see
[`esp-fpga-link.md`](esp-fpga-link.md)); whether the third one is needed on the connector, and
which protocol both projects should speak, is the open question for bontango.

## 2. The game NOR moves inside the module

The SPI bus is **not at the same connector position on every FA board** (on WillFA7, P4.21–24
are the DIP strobes). So a NOR hanging on the connector's SPI position can never be universal.
Options for the next revision:

- the FPGA has exactly **three I/Os that reach no connector** — U1.33, U1.34, U1.47 — plus
  `NOR_CS_FPGA` (U1.35), already internal: CLK + MOSI + MISO + CS fit, with no margin;
- or hang U6 on the configuration-flash bus (U1.64 / U1.65 / U1.70, dual-use pins that become
  I/O after configuration) with its own chip select.

In both cases the ESP loses its direct path to the NOR and writes it **through the FPGA** (a
bridge, like the JTAG-to-SPI one that already programs U5).

## 3. Power input

- **P6 polarity** aligned with the LISY convention, silkscreen `+5V` / `GND` on the copper
  side that is actually fabricated (the V1.0 text sat on `F.Fab`).
- Ideal-diode ORing and reverse protection on the +5 V input (two LM66100, pre-series change
  no. 1), so USB-C and P6 can coexist and a reversed cable no longer destroys the regulators.

## 4. Smaller items from the pre-series list

0 Ω series positions on the shared SPI bus (to fit damping resistors if the bus rings),
`DONE` LED rewired, 47 µF reserve next to the ESP (an ESP flash was found blank once; a supply
dip during a write is the working hypothesis).
