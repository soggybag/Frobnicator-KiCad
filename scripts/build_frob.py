"""Frobnicator (John Hollis) - faithful transcription of the user's Eagle build (Frobnicator.sch == .brd, 2023).
Wired functional blocks.  usage: build_frob.py <out.kicad_sch>"""
from sch import *
import sys
OUT = sys.argv[1]
g = lambda n: round(n * 2.54, 3)
s = Sheet('Frobnicator', 'A3')
FR = 'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal'
FC = 'Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2'
FCE = 'Capacitor_THT:CP_Radial_D5.0mm_P2.00mm'
FPOT = 'Potentiometer_THT:Potentiometer_Omeg_PC16BU_Vertical'
FPAD = 'Connector_Wire:SolderWire-0.5sqmm_1x01_D0.9mm_OD2.1mm'
FLED = 'LED_THT:LED_D3.0mm'
W = lambda *p: s.wire(*p)
P = s.P
def GND(p): s.power('GND', p)
def V9(p): s.power('+9V', p)
def lab(n, p, side='r'): s.label(n, p, side)
def Rh(ref, v, cx, y, desc=None): s.part(ref, 'Device', 'R', v, cx, y, 90, fp=FR, desc=desc or f'Resistor {v}', text='t')
def Rv(ref, v, x, cy, side='r', desc=None): s.part(ref, 'Device', 'R', v, x, cy, 0, fp=FR, desc=desc or f'Resistor {v}', text=side)
def Ch(ref, v, cx, y, desc=None): s.part(ref, 'Device', 'C', v, cx, y, 90, fp=FC, desc=desc or f'Film capacitor {v}', text='t')
def Cv(ref, v, x, cy, side='r', desc=None): s.part(ref, 'Device', 'C', v, x, cy, 0, fp=FC, desc=desc or f'Film capacitor {v}', text=side)
def Ev(ref, v, x, cy, side='r', desc=None): s.part(ref, 'Device', 'C_Polarized', v, x, cy, 0, fp=FCE, desc=desc or f'Electrolytic {v}', text=side)
def OPA(unit, x, y, mirror=None):
    s.part('U1', 'Amplifier_Operational', 'TL072', 'TL072', x, y, 0, unit=unit, mirror=mirror, fp='Package_DIP:DIP-8_W7.62mm',
           desc='Dual JFET op-amp (Eagle IC1)', text='ic')
def PAD(ref, name, x, y, right=False):
    s.part(ref, 'Connector_Generic', 'Conn_01x01', name, x, y, 0 if right else 180, fp=FPAD, desc=f'Wire pad: {name}',
           text=((x + 2.54, y - 1.27), (x + 2.54, y + 1.27), 'left') if right else ((x - 2.54, y - 1.27), (x - 2.54, y + 1.27), 'right'))
    return P(ref, '1')
def POT(ref, v, name, x, y, rot=0, mirror=None, text='r', trim=False):
    if text == 'r': text = ((x + 4.445, y - 1.27), (x + 4.445, y + 1.27), 'left')
    elif text == 'l': text = ((x - 4.445, y - 1.27), (x - 4.445, y + 1.27), 'right')
    s.part(ref, 'Device', 'R_Potentiometer_Trim' if trim else 'R_Potentiometer', v, x, y, rot, mirror=mirror,
           fp='Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical' if trim else FPOT, desc=f'{name}', text=text, extra={'Panel': name})
def LED(ref, x, y, rot, desc): s.part(ref, 'Device', 'LED', 'LED', x, y, rot, fp=FLED, desc=desc, text='t')

