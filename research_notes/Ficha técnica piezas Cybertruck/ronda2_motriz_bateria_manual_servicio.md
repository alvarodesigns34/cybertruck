# Cybertruck Service Manual: Drive Units, HV Battery, Power Conversion, Thermal (gap-filling pass, round 2)

Base URL for all manual pages: `https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/` (abbreviated "SM/" below, followed by the GUID file). Index: [SM/index.html](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html). Manual pages dated 2026-08 to 2026-10, so current production.

Status tags: **V** = Verified (read on the cited manual page), **R** = Reported (secondary source or search snippet), **I** = Inferred.

Variant naming in the manual: "Long Range" (LR, rear-wheel drive in the PCS/battery pages), "Standard", "AWD" (dual motor), "Dual Motor", "Tri Motor" (Cyberbeast). Important caveat: the Tri Motor and Cyberbeast mapping is **I** (Tri Motor pages exist in the index; I read none of them in full). Pages without a variant in the title say "none listed" and I did not assign Cyberbeast to them. Most procedure pages are marked DRAFT by Tesla. Pages are very long and the fetcher returned only the first ~100k characters, so later install-section details may be missing.

---

## 1. Drive units (front, rear, half shafts, mounts, oil pumps)

### Takeaway
Real torque tables were obtained for Front Drive Unit (FDU) and Rear Drive Unit (RDU, Dual Motor) removal, FDU/RDU mounts, half shafts, electric oil pumps and the front subframe. No drive unit mass is stated on any page read. Tri Motor (Cyberbeast) RDU pages exist (separate LH/RH rear units, LH rear oil pump, LH/RH rear inverters) but were not read in detail.

### Cited Findings

**Front Drive Unit, FDU** (qty 1, front subframe; no variant listed; early production may use a 16 mm FDU mount bolt instead of E18) — [SM/GUID-47A039C2](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-47A039C2-5509-47BA-83A1-2058CF3C67A2.html), FRT 3.54, page dated 2026-10-02. All V.

| Item | Qty / type | Torque | Status |
|---|---|---|---|
| FDU gearcase mount bolts | 2x 18 mm | 110 Nm | V |
| RH FDU mount bolt | 1x E18 (or 16 mm early) | 85 Nm | V |
| LH FDU mount bolt (through HCU bracket hole) | 1x E18 | 85 Nm | V |
| Subframe bolts | 2x 24 mm + 2x 21 mm (220 Nm) + 4x 24 mm (rearmost four with stud, 215 Nm) = 8 | 220 / 215 Nm | V |
| FDU HV harness bolt | 1x 10 mm | 10 Nm | V |
| Front skid plate | 8x 15 mm nuts + 2x 11 mm bolts | 50 Nm each | V |
| Front aero shield | 11x 10 mm (Loctite 222) | 6 Nm | V |
| LH/RH lower control arm shield | 3x 10 mm per side | 7 Nm | V |
| Caliper (each side) | 2x 24 mm | 315 Nm | V |
| Brake hose bracket (each side) | 1x 10 mm | 10 Nm | V |
| Front damper to lower control arm (each side) | 2x 21 mm | 140 Nm | V |
| Upper control arm to knuckle nut (each side, new) | 1x 18 mm | 85 Nm | V |
| Wheel liner to HV battery chinstrap | 1 push clip + 2x 10 mm | 6 Nm | V |
| Ground strap to chinstrap | 1x 10 mm | 10 Nm | V |
| Fore crossmember | 2x 18 mm | 90 Nm | V |
| Cooling fan module (CFM) lower / upper | 2x 10 mm / 2x 10 mm | 10 Nm | V |

- FDU connections: 4 steering rack connectors, breather, FDU harness (4 connectors, 10 clips), powertrain supply and return hoses, halfshafts (circlip click), HV harness connector, ground strap. Sling uses 3 hooks. Tools: subframe fixture 1099645-99-D, powertrain table 1066521-00-A. V.
- HV safety check before work: amp clamp under 0.5 A, voltage under 10 V; gloves class 0 (1000 V) with leather over-gloves. V.
- Removal order (summary): Service Mode, coolant fill/drain routine (50 min limit), disconnect MV power, HV check, aero shield / skid plate, wheels, frunk, front fascia, CFM, hoses, steering rack connectors, harness, caliper and damper and UCA release, subframe fixture and lifting tool, FDU mount bolts, subframe bolts, lower subframe, harness, halfshafts, gearcase bolts, sling the drive unit out. V.

