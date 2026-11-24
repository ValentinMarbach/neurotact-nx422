# 04 — Integration (guidelines §3)

**Owners:** Heliya (power, link) + Defne (bonding, package, surgery) — _to confirm_

Legend: `[x]` done · `[ ] 🟡` in progress · `[ ]` missing.

## Guideline questions
- [ ] 🟡 Electrical + mechanical connection interface ↔ electronics, and why it fits the electrode count → ACF vs flip-chip (C4); 8 ribbons merged (D-012)
- [x] Fully implanted or external electronics → fully implanted, Ti package, inductive link (D-011)
- [ ] 🟡 Failure points at the integration interface and mitigation → list in Defne's LSE2 docs (delamination, moisture at the bond, ribbon fatigue)
- [ ] **Powering + power budget broken down per component** (incl. inductive link losses — TA)

## TA feedback on this part
- [x] Where the receiving coil sits relative to the Ti package → D-011
- [ ] **System block diagram with the data rate on each link and the power of each block**
- [ ] One package for M1 and S1, or two? (depends on C2)

## Power budget (fill here — single source)
| Block | Power | Source |
|---|---|---|
| Recording front-end (… ch) | ? | |
| ADC | ? | |
| On-chip processing (gate + NN / encoder) | ? | |
| Stimulation drivers (64) | ? | |
| Radio / back-telemetry | ? | |
| Power management + link losses | ? | |
| **Total** | ≤ 15 mW | D-014 |