# ================================================================ LFO
s.box('LFO: SCHMITT (U1A) + INTEGRATOR (U1B), RATE, TREM range switch', g(3), g(5), g(62), g(36))
OPA(1, g(20), g(22))
W(P('U1', '2'), (g(16), g(23)), (g(16), g(26))); lab('VB', (g(16), g(26)), 'l')
W(P('U1', '3'), (g(15), g(21)))
Rh('R11', '47k', g(10.5), g(21), desc='Schmitt input from the triangle'); W(P('R11', '2'), (g(15), g(21)))
W(P('R11', '1'), (g(6), g(21))); lab('TRI', (g(6), g(21)), 'l')
Rh('R10', '100k', g(20), g(16), desc='Schmitt hysteresis (triangle = +-0.47 x square)')
W((g(15), g(21)), (g(15), g(16)), P('R10', '1')); W(P('R10', '2'), (g(25), g(16)), (g(25), g(22)))
POT('RV1', 'A100k', 'RATE', g(29), g(22) + 3.81, mirror='x', text='r')
W(P('U1', '1'), (g(25), g(22)), P('RV1', '3'))
Rv('R9', '4k7', g(29), g(28.5), side='l', desc='RATE minimum'); W(P('RV1', '1'), P('R9', '1'))
W(P('R9', '2'), (g(29), g(31))); lab('VB', (g(29), g(31)), 'l')
Rh('R12', '220k', g(36), P('RV1', '2')[1], desc='Integrator input'); W(P('RV1', '2'), P('R12', '1'))
OPA(2, g(47), P('RV1', '2')[1] + 2.54, mirror='x')
yi = P('RV1', '2')[1]
W(P('R12', '2'), (g(41), yi), P('U1', '6'))
W(P('U1', '5'), (g(43), yi + g(2)), (g(43), yi + g(4.5))); lab('VB', (g(43), yi + g(4.5)), 'l')
Ch('C6', '2n2', g(46.5), g(18), desc='Integrator cap (AUDIO range on its own)')
W((g(41), yi), (g(41), g(18)), (g(41), g(13)))
W((g(41), g(18)), P('C6', '1')); W(P('C6', '2'), (g(52), g(18)))
Ch('C7', '100n', g(44.5), g(13), desc='Range cap: TREM switch adds it across C6 (LFO range)'); W((g(41), g(13)), P('C7', '1'))
s.part('SW1', 'Switch', 'SW_SPDT', 'TREM', g(51), g(13), 0, fp='Button_Switch_THT:SW_E-Switch_EG1224_SPDT_Angled', desc='TREM range switch (Eagle M9040P); only pins 1-2 used', text=((g(49), g(9)), (g(49), g(10.5)), 'left'), extra={'Panel': 'TREM'})
W(P('C7', '2'), P('SW1', '2'))
s.noconnect(P('SW1', '3'))
yo = yi + g(1)
W(P('SW1', '1'), (g(55), P('SW1', '1')[1]), (g(55), yo))
W(P('U1', '7'), (g(52), yo), (g(55), yo), (g(58), yo)); W((g(52), g(18)), (g(52), yo)); lab('TRI', (g(58), yo))
s.text('LFO ~1-24 Hz with C7 switched in; ~50 Hz - 1.1 kHz on C6 alone (46x).', g(5), g(34))

# ================================================================ DEPTH / CONTROL CURRENT
s.box('DEPTH -> 3080 CONTROL CURRENT (rate LED D4)', g(3), g(40), g(62), g(70))
yc = g(52)
lab('TRI', (g(6), yc - g(2)), 'l')
POT('RV2', 'B10k', 'DEPTH', g(12), yc, mirror='x', text=((g(4), yc + g(1)), (g(4), yc + g(2.5)), 'left'))
W((g(6), yc - g(2)), (g(12), yc - g(2)), P('RV2', '3'))
W(P('RV2', '1'), (g(12), yc + g(4))); lab('VB', (g(12), yc + g(4)), 'l')
Rh('R13', '10k', g(17), P('RV2', '2')[1], desc='DEPTH to control current'); W(P('RV2', '2'), P('R13', '1'))
yd = P('RV2', '2')[1]
W(P('R13', '2'), (g(22), yd))
Cv('C5', '100n', g(22), yd + 3.81, side='l', desc='Control smoothing (~160 Hz with R13)'); GND(P('C5', '2'))
LED('D4', g(27.5), yd, 180, 'Rate LED (flashes with the LFO), in the control path')
W((g(22), yd), P('D4', '2'))
s.part('D1', 'Diode', '1N4148', '1N914', g(34), yd, 180, fp='Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal', desc='1N914', text='t')
W(P('D4', '1'), P('D1', '2')); W(P('D1', '1'), (g(40), yd)); lab('IABC', (g(40), yd))

