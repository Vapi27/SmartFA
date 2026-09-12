#!/usr/bin/env python3
# schema_fils.py -- schema de cablage LISIBLE du Smart FA, genere depuis la netliste.
# Chaque broche de connecteur est reliee par un FIL trace a sa broche FPGA, avec le nom
# du net sur le fil et les autres composants du net (NOR, ESP, cavalier...) sur le
# trajet. Exact par construction : meme netliste que KiCad. PDF vectoriel ecrit a la
# main (aucune dependance).
import json, re, sys

J = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
nets = J['nets']; comps = J['comps']

# ---------------------------------------------------------------- mini-ecrivain PDF
class PDF:
    def __init__(s, w=842, h=595): s.w, s.h, s.pages = w, h, []
    def page(s): s.ops = []; s.pages.append(s.ops)
    def line(s, x1, y1, x2, y2, lw=0.8, rgb=(0,0,0)):
        s.ops.append("%.2f %.2f %.2f RG %.2f w %.2f %.2f m %.2f %.2f l S" % (rgb + (lw, x1, y1, x2, y2)))
    def rect(s, x, y, w, h, lw=0.8, fill=None, rgb=(0,0,0)):
        if fill: s.ops.append("%.2f %.2f %.2f rg %.2f %.2f %.2f %.2f re f" % (fill + (x, y, w, h)))
        s.ops.append("%.2f %.2f %.2f RG %.2f w %.2f %.2f %.2f %.2f re S" % (rgb + (lw, x, y, w, h)))
    def text(s, x, y, t, size=8, bold=False, rgb=(0,0,0), align='l'):
        t = t.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        t = ''.join(c if ord(c) < 128 else '?' for c in t)
        if align == 'r': x -= s.width(t, size)
        elif align == 'c': x -= s.width(t, size) / 2
        s.ops.append("BT /%s %.1f Tf %.2f %.2f %.2f rg %.2f %.2f Td (%s) Tj ET" % ('F2' if bold else 'F1', size, rgb[0], rgb[1], rgb[2], x, y, t))
    def width(s, t, size): return len(t) * size * 0.52
    def save(s, path):
        objs = []
        def add(o): objs.append(o); return len(objs)
        f1 = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        f2 = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        pids = []
        for ops in s.pages:
            st = "\n".join(ops).encode('latin-1', 'replace')
            c = add(b"<< /Length %d >>\nstream\n" % len(st) + st + b"\nendstream")
            pids.append(add("<< /Type /Page /Parent PARENT /MediaBox [0 0 %d %d] /Contents %d 0 R /Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> >>" % (s.w, s.h, c, f1, f2)))
        pages = add("<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % p for p in pids), len(pids)))
        cat = add("<< /Type /Catalog /Pages %d 0 R >>" % pages)
        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
        for i, o in enumerate(objs, 1):
            if isinstance(o, str): o = o.replace("PARENT", "%d 0 R" % pages).encode('latin-1')
            offs.append(len(out)); out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
        xref = len(out)
        out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
        for o in offs: out += b"%010d 00000 n \n" % o
        out += b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, cat, xref)
        open(path, 'wb').write(out)

# ---------------------------------------------------------------- donnees
def net_of(ref, pin):
    for n in nets:
        for x in n['nodes']:
            if x['ref'] == ref and x['pin'] == pin: return n
    return None
def is_power(name): return bool(re.match(r'^(GND|VCC|\+|VBUS|3V3|5V|VDD)', name or ''))
def fn_short(x):
    f = x['fn'] or ''
    if x['ref'] == 'U1': return re.sub(r'^IO_', '', f)[:22]
    if x['ref'] == 'U7': return f[:8]
    return f[:10]
def libelle(ref):
    v = comps.get(ref, {}).get('value', '')
    return {'U1': 'FPGA XC6SLX9', 'U5': 'U5 config flash', 'U6': 'U6 game NOR', 'U7': 'U7 ESP32-S3',
            'JP1': 'JP1 jumper'}.get(ref, ref + (' ' + v[:14] if v else ''))

