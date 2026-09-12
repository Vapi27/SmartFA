#!/usr/bin/env python3
# schema_feuille.py -- LE schema du Smart FA sur UNE feuille A3, dans le style du
# 10CL006_dev_board de Ralf : le FPGA au centre avec fonction + numero sur chaque broche,
# un connecteur 2x14 par cote, et des NAPPES DE FILS tirees de chaque broche FPGA a sa
# broche de connecteur. Genere depuis la netliste KiCad -> exact par construction.
# PDF vectoriel ecrit a la main, aucune dependance.
import json, re, sys
from collections import defaultdict
J = json.load(open(sys.argv[1])); OUT = sys.argv[2]
nets, comps = J['nets'], J['comps']

# ---------------------------------------------------------------- mini PDF
class PDF:
    def __init__(s, w=1190, h=842): s.w, s.h, s.ops = w, h, []
    def line(s, x1, y1, x2, y2, lw=0.6, rgb=(0, 0, 0)):
        s.ops.append("%.2f %.2f %.2f RG %.2f w %.2f %.2f m %.2f %.2f l S" % (rgb + (lw, x1, y1, x2, y2)))
    def poly(s, pts, lw=0.6, rgb=(0, 0, 0)):
        if len(pts) < 2: return
        p = "%.2f %.2f m " % pts[0] + " ".join("%.2f %.2f l" % q for q in pts[1:])
        s.ops.append("%.2f %.2f %.2f RG %.2f w %s S" % (rgb + (lw, p)))
    def rect(s, x, y, w, h, lw=0.7, fill=None, rgb=(0, 0, 0)):
        if fill: s.ops.append("%.2f %.2f %.2f rg %.2f %.2f %.2f %.2f re f" % (fill + (x, y, w, h)))
        s.ops.append("%.2f %.2f %.2f RG %.2f w %.2f %.2f %.2f %.2f re S" % (rgb + (lw, x, y, w, h)))
    def dot(s, x, y, r=1.4, rgb=(0, 0, 0)):
        s.ops.append("%.2f %.2f %.2f rg %.2f %.2f %.2f %.2f re f" % (rgb + (x - r, y - r, 2 * r, 2 * r)))
    def text(s, x, y, t, size=6, bold=False, rgb=(0, 0, 0), align='l', rot=0):
        t = ''.join(c if ord(c) < 128 else '?' for c in t).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        w = len(t) * size * 0.52
        if rot == 0:
            if align == 'r': x -= w
            elif align == 'c': x -= w / 2
            s.ops.append("BT /%s %.1f Tf %.2f %.2f %.2f rg %.2f %.2f Td (%s) Tj ET" % ('F2' if bold else 'F1', size, rgb[0], rgb[1], rgb[2], x, y, t))
        else:  # 90 degres, texte vers le haut ; align sur la longueur
            if align == 'r': y -= w
            elif align == 'c': y -= w / 2
            s.ops.append("BT /%s %.1f Tf %.2f %.2f %.2f rg 0 1 -1 0 %.2f %.2f Tm (%s) Tj ET" % ('F2' if bold else 'F1', size, rgb[0], rgb[1], rgb[2], x, y, t))
    def save(s, path):
        st = "\n".join(s.ops).encode('latin-1', 'replace')
        objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
                b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
                b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>" % (s.w, s.h),
                b"<< /Length %d >>\nstream\n" % len(st) + st + b"\nendstream",
                b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
                b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"]
        out = bytearray(b"%PDF-1.4\n"); offs = []
        for i, o in enumerate(objs, 1): offs.append(len(out)); out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
        x = len(out); out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
        for o in offs: out += b"%010d 00000 n \n" % o
        out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
        open(path, 'wb').write(out)

VERT = (0.0, 0.55, 0.0); ROUGE = (0.8, 0.1, 0.1); BLEU = (0.0, 0.0, 0.7); GRIS = (0.4, 0.4, 0.4); FOND = (0.97, 0.97, 0.94)
pdf = PDF()

# ---------------------------------------------------------------- donnees
def is_power(name): return bool(re.match(r'^(GND|VCC|\+|VBUS|3V3|5V|VDD)', name or ''))
net_by_node = {}
for n in nets:
    for x in n['nodes']: net_by_node[(x['ref'], x['pin'])] = n
