# The ESP ↔ FPGA link on the Smart FA

Five wires join the ESP32-S3 (U7) and the Spartan-6 (U1) on the module. Pin numbers below are
from the netlist ([`../pinout/esp32.md`](../pinout/esp32.md)); the protocols are implemented in
[`lib_common/sound_link.vhd`](https://github.com/Vapi27/GottFA80_PLuS/blob/spartan6-feasibility/lib_common/sound_link.vhd),
[`game_beacon.vhd`](https://github.com/Vapi27/GottFA80_PLuS/blob/spartan6-feasibility/lib_common/game_beacon.vhd),
[`audio_uart.vhd`](https://github.com/Vapi27/GottFA80_PLuS/blob/spartan6-feasibility/lib_common/audio_uart.vhd) and
[`disp_inject.vhd`](https://github.com/Vapi27/GottFA80_PLuS/blob/spartan6-feasibility/lib_common/disp_inject.vhd)
on the FPGA side, and `src/fpgalink.cpp` / `src/wavplayer.cpp` / `src/dispinject.cpp` in
[gottfa-esp32](https://github.com/Vapi27/gottfa-esp32).

## 1. `ESP32_RX` — FPGA U1.142 → ESP GPIO18, 115 200 8N1

One wire, FPGA transmits. The byte map is allocated in the header of `sound_link.vhd`, which is
the single authority. Summary:

| bytes | meaning |
|---|---|
| `0x80 \| code` | a sound command latched by the game CPU (one event per strobed write) |
| `0x30` | sound bus released; `0x31` = event FIFO overflowed |
| `0x40 \| game` | the selected game number (true gamelist number) |
| `0xA0 \| ball` | ball in play |
| `0xF0 / 0xF1` | diag mode off / on; `0xF2 / 0xF3` game over / running; `0xF4 \| family` |
| `0xF8 / 0xF9` | radio token: WiFi allowed / WiFi off (carrier DIP S1-6) |
| `0xFA` + 3 bytes | **status beacon**, one atomic 4-byte frame: game number and family, 6502 out of reset, 80A/80B, running, with a checksum — emitted as a burst so a checksum byte can never be mistaken for a sound command |
| `0xBF`, `0xC0–0xDF` | RAM snapshot frame marker and payload nibbles (the "glass mirror") |
| `0xB0–0xBE`, `0xE0–0xEF` | display-injection feedback: byte counter and state |
| `0x00–0x2F` | free, and a no-op forever: a floating wire decodes as 0x00 |

The game CPU rewrites its sound port on every RIOT port-A write while a code is selected, so
the FPGA re-emits the code many times: the ESP plays **one cue per code until `0x30`**.

## 2. `ESP32_TX` — ESP GPIO47 → FPGA U1.143

Two uses of one wire:

- **Audio**, 441 000 baud 8N1: each 22 050 Hz sample is 14 bits in two self-framing bytes
  (`0 & s[13:7]`, then `1 & s[6:0]`), i.e. 20 line bits per sample, so the baud rate *is* the
  sample rate × 20. `audio_uart.vhd` reassembles the samples and sums them with GOSOF80's own
  output before the single delta-sigma modulator that drives the carrier's audio stage (P4.6
  `Sound` → RC → TDA7267). Dither and first-order noise shaping are applied on the ESP.
- **Display injection / control frames** (`disp_inject.vhd`) when no audio is streaming.

## 3. `FA_CTRL_REQ` — ESP GPIO21 → FPGA U1.141, active low

The control/request line: held low it puts the 6502 in reset and hands the lamps, coils and
the shared SPI bus to the LISYcontrol bridge. It is filtered: a dip shorter than **100 ms** is
ignored, because an ESP reboot (and opening its serial port reboots it) produces a short low
pulse that used to freeze the machine.

## 4 and 5. `Debug` and `Audio_RX` — the ESP's UART0

`Debug` (FPGA U1.46) reaches ESP **RXD0 / GPIO44** *and* carrier **P4.11**; `Audio_RX` (U1.41)
reaches ESP **TXD0 / GPIO43** *and* carrier **P4.4**. On the Cyclone boards these were the
devboard's debug pin and the DFPlayer serial input. Consequence: a firmware whose console is on
UART0 logs onto `Audio_RX` / P4.4 and receives whatever the FPGA emits on `Debug`.

## The bus hand-over

The FPGA owns CLK/MOSI/MISO while the game runs. To reach the game NOR (U6) the ESP asserts
`FA_CTRL_REQ` (the bridge exposes a `BUSREQ` register too); the FPGA parks its SPI outputs and
the ESP drives the bus with its own chip select (`NOR_CS`, bridged to the FPGA's
`NOR_CS_FPGA` through JP1). On the current FPGA build the ESP can write the NOR but not read
it back through the FPGA's MISO mux.