**Front subframe (AWD)** — [SM/GUID-794CE60D](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-794CE60D-61DE-4B22-A99B-6DB0A31A8590.html), DRAFT, 2026-09-25, variant AWD. V.
- Wheel nuts 6 per wheel, 21 mm, 205 Nm. Lower valence 6x 10 mm 6 Nm. Frunk 6x 10 mm 12 Nm. Fascia tow hook covers 4x 10 mm 4 Nm. LH and RH fascia side bolts 1 each, 6 Nm.
- Tie rod to knuckle 1 each 21 mm 170 Nm. Air spring module 2x 21 mm 140 Nm. Stabar end link to lower arm 1 each 275 Nm (corrected 2024-10-10). Lower arm to knuckle nut 1 each 24 mm 190 Nm.
- Lower arm to subframe: 2x 21 mm at 175 Nm and 1x 24 mm at 300 Nm per side. Steering actuator to subframe 2x 21 mm 175 Nm.
- Subframe bolts 8 total: 220 Nm (215 Nm for rearmost four with stud).

**Front half shafts** — [SM/GUID-9216B93E](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-9216B93E-5C78-49C4-A0F6-068666761C08.html) (LH, FRT 0.72), no variant. V.
- Half shaft bolt 1 per side (always discard and replace) 300 Nm. Wheel nuts 6x 205 Nm. Caliper bolts 2x 315 Nm. Tie rod end nut 1x 170 Nm. UCA nut 1x (new) 80 Nm on this page (the FDU page says 85 Nm; discrepancy, Tesla-internal). Brake hose bracket bolt 1x 10 Nm.
- Index also lists "Halfshafts - LH and RH - Front (Remove and Replace)" [GUID-FFC01D33](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-FFC01D33-7140-43C3-8291-39E9BE351CE0.html) (not read).

**Front electric oil pump** (qty 1) — [SM/GUID-DB3DCC55](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-DB3DCC55-1004-4B1E-ADF1-8577ECB06EDE.html), FRT 0.78. V.
- 2 bolts External Torx Plus EP10, 5 Nm + 20 deg. Fill plug 1x 8 mm Allen 15 Nm. Fluid KAF1 only; filled until it spills, no volume stated. Oil pump O-ring is green. RH acoustic cover: 2 clips lower portion + 2 clips to FDU.

**Front heat exchanger (FDU oil cooler)** — [SM/GUID-566F0C00](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-566F0C00-FA93-4D89-851A-815B36A5463F.html), FRT 1.32. V.
- 2 bolts EP10 5 Nm. Oil fill plug 8 mm Allen 15 Nm. Spring clips: 2 on FDU hoses, 1 radiator inlet, 1 radiator-to-manifold. Front fascia fasteners 6x 10 mm 4 Nm; RH and LH fascia fastener 1 each 6 Nm.

**Front gearbox fluid** — [SM/GUID-8130467F](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8130467F-7764-4BF8-82E6-319EDBAE36D1.html). V.
- Fluid KAF1 ("do not interchange or mix oil types"). Fill and drain plugs 15 Nm (8 mm Allen). Fill until it spills; if over 500 mL has to be added, further diagnosis (earlier note said 300 mL). Tesla notes Cybertruck drive unit gearbox fluid drain procedures are still under development; top-off only.

**Rear Drive Unit, Dual Motor** (qty 1, rear subframe; variant Dual Motor/AWD) — [Remove and Install SM/GUID-AD6E7236](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-AD6E7236-3510-49ED-9B80-6382667074CA.html) (FRT 3.30) and [Remove and Replace SM/GUID-B38C881E](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B38C881E-1281-466E-A66E-2DF3CA573C49.html) (FRT 3.36). V.