GRIS = (0.45, 0.45, 0.45); BLEU = (0.10, 0.30, 0.65); ROUGE = (0.75, 0.15, 0.10); VERT = (0.10, 0.5, 0.25)
FOND = (0.96, 0.96, 0.93)
pdf = PDF()

def cartouche(titre, sous):
    pdf.rect(20, 20, 802, 555, lw=1.0)
    pdf.text(30, 560, titre, 13, bold=True)
    pdf.text(30, 546, sous, 8, rgb=GRIS)
    pdf.text(812, 26, "Smart FA / GottFA_SLX16 -- generated from the KiCad netlist, 2026-09-07 -- Pstore", 6.5, rgb=GRIS, align='r')

# ---------------------------------------------------------------- page 1 : vue d ensemble
pdf.page()
cartouche("Smart FA (GottFA_SLX16 module) -- bus overview",
          "What each link carries. The following pages wire every connector pin to its FPGA pin.")
def boite(x, y, w, h, titre, lignes=(), fill=FOND):
    pdf.rect(x, y, w, h, lw=1.0, fill=fill)
    pdf.text(x + w / 2, y + h - 14, titre, 9, bold=True, align='c')
    for i, l in enumerate(lignes): pdf.text(x + 8, y + h - 28 - 11 * i, l, 7.5)
boite(330, 250, 190, 250, "U1  FPGA XC6SLX9-2TQG144", [
    "144 pins, 125 reach a connector",
    "3 free IOs reaching no connector:",
    "   P33, P34, P47",
    "config: P38 CS, P64 MOSI, P65 MISO, P70 CCLK",
    "game NOR: P61 CS, P62 MISO, P66 MOSI, P67 CLK",
    "ESP link: P141 CTRL_REQ, P142 ->ESP IO18, P143 <-ESP IO47",
    "  + ESP UART0: P46 Debug ->RXD0, P41 Audio_RX <-TXD0",
    "clock: P51 <- Y2 50 MHz"])
boite(60, 420, 170, 80, "U5  W25Q32  config flash", ["FPGA dedicated config SPI bus", "(configuration pins)"])
boite(60, 300, 170, 80, "U6  W25Q32  game NOR", ["on the SHARED bus P4.21-24", "CS via JP1 -> P35 (FPGA)"])
boite(60, 170, 170, 90, "U7  ESP32-S3-WROOM-1", ["serial link: IO18 RX, IO47 TX, IO21 REQ", "UART0: RXD0<-Debug, TXD0->Audio_RX", "shared SPI: IO13 MOSI IO14 CLK IO16 MISO"])
boite(620, 400, 180, 100, "P1 / P2 / P3  (3 x 28)", ["display, U4/U5/U6 PA-PB", "(Cyclone 10 devboard contract)"])
boite(620, 270, 180, 100, "P4  (28)  LED / sound / SPI", ["P4.21 CS_EEprom  P4.22 MISO", "P4.23 MOSI  P4.24 CLK", "= the U6 NOR bus, exposed"])
boite(620, 150, 180, 90, "P5 JTAG (10)  /  P6 5V (2)", ["JTAG: ESP IO4..7 -> FPGA", "P6: +5V from machine (P6.1 = +5V)"])
def fil(x1, y1, x2, y2, txt, rgb=BLEU, dy=4):
    pdf.line(x1, y1, x2, y2, lw=1.2, rgb=rgb); pdf.text((x1 + x2) / 2, (y1 + y2) / 2 + dy, txt, 7, rgb=rgb, align='c')
