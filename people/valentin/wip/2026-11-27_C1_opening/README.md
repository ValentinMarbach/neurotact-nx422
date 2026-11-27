# C1 (footprint) and craniotomy size — LSE1 proposal, 27 Nov 2026 (not validated)

Answers to two open items in the integration text (EE): (1) final dimensions of the opening,
(2) depth of area 3b along the trajectory. Status: **LSE1 proposal**, to be agreed by the team.

## Decision proposed for C1: 4 × 16 shanks at 400 µm → 6.0 × 1.2 mm strip
- Mediolateral span is the same for both options (5.6 mm square vs 6.0 mm strip). Thumb–index
  centre distance = 5.7 ± 1.4 mm in 3b, 6.9 ± 2.7 mm in area 1 [martuzzi2014] → both reach from
  ~thumb centre to ~index centre; the strip slightly better.
- Anteroposterior: areas are ordered 3b (posterior bank) → 1 (crown) → 2 (caudal crown)
  [martuzzi2014; sanchezpanchuelo2010]. A 5.6 mm-deep square extends its back rows away from the
  lip (likely towards area 2, mostly proprioceptive [armentasalas2018]) and those rows cannot reach 3b.
  The strip keeps all 64 shanks within 1.2 mm of the lip.
- Pitch along the finger map 400 µm instead of 800 µm (2× resolution). No overlap at 40 µA
  (activated radius 0.176 mm, k = 1292 µA/mm² [stoney1968], calc).
- Cost: less proximal–distal coverage; Flesher 2016 saw no proximal–distal progression on arrays
  of this size. Fabrication: 4 combs of 16 instead of 8 of 8; same shank/site count → no change to electronics.
- Note: this supersedes Valentin's 12.11 preference (8 × 8 at 800 µm).

## Opening (calc)
| Item (anteroposterior) | mm | Source |
|---|---|---|
| Utah array | 4.0 | Blackrock NeuroPort 4 × 4 mm |
| Utah edge to precentral lip | ~1 | assumption; widened subarachnoid space near sulci [szymanski2021] |
| Central sulcus | 2.5 (range 1.3–2.7) | MRI sulcal width (PMC6240579; postmortem/MRI 2.4–2.7 mm, ages 20–30) |
| S1 strip | 1.2 | design |
| Stiffener / inserter clearance | ~1.5 | **assumption** |
| Bone margin | 2 × 2 | **assumption** |
| **Total** | **~14** | |

Mediolateral: 2 × 4.0 + 1 mm gap + 2 × 2 mm ≈ 13 mm. → **minimum ~15 × 15 mm**, final size on the
patient MRI (vessels of the central sulcus). Precedent: 4 arrays (2 M1, 2 S1 area 1) in one patient,
ROSA-planned (PMC12445443). Unverified figure seen: a 30 × 20 mm craniotomy for a human motor Utah
implant — do not cite until the primary source is found.

## Final text for the report

> The patient also carries two 96-channel Utah arrays (4 × 4 mm each) in M1, so the layout has to leave room for them. M1 and S1 hand areas face each other across the central sulcus at the hand knob, so a single craniotomy reaches both, as in the Pittsburgh implant of two M1 and two S1 arrays in one patient, planned with ROSA from fMRI. Our S1 footprint is a 6.0 × 1.2 mm strip of 4 × 16 shanks at 400 µm along the crown of the postcentral gyrus, next to the lip of the sulcus, with the shanks angled towards the posterior bank; the Utah arrays lie side by side on the precentral crown. The strip spans the same mediolateral width as an 8 × 8 square at 800 µm (thumb to index, 5.7 ± 1.4 mm apart in area 3b; Martuzzi 2014), but keeps every shank within 1.2 mm of the lip, where area 3b can be reached, instead of extending 5.6 mm back towards area 2. Each Utah array is bonded to a polyimide ribbon made in the same process as ours, and all the ribbons leave through the same notch towards the same package; the ribbons of the two systems are kept apart until the notch so that moving one does not pull on the other. The S1 combs are inserted first, since they need the most room for the stiffener, and the M1 arrays are then inserted pneumatically with the inserter held on a stereotaxic arm, a change adopted after hand-held insertion required repeated firings in a human implant (Szymanski 2021). The opening is sized from the layout rather than fixed in advance: 4.0 mm of Utah array, ~1 mm to the precentral lip, ~2.5 mm of sulcus (1.3–2.7 mm on MRI), the 1.2 mm strip, ~1.5 mm for the stiffener and 2 mm of bone margin on each side give ~14 mm anteroposterior, and two arrays side by side give ~13 mm mediolateral. We therefore plan a minimum opening of ~15 × 15 mm, adjusted on the patient's MRI to avoid the veins of the central sulcus; the stiffener and bone margins are assumptions.

> The four sites of each shank are placed 500 µm apart, the first 200 µm from the tip, so they span 0.2 to 1.7 mm from the tip. The 1.81 mm figure is the thickness of the posterior-bank cortex (Fischl 2000), not the depth of area 3b: the depth of the border between areas 1 and 3b along the trajectory depends on the entry point, the angle and the patient, since the position of these areas varies between individuals (Geyer 2001). It is therefore measured for each patient before surgery. Probabilistic cytoarchitectonic maps of areas 3b and 1 (Jülich atlas) and 7T fMRI or MEG finger maps are projected on the patient's MRI, as Flesher et al. (2016) did with MRI and MEG; for each shank, the planned trajectory gives the distance to the 1/3b border, and the insertion depth is chosen so that this border falls at the centre of the site span, ~0.95 mm from the tip. A depth error of up to about ±0.75 mm then still leaves one or two sites in 3b (calc). This is why we keep four sites per shank: the algorithm picks the best of four, and when a site needs more than 40 µA it switches to another site on the same shank rather than raising the current. After surgery, CT co-registered with the atlas shows which sites lie in 3b or in area 1, and the projected fields measured during calibration confirm it.