| Item | Qty / type | Torque | Status |
|---|---|---|---|
| Rear subframe to body | 4x 24 mm | 355 Nm | V |
| RDU gearcase mount | 2x 18 mm | 110 Nm | V |
| RDU mounting bolts | 2x E18 | 85 Nm | V |
| RDU HV cable assembly | 4x 10 mm | 4 Nm | V |
| Rear diffuser bracket | 6x 13 mm | 30 Nm | V |
| Rear diffuser | 6x 10 mm + 8x T30 (14 total) | 6 Nm | V |
| Mid aeroshield | 3x 15 mm (70 Nm) + 3x 13 mm (28 Nm) + 2x 10 mm (6 Nm) | as listed | V |
| Rear skid plate (RDU page) | 3x 15 mm 42 Nm, 5x 13 mm 28 Nm, 2x 10 mm 6 Nm, 6 clips | as listed | V |
| Rear aero shield | 5x 10 mm + 2 guides | 6 Nm | V |
| Rear brake caliper (each) | 2x 21 mm | 150 Nm | V |
| Rear brake line to UCA (each) | 1x 10 mm | 10 Nm | V |
| UCA to knuckle nut (each, new) | 1x 21 mm | 150 Nm | V |
| Rear air spring to lower control arm | 2x 21 mm (nylon or cinch nuts) | 140 Nm | V |
| Lower control arm aeroshield (each) | 3x 10 mm | 7 Nm | V |
| Wheel nuts | 6 per wheel, 21 mm | 205 Nm | V |

- Halfshaft to RDU uses a U-bolt, 2 nuts per shaft, 10 mm, hand-tight then U-bolt. New RDU arrives prefilled with gearbox fluid. Coolant fill at least 15 L in container. Test drive at least 25 mph. Alignment correction code 00040100. V.

**Rear half shafts (LH/RH)** — [SM/GUID-8B961BB8](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8B961BB8-A23B-4B5E-9BAC-FAFDA52BF4DF.html). V.
- Half shaft bolt 1 per side (24 mm, discard) 300 Nm. Caliper 2x 21 mm 150 Nm. UCA nut 1x (new) 150 Nm. Brake line bolt 1x 10 mm 10 Nm. Wheel nuts 205 Nm. Removal uses cable puller and U-bolt with 2 fasteners.

**Rear motor mount / inverter mount (RH)** — [SM/GUID-B9080049](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B9080049-BD89-46E8-B378-54EB8558D668.html), DRAFT, FRT 2.22. V.
- RH motor mount bolt to subframe 1x 16 mm or E18, 85 Nm. Inverter mount assembly 3x EP14, 35 Nm + 55 deg. RH motor mount to RDU 4x E14, 35 Nm + 55 deg. Lower tub crossmember 2x 13 mm 36 Nm. Acoustic cover 5 clips. Subframe Revision D has no NVH mass and cannot take 16 mm hex bolts; others have an NVH mass. Coolant hose has 1 spring clip at the rear inverter upper fitting. Coolant plug kit 1135762-00-A.

**Rear electric oil pump (LH rear)** — [SM/GUID-6ED50306](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-6ED50306-498C-4269-A688-B7A7ED1E5244.html), DRAFT, FRT 0.66, dated 2026-08-09. V. Variant not stated (index also lists a Tri Motor LH oil pump, [GUID-F05C97C5](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-F05C97C5-00E2-4D06-A52C-2C81ED6D927C.html), not read).
- 2 bolts EP10, 5 Nm + 20 deg. Drain plug 1x 8 mm Allen 15 Nm; fill plug 1x 8 mm Allen 15 Nm. Fluid KAF1 only, fill until spill. Rear acoustic cover clips: 3 lower + 2 to RDU. Verification ODIN routine TEST-SELF_DIF_X_OIL-PUMP-PRESSURE.