def fn_of(ref, pin):
    n = net_by_node.get((ref, pin))
    if not n: return ''
    for x in n['nodes']:
        if x['ref'] == ref and x['pin'] == pin: return x['fn']
    return ''
def fpga_label(pin):
    f = fn_of('U1', str(pin)); f = re.sub(r'_%d$' % pin, '', f)          # enlever le suffixe _NN
    f = re.sub(r'^IO_', '', f)
    return f[:20]

# ---------------------------------------------------------------- FPGA au centre
CX, CY = 595, 445
PITCH = 6.5; SPAN = 35 * PITCH                 # 36 broches par cote
BOX = SPAN + 40; HALF = BOX / 2
L, R, B, T = CX - HALF, CX + HALF, CY - HALF, CY + HALF
PINLEN = 16
def fpga_pin_xy(p):
    """coordonnees de l extremite exterieure de la broche p, et la direction sortante"""
    p = int(p)
    if p <= 36:   return (L - PINLEN, T - 20 - (p - 1) * PITCH, 'g')             # gauche, haut->bas
    if p <= 72:   return (L + 20 + (p - 37) * PITCH, B - PINLEN, 'b')            # bas, gauche->droite
    if p <= 108:  return (R + PINLEN, B + 20 + (p - 73) * PITCH, 'd')            # droite, bas->haut
    return (R - 20 - (p - 109) * PITCH, T + PINLEN, 'h')                          # haut, droite->gauche
pdf.rect(L, B, BOX, BOX, lw=1.2, fill=FOND)
pdf.text(CX, CY + 12, "U1", 11, bold=True, align='c')
pdf.text(CX, CY - 2, "XC6SLX9-2TQG144C", 8, bold=True, align='c')
pdf.text(CX, CY - 13, "Spartan-6, TQFP-144", 6.5, rgb=GRIS, align='c')
for p in range(1, 145):
    x, y, d = fpga_pin_xy(p); lab = fpga_label(p); n = net_by_node.get(('U1', str(p)))
    name = n['name'] if n else ''
    pw = is_power(name)
    if d == 'g':
        pdf.line(x, y, L, y, lw=0.7); pdf.text(L + 3, y - 2, lab, 4.6, rgb=GRIS); pdf.text(x + 8, y + 1.2, str(p), 4.2, rgb=ROUGE, align='c')
    elif d == 'd':
        pdf.line(R, y, x, y, lw=0.7); pdf.text(R - 3, y - 2, lab, 4.6, rgb=GRIS, align='r'); pdf.text(x - 8, y + 1.2, str(p), 4.2, rgb=ROUGE, align='c')
    elif d == 'b':
        pdf.line(x, B, x, y, lw=0.7); pdf.text(x + 2, B + 3, lab, 4.6, rgb=GRIS, rot=90); pdf.text(x - 1.5, y + 6, str(p), 4.2, rgb=ROUGE, rot=90, align='c')
    else:
        pdf.line(x, T, x, y, lw=0.7); pdf.text(x + 2, T - 3, lab, 4.6, rgb=GRIS, rot=90, align='r'); pdf.text(x - 1.5, y - 6, str(p), 4.2, rgb=ROUGE, rot=90, align='c')
    if pw:   # alimentation : stub + nom
        if d == 'g':   pdf.line(x, y, x - 10, y, lw=0.7, rgb=GRIS); pdf.text(x - 12, y - 2, name, 4.5, rgb=GRIS, align='r')
        elif d == 'd': pdf.line(x, y, x + 10, y, lw=0.7, rgb=GRIS); pdf.text(x + 12, y - 2, name, 4.5, rgb=GRIS)
        elif d == 'b': pdf.line(x, y, x, y - 10, lw=0.7, rgb=GRIS); pdf.text(x + 1.5, y - 12, name, 4.5, rgb=GRIS, rot=90, align='r')
        else:          pdf.line(x, y, x, y + 10, lw=0.7, rgb=GRIS); pdf.text(x + 1.5, y + 12, name, 4.5, rgb=GRIS, rot=90)

