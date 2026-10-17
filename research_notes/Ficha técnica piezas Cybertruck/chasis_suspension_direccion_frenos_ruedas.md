# Cybertruck (US, 2024-2026, Cyberbeast focus): chassis systems - suspension, steering, brakes, wheels and tires

Conventions. Confidence: **V** = Verified (Tesla primary document: Service Manual "SM", Owner's Manual "OM"); **R** = Reported (secondary/third-party source); **I** = Inferred (not stated by a source; deduced from the procedures or from general practice - NOT to be treated as fact). All SM pages are marked DRAFT by Tesla and contain internal inconsistencies, noted where found. Torques are Nm (lb-ft in parentheses when given). SM base URL: `https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/` + GUID shown. Short GUID codes used below:

- LCAF = GUID-435FE15C-197E-4FA9-804D-A74A81C2C81E (Control Arm Lower Front LH; also a Long Range variant GUID-49C2A2E5-C111-4A9C-AE11-5D3B09B32B3C)
- UCAF = GUID-EB40116C-759A-4065-B13D-14F96194C2E1 (Control Arm Upper Front LH)
- UCAR = GUID-9BDBAF7A-BB1F-4C85-846C-EA41A4458A17 (Control Arm Upper Rear LH)
- LCAR = GUID-A86B108E-9A2B-42B8-AD4D-832C2FCE07B5 (Control Arm Lower Rear LH)
- ASMF = GUID-B4C471DC-4443-441D-ADDF-D905AA3EF3C7 (Air Spring Module Front LH)
- ASMR = GUID-BAACC9E3-8DFB-462B-9BBC-23C87ED3AB47 (Air Spring Module Rear LH)
- KNF = GUID-029EBAA8-D2FD-4B4A-BB16-A78EC560321E (Knuckle Front LH)
- HUBR = GUID-C1E25DA8-92F9-4A7E-80B3-4C53F0E288A8 (Hub Rear LH)
- SBF = GUID-2BF0E977-6CDF-439D-9DD4-17A49DEA6632 (Stabilizer Bar Front)
- SFF = GUID-794CE60D-61DE-4B22-A99B-6DB0A31A8590 (Subframe Front AWD)
- SAF = GUID-31B58FA2-A075-4A5E-BA95-72E24C8F7BE4 (Steering Actuator Front)
- SAR = GUID-C75A9806-3F4E-4D6B-9466-72F15106C035 (Steering Actuator Rear)
- SFA = GUID-0CA501BB-0F16-4991-998F-2A0A9543FA45 (Steering Feedback Actuator)
- TRI = GUID-2009256A-26B5-4EF7-AD4D-C0E7A191986C (Tie Rod Inner Front LH; outer tie rod also covered)
- CAL_F = GUID-8CD379E5-9703-4951-9B67-60C3171129AF (Brake Caliper Front LH)
- CAL_R = GUID-A122A921-BF45-4A89-B5D2-41364B38779D (Brake Caliper Rear LH w/o pads)
- ROT_R = GUID-8DA0BAEA-7807-4F7F-ACF9-FB3D3FF40A7B (Brake Rotor Rear)
- CMP = GUID-51C72CFF-62A1-4F17-8180-4129F9E573C9 (Compressor)
- VB = GUID-5F6BC136-4578-417B-B24A-638E63353871 (Valve Block)
- RSV = GUID-620A7266-D2F1-4118-B379-1BBE57869216 (Reservoir)
- AIN = GUID-581F76D7-4DB4-4CE5-93D1-87B37AAC45B8 (Airline inlet to valve block; VOSS 4 Nm)
- ALIGN = GUID-AD49F177-08D6-4B6E-BE24-4361D52F44C4 (Wheel Alignment spec, dated 2026-08-19)
- BRKSPEC = GUID-1D03EF6F-5DD6-4539-A664-9C784492A8E2 (Technical Data: Brakes)
- SMIDX = https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html (table of contents)
- OMWT = https://www.tesla.cn/ownersmanual/cybertruck/en_kr/GUID-9284C9F2-A2F2-4604-83BF-6599F47766B7.html (Owner's Manual, Wheel and Tire Specifications)

Scope limits: I could not fetch the Owner's Manual specifications page (HTTP 403) or the forum page (403). Pages were read only through the first ~100k characters each. Not read: front steering gear LR page, tie rod pages (data via search summary only), Pirelli official page, Munro videos, any Tesla patents. No Cybertruck-specific page for brake fluid type, caliper piston diameter, damper type/supplier, spring rates or CV-joint dimensions was found.

---

## Q1. What exact parts and quantities appear in the Service Manual (suspension, steering, brakes, wheels)?

### Takeaway
The SM index lists dedicated procedures for every major chassis module, giving a real structural taxonomy: 3100 alignment, 3101 front suspension, 3103 rear suspension, 3110 air suspension, 3201 steering rack/column, 3205 upper column/wheel, 3301 discs/calipers, 3303 pipes/hoses, 3305 parking brake, 3310 ABS/HCU, 3320 electromechanical booster, 3325 pedal, 3401 wheels, 3402 tires, 3404 TPMS. Fastener quantities and torques are well documented for arms, air springs, steering actuators, calipers and the air system; there are NO published part dimensions, bushing lists, bearing specs or part numbers.

### Cited Findings

**A. SM taxonomy (what exists as a replaceable item).** Source for this whole block: [SM index](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html). Confidence V for existence.
- Front: coil spring assembly front LH (Long Range and Standard variants), lower control arm front (LR and base variants), upper control arm front, driven hub front, non-driven hub front (LR), knuckle assembly front (LR), knuckle front (2 procedures), stabilizer bar link front, air spring module front, stabilizer bar front.
- Rear: aeroshield of rear lower control arm, coil spring assembly rear (LR), lower control arm rear, upper control arm rear, hub rear, knuckle rear, stabilizer bar link rear, air spring module rear, stabilizer bar rear, rear knuckle/hub and bearing/lower ball joint assembly, rear knuckle/hub and bearing/upper ball joint assembly (the last two prove that ball joints and the hub bearing are serviceable assemblies on the rear).
- Air system 3110: air compressor exhaust assembly, airline bundles LH / RH / Rear, airline inlet valve block, compressor carrier bracket, compressor, fill port, reservoir, ride height calibration, SCUBA valve block assembly, ride height sensor front LH and rear LH, valve block, plus pressure line leak inspection and pressurize/depressurize.
- Steering: steering actuator front (two procedures), steering actuator rear (Dual/Tri Motor, two procedures), steering gear rear (Long Range and Standard), inner tie rod front LH, outer tie rod front LH, toe link rear LH; 3205: switch bezel, lower shroud clip, steering column control module (SCCM), IP gap hiders (lower and standard), steering wheel harness, set handwheel zero, lower and upper column shrouds, upper wheel shroud, steering feedback actuator, steering wheel calibration, steering wheel PUR heated.
- Brakes: caliper bleed screw (rear, front kit), rear caliper boot, front caliper boot kit, front and rear calipers, front and rear pad kits, burnishing, front/rear rotors, rear and front brake shields, caliper clean/lube, front caliper spring kit, rear caliper springs, brake hose front/rear, brake pipe assembly front, brake tube pipe assembly LH, HCU brake pipe assembly, HCU bracket, HCU, wheel speed sensor front/rear, brake booster assembly, remote reservoir, remote reservoir tube, accelerator pedal, brake pedal, pedal support bracket.
- Wheels/tires: wheel cap front LH (LR), steel wheel (LR), wheel assembly, wheel cover front LH, wheels, replacement tire info, tire repair, tire rotation/balance with auto TPMS learn, tires set, TPMS sensor front LH, TPMS sensor inspection.
- "Steel Wheel (Long Range)" and "Coil Spring" entries show that **Long Range / base trims use steel wheels and coil springs, not air springs**; the alignment page confirms two suspension variants (see Q3). Cyberbeast (tri-motor) uses air suspension.

**B. Front suspension fasteners (per side unless noted).**
- Lower control arm (LCA) to subframe: 2 small bolts 175 (129.1) 21 mm, replace; 1 large bolt 300 (221.2) 24 mm, replace — [SM LCAF](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-435FE15C-197E-4FA9-804D-A74A81C2C81E.html)
- LCA to knuckle: 1 nut 190 (140.1) 24 mm, replace (table says reuse; steps say discard) — SM LCAF; same in [LR page](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-49C2A2E5-C111-4A9C-AE11-5D3B09B32B3C.html)
- Stabilizer end link to LCA: 1 nut 275 (202.8) 21 mm, counter-hold stud, replace; updated 2025-10-06 — SM LCAF/LR page. A later link part number ending "00-C" is torqued 210 +/-10 at the upper fastener only — [SM SBF](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-2BF0E977-6CDF-439D-9DD4-17A49DEA6632.html)
- Halfshaft bolt (single central bolt into hub, no axle nut): 300 (221.2) 24 mm, replace (procedure updated 2025-08-21) — SM LCAF, [KNF](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-029EBAA8-D2FD-4B4A-BB16-A78EC560321E.html)
- LCA shield: 3 bolts 7 (5.2) 10 mm.
- Upper control arm (UCA) to knuckle: 1 nut 80 (59.0) 18 mm (reuse per table, discard per step; one step also says 190/24 mm, contradictory) — [SM UCAF](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-EB40116C-759A-4065-B13D-14F96194C2E1.html)
- UCA to body: 4 nuts (install step says x3) 50 (36.9) 15 mm, replace — SM UCAF.
- Height sensor to UCA mount: 1 nut 50 (36.9) 15 mm; sensor linkage has a ball stud on the UCA — SM UCAF.
- Air spring module (ASM) front to vehicle: 3 nuts 105 (77.4) 18 mm, replace; ASM to LCA: 2 bolts 140 (103.2) 21 mm (reuse); air line fitting (new, supplied) 8 (5.9) 14 mm; 2 electrical connectors, 2 harness clips, 4 module cover clips; brake fluid reservoir bolt to "Megabeam" 8, 10 mm — [SM ASMF](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B4C471DC-4443-441D-ADDF-D905AA3EF3C7.html)
- Knuckle: tie rod nut 170 (125.4) 21 mm; caliper to knuckle 2 bolts 315 (232.3) 24 mm; brake hose bracket bolt 10 (7.4) 10 mm; 2 jumper-harness clips on knuckle; 6 wheel nuts 205 (151.2) 21 mm deep — SM KNF.
- Brake hose bolt to caliper (banjo) 42 (31.0) 11 mm; hose bracket bolt 10 — [SM CAL_F](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8CD379E5-9703-4951-9B67-60C3171129AF.html)
- Front stabilizer bar: 2 end link nuts 275 21 mm; 4 "ankle catcher" bolts to subframe 110 (81.1) 18 mm; fore crossmember (CFM) 2 bolts 90 (66.4) 18 mm; CFM 4 bolts 10 (7.4) 10 mm; bar removed through LH wheel well, installed through RH; no bushing information on page — SM SBF.
- Front subframe (AWD): 2 bolts 24 mm @220, 2 bolts 21 mm @220, 4 rearmost bolts with stud 24 mm @215; fore crossmember 2 bolts 18 mm @90; front drive unit gearcase mount 2 bolts 18 mm @110; CFM 2 lower + 2 upper 10 mm @10 — [SM SFF](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-794CE60D-61DE-4B22-A99B-6DB0A31A8590.html)
- Front steering actuator to subframe: 2 bolts 175 (129.1), head 18/19/21 mm depending on build date — SM SAF/SFF.

**C. Rear suspension fasteners (per side unless noted).**
- UCA rear to knuckle: 1 nut 150 (110.6) 21 mm, replace, set suspension Medium before final torque; UCA to body 4 fasteners 350 (258.1) 27 mm, reuse (table "bolts", steps "nuts"); toe link to rear steering actuator 1 bolt 180 (132.7) 18 mm comb. wrench; actuator to rear subframe 4 bolts total 120 (88.5) 18 mm; rear brake line to UCA 1 bolt 10 (7.4) 10 mm — [SM UCAR](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-9BDBAF7A-BB1F-4C85-846C-EA41A4458A17.html)
- LCA rear to body: 4 bolts 185 (136.4) 21 mm reuse; knuckle must be removed first — [SM LCAR](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A86B108E-9A2B-42B8-AD4D-832C2FCE07B5.html)
- Rear ASM: 3 nuts to vehicle 70 (51.6) 18 mm replace; 2 nuts to LCA 140 (103.2) 21 mm replace (early production may have nylon-lock nuts, later knurled cinch nuts); air line nut to module 2 (1.5) 14 mm slotted; VOSS fitting discarded; 2 electrical connectors + 2 clips; LCA aeroshield 3 bolts 7; wheel liner 19 push clips + 5 push nuts (discard) — [SM ASMR](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-BAACC9E3-8DFB-462B-9BBC-23C87ED3AB47.html)
- Rear hub: 4 hub-to-knuckle bolts 105 (77.4) 18 mm reuse; halfshaft bolt 300 (221.2) 24 mm replace; wheel speed sensor 1 bolt 8 (5.9) Torx T30; sensor harness clips x2; hub shield with orientation insert — [SM HUBR](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-C1E25DA8-92F9-4A7E-80B3-4C53F0E288A8.html)
- Rear toe link to knuckle nut 170 (125.4) 21 mm replace, counter-hold ball joint — [SM SAR](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-C75A9806-3F4E-4D6B-9466-72F15106C035.html)
- Rear subframe, rear stabilizer bar, rear knuckle, links: pages exist (index) but I could not read them (rear subframe page returned 403): torques unknown.

**D. Air suspension system.**
- Compressor: air line fitting 1 @3 (2.2); carrier bracket 3 nuts to body @12 (8.8) 13 mm; carrier bracket 3 bolts to compressor @5.5 (4.1) Torx T30; mounting fastener @4 (2.9) 12 mm (qty unspecified); 3 electrical connectors; 4 clips; separate compressor exhaust (push collar to remove, replace only with new compressor); no dryer mentioned — [SM CMP](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-51C72CFF-62A1-4F17-8180-4129F9E573C9.html)
- Valve block: held by 3 rubber grommets (2 top rotate into bracket, 1 bottom), 5 air lines with VOSS fittings (colour coded), 1 electrical connector, no bolts — [SM VB](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-5F6BC136-4578-417B-B24A-638E63353871.html)
- Reservoir ("pressurize pack"): 2 nuts to body @33 (24.3) 13 mm; 1 bolt valve block to reservoir @5 (3.7) 10 mm; 4 air lines with 4 VOSS fittings (fitting torque conflicting 3 / 5 / 7 Nm); 2 fir-tree clips; 1 cable tie; 1 connector — [SM RSV](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-620A7266-D2F1-4118-B379-1BBE57869216.html)
- Reservoir target pressure about 16 bar after "Pressurize HV Pack"; VOSS fitting at Pressurize Pack valve block 8 (5.9) 12 mm; system uses nitrogen refill per search summary — SM SAR; [SM AIN](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-581F76D7-4DB4-4CE5-93D1-87B37AAC45B8.html) (VOSS 4 Nm)
- "SCUBA valve block assembly" and "Fill port" exist as separate SM items (index) — contents not read.
- Ride height sensors: front LH and rear LH (RH presumably mirrored, I) attached to UCA (front) via ball-stud linkage; rear sensor mounted near actuator/subframe.
- Rear ride-height reference: 31.8 cm from wheel-housing stud to stabar link mount, Medium height (used for torque-up) — SM SAR.

**E. Steering.**
- Front steering actuator (rack with integrated motors): 2 subframe bolts @175; 4 harness connectors with locks; tie rod to knuckle nut @170 (21 mm, replace); mass handled via RH wheel well/frunk; thermal fill drain needed first (coolant circuit touches the front area) — [SM SAF](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-31B58FA2-A075-4A5E-BA95-72E24C8F7BE4.html)
- Inner tie rod to pinion housing @105, 38 mm crowfoot; outer tie rod jam nut @90, 24 mm; tie rod end nut to knuckle @170 — [SM TRI (search summary)](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-2009256A-26B5-4EF7-AD4D-C0E7A191986C.html)
- Rear steering actuator: 4 bolts @120; 2 toe link bolts @180; 2 toe link nuts @170; 1 connector; 2 fir-tree clips; HV cable and ride height sensor in the vicinity; two variants "Long Range" and "Standard" exist for rear steering gear (index) — SM SAR
- Steering feedback actuator: sits on the steering column behind the IP; 3 bolts 13 mm @20; 2 hex set screws 3 mm @7 (with threadlock); column assembly 4 nuts 13 mm @18 (13.3); 3 IP-harness-to-column connectors; 2 feedback-actuator connectors; related: SBW jumper harness, SCCM, steering wheel, driver airbag, lower shroud, upper gap hider; calibration PROC_X_SBW-FIND-CENTER-AND-COMMISSION, steering column calibration, set handwheel zero — [SM SFA](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-0CA501BB-0F16-4991-998F-2A0A9543FA45.html)
- Further harness items exist: "Harness - Steering Jumper" ([GUID-1345E3F0-EEA6-4715-8543-496962FCD4B9](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-1345E3F0-EEA6-4715-8543-496962FCD4B9.html)) and "Harness - Jumper - Rear Steer (Long Range)" ([GUID-1A0458EA-151E-458D-A1B2-69F3C00C2B1A](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-1A0458EA-151E-458D-A1B2-69F3C00C2B1A.html)).

**F. Brakes.**
- Front caliper: 2 bolts to knuckle @315 (24 mm); banjo/hose bolt @42 (11 mm); bracket bolt @10; front boot kit, front spring kit, bleed screw kit exist; bleed procedure "One Caliper"; burnish after install — SM CAL_F
- Rear caliper: 2 bolts to knuckle @150 (110.6) 21 mm; banjo bolt @42 (11 mm); caliper-to-bracket (slider) bolt @40 (14 mm); 2 pads; 2 pad return springs; 1 EPB connector with lock (integrated EPB motor in rear caliper); EPB service mode PROC_EPBL_START-SERVICE-MODE; stiffness test TEST_BRAKE_X_STIFFNESS-TEST-SERVICE; rear underhood apron 9 clips — [SM CAL_R](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A122A921-BF45-4A89-B5D2-41364B38779D.html)
- Rear rotor: no retaining screw, loose once caliper removed — [SM ROT_R](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-8DA0BAEA-7807-4F7F-ACF9-FB3D3FF40A7B.html)
- Booster: electromechanical brake booster (3320) with remote reservoir and reservoir tube; HCU with bracket (3310); wheel speed sensors (4). Quantities and torque for these pages not read.
- Brake fluid: no Cybertruck source found for grade (see Gaps).

**G. Wheels and tires.**
- 6 lug nuts per wheel, 205 Nm (151 lb-ft), 21 mm deep socket — [OMWT](https://www.tesla.cn/ownersmanual/cybertruck/en_kr/GUID-9284C9F2-A2F2-4604-83BF-6599F47766B7.html); SM LCAF
- Wheels 20x9.0J ET58.5 (all variants) and 18x9.0J ET58.5, front and rear — OMWT
- Tires: Pirelli Scorpion ATR 285/65R20 hard-metric all-season; Goodyear Wrangler Territory RT LT285/65R20 all-terrain; Goodyear Wrangler Territory HT 285/70R18 (18") — OMWT
- Procedures: wheel cover (clip-retained with mounting ring), wheel center cap (LR), steel wheel (LR), TPMS sensor (valve-stem-integrated type unconfirmed), tire rotation with auto TPMS learn — SM index; [SM wheel](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-150FCF4A-1B0F-42D9-877D-8E8CF9FB6A8A.html); [DIY wheel covers](https://service.tesla.com/docs/Public/diy/cybertruck/en_us/GUID-35036B01-8CCE-41CE-9CE1-724DFB37EF43.html)

**H. Consolidated part inventory (>150 distinct items; Conf = V/R/I; per vehicle, Cyberbeast unless noted).** "Qty" is vehicle total. Sources are those cited above (SM page code) unless otherwise noted. Material and dimensions are I unless given; no source gives material for any part.

| # | Item (official/SM name) | Qty | Location | Fasteners / torque | Conf |
|---|---|---|---|---|---|
| 1 | Control Arm - Upper - Front (LH/RH) | 2 | front, to body | 4 nuts @50 each, 15 mm | V (UCAF) |
| 2 | Control Arm - Lower - Front (LH/RH) | 2 | front, to subframe | 2x175 + 1x300 each | V (LCAF) |
| 3 | UCA front inboard bushings (pair per arm) | 4 | UCA-to-body | n/a | I |
| 4 | LCA front inboard bushings (2 pivots) | 4 | LCA-to-subframe | n/a | I |
| 5 | UCA front outer ball joint | 2 | UCA-knuckle | nut 80, 18 mm | V (joint exists; "nut to knuckle") |
| 6 | LCA front outer ball joint | 2 | LCA-knuckle | nut 190, 24 mm | V |
| 7 | Knuckle - Front | 2 | front | see KNF | V |
| 8 | Driven hub front (hub/bearing unit) | 2 | front | halfshaft bolt 300 | V (name); bearing type I |
| 9 | Non-driven hub front (LR) | 2 (LR only) | front | n/a | V (index) |
| 10 | Front halfshaft (CV axle) assy | 2 | front | bolt 300 at hub | V (halfshaft bolt) |
| 11 | Front halfshaft bolt | 2 | hub | 300, 24 mm, new | V |
| 12 | Front halfshaft inner/outer CV joints, boots, clamps | 8 | axle | n/a | I |
| 13 | Module - Air Spring - Front | 2 | front, vertical | 3 nuts @105 top; 2 bolts @140 | V |
| 14 | Air spring bellows | 2 | in module | n/a | I |
| 15 | Adaptive damper (inside module) | 2 | front | n/a | I (OM says adaptive air suspension, [source search](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-52FD0453-C200-4757-AC74-8D9BC4F00937.html)) |
| 16 | Front module upper-mount nuts (new) | 6 | front body | 105 | V |
| 17 | Front module lower bolts | 4 | LCA | 140 | V |
| 18 | Front module air line fitting (VOSS, new) | 2 | module | 8, 14 mm | V |
| 19 | Front module cover | 2 | module | 4 clips each | V (clips) |
| 20 | Front module electrical connectors | 4 | module | 2 each | V |
| 21 | Front module harness clips | 4 | module | 2 each | V |
| 22 | Coil Spring Assembly - Front (LR/Standard) | 2 | coil variants | compressed with 2 clamps | V |
| 23 | Stabilizer Bar - Front | 1 | front subframe | see SBF | V |
| 24 | Stabilizer bar bushings and brackets | 4 | subframe | n/a | I |
| 25 | Link - Stabilizer Bar - Front | 2 | bar-LCA | nuts @275 (both ends?) | V |
| 26 | Stabilizer end link nuts front | 2-4 | link | 275 (210 upper on 00-C) | V |
| 27 | Ankle catcher (subframe bracket) | 2 | front subframe | 4 bolts @110 | V |
| 28 | Subframe - Front (AWD) | 1 | front | 8 main bolts 215-220 | V |
| 29 | Subframe bolt 24 mm @220 | 2 | subframe | 220 | V |
| 30 | Subframe bolt 21 mm @220 | 2 | subframe | 220 | V |
| 31 | Subframe bolts with stud 24 mm | 4 | rear of subframe | 215 | V |
| 32 | Fore crossmember (CFM) | 1 | front | 2 bolts @90 18 mm | V |
| 33 | CFM upper/lower fasteners | 4 | CFM | 10 each | V |
| 34 | Front drive unit gearcase mount fasteners | 2 | FDU | 110 | V |
| 35 | Front aero shield (Aeroshield - Front) | 1 | under front | n/a | V (named) |
| 36 | Lower control arm shield (front) | 2 | LCA | 3 bolts each @7 | V |
| 37 | LCA shield bolts front | 6 | LCA | 7 | V |
| 38 | Front ride height sensor | 2 (LH SM; RH I) | UCA | nut @50 | V |
| 39 | Ride height sensor linkage/ball stud | 2 | UCA | n/a | V |
| 40 | Front tie rod, outer end | 2 | knuckle | nut 170; jam nut 90 | V |
| 41 | Front tie rod, inner | 2 | rack | 105, 38 mm crowfoot | V |
| 42 | Front tie rod ball joint boots | 4 | rods | n/a | I |
| 43 | Steering Actuator - Front (rack + motors) | 1 | front subframe | 2 bolts @175 | V |
| 44 | Front rack harness connectors | 4 | actuator | locks | V |
| 45 | Front rack mount bolts | 2 | subframe | 175 (18/19/21 mm) | V |
| 46 | Front steer motor(s), ECUs, position sensors | n/q | rack housing | n/a | R (redundancy, [Basenor](https://www.basenor.com/blogs/news/how-cybertrucks-steer-by-wire-and-rear-steering-work)) |
| 47 | Control Arm - Upper - Rear | 2 | rear | 4 @350, knuckle nut 150 | V |
| 48 | Control Arm - Lower - Rear | 2 | rear | 4 @185 | V |
| 49 | Rear UCA/LCA inboard bushings | 8 | rear | n/a | I |
| 50 | Rear knuckle | 2 | rear | n/a | V |
| 51 | Rear upper ball joint assembly | 2 | knuckle | nut 150 | V (separate SM item) |
| 52 | Rear lower ball joint assembly | 2 | knuckle | n/a | V |
| 53 | Hub and bearing, rear | 2 | rear | 4 bolts @105 | V |
| 54 | Rear hub shield | 2 | hub | n/a | V |
| 55 | Rear hub bolts | 8 | hub | 105 | V |
| 56 | Rear halfshaft | 2 | rear | bolt 300 | V |
| 57 | Rear halfshaft bolt | 2 | hub | 300 | V |
| 58 | Rear CV joints/boots | 8 | axle | n/a | I |
| 59 | Module - Air Spring - Rear | 2 | rear | 3 nuts @70; 2 @140 | V |
| 60 | Rear module top nuts | 6 | body | 70 | V |
| 61 | Rear module lower nuts | 4 | LCA | 140 | V |
| 62 | Rear module air line fitting (VOSS) | 2 | module | nut 2 | V |
| 63 | Rear module electrical connectors | 4 | module | 2 each | V |
| 64 | Rear module harness clips | 4 | module | 2 each | V |
| 65 | Rear adaptive damper | 2 | module | n/a | I |
| 66 | Rear bump stop/jounce | 2 | module | n/a | I |
| 67 | Front bump stop/jounce | 2 | module | n/a | I |
| 68 | Rear Coil Spring Assembly (LR) | 2 | coil variant | n/a | V (index) |
| 69 | Stabilizer Bar - Rear | 1 | rear | n/a | V (index) |
| 70 | Link - Stabilizer Bar - Rear | 2 | rear | n/a | V (index) |
| 71 | Rear stabilizer bar bushings/brackets | 4 | rear | n/a | I |
| 72 | Rear Subframe (Dual/Tri motor) | 1 | rear | not read | V (name) |
| 73 | Rear subframe bolts | n/q | rear | not read | I |
| 74 | Rear steering actuator (Steering Gear - Rear) | 1 | rear subframe | 4 @120 | V |
| 75 | Rear actuator mount bolts | 4 | subframe | 120 | V |
| 76 | Toe Link - Rear (LH/RH) | 2 | actuator-knuckle | 180 / 170 | V |
| 77 | Toe link actuator-end bolt | 2 | actuator | 180, 18 mm | V |
| 78 | Toe link knuckle nut | 2 | knuckle | 170, new | V |
| 79 | Toe link ball joint | 2 | toe link | n/a | V ("counter-hold ball joint") |
| 80 | Rear steer connector + jumper harness | 1 | actuator | n/a | V |
| 81 | Rear steer motors/ECUs/sensors | n/q | actuator | n/a | R |
| 82 | Rear ride height sensor | 2 (LH SM) | rear | n/a | V |
| 83 | Compressor - Air Suspension | 1 | rear underhood/bed floor area | see CMP | V |
| 84 | Compressor carrier bracket | 1 | body | 3 nuts @12 | V |
| 85 | Carrier bracket bolts | 3 | compressor | 5.5 T30 | V |
| 86 | Compressor air line fitting | 1 | compressor | 3 | V |
| 87 | Compressor mount fastener | n/q | compressor | 4 | V |
| 88 | Compressor connectors | 3 | compressor | n/a | V |
| 89 | Compressor clips | 4 | compressor | n/a | V |
| 90 | Air compressor exhaust assembly | 1 | compressor | push-collar | V |
| 91 | Reservoir - Air Suspension (pressurize pack) | 1 | body | 2 nuts @33 | V |
| 92 | Reservoir nuts | 2 | body | 33 | V |
| 93 | Pressurize Pack valve block | 1 | reservoir | bolt @5 | V |
| 94 | Pressurize pack bolt | 1 | reservoir | 5 | V |
| 95 | Valve Block - Air Suspension | 1 | rear | 3 grommets | V |
| 96 | Valve block grommets | 3 | bracket | n/a | V |
| 97 | Valve block bracket | 1 | body | n/a | V |
| 98 | SCUBA valve block assembly | 1 | ? | not read | V (name) |
| 99 | Air line bundle LH / RH / Rear | 3 | body | n/a | V (index) |
| 100 | VOSS fittings (air system) | about 15+ | various | 2-8 Nm | V |
| 101 | Airline inlet to valve block | 1 | valve block | 4 | V |
| 102 | Fill port | 1 | body | n/a | V (name) |
| 103 | Fir-tree clips (reservoir) | 2 | reservoir | n/a | V |
| 104 | Cable tie (reservoir bundle) | 1 | reservoir | n/a | V |
| 105 | Brake caliper front (4-piston fixed) | 2 | front | 2 bolts @315 | V |
| 106 | Front caliper pistons | 8 | calipers | n/a | V (4 per caliper) |
| 107 | Front caliper bolts | 4 | knuckle | 315, 24 mm | V |
| 108 | Front caliper boot kit | 2 | caliper | n/a | V (name) |
| 109 | Front caliper spring kit | 2 | caliper | n/a | V (name) |
| 110 | Front bleed screw kit | 2 | caliper | n/a | V (name) |
| 111 | Front pad kit (set) | 2 | caliper | n/a | V |
| 112 | Front brake pad (10 mm new, 3 mm limit) | 4 | caliper | n/a | V |
| 113 | Front pad shims/anti-rattle clips | 4+ | caliper | n/a | I |
| 114 | Front brake hose | 2 | knuckle-caliper | banjo 42 | V |
| 115 | Front hose bracket bolt | 2 | knuckle | 10 | V |
| 116 | Front rotor 351 mm | 2 | hub | none | V |
| 117 | Front brake shield | 2 | knuckle | n/a | V (name) |
| 118 | Rear caliper (1-piston floating, EPB) | 2 | rear | 2 bolts @150 | V |
| 119 | Rear caliper bolts | 4 | knuckle | 150 | V |
| 120 | Rear slider/bracket bolt | 2 | caliper | 40, 14 mm | V |
| 121 | Rear banjo bolt | 2 | caliper | 42 | V |
| 122 | Rear pad (11 mm new, 2 mm limit) | 4 | caliper | n/a | V |
| 123 | Rear pad return springs | 4 | caliper | n/a | V |
| 124 | Rear caliper boot | 2 | caliper | n/a | V (name) |
| 125 | Rear bleed screw | 2 | caliper | n/a | V |
| 126 | Rear caliper EPB motor/connector | 2 | caliper | lock | V (connector) |
| 127 | Rear brake hose | 2 | UCA-caliper | UCA bolt @10 | V |
| 128 | Rear hose-to-UCA clip bolt | 2 | UCA | 10 | V |
| 129 | Rear rotor 356 mm | 2 | hub | none | V |
| 130 | Rear brake shield | 2 | knuckle | n/a | V (name) |
| 131 | Brake pipe assembly front | 1 | body | n/a | V (name) |
| 132 | Brake tube pipe assembly LH | 1 | body | n/a | V (name) |
| 133 | HCU brake pipe assembly | 1 | HCU | n/a | V (name) |
| 134 | Hydraulic Control Unit (HCU) | 1 | frunk/bulkhead (I) | n/a | V (name) |
| 135 | HCU bracket assembly | 1 | HCU | n/a | V |
| 136 | Electromechanical brake booster assy | 1 | bulkhead | n/a | V (name) |
| 137 | Remote reservoir | 1 | frunk | 8 Nm bolt to megabeam (front module page) | V (name); torque likely this item (I) |
| 138 | Remote reservoir tube | 1 | booster | n/a | V (name) |
| 139 | Brake pedal / support bracket | 1 | cabin | n/a | V (name) |
| 140 | Wheel speed sensor (front) | 2 | knuckle | no fastener listed | V |
| 141 | Wheel speed sensor (rear) | 2 | rear knuckle | 8 T30 | V |
| 142 | Parking brake (integrated EPB in rear calipers) | 2 | rear | n/a | V |
| 143 | Steering feedback actuator | 1 | column | 3x20; 2x7 set screws | V |
| 144 | Steering column assembly | 1 | cabin | 4 nuts @18 | V |
| 145 | Steering Column Control Module (SCCM) | 1 | column | n/a | V (name) |
| 146 | Steering wheel (yoke) with switches | 1 | cabin | n/a | V (names: switch bezel, heated PUR) |
| 147 | Driver airbag | 1 | wheel | n/a | V |
| 148 | Upper/lower column shrouds + clip | 3 | column | n/a | V |
| 149 | SBW jumper harness / steering wheel harness | 2 | column | n/a | V |
| 150 | Wheel 20x9.0J ET58.5 | 4 | corners | 6 lugs | V |
| 151 | Wheel 18x9.0J ET58.5 (LR) | 4 | corners | 6 lugs | V |
| 152 | Steel wheel (LR) | 4 | corners | n/a | V (name) |
| 153 | Wheel lug nuts 21 mm hex | 24 | wheels | 205 | V |
| 154 | Wheel studs (6 per hub) | 24 | hubs | n/a | I (studs; thread M14x1.5 per [Unplugged](https://unpluggedperformance.com/cybertruck/wheel-and-tire-guide/) R) |
| 155 | Wheel cover (aero) with mounting ring | 4 | wheels | clip-retained | V |
| 156 | Wheel center cap (LR) | 4 | wheels | n/a | V (name) |
| 157 | TPMS sensor | 4 | wheels | about 8 Nm nut (Model Y manual, not Cybertruck) | V (name) |
| 158 | Tire 285/65R20 Pirelli ATR | 4 | wheels | n/a | V |
| 159 | Tire valve stem | 4 | wheels | n/a | I |
| 160 | Balance weights | 4 sets | wheels | n/a | I |
| 161 | Spare tire | 0 | not standard | n/a | see below |

### Inferences
- LR / base trim has coil springs, steel wheels (SM names "Steel Wheel (Long Range)") and non-driven front hubs ("Non-Driven Hub - Front - LH (Long Range)"), suggesting RWD LR uses a front hub without halfshaft; the Cyberbeast has driven hubs and air suspension. Items 9, 22, 68, 152 are trim-specific.
- Torque patterns suggest ball joints are riveted/pressed into arms rather than service parts on the front (no front ball joint procedure), while the rear lists upper/lower ball joint assemblies as serviceable.
- Compressor, valve block and reservoir lie rearward: procedures require removing the rear underhood apron and bed floor.

### Gaps
- No material, mass or dimension for any individual arm, knuckle, spring, subframe or bushing.
- Bushing, bump stop, top-mount and damper details are not in the SM pages read.
- Rear subframe, rear stabilizer, rear knuckle, HCU, booster, front pad kit, parking brake pages were not read (403 or not fetched).
- Part numbers: none found.

---

## Q2. What do teardowns and engineering interviews say about geometry and construction?

### Takeaway
Primary coverage is thin. Munro & Associates comments (via secondary summary) say the suspension air cylinder is the largest seen on a consumer pickup and the lower arms look longer than other Teslas. Steer-by-wire facts come from Tesla's own posts as relayed by a third-party shop blog; numeric angles are inconsistent across sources.

### Cited Findings
- Munro noted a very large air spring cylinder and long lower arms (secondary summary) — [Lean Design / Munro news](https://leandesign.com/2024/03/14); summarized in search output, original not read. R
- Adaptive air suspension is on AWD and Cyberbeast variants — [Owner's Manual](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-52FD0453-C200-4757-AC74-8D9BC4F00937.html) (search-snippet only; page 403). R
- 12 inches total suspension travel, Entry 2.2 in below Medium, Extract Mode 17.4 in ground clearance — [Basenor](https://www.basenor.com/blogs/news/cybertrucks-adaptive-air-suspension-explained-in-6-points) R. A dealer listing also cites 12 in travel and "Bilstein adaptive dampers" — [dealer listing](https://clients.automanager.com/7c0c23dee9d84201a364705868e6a182/vehicle-details/2024-tesla-cybertruck-cyberbeast-truck-be2d2bc7efde46cf840d747cd7848c74) R (weak).
- Steer-by-wire: no mechanical link to the rack, front and rear steering actuators; ratio software-variable; redundancy with triple position sensors and dual power/communication; rear steer currently 3 degrees max, reported future 10 degrees; 340 deg or 200 deg lock-to-lock claims conflict — [Basenor SBW](https://www.basenor.com/blogs/news/how-cybertrucks-steer-by-wire-and-rear-steering-work), [e-vehicleinfo](https://e-vehicleinfo.com/global/tesla-cybertrucks-steering-by-wire-and-rear-wheel-steering/). R (low confidence; Basenor's own sourcing is an X post, unnamed documents).
- Turning circle 43.5 ft cited — Basenor SBW. R
- SM confirms hardware: the rear steering is a rack-type actuator on the rear subframe with two toe links and ball joints (V, SM SAR); the front is a rack-type actuator with inner/outer tie rods, 4 connectors (V, SM SAF); the feedback actuator is a separate unit on a shortened column behind the IP (V, SM SFA).
- Wheelbase 3635 mm; track 1777 mm front, 1772 mm rear — [SM ALIGN](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-AD49F177-08D6-4B6E-BE24-4361D52F44C4.html) V.
- Front caster 3.60 deg suggests a conventional double-wishbone geometry; rear caster "not applicable" (fixed by arms) — SM ALIGN V/I.

### Inferences
- A "Megabeam" is named in the front ASM page (brake reservoir bolts to it): the front casting structure, relevant to the front body-in-white.
- Rear steering uses two toe links and thus a rear actuator centered on the subframe; "Rear steer max 3 deg" is a software limit (R).
- Cyberbeast and Long Range differences in the rear steering gear ("Long Range" vs "Standard" pages) point to different actuator variants (I).

### Gaps
- No primary-source spring travel, steering ratio, lock-to-lock, or rear steer angle; no Munro teardown video findings read; no Tesla patent review; Multimatic involvement not found.

---

## Q3. Numeric specs

### Takeaway
Brake, alignment, wheel, torque and tire numbers are strongly sourced from Tesla manuals; damper, spring rate and tread pattern figures are not.

### Cited Findings
- Brakes: four-piston fixed front calipers, single-piston floating rear; vented rotors 351 mm (13.8 in) front, 356 mm (14 in) rear; thickness new/service limit front 32/30 mm, rear 23/21 mm; pad (without backing) front 10 mm new / 3 mm limit, rear 11 mm / 2 mm; lateral runout 0.050 mm, chordal 0.040 mm, DTV 0.010 mm (front and rear) — [SM BRKSPEC](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-1D03EF6F-5DD6-4539-A664-9C784492A8E2.html) V. Same calipers/rotor diameters in [Owner's Manual specs](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html) (search snippet).
- Aftermarket 6-piston front kit exists; rear caliper retained due to EPB — [T Sportline](https://tsportline.com/collections/tesla-cybertruck-cyberbeast-performance-upgrades/products/tesla-cybertruck-big-brake-caliper-rotor-kit-two-piece-high-performance-slotted-cross-drilled-brake-rotors) R.
- Alignment, air suspension (Cyberbeast/AWD), as of 2026-08-19: camber front -0.50 +/-0.45 deg, rear -1.00 +/-1.00; camber split +/-0.60 front, +/-0.80 rear; caster front 3.60 +/-1.00 deg (split +/-1.0), rear n/a; individual toe front out 0.05, rear in 0.20; toe limits front +/-0.10, rear +/-0.05; toe split +/-0.10 both; thrust angle +/-0.25; handwheel clear vision +/-0.5; wheelbase 3635 mm; track width 1777 / 1772 mm — [SM ALIGN](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-AD49F177-08D6-4B6E-BE24-4361D52F44C4.html) V. (An earlier search snippet of the same page showed camber -0.70 front and toe limits +/-0.15: the page appears to have been revised; use the 2026-08-19 values.)
- Coil suspension: camber front -0.37 +/-0.45, rear -0.95 +/-1.00; caster 3.45 +/-1.00; toe front out 0.04, rear in 0.19; limits +/-0.15 — SM ALIGN V.
- Ride height (chassis, mid-laden, Medium): air 265 +/-5 mm (250 with Terrestrial Armor); coil, 18 in: 264/262 mm (249/247 with Armor), 20 in: 274/272 (259/257) — SM ALIGN V (front/rear assignment is presumed).
- Rear ride-height reference for service: 31.8 cm (wheel housing stud to stabar link mount) — SM SAR V.
- Wheels: 20x9.0J ET58.5; 18x9.0J ET58.5; lug torque 205 Nm / 151 lb-ft; 21 mm socket — OMWT V. Bolt pattern 6x139.7, center bore 84 mm, stud thread M14x1.5, 35.2 lb wheel (39.6 lb with cover, about 4 lb cover) — [Unplugged Performance](https://unpluggedperformance.com/cybertruck/wheel-and-tire-guide/) R. A conflicting EVANNEX listing gives 6x139.5 / 84.15 mm — [EVANNEX](https://evannex.com/products/20-cyber-t-satin-black-for-tesla-cyber-truck-owners-set-of-4) R (likely typo).
- Tire Pirelli Scorpion ATR 285/65R20 116H XL: tread depth 12/32 in [TireSize](https://tiresize.com/tires/Pirelli/Scorpion-ATR-285-65R20.htm) vs 10/32 in [Discount Tire](https://www.discounttire.com/buy-tires/pirelli-scorpion-atr/p/180908) (conflict); weight 45 lb (TireSize) / about 46.3 lb (Discount Tire); max load 2756-2760 lb; max pressure 50-51 psi; rim range 8-10 in; speed rating H (130 mph) R.
- Tire pressure: 50 psi normal for all-season and all-terrain tires; 65 psi for loaded all-terrain to GVWR — [Owner's Manual tire pressures](https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-B3DD905E-4642-4B5C-9149-480CA2C4F177.html) (via search summary) V/R. TPMS relearn after driving >15 mph for a period.
- Spare: the OM has an "Installing a Spare Tire" page ([OM](https://www.tesla.cn/ownersmanual/cybertruck/en_ae/GUID-C482029E-58E5-47A8-A748-8265A502A57C.html)) but no factory spare is standard (I; not verified).
- Steering: lock-to-lock 200 or 340 deg and ratio 5:1 to 12:1; rear steer 3 deg: all R (Basenor), conflicting.

### Inferences
- Tire outer diameter for 285/65R20 is about 34.1 in (computed: 20 in + 2 x 0.65 x 285 mm = 508 + 370.5 = 878.5 mm); this is arithmetic, not sourced.
- Rotor mass-per-axle and hat design cannot be derived; rear pad is 11 mm vs front 10 mm.
- Tread pattern: no source gives rows, pitch counts or groove depth beyond 10-12/32; modelling must use photographs/visual references.

### Gaps
- Caliper piston diameters, rotor weights, hub bolt circle for rotor, spring rates, damper stroke, steering rack ratio (mm/rev), steer angle at the wheel, curb weights per axle, wheel offset to hub-face geometry, and ball joint dimensions: none found.
- Brake fluid grade for Cybertruck not found (Roadster page says DOT 4, different vehicle).
- Tesla Owner's Manual spec page and Pirelli product page not accessible.

---

## Q4. Small parts likely missing in a "complete" model

### Takeaway
Based on SM-listed items, a "complete" chassis model should include the following, all of which are named in Tesla's own procedures (V) unless marked I.

### Cited Findings
- Fasteners/clips named in SM: LCA shield bolts (3 per side, 7 Nm), rear wheel liner 19 push clips + 5 push nuts per side, rear underhood apron 9 clips, front module cover 4 clips, harness clips (2 per module, 2 on front knuckle, 2 on rear wheel speed sensor), 2 fir-tree clips and 1 cable tie at the reservoir, 3 valve-block grommets, nylon-lock or cinch nuts on rear module flange (SM ASMR) V.
- Ride-height sensor ball stud and mount nut (SM UCAF) V; hub shield with orientation insert (SM HUBR) V; caliper pad springs (rear, 2) (SM CAL_R) V; spring kit and boot kit for front caliper, bleed screws (SM index) V.
- Sensors: wheel speed (4), ride height (4 expected), TPMS (4), SCCM position sensors, steering wheel switches (SM index).
- Harnesses: chassis corner harness connector at rear caliper (SM HUBR), SBW jumper, rear steer jumper, EPB connectors.

### Inferences
- Likely also required for completeness (not sourced): bushing sleeves, jounce bumpers, spring seats, dust boots, lock-wire/cotter hardware for tie rod nuts, brake line clips and P-clips on the body, grease zerks (none expected on sealed ball joints), balance weights, valve stems, hub-centric rings (none), caliper slider pins and boots, rotor hat spacers, TPMS nuts, and wheel-well splash guards (fender flares, wheel liners are named in SM UCAR).

### Gaps
- No exploded diagrams or part catalogue access; Tesla's EPC is behind login.

---

### Sources not cited above but consulted
- [Cybertruck SM index](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html); [Tesla Owner's Manual root](https://www.tesla.com/ownersmanual/cybertruck/en_us)