**Other drive-unit pages that exist (index, V as titles only; not read)**: oil filters (FDU [058DE3A8](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-058DE3A8-DB38-4CDA-AB5F-33AFD2FE85A8.html), RDU [AA7647B7](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-AA7647B7-A4C7-4B9D-9AA5-DAD3D994FEE9.html)), breather housings, gearcase and side bushings, ground straps, output axle seals, NVH covers (inverter and motor side), phase-out covers, front inverter, rear inverters (LR, standard, LH/RH Tri-Motor, "Front and Rear Set (Dual Motor)"), HV harness FDU [49C49CBB](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-49C49CBB-B604-4716-A8FD-9022E3EA8217.html), HV harness RDU Dual Motor [C7E99D5B](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-C7E99D5B-D1E1-4EF3-B4B9-B764A6BE1BE4.html), and HV harness RDU LH and RH Tri Motor ([F4491A6D](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-F4491A6D-98C2-43B9-B403-25C16385CB70.html), [B6956D4A](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B6956D4A-C680-4A0F-BA74-6131B48FE29C.html)). Coolant hoses: FDU supply inline, FDU inverter-to-heat-exchanger, RDU supply/return for Dual Motor, Long Range and Tri Motor. Index: [SM/index.html](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html).

### Inferences
- Cyberbeast = Tri Motor: 1 FDU + two rear drive units (LH/RH) with LH rear oil pump listed, per the "Tri Motor" page set (I). The Dual Motor RDU page is the AWD single-RDU case.
- Both FDU and RDU appear to use the same 110 Nm gearcase mount and 85 Nm E18 mount bolts, and the same KAF1 gearbox fluid with 15 Nm plugs (I from matching tables).

### Gaps
- Drive unit, motor, inverter and half shaft masses: not stated on any page read. Lifting is by 3-hook sling; mass not given.
- Rear subframe, rear mount and Tri Motor torque tables were not read.
- Gearbox fluid capacity in litres: not stated.

---

## 2. High-voltage battery, service disconnect, pyro fuse, busbars, HV cables

### Takeaway
Full torque tables exist for the LR and AWD pack removal. No pack mass, cell count, brick layout, pack voltage or kWh figure appears in these procedure pages. The "service disconnect" in this truck is the First Responder Loop (FRL) plus MV battery connector disconnect, followed by a zero-voltage check, and the primary and secondary pyro fuses sit in the ancillary bay on top of the pack.

### Cited Findings

**HV battery removal (Long Range)** — [SM/GUID-D3E09C6D](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-D3E09C6D-D7C0-4B32-99DC-978163028DEF.html), DRAFT, 2026-09-24, FRT 4.20. V.

| Item | Qty / type | Torque | Status |
|---|---|---|---|
| Front exterior pack mounts | 6x 18 mm | 115 Nm | V |
| Front exterior ground strap | 1x 10 mm | 10 Nm | V |
| Side exterior pack mounts | 16x 15 mm | 62 Nm remove / 60 Nm install | V |
| HV battery to RUB (rear underbody) | 4x 21 mm | 119 Nm remove / 115 Nm install | V |
| Front interior pack mounts (each side) | 3x 24 mm (6 total) | 160 Nm | V |
| Rear interior pack mounts (each side) | 4x 13 mm (8 total) | 60 Nm | V |
| Rocker cover to side ski (each side) | 6x 10 mm | 10 Nm | V |
| Rocker step reinforcements | 3 per location, 10 mm | 15 Nm | V |
| Rocker fasteners (4 locations) | 1x 10 mm | 4 Nm | V |
| Seat track patch bolts | 2 per track, T45P (discard) | 34 Nm | V |
| Footwell cover | 1x 10 mm | 3 Nm | V |
| Bed floor assembly | 10 short + 2 long, 15 mm | 56 / 46 Nm | V |
| MV controller locking covers | 1x 8 mm each | 6 Nm (LH frame 4 Nm) | V |
| HV outlet to console panel | 2x T20 | 1 Nm | V |
| Center console | 4 front + 2 rear, 10 mm | 5 Nm | V |
| Busbar HV connector lid | 1x EP10 | 9 Nm | V |
| Busbar to DC FC header | 2x 10 mm | 9 Nm | V |
| Mid-aero shield | 3x 15 mm 70 Nm, 3x 13 mm 28 Nm, 2x 10 mm 6 Nm | as listed | V |
| Front aero shield | 17x 10 mm (Loctite 222) | 6 Nm | V |
| Front skid plate | 8 nuts 15 mm + 2 bolts 11 mm | 50 Nm | V |