# ---------------------------------------------------------------- connecteurs 2x14
CONN_NAME = {'P1': 'display', 'P2': 'U5/U6 port A-B', 'P3': 'U4/U6 port A-B', 'P4': 'LED / sound / SPI',
             'P5': 'JTAG', 'P6': '5V from machine'}
def conn_geom(ref, side):
    """place un connecteur 2x14 sur un cote ; rend {pin: (x, y, dir_entrante)} et dessine"""
    val = CONN_NAME.get(ref, comps[ref]['value'])
    geo = {}
    if side in ('h', 'b'):                     # 14 colonnes x 2 rangees, rangee proche = impairs
        pas = 12.5; w = 13 * pas + 24; x0 = CX - w / 2 + 12
        yn = (T + 150) if side == 'h' else (B - 150)
        yf = yn + (12 if side == 'h' else -12)
        y_box0 = min(yn, yf) - 8; pdf.rect(x0 - 12, y_box0, w, 28, lw=1.0, fill=(1, 1, 1))
        pdf.text(x0 - 12, (y_box0 + 62) if side == 'h' else (y_box0 - 40), "%s  %s" % (ref, val), 7, bold=True)   # au-dela des etiquettes de la rangee eloignee
        for i in range(14):
            x = x0 + i * pas
            for p, y in ((2 * i + 1, yn), (2 * i + 2, yf)):
                pdf.rect(x - 2.2, y - 2.2, 4.4, 4.4, lw=0.5, fill=(1, 1, 1) if p != 1 else (0.9, 0.9, 0.9))
                geo[p] = (x, y, 'h' if side == 'h' else 'b', p % 2 == 1)
                pdf.text(x, y + ((-9 if side == 'h' else 5) if p % 2 == 1 else (5 if side == 'h' else -9)), str(p), 3.8, rgb=ROUGE, align='c')
    else:                                      # 2 colonnes x 14 rangees, colonne proche = impairs
        pas = 12.5; h = 13 * pas + 24; y0 = CY + h / 2 - 12
        xn = (R + 150) if side == 'd' else (L - 150)
        xf = xn + (12 if side == 'd' else -12)
        x_box0 = min(xn, xf) - 8; pdf.rect(x_box0, y0 - h + 12, 28, h, lw=1.0, fill=(1, 1, 1))
        pdf.text(x_box0 - 2, y0 + 16, "%s  %s" % (ref, val), 7, bold=True)
        for i in range(14):
            y = y0 - i * pas
            for p, x in ((2 * i + 1, xn), (2 * i + 2, xf)):
                pdf.rect(x - 2.2, y - 2.2, 4.4, 4.4, lw=0.5, fill=(1, 1, 1) if p != 1 else (0.9, 0.9, 0.9))
                geo[p] = (x, y, 'd' if side == 'd' else 'g', p % 2 == 1)
                _out = (p % 2 == 0) == (side == 'd')    # broche eloignee cote exterieur
                pdf.text(x + (6 if _out else -6), y - 1.4, str(p), 3.8, rgb=ROUGE, align='l' if _out else 'r')
    return geo

placement = {'P2': 'h', 'P1': 'd', 'P4': 'b', 'P3': 'g'}
geos = {ref: conn_geom(ref, side) for ref, side in placement.items()}