fil(230, 460, 330, 440, "config SPI (4 wires)")
fil(230, 340, 330, 380, "NOR bus: CLK/MOSI/MISO + CS", ROUGE)
fil(230, 220, 330, 320, "ESP<->FPGA serial (5 wires)", VERT)
fil(520, 450, 620, 450, "3.3 V IO", GRIS)
fil(520, 330, 620, 320, "NOR bus exposed on P4.21-24", ROUGE)
fil(520, 290, 620, 200, "JTAG", GRIS)
pdf.line(230, 300, 300, 300, lw=1.2, rgb=ROUGE); pdf.line(300, 300, 300, 175, lw=1.2, rgb=ROUGE); pdf.line(300, 175, 230, 175, lw=1.2, rgb=ROUGE)
pdf.text(305, 235, "the ESP is ALSO on", 7, rgb=ROUGE); pdf.text(305, 226, "the NOR bus", 7, rgb=ROUGE)
pdf.rect(60, 40, 740, 110, lw=0.8, fill=(1, 0.98, 0.9))
pdf.text(70, 135, "What this module cannot do, and why (reply to Ralf, 2026-09-07)", 8.5, bold=True)
for i, l in enumerate([
    "- P4.21..24 = the NOR SPI bus, at the GottFA80 positions. On WillFA7 those positions are the DIP strobes: incompatible.",
    "- SPI is not at the same place from one FA board to the next (Ralf): a NOR on the connector can never be universal.",
    "- P2.59, P2.64, P2.65: NOT CONNECTED on this module, and free on every FA board -> the designated place for the ESP<->FPGA serial link.",
    "- For an internal NOR: only 3 FPGA IOs reach no connector (P33, P34, P47) + CS P35. CLK+MOSI+MISO+CS fits, with no spare.",
    "- The ESP would then lose direct NOR access: U6 written through the FPGA (a bridge), as U5 is already programmed through the BSCAN bridge."]):
    pdf.text(70, 120 - 13 * i, l, 7.2)

# ---------------------------------------------------------------- pages connecteurs
def page_connecteur(ref, titre):
    pdf.page()
    cartouche("%s -- %s" % (ref, titre), "Every pin is wired to its FPGA pin; the other parts on the same net sit along the wire. Power in grey.")
    pins = sorted({int(x['pin']) for n in nets for x in n['nodes'] if x['ref'] == ref})
    n = len(pins); pas = min(17.0, 470.0 / max(n, 1)); y0 = 520
    X0, XM, XF = 95, 430, 720
    pdf.rect(X0 - 35, y0 - pas * (n - 1) - 12, 34, pas * (n - 1) + 24, lw=1.0, fill=FOND)
    pdf.text(X0 - 18, y0 + 18, ref, 9, bold=True, align='c')
    pdf.rect(XF, y0 - pas * (n - 1) - 12, 95, pas * (n - 1) + 24, lw=1.0, fill=FOND)
    pdf.text(XF + 47, y0 + 18, "U1  FPGA", 9, bold=True, align='c')
    for i, p in enumerate(pins):
        y = y0 - i * pas
        pdf.text(X0 - 18, y - 2.5, str(p), 7.5, bold=True, align='c')
        net = net_of(ref, str(p))
        if not net: pdf.text(X0 + 6, y - 2.5, "n.c.", 7, rgb=GRIS); continue
        name = net['name'] or ''
        autres = [x for x in net['nodes'] if x['ref'] != ref]
        fpga = [x for x in autres if x['ref'] == 'U1']
        reste = [x for x in autres if x['ref'] != 'U1' and not re.match(r'^P[1-6]$', x['ref'])]
        autres_conn = [x for x in autres if re.match(r'^P[1-6]$', x['ref'])]
        if is_power(name):
            pdf.line(X0, y, X0 + 40, y, lw=1.2, rgb=GRIS); pdf.text(X0 + 44, y - 2.5, name, 7, rgb=GRIS); continue
        couleur = ROUGE if name in ('CLK', 'MOSI', 'MISO', 'CS_EEprom') else BLEU
        xfin = XF if fpga else XM + 120
        pdf.line(X0, y, xfin, y, lw=1.0, rgb=couleur)
        pdf.text(X0 + 6, y + 2, name, 7, bold=True, rgb=couleur)
        if reste:
            t = "  ".join("%s.%s%s" % (x['ref'], x['pin'], (' ' + fn_short(x)) if x['ref'] in ('U6', 'U7', 'U5') and fn_short(x) else '') for x in reste)
            pdf.text(XM, y + 2, t[:60], 6.5, rgb=(0.3, 0.3, 0.3))
        if autres_conn:
            pdf.text(XM, y - 6, "also: " + " ".join("%s.%s" % (x['ref'], x['pin']) for x in autres_conn), 6, rgb=GRIS)
        for k, x in enumerate(fpga[:2]):
            pdf.text(XF + 4, y - 2.5 - 7 * k, "P%s" % x['pin'], 7.5, bold=True)
            pdf.text(XF + 30, y - 2.5 - 7 * k, fn_short(x), 6, rgb=GRIS)