- Pack coolant hoses disconnected: RDU supply and return, powertrain (PT) supply and return, battery supply and return. Spring clips, plugged. Alignment rods: 4 (2 larger, 2 smaller). Lift: 4 Universal Lift Pad adapters, jack mode, battery table. V.
- HV joint check after reinstall: Hioki resistance 0.050 to 0.195 milliohm at each HV joint (stop and escalate above 0.195). Penetrox A-13, about 2 drops per HV joint. V.
- Order: remove rocker covers and step reinforcements, fender flare sections, seats, trim and carpet, interior HV mount bolts, bed floor, lift, enter Service Mode, drain coolant, power down, disconnect FRL and MV battery connectors, wait 2 min, release MV controller locking covers, backbone harness, zero-voltage check, remove aero shields and skid plates, drain and disconnect hoses, A/C HV and RDU HV harnesses, ancillary MV connector, busbar lid and connector bolts, battery table, front and side bolts, lower. V.

**HV battery (AWD)** — [SM/GUID-D6F2FED3](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-D6F2FED3-46D3-4915-8D55-C47633D5739C.html), DRAFT, 2026-08-12, FRT 6.55. V.
- Same pack mounts as LR with these differences: front interior 6x 24 mm 160 Nm; rear interior 8x 13 mm 60 Nm; seat risers 8x 13 mm 40 Nm; accelerator pedal 2x 13 mm nuts 10 Nm; subwoofers 4x 13 mm 8 Nm; interior HV harness bulkhead cover 3x 10 mm nuts 9 Nm; FDU HV harness 1x 10 mm 10 Nm.
- Pressurized pack lines: 2 VOSS fittings, 12 mm, 8 Nm. Forward bed panel 6x 15 mm 85 Nm. Tonneau NVH barriers: pre-April 2024 11x T25 5 Nm; post-April 2024 10x 8 mm 5 Nm; post-October 2024 18x 4 mm Allen 5 Nm. Variant tags: Terrestrial Armor yes/no; Post date (April 2024, October 2024).
- Special tools: battery alignment rods 1134523-00-B, coolant drain kit 1065131-00-A, plug kit 1135762-00-A, fluid catcher 1080568-00-A, Hioki 1076927-00-A, HV battery table 1020566-00-F, lift pad adapters 1936724-00-A, vacuum refill tool 1050448-00-B.
- RCM disarm and transfer only if pack replaced.
- Other variant pages: HV Battery (Standard) [GUID-1491FFC9](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-1491FFC9-1908-4FF7-8FA9-77520ECA46D2.html) (not read).

**Pyro disconnect (pyro fuses)** — [SM/GUID-828B37BC](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-828B37BC-A40A-440C-BA7D-7B6E622ACD9D.html). V.
- Primary pyro fuse: 2 bolts 13 mm, 5 Nm + 60 deg. Secondary pyro fuse: 2 bolts 13 mm, 5 Nm + 60 deg. Pyro access cover 4x E-Torx 5-lobe 10 Nm. Hioki test across 4 HV joints. No electrical rating on page.

**Fuses (Power Conversion, LR)** — [SM/GUID-640D91ED](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-640D91ED-4713-4A2E-A12F-40854CBF2F99.html). V.
- PCS fuse 2x 8 mm 6 Nm. HV compressor fuse 2x 8 mm 6 Nm. Low voltage header 2x EP10 6 Nm. Ancillary cover 22x E10 5-lobe 6 Nm. Fast charger header doubler 2x E10 10 Nm. Charge port busbar kit to HV header 2x 10 mm 9 Nm.
- Ancillary fuse named in index: "Fuse, 60A, 1000VDC, Eaton EVK22-60-T - Ancillary" ([GUID-45986159](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-45986159-E5DF-45C1-ABF6-96E6999ACF44.html), title only; rating V from the title).