# ---------------------------------------------------------------- nappes de fils
def route(ref, side, geo):
    """pour chaque broche du connecteur : fil orthogonal vers sa broche FPGA du meme cote,
    en voies paralleles (lane) pour que la nappe reste lisible."""
    lignes = []
    for p, (cx, cy, d, proche) in geo.items():
        n = net_by_node.get((ref, str(p)))
        if not n: continue
        name = n['name']
        if is_power(name):
            if side == 'h':   pdf.line(cx, cy, cx, cy + (8 if not proche else -0)); 
            if side in ('h', 'b'):
                yy = cy + (10 if side == 'h' else -10) if not proche else cy + (-10 if side == 'h' else 10)
                pdf.line(cx, cy, cx, yy, lw=0.6, rgb=GRIS); pdf.text(cx + 1.5, yy + (2 if side == 'h' and not proche else -2 - len(name) * 2.3), name, 4.2, rgb=GRIS, rot=90)
            else:
                xx = cx + (10 if side == 'd' else -10) if not proche else cx + (-10 if side == 'd' else 10)
                pdf.line(cx, cy, xx, cy, lw=0.6, rgb=GRIS); pdf.text(xx + (2 if xx > cx else -2), cy - 1.4, name, 4.2, rgb=GRIS, align='l' if xx > cx else 'r')
            continue
        u1 = [x for x in n['nodes'] if x['ref'] == 'U1']
        if not u1: continue
        fx, fy, fd = fpga_pin_xy(u1[0]['pin'])
        lignes.append((p, proche, cx, cy, fx, fy, fd, name, u1[0]['pin']))
    # voies : on trie par la position le long du cote, une voie par fil
    lignes.sort(key=lambda t: (t[2] if side in ('h', 'b') else t[3]))   # ordre du connecteur
    k = 0
    for (p, proche, cx, cy, fx, fy, fd, name, fp) in lignes:
        k += 1; lane = 22 + (k % 18) * 5.5
        if side == 'h':
            ymid = fy + lane
            pts = [(fx, fy), (fx, ymid), (cx, ymid), (cx, cy - 2.2)] if proche else [(fx, fy), (fx, ymid), (cx + 6, ymid), (cx + 6, cy + 9), (cx, cy + 9), (cx, cy + 2.2)]
        elif side == 'b':
            ymid = fy - lane
            pts = [(fx, fy), (fx, ymid), (cx, ymid), (cx, cy + 2.2)] if proche else [(fx, fy), (fx, ymid), (cx + 6, ymid), (cx + 6, cy - 9), (cx, cy - 9), (cx, cy - 2.2)]
        elif side == 'd':
            xmid = fx + lane
            pts = [(fx, fy), (xmid, fy), (xmid, cy), (cx - 2.2, cy)] if proche else [(fx, fy), (xmid, fy), (xmid, cy - 6), (cx + 9, cy - 6), (cx + 9, cy), (cx + 2.2, cy)]
        else:
            xmid = fx - lane
            pts = [(fx, fy), (xmid, fy), (xmid, cy), (cx + 2.2, cy)] if proche else [(fx, fy), (xmid, fy), (xmid, cy - 6), (cx - 9, cy - 6), (cx - 9, cy), (cx - 2.2, cy)]
        col = ROUGE if name in ('CLK', 'MOSI', 'MISO', 'CS_EEprom') else VERT
        pdf.poly(pts, lw=0.55, rgb=col)
        # nom du net pres du connecteur
        if side == 'h':
            if proche: pdf.text(cx + 1.6, cy - 30, name, 3.6, rgb=col, rot=90, align='r')
            else:      pdf.text(cx + 1.6, cy + 14, name, 3.6, rgb=col, rot=90, align='l')
        elif side == 'b':
            if proche: pdf.text(cx + 1.6, cy + 12, name, 3.6, rgb=col, rot=90, align='l')
            else:      pdf.text(cx + 1.6, cy - 14, name, 3.6, rgb=col, rot=90, align='r')
        elif side == 'd':
            if proche: pdf.text(cx - 12, cy + 3.2, name, 3.6, rgb=col, align='r')
            else:      pdf.text(cx + 12, cy + 3.2, name, 3.6, rgb=col, align='l')
        else:
            if proche: pdf.text(cx + 12, cy + 3.2, name, 3.6, rgb=col, align='l')
            else:      pdf.text(cx - 12, cy + 3.2, name, 3.6, rgb=col, align='r')
for ref, side in placement.items(): route(ref, side, geos[ref])

# ---------------------------------------------------------------- blocs peripheriques (fils nommes)
def bloc(x, y, w, h, titre, pins, fill=(1, 1, 1)):
    pdf.rect(x, y, w, h, lw=1.0, fill=fill); pdf.text(x + w / 2, y + h - 10, titre, 7, bold=True, align='c')
    for i, (pin, fn, name) in enumerate(pins):
        yy = y + h - 22 - i * 8.2
        pdf.text(x + 4, yy, "%s" % pin, 5, rgb=ROUGE); pdf.text(x + 22, yy, '' if fn.startswith('Pin_') else fn[:12], 5)
        pdf.line(x + w, yy + 2, x + w + 14, yy + 2, lw=0.6, rgb=(ROUGE if name in ('CLK', 'MOSI', 'MISO') else BLEU))
        pdf.text(x + w + 16, yy, name, 4.6, rgb=(ROUGE if name in ('CLK', 'MOSI', 'MISO') else BLEU), bold=True)
