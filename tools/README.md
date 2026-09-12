# tools/ — GottFA_SLX16 module (Smart FA)

The KiCad schematic of this module is **label-only**: a net label on every pin, no drawn
wire. Fine for KiCad, unreadable for anyone who has to follow a connection from sheet to
sheet — Ralf asked for a schematic "with cables". Both scripts below generate one from the
**netlist**, so they are exact by construction (same source KiCad uses). Hand-written
vector PDF, no Python dependency. All output is in English.

## `schema_feuille.py` — single sheet, in the style of Ralf's 10CL006 devboard schematic

The FPGA in the centre with **pin function + pin number** on all 144 pins, one 2x14 connector
per side (P2 top, P1 right, P4 bottom, P3 left — the devboard geometry the module
reproduces), and **wire fans** from every FPGA pin to its connector pin. Near-row pins are
labelled on the FPGA side, far-row pins on the outside, so nothing overlaps. Side blocks for
the ESP32 (with the **real GPIO**, not the pad number), the game NOR, the config flash, JP1,
JTAG, P6 and the crystal. A3 landscape. -> `SmartFA_schematic_sheet.pdf`

## `schema_fils.py` — 7 pages, one connector per page

Overview of the buses (with the FA-board compatibility points), then P1..P5 with one wire per
pin to its FPGA pin and the other parts of the net along the wire, then the internal links
(config U5, ESP link, shared NOR bus, free FPGA IOs). -> `SmartFA_wiring.pdf`

## Regenerate

```bash
K=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
$K sch export netlist --format kicadxml -o /tmp/smartfa.xml GottFA_SLX16_Module.kicad_sch
python3 - <<'PY'   # XML netlist -> the JSON both scripts expect
import xml.etree.ElementTree as ET, json
r=ET.parse('/tmp/smartfa.xml').getroot()
comps={c.get('ref'):{'value':c.findtext('value') or '','fp':c.findtext('footprint') or ''} for c in r.find('components')}
nets=[{'name':n.get('name'),'nodes':[{'ref':x.get('ref'),'pin':x.get('pin'),'fn':x.get('pinfunction') or '','type':x.get('pintype') or ''} for x in n.findall('node')]} for n in r.find('nets')]
json.dump({'comps':comps,'nets':nets},open('/tmp/smartfa_nets.json','w'))
PY
python3 tools/schema_feuille.py /tmp/smartfa_nets.json SmartFA_schematic_sheet.pdf
python3 tools/schema_fils.py    /tmp/smartfa_nets.json SmartFA_wiring.pdf
```

⚠️ ESP module pad numbers (`U7.36`) are NOT GPIOs. The scripts print the pin function read
from the netlist (`RXD0`, `IO47`...). Getting this wrong has cost this project several times.

⚠️ `Debug` (P46) and `Audio_RX` (P41) reach the ESP's UART0 (RXD0 = GPIO44, TXD0 = GPIO43)
AND connector P4.11 / P4.4. Five ESP<->FPGA wires in total, not three.