**Last Mile Busbar Assembly** — [SM/GUID-CA82FD25](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-CA82FD25-8997-4FD2-8EF8-8C0F82F1C53A.html), FRT 4.56. V.
- Last mile busbar assembly: 3x 10 mm 10 Nm + 3x T55 captive 5 Nm + 60 deg. LHRDU, FDU and RHRDU headers: 6x 5-lobe 10 mm 10 Nm. 2x4 header assembly 4x 6 Nm. PCS to ancillary 6x 8 mm captive 6 Nm. Device cluster busbar fasteners 4x Torx Plus 55, 5 Nm + 60 deg; device cluster assembly 4x E10 6 Nm. PCS coolant header 2x EP10 6 Nm. Air suspension reservoir 2x 13 mm nuts 33 Nm. Pressurized pack valve block 1x 10 mm 5 Nm; pack lines 2 VOSS 8 Nm. Coverbox cross supports 8x T25 5 Nm.

**HV battery electrical components list (section 1630, 44 procedures, titles only, V)** — [SM/GUID-5DA3FE21](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-5DA3FE21-AC08-47AA-9DC3-B57AB94474F3.html): AC junction box (LR, Standard), ancillary cover, device cluster assembly (LR, Standard), flood port, ancillary fuse, shunt jumper harness, DC input header/busbar, contactor seize check, ACJB-to-FC and ACJB-to-PCS HV harnesses, pyro disconnect, positive/negative DC inlet in the ancillary bay, last mile busbar. The page has no BMS entry. HV battery enclosure section 1610 has only the two air leak tests; cooling section 1620 lists no children. Coolant/air leak: pack valve block and VOSS lines exist.

**Charge port (NACS) busbar (LR)** — [SM/GUID-3BF96D09](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-3BF96D09-6DF7-401C-BA93-F2AC82564EC0.html). V.
- Charge port to body 2x 10 mm 6 Nm (hand tools, stainless galling warning). Charge port to outer sail 1x 6.5 Nm. Ground cable 1x 6.5 Nm. Busbar kit to HV header 2x 9 Nm. Fender flare carriers: aft 2x 7 Nm, fore 6x 7 Nm. LH rear location (charge port on LH rear quarter). Hioki 0.050 to 0.195 milliohm. Index also lists charge port door, Charge Port Controller ECU (Gen 4), charge port voltage check ([GUID-D32D2226](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-D32D2226-FCF5-4FA4-9BB7-8666B594BFEB.html)), bed outlet assembly and HV harnesses for cabin and bed outlets and AC compressor.