def pins_of(ref, only=None, exclude_power=True):
    out = []
    for n in nets:
        for x in n['nodes']:
            if x['ref'] == ref and (not exclude_power or not is_power(n['name'])) and (only is None or n['name'] in only):
                out.append((int(x['pin']), x['fn'], n['name']))
    return sorted(out)
# ESP32 : seulement les nets qui vont au FPGA ou au bus
esp = [(p, f, nm) for p, f, nm in pins_of('U7') if nm in ('ESP32_TX', 'ESP32_RX', 'FA_CTRL_REQ', 'Debug', 'Audio_RX', 'CLK', 'MOSI', 'MISO', 'NOR_CS', 'ESP_TCK', 'ESP_TMS', 'ESP_TDI', 'ESP_TDO')]
bloc(40, 560, 150, 22 + 8.2 * len(esp) + 6, "U7  ESP32-S3-WROOM-1  (pin function = GPIO)", [(p, f, nm) for p, f, nm in esp])
u6 = pins_of('U6'); bloc(40, 380, 150, 22 + 8.2 * len(u6) + 6, "U6  W25Q32  game NOR", u6)
u5 = pins_of('U5'); bloc(40, 235, 150, 22 + 8.2 * len(u5) + 6, "U5  W25Q32  config flash", u5)
jp = pins_of('JP1', exclude_power=False); bloc(40, 170, 150, 22 + 8.2 * len(jp) + 6, "JP1  solder jumper: NOR CS -> FPGA", jp)
p5 = pins_of('P5', exclude_power=False); bloc(990, 560, 150, 22 + 8.2 * len(p5) + 6, "P5  JTAG (ESP -> FPGA)", p5)
p6 = pins_of('P6', exclude_power=False); bloc(990, 470, 150, 22 + 8.2 * len(p6) + 6, "P6  5V from machine", p6)
y2 = pins_of('Y2', exclude_power=False); bloc(990, 400, 150, 22 + 8.2 * len(y2) + 6, "Y2  50 MHz -> P51", y2)
# legende
pdf.rect(990, 60, 160, 120, lw=0.8, fill=FOND)
pdf.text(1000, 168, "Legend", 7, bold=True)
pdf.line(1000, 156, 1030, 156, lw=1.0, rgb=VERT); pdf.text(1034, 154, "wire connector <-> FPGA", 5.5)
pdf.line(1000, 144, 1030, 144, lw=1.0, rgb=ROUGE); pdf.text(1034, 142, "shared SPI bus (NOR U6 / ESP / P4.21-24)", 5.5)
pdf.line(1000, 132, 1030, 132, lw=1.0, rgb=BLEU); pdf.text(1034, 130, "internal net (side block), same name", 5.5)
pdf.line(1000, 120, 1030, 120, lw=0.7, rgb=GRIS); pdf.text(1034, 118, "power (stub + name)", 5.5)
pdf.text(1000, 104, "pin number in red, pin function in grey", 5.5)
pdf.text(1000, 92, "P2.59/64/65 do not exist on this 28-pin module", 5.5)
pdf.text(1000, 80, "FPGA IOs reaching no connector: P33, P34, P47", 5.5)
pdf.text(1000, 68, "Generated from the KiCad netlist, 2026-09-07", 5, rgb=GRIS)
# cartouche
pdf.rect(20, 20, 1150, 802, lw=1.2)
pdf.text(30, 806, "Smart FA -- GottFA_SLX16 module (Spartan-6 XC6SLX9)  --  wiring schematic, single sheet", 12, bold=True)
pdf.text(30, 794, "Every connector pin is wired to its FPGA pin. One connector per side, as on the Cyclone 10 devboard whose pinout this module reproduces.", 6.5, rgb=GRIS)
pdf.text(1160, 26, "Pstore -- Valere Pillet -- generated 2026-09-07 from GottFA_SLX16_Module.kicad_sch", 5.5, rgb=GRIS, align='r')
pdf.save(OUT); print("PDF :", OUT)