page_connecteur('P1', 'display')
page_connecteur('P2', 'U5/U6 port A-B' + "   (P2.59/64/65 do not exist on this 28-pin module: see page 1)")
page_connecteur('P3', 'U4/U6 port A-B')
page_connecteur('P4', 'LED / sound / SPI')
page_connecteur('P5', 'JTAG')

# ---------------------------------------------------------------- page : liaisons internes
pdf.page()
cartouche("Internal links (no connector) -- config U5, NOR U6, ESP link, jumper JP1",
          "The nets that never leave the module. This is where compatibility with the other FA boards is decided.")
y = 500
def section(titre):
    global y
    pdf.text(40, y, titre, 9, bold=True); y -= 14
def ligne(a, b, name, extra=''):
    global y
    pdf.text(60, y - 2, a, 7.5, bold=True); pdf.line(180, y, 460, y, lw=1.0, rgb=BLEU)
    pdf.text(320, y + 2, name, 7, bold=True, rgb=BLEU, align='c'); pdf.text(468, y - 2, b, 7.5, bold=True)
    if extra: pdf.text(640, y - 2, extra, 6.5, rgb=GRIS)
    y -= 13
def nets_between(refA, refB):
    out = []
    for n in nets:
        a = [x for x in n['nodes'] if x['ref'] == refA]; b = [x for x in n['nodes'] if x['ref'] == refB]
        if a and b and not any(re.match(r'^P[1-6]$', x['ref']) for x in n['nodes']):
            out.append((n['name'], a[0], b[0], [x for x in n['nodes'] if x['ref'] not in (refA, refB)]))
    return sorted(out, key=lambda t: int(t[1]['pin']))
section("Config flash U5 <-> FPGA (configuration pins, not exposed)")
for name, a, b, r in nets_between('U1', 'U5'):
    ligne("U1.P%s %s" % (a['pin'], fn_short(a)), "U5.%s %s" % (b['pin'], fn_short(b)), name)
y -= 6; section("ESP32 <-> FPGA serial link (three internal wires -> candidates for P2.59/64/65 on the next board)")
for name, a, b, r in nets_between('U1', 'U7'):
    if name in ('CLK', 'MOSI', 'MISO'): continue
    ligne("U1.P%s %s" % (a['pin'], fn_short(a)), "U7.%s %s" % (b['pin'], fn_short(b)), name)
y -= 6; section("U6 NOR bus -- SHARED between FPGA, ESP and connector P4 (the WillFA7 conflict)")
for name in ('CLK', 'MOSI', 'MISO', 'NOR_CS_FPGA', 'NOR_CS', 'CS_EEprom'):
    for n in nets:
        if n['name'] == name:
            t = "   ".join("%s.%s%s" % (x['ref'], x['pin'], (' ' + fn_short(x)) if x['ref'] in ('U1', 'U6', 'U7') else '') for x in n['nodes'])
            pdf.text(60, y - 2, name, 7.5, bold=True, rgb=ROUGE); pdf.text(150, y - 2, t[:118], 6.5); y -= 13
y -= 6; section("Free FPGA IOs reaching NO connector (the only place for an internal NOR)")
for n in nets:
    for x in n['nodes']:
        if x['ref'] == 'U1' and n['name'].startswith('unconnected'):
            pdf.text(60, y - 2, "U1.P%s   %s   (not connected)" % (x['pin'], fn_short(x)), 7.5, rgb=VERT); y -= 12

pdf.save(OUT)
print("PDF ecrit :", OUT, "-", len(pdf.pages), "pages")