# ================================================================ VCA
s.box('VCA: 3080 OTA (U2) + Q1 OUTPUT FOLLOWER', g(66), g(5), g(160), g(70))
yv = g(26)
lab('IN', (g(69), yv), 'l'); W((g(69), yv), (g(72), yv))
Rv('R1', '10M', g(72), yv + 3.81, side='l', desc='Input pull-down'); GND(P('R1', '2'))
Ch('C4', '47n', g(76.5), yv, desc='Input coupling'); W((g(72), yv), P('C4', '1'))
Rh('R2', '330k', g(82.5), yv, desc='Input attenuator (with R3: /34)'); W(P('C4', '2'), P('R2', '1'))
s.part('U2', 'Amplifier_Operational', 'CA3080', '3080', g(98), yv - g(1), 0, fp='Package_DIP:DIP-8_W7.62mm', desc='OTA (Eagle IC2, LM3080N)', text='ic')
W(P('R2', '2'), (g(86), yv), (g(90), yv), P('U2', '3'))
Rv('R3', '10k', g(86), yv + 3.81, side='l', desc='Input attenuator'); W(P('R3', '2'), (g(86), yv + g(3.5))); lab('VB', (g(86), yv + g(3.5)), 'l')
Rv('R6', '10M', g(90), yv + 3.81, side='r', desc='Bleed-through null feed')
POT('RV3', '100k', 'TRIM', g(90), yv + g(5.5), rot=90, trim=True, text=((g(93), yv + g(7.5)), (g(93), yv + g(9)), 'left'))
W(P('R6', '2'), P('RV3', '2'))
W(P('RV3', '1'), (P('RV3', '1')[0], yv + g(7))); GND((P('RV3', '1')[0], yv + g(7)))
V9(P('RV3', '3'))
ym = P('U2', '2')[1]
W(P('U2', '2'), (g(93), ym), (g(93), g(15)), (g(93), g(12)))
Rh('R5', '10k', g(89.5), g(15), desc='Feedback to VB'); W((g(93), g(15)), P('R5', '2')); W(P('R5', '1'), (g(86), g(15))); lab('VB', (g(86), g(15)), 'l')
Rh('R4', '470k', g(98), g(12), desc='Output-to-inverting feedback'); W((g(93), g(12)), P('R4', '1'))
W(P('R4', '2'), (g(107), g(12)), (g(107), P('U2', '6')[1]))
V9(P('U2', '7')); GND(P('U2', '4'))
W(P('U2', '5'), (P('U2', '5')[0], g(18))); lab('IABC', (P('U2', '5')[0], g(18)), 'r')
s.part('Q1', 'Transistor_BJT', 'BC547', '2N5089', g(113), P('U2', '6')[1], 0, fp='Package_TO_SOT_THT:TO-92_Inline', desc='2N5089 emitter follower (Eagle pads 1=C 2=B 3=E)', text='r')
W(P('U2', '6'), (g(107), P('U2', '6')[1]), P('Q1', '2'))
V9(P('Q1', '1'))
ye = P('Q1', '3')[1] + g(1)
W(P('Q1', '3'), (P('Q1', '3')[0], ye), (g(116), ye))
Rv('R7', '22k', P('Q1', '3')[0], ye + g(2.5), side='l', desc='Emitter load'); W((P('Q1', '3')[0], ye), P('R7', '1')); GND(P('R7', '2'))
Ch('C3', '1u', g(117.5), ye, desc='Output coupling'); W((g(116), ye), P('C3', '1'))
W(P('C3', '2'), (g(122), ye), (g(126), ye)); lab('OUT', (g(126), ye))
Rv('R8', '100k', g(122), ye + 3.81, side='r', desc='Output pull-down'); GND(P('R8', '2'))
s.text('TRIM (through R6 10M) nulls the LFO bleed-through at the 3080 input.', g(68), g(66))