**Rescue sheet** — [Tesla Cybertruck Rescue Sheet PDF](https://digitalassets.tesla.com/tesla-contents/image/upload/Cybertruck-Rescue-Sheet.pdf) (R via search summary only; PDF text could not be extracted locally, no Python available): double-cut the First Responder Loop under the hood, disconnect the 48 V battery, do not open or push on the HV or 48 V battery, HV cables are orange. The Spanish sheet differs (48 V negative only if necessary) ([ES sheet](https://digitalassets.tesla.com/tesla-contents/image/upload/First-Responders-Cybertruck-Rescue_Sheet-ES.pdf)). tesla.com/firstresponders returned HTTP 403.

### Inferences
- The pyro fuses sit in the ancillary bay under the bed floor, behind the rear seat and above the rear of the pack, since the PCS/fuse procedures access them via the bed floor and Ancillary Access Bench (I).
- Pack is held by about 22 exterior bolts (6 front + 16 side), 14 interior bolts (6 front + 8 rear) and 4 bolts to the RUB; total about 40 structural fasteners on LR (I, summed from V rows).

### Gaps
- Pack mass, dimensions, cell format/count, module/brick layout, nominal voltage, kWh: not on any page read. Not found in the Rescue Sheet text accessible to me. Do not take outside figures as verified.
- BMS location/part: no procedure in 1630 index.

---

## 3. Power conversion (PCS, charger, DC-DC) and charge system

### Takeaway
The PCS is a roof-of-pack ancillary-bay unit held by 6 bolts, with a 22-bolt ancillary cover; PCS removal needs the bed floor off. No PCS mass.

### Cited Findings
- **PCS (Long Range)**: [SM/GUID-A78D3394](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A78D3394-E837-4960-9EBF-41BC37F7A51A.html), FRT 2.52. V. PCS mounting 6x E10 5-lobe, 6 Nm. PCS MV harness pigtail 1x EP10 6 Nm. MV header 2x EP10 6 Nm. Ancillary cover 22x E10 6 Nm. Fast charger header doubler 2x 10 Nm. Pyro cover 4x 10 Nm. Primary/secondary pyro fuses 4x 13 mm 5 Nm + 60 deg. HV connector to DC FC header 2x 9 Nm. Bed floor 12 short (56 Nm) + 2 long (46 Nm). Connectors: RDU HV harness, ancillary MV (double lock; red LV+, black LV-), device cluster HV DC harness, HV AC harness, PCS coolant couplers (inlet, outlet). Coolant leak test 50 psi, max delta 0.35 psi; at least 15 L waste container; vacuum 60-70 cmHg. Older vehicles (before 2023-12-22) may need the updated hose bundle (Post date tag).
- Other PCS pages (titles): PCS Remove and Replace [GUID-8F133FA6](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8F133FA6-44FC-4D62-9BD3-03C92951B916.html) (Standard/generic), coolant hose assemblies for PCS (LR and generic), Fuse PCS Standard [GUID-8C4618B2](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8C4618B2-87C6-422E-8CF8-4571C08ECCED.html), jumper harness ACJB-to-PCS (LR, Standard). V as titles.
- **Charge port busbar**: see section 2 (torques V).

### Inferences
- A separate DC-DC converter part is not listed in the index; DC-DC function appears integrated into the PCS (I).

### Gaps
- PCS mass, charger kW rating, DC-DC rating: not on pages read.

---

## 4. Thermal: supermanifold, Octovalve, pumps, chiller, condenser, compressor, refrigerant, coolant

### Takeaway
Refrigerant is R1234yf with POE RB100EV oil. The vehicle information label holds the charge, and the manual page gives no grams. Total coolant volume is not given, but about 20 L drains from the HV battery side and a drain container of at least 15 L is used for refill.

### Cited Findings
- **Refrigerant**: R1234yf; oil POE RB100EV; recharge the same oil amount that was recovered; hose equalize limits: discharge max 26 bar, suction min 1.15 bar; machine Snap On Ecotechnics 1711245-00-A — [SM/GUID-9D760C9C](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-9D760C9C-F95C-4D58-AF74-AFFC330168B0.html). V. Charge in grams: not stated (read the vehicle label).
- **Flush**: minimum 3200 g refrigerant in tank; about 90 min flush with 25 min vacuum; leak test vacuum 20 min — [SM/GUID-B1831D39](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B1831D39-D817-485C-8ED8-4C32042A1BA5.html). V. Compressor oil addition: dry weight + 250 g (page example 7000 g dry gives 7250 g; the example suggests a compressor mass of order 7 kg, but this is Tesla's illustrative number, I).
- **Supermanifold** (qty 1, front, on megabeam) — same page: 2x 15 mm bolts to megabeam 33 Nm; Penta HVAC line nut 1x 13 mm 36 Nm; A/C line bolt 13 mm 22 Nm; line bracket bolt 10 mm 8 Nm; remote brake fluid reservoir bolt 8 Nm; FRT 1.68. V.
- **A/C compressor** (qty 1): [SM/GUID-EC799465](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-EC799465-6989-44B2-B722-EE04F7F533C8.html), FRT 0.72. 3x 10 mm to megabeam 5 Nm; suction/discharge line nuts 2x 13 mm 22 Nm; ground strap bolt 1x 10 mm 16 Nm (7 Nm on removal in the supermanifold page, a discrepancy); HV connector with red lock and black lever. V.
- **Octovalve**: [SM/GUID-12EE5DD0](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-12EE5DD0-FB31-4EDA-8F2D-D28A1DC00CB6.html), FRT 1.80. 4x T25 to supermanifold 7 Nm; 7 spring clips, 4 electrical connectors, 5 seal washers on Penta line plus 2 on compressor line. V.
- **Coolant pump (supermanifold)** qty 1: [SM/GUID-B4481962](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B4481962-AD1D-404E-9087-F5BE7DF2E100.html), FRT 0.96. 4x T20 screws 2 Nm, 1 O-ring, 1 connector. V.
- **Chiller**: [SM/GUID-D131CB52](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-D131CB52-2E0F-441F-B46B-3B880EAF5728.html), FRT 0.54. 4 nuts 8 mm 7 Nm; controller 3 bolts 4 Nm; harness bracket 3 bolts 8 Nm; 9 harness connectors. More than 30 mL oil drained triggers Toolbox article 353700. V.
- **Liquid cooled condenser (LCCR)**: [SM/GUID-FAC16ECE](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-FAC16ECE-F2C6-48CC-879C-666C2A9DD363.html), FRT 0.96. 4 nuts 8 mm 7 Nm; 3 spring clips; 2 AC port caps; refrigerant vacuum 20 min; Heat Pump Commissioning required. V.
- **Cooling fan module (CFM)**: [SM/GUID-CE0EE886](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-CE0EE886-A065-442E-8944-97429812878B.html), FRT 1.26. Upper 4x 10 mm 10 Nm, lower 2x 10 mm 10 Nm, fore crossmember 2x 18 mm 90 Nm; LH and RH modules; radiator has 1 inlet and 1 outlet hose with spring clips; harness 5 clips + 1 grommet. V. The FDU/subframe pages show upper 2x and lower 2x CFM bolts for the one-side case (varies by page, caution).
- **Coolant**: drain about 20 L (HV battery side) at 5.0 psi regulator; vacuum refill 60-70 cmHg, hold 30 s, evacuate 3 min; air purge pumps 10 min at 3500-6500 RPM (7000 RPM means air lock); thermal fill/drain routine 50 min limit — [SM/GUID-572AEDB1](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-572AEDB1-54B5-4DF4-89EF-A8B53E4D28E1.html), [SM/GUID-F1AD9C0B](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-F1AD9C0B-AB56-4423-AB30-70C85E855F46.html). V. Coolant type: not specified (page defers to a Fluids section).
- **Thermal index** (titles, V): 1810 Cabin HVAC, 1820 Refrigerant (5 procedures: compressor and supermanifold, compressor, recovery/recharge, compressor acoustic cover, compressor/supermanifold/A-C lines), 1830 Cooling (20 procedures: hose bundles for powertrain, HV battery, FDU/RDU supply and return, manifold-radiator hoses, CFM, radiator clean), 1840 Supermanifold (20 procedures: coolant bottle, check valves, chiller, expansion valve coils and cores, controller, desiccant, ACC/chiller/LCCR filters, Octovalve, pump, powertrain pressure sensors high/low, supermanifold). [SM/GUID-F1BA8698](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-F1BA8698-924F-458F-A2F4-AD55234544AE.html), [GUID-B2A8FCB0](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B2A8FCB0-28AB-4002-9192-2B6EBF4EF5E8.html), [GUID-C4D37B9C](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-C4D37B9C-F199-437B-BFA0-5DE846CAEFC8.html).
- No separate radiator, condenser or battery coolant pump removal procedure exists in section 1830 (only "Radiator Clean"). V.

### Inferences
- Hybrid single-integrated "supermanifold" holds Octovalve, coolant pump, chiller, LCCR, and expansion valves (I from the procedure set).
- Total coolant system volume is more than 20 L, because 20 L drains from only the pack side and the vacuum refill uses at least 15 L container (I).

### Gaps
- Refrigerant charge in grams, coolant type/spec, total coolant volume: not in pages read (Fluid Capacities page not found).
- Brake lines/brake fluid line torques beyond those above: not read.
- Variant tags of Cyberbeast on thermal pages: none listed.

---

## 5. Not obtained
- Emergency Response Guide/Rescue Sheet content (cut zones, pack weight): PDF text not extractable here; tesla.com/firstresponders returned 403. Only a search summary of the Rescue Sheet is available (R). A re-try with a PDF-capable tool on `C:\Users\Álvaro\.claude\projects\C--Users--lvaro-CYBERTRUCK\20d6a30c-b70f-4b9b-b0da-cceaa977c8ac\tool-results\webfetch-1792225093171-b0071q.pdf` is recommended.
- Count of numeric items recorded: roughly 230 fastener/torque rows, against the 150 target; item entries with mass: zero.
