"""Build the two LSE1 v2 PDFs (Q&A + full explanations), updated to the team decisions of 2026-11-27.

Source of truth for the content = this file. Run:  python3 build_lse1_v2.py
Needs reportlab and the Calibri/Cambria fonts shipped with Microsoft Office (macOS path below).
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

OUT = os.path.dirname(os.path.abspath(__file__))
FD = "/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/"
for n, f in [("Cal", "Calibri.ttf"), ("CalB", "Calibrib.ttf"), ("CalI", "Calibrii.ttf"),
             ("CalBI", "Calibriz.ttf"), ("CamB", "Cambriab.ttf")]:
    pdfmetrics.registerFont(TTFont(n, FD + f))
registerFontFamily("Cal", normal="Cal", bold="CalB", italic="CalI", boldItalic="CalBI")

INK = colors.HexColor("#1B1F3B"); INK2 = colors.HexColor("#4A5070"); MIST = colors.HexColor("#F0F1F6")
CORAL = colors.HexColor("#E4572E"); TEAL = colors.HexColor("#2A9D8F"); AMBER = colors.HexColor("#E09F3E")
GREY = colors.HexColor("#8D93AB"); PURPLE = colors.HexColor("#6C4AB6")

S = lambda **k: ParagraphStyle("x", **{"fontName": "Cal", "fontSize": 9.5, "leading": 12.3, "textColor": INK, **k})
H1 = S(fontName="CamB", fontSize=17, leading=21, spaceAfter=2)
SUB = S(fontSize=9.5, textColor=INK2, spaceAfter=6)
H2 = S(fontName="CamB", fontSize=12.5, leading=16, spaceBefore=9, spaceAfter=3, keepWithNext=1)
H3 = S(fontName="CalB", fontSize=9.5, leading=12, spaceBefore=4, spaceAfter=1, textColor=CORAL, keepWithNext=1)
BODY = S()
SMALL = S(fontSize=8.3, leading=10.4, textColor=INK2)
BUL = S(leftIndent=10, bulletIndent=1)
CELL = S(fontSize=8.3, leading=10.2)
CELLB = S(fontName="CalB", fontSize=8.3, leading=10.2)
HEAD = S(fontName="CalB", fontSize=8.3, leading=10.2, textColor=colors.white)

STATUS = {"Sourced": TEAL, "Estimate": AMBER, "Design choice": INK2, "Team decision": CORAL,
          "Open conflict": PURPLE, "To discuss": GREY, "To source": GREY, "Correction": CORAL,
          "Proposal": AMBER, "Next step": GREY}
NEW = '<font color="#E4572E"><b>[v2]</b></font> '


def P(t, st=BODY): return Paragraph(t, st)
def B(items): return [Paragraph(i, BUL, bulletText="•") for i in items]


def table(head, rows, widths, status_col=None):
    data = [[P(h, HEAD) for h in head]]
    for r in rows:
        line = []
        for j, c in enumerate(r):
            if status_col is not None and j == status_col:
                key = c.split(" (")[0].split(" +")[0]
                col = STATUS.get(key, INK2).hexval().replace("0x", "#")
                line.append(P(f'<font color="{col}"><b>{c}</b></font>', CELL))
            else:
                line.append(P(c, CELLB if j == 0 else CELL))
        data.append(line)
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, MIST]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#D5D8E3")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def box(flow, color=MIST, border=None):
    t = Table([[flow]], colWidths=[174 * mm])
    st = [("BACKGROUND", (0, 0), (-1, -1), color), ("LEFTPADDING", (0, 0), (-1, -1), 7),
          ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    if border: st.append(("LINEBEFORE", (0, 0), (0, -1), 2.5, border))
    t.setStyle(TableStyle(st))
    return t


def build(name, title, story):
    def deco(c, d):
        c.saveState(); c.setFont("Cal", 7.5); c.setFillColor(GREY)
        c.drawString(18 * mm, 10 * mm, f"NX-422 · Group 12 · NeuroTact · LSE1 · {title} · v2, 27 Nov 2026 · draft (people/valentin/wip)")
        c.drawRightString(192 * mm, 10 * mm, str(d.page)); c.restoreState()
    doc = BaseDocTemplate(os.path.join(OUT, name), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                          topMargin=15 * mm, bottomMargin=16 * mm, title=title, author="Group 12 – LSE1")
    doc.addPageTemplates([PageTemplate(frames=[Frame(18 * mm, 16 * mm, 174 * mm, 266 * mm, id="f",
                          leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=deco)])
    doc.build(story)


DESIGN = ("<b>NeuroTact as of 27 Nov 2026.</b> <i>Motor side (now part of NeuroTact):</i> 2 Utah arrays in M1 "
          "(192 electrodes) → M1 chip (MiBMI class), linear decoder first; stimulation artefact handled by filtering, no blanking. "
          "<i>Touch side:</i> 64 polyimide shanks (10 × 50 µm, ≤ 4 mm), 8 combs of 8, 4 SIROF sites/shank (1000 µm²) = 256 sites, "
          "64 current drivers via a 256 → 64 switch matrix; biphasic cathodic-first, 200 µs/phase; encoder on the S1 chip "
          "(input: 6 zone pressures + slip flags); <b>no recording in S1</b>. Titanium package, 13.56 MHz inductive link, "
          "3.2 kb/s out / 12.8 kb/s in, &lt; 15 mW. Pitch (C1) and current cap (C7) still open.")

# ===================================================================== Q&A
QA = [
    ("1 · Target population",
     "Amputees with a motor BCI are rare: who is the target?",
     "People with cervical SCI (C4–C6) who need both a motor BCI and touch feedback; amputees with no usable nerve "
     "(shoulder disarticulation, plexus avulsion) as a sub-case. " + NEW + "NeuroTact now provides the motor side itself "
     "(2 Utah arrays in M1), so the patient gets one implant system. Implant early after injury.",
     "All human ICMS/BCI implants so far are in tetraplegic SCI patients (0 amputees), and amputees already have EMG control "
     "plus nerve interfaces; the S1 hand map stays sharp after amputation (r = 0.68–0.91) but blurs with time after SCI (ρ = −0.59)."),
    ("2 · Threshold drift and recalibration",
     "What physiology causes drift, how do we detect it, and why recalibrate with flexible probes?",
     "Drift comes from the glial scar pushing neurons away (I = k·r², k ≈ 1292 µA/mm²). " + NEW + "Recalibration = a daily "
     "on-chip self-check of each site (electrode side) + a weekly threshold staircase that the patient answers through the "
     "motor BCI (\"felt / not felt\"). No recording in S1; evoked responses are the next step.",
     "Human Utah thresholds vary &gt; 10 µA day to day and drift over months (Hughes 2021), and our 10 µm shanks are ~1000× stiffer "
     "than 1 µm ultraflexible probes, so a scar still forms. The weekly staircase replaces today's 4 h × 3/week manual sessions; "
     "it tracks the slow trend, not the daily noise."),
    ("3 · Mouse → human thresholds and current range",
     "Do Lycke 2023's mouse thresholds (2–7 µA) transfer to humans?",
     "No. Estimated NeuroTact threshold ~8–20 µA (range ~3–40 µA). " + NEW + "No fixed 30 µA target: the encoder works per site "
     "between its threshold and its maximum. LSE1 proposal (open conflict C7): hardware 0–100 µA, charge cap 10–12 nC/phase, "
     "40 µA = switch to another site; cheaper compromise 0–60 µA with ~±8 V compliance.",
     "Lycke measured mice only and made no human projection; humans need more current (thicker cortex, thicker shanks, more motion), "
     "and 4 intensity levels need ≈ 75 µA (JND ≈ 13–15 µA, Greenspon 2025): a 40 µA cap leaves 1–2 levels."),
    ("4 · Why 256 sites, and which layout",
     "How big is the hand map, what resolution, what gain over Utah?",
     "Hand map ≈ 15.5 mm, ~3.9 mm per finger. " + NEW + "LSE1 recommends 8 × 8 at <b>800 µm</b> pitch = 5.6 mm, covering thumb + index "
     "(open conflict C1; 400 µm = 2.8 mm covers one finger). 256 sites are justified by depth (area 3b), redundancy and groups of 4 "
     "sites on one shank.",
     "Utah sits in area 1 only, loses 25–58% of electrodes and never gave thumb or fingertip sensations; groups of 4 electrodes cut "
     "mislocalisation from 42% to 7% (Greenspon 2025). At 800 µm, lateral sampling is 4× sparser than Utah: the gain is depth and 2-finger coverage."),
    ("5 · Tissue safety",
     "Shannon / charge density: which limits apply to humans?",
     "Reason in charge per phase (~4 nC conservative, Cogan 2016), not Shannon. Hardware safeguards: charge cap 10–12 nC/phase "
     "(20 nC absolute), duty cycle limit, site disabled if E_mc &lt; −0.6 V or interphase voltage &lt; −1.5 V.",
     "Shannon was fitted on 0.01–0.5 cm² surface discs, ≥ 1000× larger than our sites; 4 nC is reached at 20 µA × 200 µs, "
     "so even the 40 µA cap (8 nC) is not \"safe by Shannon\". The intensity/safety conflict is real and stated openly."),
]

s = [P("NeuroTact · LSE1 decisions: questions and answers (v2)", H1),
     P("Biological and clinical justification · Group 12 · updated to the team decisions of 27 Nov 2026. "
       f"{NEW}marks what changed since v1. Full reasoning: <i>LSE1_Decisions_Full_v2.pdf</i>.", SUB),
     box(P(DESIGN, SMALL), border=INK2), Spacer(1, 4)]
for pt, q, a, j in QA:
    s.append(KeepTogether([P(pt, H2), P(f"<b>Q.</b> {q}"), Spacer(1, 2),
                           box(P(f"<b>A.</b> {a}"), border=TEAL), Spacer(1, 2), P(f"<i>Why:</i> {j}", SMALL)]))
build("LSE1_Decisions_QA_v2.pdf", "Q&A", s)

# ===================================================================== FULL
s = [P("NeuroTact · LSE1 decisions: full explanations (v2)", H1),
     P("Biological and clinical justification · Group 12 · updated to the team decisions of 27 Nov 2026 "
       f"(motor side inside NeuroTact, recalibration by self-check + staircase, no S1 recording, no blanking). {NEW}marks changes since v1. "
       "Values marked <i>estimate</i> or <i>calc</i> are our own, not measurements.", SUB)]

s += [P("0 · System context", H2), P(DESIGN), Spacer(1, 3)]
s += B(["<b>Outer loop (through the patient):</b> intention → 2 Utah arrays in M1 → M1 chip decodes (linear decoder first) → "
        "UR arm + PSYONIC hand → thumb/index pressure → S1 chip encoder → ICMS in S1 → sensation on their own fingers → corrected grasp. "
        "Clinical benefit of ICMS feedback: grasp time 20.9 → 10.2 s (−51%, Flesher 2021, n = 1).",
        NEW + "<b>Recalibration loop:</b> daily on-chip self-check of each site + weekly threshold staircase answered through the motor BCI; "
        "thresholds and maxima per site are stored on the S1 chip and used by the encoder. Evoked responses (needs S1 recording) = next step.",
        NEW + "<b>Artefact:</b> S1 stimulation is seen on the M1 recordings; the team chose filtering only (blanking = fallback). "
        "Whether the decoder still works with stimulation running is still to be checked offline (follow-up F5)."])
s += [Spacer(1, 3), table(["Term", "Meaning"], [
    ["Threshold vs cap", "Threshold = smallest perceived current (biology). Cap = maximum the stimulator delivers (design choice)."],
    ["JND / step", "Smallest perceived current difference, ~13–15 µA in humans = one intensity step."],
    ["Staircase", "Psychophysical method: current lowered after each \"felt\", raised after each \"not felt\"; converges on the threshold."],
    ["Q, D, k", "Q = I × phase duration (nC); D = Q / area (mC/cm²); Shannon k = log D + log Q."],
    ["E_mc / interphase", "Maximum cathodic electrode potential (limit −0.6 V); voltage between the two phases (limit −1.5 V)."],
    ["Compliance", "Maximum voltage the stimulator can supply to impose the current (V = R × I)."],
], [34, 140])]

# ---- 1
s += [P("1 · Target population", H2),
      box(P("<b>TA's remark:</b> \"Amputees using a motor BCI are rare: human BCIs mostly involve people with tetraplegia, and amputees "
            "drive their prosthesis via EMG.\" <b>Verdict:</b> the TA is right; the S6 target matched nobody in the literature.", BODY), border=CORAL),
      P("Why", H3)]
s += B(["<b>0 amputees</b> among implanted humans (BCI or ICMS). All ICMS implants are cervical SCI (C4–C6): Collinger 2013, Flesher 2016/2021, "
        "Hughes 2021, Armenta Salas 2018, Greenspon 2025; 1–3 participants per study.",
        "Amputees already have better options: prosthesis via EMG or cable; touch via residual-limb nerves (cuff, TIME, USEA) without opening the skull. "
        "Flesher 2016: ICMS is for those who \"cannot benefit from an interface with the PNS\".",
        "169,000 people with SCI tetraplegia in the US (Flesher 2021) = candidate pool; ~50% rank hand function as top priority.",
        "S1 hand map: preserved after amputation (r = 0.68–0.91, Schone 2025; Makin 2013); blurs with time after SCI (ρ = −0.59, Kikkert 2021)."])
s += [P("Solution", H3)]
s += B(["Target = people with cervical SCI first; sub-case = amputees with no usable nerve. Implant early after injury.",
        NEW + "The motor BCI is <b>no longer a companion system</b>: NeuroTact includes 2 Utah arrays in M1 and the M1 chip. "
        "For this population that is consistent: they need a motor BCI anyway, and one surgery can place both M1 and S1 arrays "
        "(M1 and S1 face each other across the central sulcus). The Utah array has been used for motor decoding in humans since "
        "2012 (Hochberg 2012), so the novelty stays on the S1 side."])

# ---- 2
s += [P("2 · Threshold drift and recalibration", H2),
      box(P("<b>TA's remark:</b> \"Which physiology explains the drift, which signal detects it, and why recalibrate even with flexible probes?\" "
            "<b>Verdict:</b> justified; the mechanism, the detection method and the value over flexible probes were missing.", BODY), border=CORAL),
      P("Why: physiology", H3)]
s += B(["Foreign-body response: microglia (minutes–24 h) → astrocytes (week 1) → 50–100 µm glial sheath, neuronal loss, BBB leakage (6–8 weeks) "
        "(Polikov 2005; Kozai 2015).",
        "<b>I = k·r²</b>, k ≈ 1292 µA/mm² (Stoney 1968): neurons 2× further → 4× more current.",
        "Flexible ≠ no scar: ultraflexible probes are 1 µm thick, ours 10 µm; stiffness ∝ thickness³ → ~1000× stiffer (estimate)."])
s += [P("Why: what thresholds actually do", H3)]
s += B(["Human Utah: median threshold <i>decreases</i> 31.5 → 10.4 µA (day 100 → 1500) but varies &gt; 10 µA day to day (Hughes 2021).",
        "5/19 electrodes rise by +0.35 µA/day over 6 months (Flesher 2016); damaged tips 41% stimulated vs 6% unstimulated (Woeppel 2021).",
        "Mouse ultraflexible: decrease over 20–70 d then ±1 µA plateau; a lesion event 4.45 → 13.73 → 4.87 µA within 116 d (Lycke 2023).",
        "Today: manual calibration, 4 h × 3 sessions/week; only 4 complete threshold maps in 1500 days (Hughes 2021)."])
s += [P("Solution " + NEW, H3)]
s += B(["<b>Daily self-check (on the S1 chip):</b> electrode-side measurements per site (e.g. impedance, voltage transients, E_mc). "
        "It detects broken or worn sites and disables them, but it says nothing about the neurons, so it cannot track the threshold. "
        "Exact content to confirm with Heliya/Alae.",
        "<b>Weekly staircase:</b> the chip delivers test pulses on a site; the patient answers \"felt / not felt\" through the motor BCI "
        "(no therapist needed); the current steps down after \"felt\" and up after \"not felt\" until it converges. The chip stores "
        "each site's threshold and maximum; the encoder uses them. Above 40 µA (or the chosen cap) → switch to another site on the same shank.",
        "<b>Time budget (calc, assumptions: ~20 trials per site, ~2 s per trial):</b> ~40 s per site → 64 active sites ≈ 45 min/week; "
        "all 256 sites ≈ 3 h. Testing groups of 4 sites, or only the active sites, keeps it short.",
        "<b>Benefits:</b> less manual tuning than 4 h × 3/week; equal sites (no point \"shouts\"); stimulate close to threshold "
        "(less charge). Do <i>not</i> promise longer lifetime: Utah arrays already last &gt; 1500 days.",
        "<b>Limit to state:</b> a weekly staircase follows the slow drift (months) but not the &gt; 10 µA day-to-day variation (Hughes 2021). "
        "Options: keep a margin above threshold, or a short daily check on a few sentinel sites (to discuss).",
        "<b>Next step:</b> evoked responses on neighbouring sites would make recalibration automatic, but need recording in S1 "
        "(dropped for now). Building blocks exist separately: response from 0.7 ms in monkey (Sombeck 2022), 1.6 ms blanking in humans "
        "(Shelchkova 2023); no paper yet shows it tracks the perceived threshold."])

# ---- 3
s += [P("3 · Thresholds: mouse → human, and current range", H2),
      box(P("<b>TA's remark:</b> \"Can the very low thresholds Lycke 2023 measured in mice be transferred to humans?\" "
            "<b>S6 said:</b> \"thresholds projected below 30 µA [Lycke]\", hence a 40 µA cap. "
            "<b>Verdict:</b> the citation is wrong and the cap leaves no room to code intensity.", BODY), border=CORAL),
      P("Why", H3)]
s += B(["Lycke 2023: 5 mice, 1 µm probes, ~450 µm² sites; thresholds 2–7 µA; 1.5 µA (0.25 nC/phase) enough &gt; 8 months. "
        "<b>No projection to humans.</b> Rigid probes in mice: 15–30 µA; monkey ~30 µA (Kim 2015b).",
        "Human Utah: 15–88 µA, median 34.9 µA (Flesher 2016).",
        "Humans need more: thicker, less dense cortex (~1.5×, estimate; area 3b wall 1.81 mm, Fischl 2000); 10× thicker probes; "
        "more brain motion; and I = k·r².",
        "Headroom: JND ≈ 13–15 µA, ~7 levels between threshold and 100 µA (Greenspon 2025). 20 µA + 4 × 14 µA ≈ 75 µA."])
s += [P("Solution", H3)]
s += B(["Estimated NeuroTact threshold: median ~8–20 µA, range ~3–40 µA, tail 40–60 µA (estimate).",
        NEW + "<b>No fixed 30 µA target</b> (replaces D-005's \"target 30 µA\"): per site, the encoder maps pressure between that site's "
        "threshold and its maximum = min(threshold + ~4 JND, charge cap).",
        "<b>LSE1 proposal for C7 (open):</b> hardware 0–100 µA; software charge cap 10–12 nC/phase (≈ 50–60 µA at 200 µs), 20 nC absolute; "
        "40 µA = switch-over point. Compliance: ~70–140 kΩ access × 100 µA → 7–14 V → ±12 V (estimate).",
        NEW + "<b>Compromise if the chip cost is too high (estimate):</b> hardware 0–60 µA = the charge cap; compliance ~±8 V "
        "(60 µA × 140 kΩ ≈ 8.4 V); still ~3 levels above an 8–20 µA threshold.",
        "If the 40 µA cap is kept: say explicitly that only ~1–2 intensity levels remain above threshold."])

# ---- 4
s += [P("4 · Why 256 sites, and which layout", H2),
      box(P("<b>TA's remark:</b> \"How large is the hand map, what spatial resolution do we aim for, and what do we gain over the Utah array?\" "
            "<b>S6 said:</b> \"4× density\" vs Utah. <b>Verdict:</b> target size not quantified; the \"4×\" only holds in depth.", BODY), border=CORAL),
      P("Why", H3)]
s += B(["Hand map D1 → D5 ≈ 15.5 mm (7 T fMRI, Martuzzi 2014) → ~3.9 mm between adjacent finger centres (calc).",
        "Human Utah (Pittsburgh): 2 arrays of 2.4 × 4 mm, 1.5 mm shanks, 64 wired electrodes; all in area 1, none in 3b; no thumb or "
        "fingertip sensations; 25–58% of electrodes unusable; 7–20% of the palm covered.",
        "Only 64 sites can stimulate at once (64 drivers, 256 → 64 matrix)."])
s += [P("Solution " + NEW, H3)]
s += B(["<b>Layout (open conflict C1): LSE1 recommends 8 × 8 at 800 µm pitch = 5.6 mm</b>, which spans the thumb (D1) and index (D2) "
        "centres with margin and matches \"32 drivers per finger\". At 400 µm (2.8 mm) the grid sits inside one finger territory. "
        "Alternative with the same shank count: 4 × 16 at 400 µm (~6 × 1.2 mm, longer implant).",
        "Cost of 800 µm: lateral sampling 4× sparser than Utah. Activated radius r = √(I/k): 40 µA → 176 µm, 60 µA → 215 µm (calc), "
        "so there are unstimulated gaps between shanks, but neighbouring shanks are fully independent.",
        "<b>Defend:</b> depth (4 staggered sites on ≤ 4 mm shanks reach area 3b, which Utah misses); redundancy (best of 4 sites per shank); "
        "<b>site groups</b>: mislocalisation 42% with 1 electrode → 7% with 4 (Greenspon 2025). " + NEW + "At 800 µm, groups should be the "
        "4 depth sites of one shank (same cortical column) rather than adjacent shanks; that the Utah result transfers is a hypothesis.",
        "Consequences for LSE2: comb width and package footprint 5.6 mm; craniotomy size."])

# ---- 5
s += [P("5 · Tissue safety", H2),
      box(P("<b>TA's remark:</b> \"Charge density, Shannon criterion: which safety limits apply, and with what caveats for humans?\" "
            "<b>S6 said:</b> \"k &lt; 1.85 [Shannon]\"; \"8 nC well below the human 20 nC\"; SIROF Qinj 1–5 mC/cm². "
            "<b>Verdict:</b> arithmetic right, criterion does not apply to our sites.", BODY), border=CORAL),
      P("Why", H3)]
s.append(table(["Current (200 µs, 1000 µm²)", "Q / phase", "Density D", "Shannon k", "vs 4 nC"], [
    ["20 µA", "4 nC", "0.4 mC/cm²", "0.20", "at the limit"], ["30 µA", "6 nC", "0.6 mC/cm²", "0.56", "above"],
    ["40 µA", "8 nC", "0.8 mC/cm²", "0.81", "2× above"], ["60 µA", "12 nC", "1.2 mC/cm²", "1.16", "3× above"],
    ["100 µA", "20 nC", "2.0 mC/cm²", "1.60", "5× above"]], [52, 28, 32, 28, 34]))
s += [Spacer(1, 3)]
s += B(["Shannon 1992: 0.01–0.5 cm² discs on the surface of cat cortex (7 h, 50 Hz); our sites are ≥ 1000× smaller and inserted. "
        "His conservative value is k = 1.5; 1.85 comes from Cogan 2016.",
        "Microelectrodes: damage around <b>~4 nC/phase</b> (Cogan 2016), depending on frequency and duty cycle; first mechanism is neuronal hyperactivity.",
        "Pittsburgh uses up to 20 nC/phase without clear damage (Flesher 2016), but on ~2000 µm² sites: our 50 µA ≈ their 100 µA in density.",
        "SIROF Qinj 1–5 mC/cm² is in vitro with bias; ~4× lower in vivo; unbiased SIROF saturates ~50 µA at 200 µs."])
s += [P("Solution", H3)]
s += B(["Reason in charge per phase; Shannon only as a reference point.",
        "Hardware safeguards, independent of the encoder and of the staircase: charge cap 10–12 nC/phase per site, 20 nC absolute; "
        "duty-cycle limit (15 s on / 15 s off proposed, to check against continuous grasp feedback); disable a site if E_mc &lt; −0.6 V "
        "or interphase voltage &lt; −1.5 V (Woeppel 2021) — these voltage checks fit naturally in the daily self-check.",
        "Low thresholds (8–20 µA) keep most stimulation near 4 nC; the intensity/safety conflict is stated openly."])

# ---- 6
s += [P("6 · Decisions and open items for LSE1", H2)]
s.append(table(["Item", "With", "Proposal / value", "Status"], [
    ["Project target", "Group", "Cervical SCI C4–C6 first; amputees without usable nerve as sub-case; implant early", "Team decision (D-015)"],
    ["Motor side", "Group", "Part of NeuroTact: 2 Utah arrays in M1 + M1 chip, linear decoder first", "Team decision (27.11)"],
    ["Recalibration", "Alae·Heliya", "Daily self-check + weekly staircase answered through the motor BCI; no S1 recording", "Team decision (27.11)"],
    ["Self-check content", "Heliya", "Impedance, voltage transients, E_mc / interphase limits per site", "To discuss"],
    ["Staircase design", "Alae·Valentin", "~20 trials/site, ~2 s/trial → ~45 min/week for 64 sites; groups of 4 to shorten", "Estimate"],
    ["Day-to-day variation", "Group", "&gt; 10 µA/day not tracked weekly: margin above threshold or daily sentinel sites", "To discuss"],
    ["Evoked responses", "Group", "Automatic recalibration once S1 recording is added", "Next step"],
    ["Shank pitch", "Group", "800 µm → 5.6 mm, thumb + index (LSE1); 400 µm → 2.8 mm, one finger", "Open conflict (C1)"],
    ["Current range", "Valentin·Defne·Heliya", "0–100 µA hw + 10–12 nC cap, or 0–60 µA / ±8 V compromise, or 40 µA cap", "Open conflict (C7)"],
    ["Operating current", "Valentin·Heliya", "No fixed target; threshold → min(threshold + ~4 JND, cap)", "Proposal"],
    ["Site groups", "Alae", "Groups of 4 depth sites on one shank", "Proposal"],
    ["Duty cycle", "Heliya·Alae", "15 s / 15 s vs continuous feedback during grasp", "To discuss"],
    ["SIROF biasing", "Heliya·Defne", "Unbiased saturates ~50 µA: bias or not?", "To discuss"],
    ["BCI users worldwide", "Valentin", "\"A few tens\": needs a source", "To source"],
], [32, 26, 86, 30], status_col=3))

s += [P("7 · Sentences to correct in team documents", H2)]
s.append(table(["Where", "Says", "Correction", "Reason"], [
    ["S6 / 2-pager", "Target: amputees with a motor BCI", "Cervical SCI first; amputees without nerve as sub-case", "0 amputees implanted"],
    ["S6 / 2-pager", "\"Thresholds projected below 30 µA [Lycke]\"", "Lycke = mice, no projection; humans: Flesher 2016 (median 34.9 µA)", "Wrong citation"],
    ["D-005, Defne Q4", "\"Target 30 µA, cap 40 µA, Shannon k = 0.81 &lt; 1.85\"", "No fixed target; charge-based cap; ~4 nC/phase reference", "Wrong criterion"],
    ["S6", "\"8 nC well below the human 20 nC\"", "That 20 nC was on ~2000 µm² sites", "Density ×2"],
    ["S6", "SIROF Qinj 1–5 mC/cm²", "In vitro value with bias; ~4× lower in vivo", "In vitro"],
    ["S6 / Defne Q5", "\"4× density\" / \"2.56× Utah\"", "True in depth only; lateral sampling = Utah at 400 µm, 4× sparser at 800 µm", "Pitch"],
    ["LSE1 v1, Defne Q1", "Motor BCI = companion system", "Part of NeuroTact (27.11)", "Team decision"],
    ["LSE1 v1", "Evoked-response recalibration, blanking ~2 ms", "Self-check + weekly staircase; evoked responses = next step", "Team decision"],
], [24, 46, 72, 32]))

s += [P("8 · Key sources", H2), P(
    "Armenta Salas 2018 · Cogan 2016 (~4 nC/phase) · Collinger 2013 · Fischl 2000 (area 3b 1.81 mm) · Flesher 2016 (Utah thresholds, 20 nC) · "
    "Flesher 2021 (grasp −51%) · Greenspon 2025 (JND, levels, multi-electrode groups) · Hochberg 2012 (Utah motor BCI) · Hughes 2021 (thresholds over 1500 days) · "
    "Kikkert 2021 (hand map after SCI) · Kim 2015b · Kozai 2015, Polikov 2005 (foreign-body response) · Lycke 2023 · Makin 2013, Schone 2025 (map after amputation) · "
    "Martuzzi 2014 (7 T hand map) · Shannon 1992 · Shelchkova 2023 · Sombeck 2022 · Stoney 1968 (I = k·r²) · Woeppel 2021 (electrode damage, E_mc). "
    "Not all of these are in 05_literature/references.bib yet.", SMALL)]
build("LSE1_Decisions_Full_v2.pdf", "Full explanations", s)
print("ok")