# ================================================================ POWER, VB, LEDs, PADS
s.box('POWER, VB (two-LED reference), LEDs & PADS', g(3), g(74), g(160), g(112))
ry = g(82)
PAD('J5', 'V+', g(8), ry)
s.part('D5', 'Diode', '1N5817', '1N5817', g(16), ry, 180, fp='Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal', desc='Series polarity protection', text='t')
W(P('J5', '1'), (g(12), ry), P('D5', '2'))
W(P('D5', '1'), (g(22), ry), (g(26), ry), (g(32), ry), (g(40), ry))
V9((g(22), ry)); s.power('PWR_FLAG', (g(26), ry))
Ev('C1', '100u', g(32), ry + 3.81, desc='Supply bulk'); GND(P('C1', '2'))
Rv('R15', '1k', g(12), ry + 3.81, side='l', desc='Power LED current (Eagle RLED, from V+ before D5)'); W((g(12), ry), P('R15', '1'))
LED('D6', g(12), ry + g(7), 90, 'Power LED (to LS footswitch pad)')
W(P('R15', '2'), P('D6', '2'))
W(P('D6', '1'), (g(12), ry + g(11)), (g(16), ry + g(11)))
j7 = PAD('J7', 'LS', g(20), ry + g(11), right=True); W((g(16), ry + g(11)), j7)
# VB: 10k from +9V into two LEDs in series
Rv('R14', '10k', g(40), ry + 3.81, side='r', desc='VB feed')
W(P('R14', '2'), (g(40), ry + g(4)), (g(40), ry + g(5)))
LED('D2', g(40), ry + g(7), 90, 'VB reference LED (upper)')
W((g(40), ry + g(5)), P('D2', '2'))
LED('D3', g(40), ry + g(12), 90, 'VB reference LED (lower)')
W(P('D2', '1'), P('D3', '2')); GND(P('D3', '1'))
W((g(40), ry + g(4)), (g(46), ry + g(4)), (g(50), ry + g(4))); lab('VB', (g(50), ry + g(4)))
Ev('C2', '100u', g(46), ry + g(4) + 3.81, desc='VB filter'); GND(P('C2', '2'))
OPA(3, g(70), g(92)); V9(P('U1', '8')); GND(P('U1', '4'))
for i_, (ref, name, net) in enumerate((('J1', 'IN', 'IN'), ('J3', 'OUT', 'OUT'))):
    y = g(86) + i_ * g(4)
    j = PAD(ref, name, g(96), y); W(j, (g(101), y)); lab(net, (g(101), y))
for i_, (ref, name) in enumerate((('J2', 'IG'), ('J4', 'OG'), ('J6', 'V-'), ('J8', 'LG'))):
    y = g(86) + i_ * g(4)
    j = PAD(ref, name, g(118), y); W(j, (g(123), y)); GND((g(123), y))
    if ref == 'J6': s.power('PWR_FLAG', (g(121), y))

s.write(OUT, {'title': 'Frobnicator (as built)', 'date': '2026-09-29', 'rev': 'Eagle 2023',
              'company': 'Super-Freq',
              'comments': ['Faithful transcription of ~/Documents/eagle/projects/Frobnicator (sch == brd)',
                           'John Hollis design: TL072 LFO + 3080 OTA tremolo, TREM switch = LFO / audio range',
                           'Eagle refs: IC1/2=U1/2, RATE/DEPTH/TRIM=RV1-3, TREM=SW1, RLED=R15']})
print('ok', len(s.syms), 'symbols')
