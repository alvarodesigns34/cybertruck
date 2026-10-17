# Cybertruck (US, 2024-2026, Cyberbeast focus): electrical/electronic architecture, 48 V low-voltage system, sensors and connectivity

Method note: ~14 tool calls. The Tesla Service Manual TOC (index page) was readable; individual procedure pages, the Owner's Manual on tesla.com (403) and several press sites (designnews, tesla.com/powershare) were NOT readable. Confidence tags: Verified = primary Tesla source or direct Tesla-engineer statement read in this session; Reported = secondary press; Inferred = my deduction.

Primary URLs:
- Service Manual TOC: https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-2390C88D-E2A0-4DDB-814D-C03532250D36.html
- Owner's Manual cameras: https://www.tesla.com/ownersmanual/cybertruck/en_us/GUID-60A2EFBA-78D7-47BB-BCDE-77582529EB48.html (mirror read: https://tesla.cn/ownersmanual/cybertruck/en_us/GUID-60A2EFBA-78D7-47BB-BCDE-77582529EB48.html)

## 1. 48 V ("mid-voltage") low-voltage system, DC-DC, battery, distribution

### Takeaway
Cybertruck is the only Tesla passenger EV with a 48 V low-voltage system (no 12 V main battery). Tesla's service manual calls it "mid voltage / MV". Battery is a small lithium-ion unit reported at 4 Ah (~192 Wh). Zonal controllers step 48 V down to 12 V locally where legacy loads need it.

### Cited Findings
- Service manual lists "Battery - Mid-Voltage" (remove/install, remove/replace, "Recover"), "Maintainer - Mid-Voltage (Connect and Disconnect)", "MV Backbone harness", "MV locking cover circlip", and an "MV controller (rear, long range)". [Verified] — [Service Manual TOC](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-2390C88D-E2A0-4DDB-814D-C03532250D36.html)
- A service procedure states Cybertruck electronics are powered by a 48 V "mid voltage (MV)" architecture requiring extra care; also references testing "Super Connectors" on the Cybertruck "Vehicle Controller". [Reported via search snippet] — [Service Manual page](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-FC568245-9843-4397-B8F6-27B26C6FB3C7.html)
- Only explicitly 48 V-labelled part in TOC: "Window Regulator, 48V Q-Motor". [Verified] — Service Manual TOC (above)
- 48 V lithium-ion low-voltage battery rated 4 Ah (~192 Wh). [Reported] — [InsideEVs](https://insideevs.com/news/704749/tesla-cybertruck-low-voltage-battery-48v-4ah/) (page itself returned 502; figure from search snippet). Chemistry/cell count: not found.
- Two 48 V accessory feeds (roof and frunk), each up to 400 W per owner's manual (as reported). [Reported] — InsideEVs link above
- Tesla engineers (Pete Bannon, dir. low-voltage electronics; Lars Moravy, VP vehicle engineering) on Munro interview: a switched-tank converter detects 12 V vs 48 V source, boosts 12 V to 48 V or passes 48 V directly (jump-start behaviour); accessory motors (windows, wipers) redesigned for 48 V; much LV electronics needs no heatsinks; main controller board connectors have no plastic housing (pins soldered on PCB, mating plastic half in controller housing). [Reported, direct engineer quotes] — [Autopian](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/)
- Reason for 48 V: existing lines were 12 V (Model Y stayed 12 V); new tooling had to be bought anyway. 4x voltage = 1/4 current = 1/16 heat. — Autopian (above)
- Not a full 48 V car: 48 V runs through the vehicle and zones step down to 12 V. [Reported] — [Autoline](https://www.autoline.tv/?p=91080)
- 48 V connectors are blue; 48 V wires marked with blue tape. [Reported] — [Basenor](https://www.basenor.com/blogs/news/cybertrucks-engineering-firsts-48v-steer-by-wire-explained)
- Steer-by-wire: triple-redundant position sensors; dual-redundant power supplies, converters, controllers, buses; critical signals on dual-redundant 48 V Ethernet loop; 340 deg lock-to-lock; rear wheels up to 10 deg. [Reported] — Basenor (above)
- Fuses named in manual: Eaton EVK22-60-T 60 A/1000 VDC (ancillary, HV), Littelfuse 828-30, PCS fuses (standard/long range). These are HV-side. [Verified] — Service Manual TOC

### Inferences
- Rear "MV controller (long range)" suggests a dedicated MV power-distribution/DC-DC controller in the rear of the vehicle (Inferred); a separate front/ancillary DC-DC is likely inside the Power Conversion System (PCS), which the TOC lists under HV components (Inferred; the PCS typically contains HV-to-LV DC-DC).
- Standalone relays and a fuse box list were not found: Tesla zonal design likely uses solid-state (eFuse) protection in body controllers (Inferred; "digital breaker" for 400 W feed reported by owners).

### Gaps
- DC-DC converter rating/count, 48 V battery chemistry, exact location, voltage window, and fuse/eFuse list: not found.
- Munro's DesignCon 2025 48 V session content (designnews.com returned 403).

## 2. Zonal controllers, central computers, Ethernet ring

### Takeaway
Three Body Controllers (LH, RH, Rear) act as zone controllers, with front/rear door controllers, plus a car computer (MCU/Autopilot in one unit as far as the manual indicates), TCU, and many feature ECUs, linked by a managed Gigabit Ethernet "etherloop".

### Cited Findings
- Service manual controllers: Body Controller LH / RH / Rear; Door Controller front and rear LH (RH presumably mirrored); MV controller (rear, long range); Trailer ECU; Supermanifold controller; USB controller (center console) with USB hub (rear of console); Restraint Control Module; Device Cluster assembly (std/LR variants); Steering Column Control Module; Telematics Control Unit (TCU) with bracket; Charge Port Controller (Gen 4); "Car Computer"; "Gateway (Unlock)". [Verified] — Service Manual TOC
- Gigabit Ethernet loop connects all high-speed controllers; bidirectional for redundancy; managed/time-sliced (compared to Token Ring); halves communication wiring mass; audio distributed over it. [Reported, engineer quotes] — Autopian
- Wire count 155 (Cybertruck) vs 490 (Model 3); endpoints 368 vs 273 (+50%); etherloop credited with 68% reduction in wiring; high-power harness mass down 84%. Door example: one door controller runs locking, lighting, audio. Tesla patent describes backbone with sheath, two conductors, insulating members, shield. [Reported] — [Assembly Magazine](https://assemblymag.com/articles/98504-teslas-new-cybertruck-features-modular-wiring)
- Munro describes zonal E/E; its report covers Autopilot, MCU/Gateway, Telematics, Body, Trailer, Door ECUs. [Reported] — [MarkLines](https://www.marklines.com/en/teardown/munro-tesla-cybertruck?rf=prtimes), [Munro prospectus PDF](https://leandesign.com/wp-content/uploads/2024/11/Munro-2024-Cybertruck-Report-Prospectus-Oct-2024.pdf)
- Ethernet diagnostic RJ45 module in instrument panel. [Verified] — Service Manual TOC
- Harness items in TOC: MV backbone, ancillary, LV device cluster, steering jumper, rear subframe (dual/tri motor), seat, door, fascia, windshield, LH/RH frunk harnesses, tailgate harness, cowl speaker harness, shunt jumper harness, ferrite core (device cluster); coax cables for side repeater, front LH/RH, jumper. [Verified] — Service Manual TOC

### Inferences
- Tri-motor (Cyberbeast) has its own rear subframe harness variant ("dual and tri motor") (Verified listing; applicability to Cyberbeast Inferred).
- Ethernet-ring nodes likely = three body controllers, car computer, TCU, MV controller, steering/brake controllers (Inferred).

### Gaps
- Absolute harness lengths/weights (no source gives meters or kg), supplier names (Aptiv/Yazaki/Samsung etc.: none found), computer SoC specs for the Cybertruck unit, exact node list of the loop.

## 3. Cameras, radar, ultrasonics

### Takeaway
Owner's manual lists cameras: tailgate (rear) 1, door pillars 1 each (2), windshield 2 (above mirror), front wheels/fender flares 1 each (2), front bumper/fascia 1, plus cabin camera 1 = 9 total. No ultrasonic sensors listed; a cabin radar exists.

### Cited Findings
- Camera locations: tailgate, each door pillar, two on windshield above mirror, above each front wheel, front bumper above grille (with sprayer nozzle); cabin camera above mirror. [Verified] — [Owner's Manual (cn mirror)](https://tesla.cn/ownersmanual/cybertruck/en_us/GUID-60A2EFBA-78D7-47BB-BCDE-77582529EB48.html)
- Service manual items: "Bi-Cam - Forward Facing", "Camera - B-Pillar - LH", "Camera - Fender Flare - LH", "Camera - Forward Facing - Front Fascia", "Camera - Rear", "Fan - Camera - Windshield", "Interior Camera", "Cover - Camera - Lower - Fascia - Front", "Radar - Cabin". [Verified] — Service Manual TOC
- Cabin radar (occupant/child presence) exists as "Radar - Cabin". [Verified listing; function Inferred]
- HW4-generation cameras reported 2880x1876 max, up to 45 fps (firmware analysis, Model 3/Y 2-SoC; Cybertruck-specific resolution unconfirmed). [Reported] — [search summary of notateslaapp/Hacker Green](https://www.notateslaapp.com/news/1298/cc593c6f-ff77-4eb7-b604-d3c0f7cbf2d9)
- Bumper camera tied to removal of ultrasonic sensors (speculation). [Reported/speculative] — [notateslaapp](https://www.notateslaapp.com/news/1238/un)
- Samsung reported as HW4 chip maker (2021 reports); Samsung/high-res cameras. [Reported, dated] — [Teslarati](https://teslarati.com/tesla-cybertruck-hw4-supplier-secured), [CleanTechnica](https://cleantechnica.com/2021/10/10/samsung-will-play-a-key-role-as-tesla-cybertruck-comes-to-market/)

### Inferences
- Front: "Bi-Cam" = two-camera windshield module (Verified listing) so no triple-camera cluster, contrary to the brief's "windshield triple cameras".
- No ultrasonic or forward radar in the manual's camera section or TOC (Inferred from absence; "no ultrasonics" is not explicitly stated by Tesla in sources read).

### Gaps
- Pixel counts per camera, the 'Phoenix' forward radar status on Cybertruck (conflicting rumor, not confirmed), supplier of camera modules, computer module details.

## 4. Antennas, connectivity, audio, sensors, small switches

### Takeaway
Service manual shows GPS, Wi-Fi, AM/FM/HD, satellite radio antennas, many BLE end points (phone key), TCU, telephony microphone, multiple speakers, super horn and pedestrian warning speaker. TPMS sensors per wheel.

### Cited Findings (all Verified listings, Service Manual TOC unless noted)
- Antenna - GPS; Antenna - Wi-Fi; Antenna - AM/FM/HD; Antenna - Satellite Radio; "Antennas and Amplifiers".
- BLE end points: Front/Rear, Interior, Rear, Wheel Well front LH/RH, Wheel Well rear LH/RH.
- Telephony Microphone - LH; Speaker (Full Range) LH; Rear header speaker LH; Speaker - Super Horn; Pedestrian Warning Speaker; Horn - Low Tone - LH.
- Windshield wiper motor, arms, blades; no rain sensor listed (Inferred: vision-based auto wipers).
- Exterior door switches at B-pillar (front) and C-pillar (rear); interior and exterior door handles sections; frunk switch, safety lock switch, frunk lamp; tonneau motor assembly (LH), rails, slats, lower assembly; tailgate cinching latch, manual release, tailgate harness; bed outlet door.
- Seat track position sensor (driver); Restraint Control Module; airbags: driver, front passenger, driver curtain, driver knee, passenger knee.
- Key Card programming (with/without existing key). Steering column control module. Front lightbar, headlamp assemblies. TPMS sensor per wheel. Charge Port Controller (Gen 4), charge port door, charge port busbar and HV header doubler.
- Cybertruck LTE: inside TCU (Inferred); UWB: not listed anywhere found.

### Gaps
- Humidity sensor, occupant-classification sensors, lighting-controller part names, FCC IDs, antenna counts/positions: not found.

## 5. Powershare, outlets, V2L

### Takeaway
AWD/Cyberbeast: 5 onboard outlets, 9.6 kW combined; home backup up to 11.5 kW (11.52 kW at 240 V) with Universal Wall Connector and Gateway.

### Cited Findings
- 2 x 120 V/20 A (cabin), 2 x 120 V/20 A (bed), 1 x 240 V/40 A (bed, NEMA 14-50); 9.6 kW continuous combined; bidirectional charge port 120 V/20 A up to 2.4 kW; RWD has no onboard outlets. [Reported, consistent with Tesla search snippets] — [Basenor](https://www.basenor.com/blogs/news/cybertruck-powershare-explained-every-outlet-and-what-it-can-do), [Tesla Powershare](https://www.tesla.com/powershare) (403 on fetch; snippet only)
- Home backup 11.5 kW continuous. [Reported] — Basenor; [Tesla](https://www.tesla.com/en_pr/support/powershare)
- 48 V 400 W accessory feeds on roof and frunk. [Reported] — InsideEVs
- AC outlets power electronics: the onboard inverter is the Power Conversion System (PCS) with AC Junction Box (ACJB) in the HV battery electrical components. [Verified listing; function Inferred] — Service Manual TOC

### Gaps
- PCS/ACJB specs and supplier, outlet module part names.

## 6. Itemized part list (condensed; confidence per line)

| # | Item | Qty | Location | Confidence |
|---|---|---|---|---|
| 1 | MV (48 V) battery | 1 | not found | Verified (exists), 4 Ah Reported |
| 2 | MV maintainer connection | 1 | n/a | Verified |
| 3 | MV controller (LR) | 1 | rear | Verified |
| 4 | MV backbone harness | 1 | vehicle | Verified |
| 5-7 | Body Controller LH / RH / Rear | 3 | zones | Verified |
| 8-9 | Door controllers front/rear (per side) | 4 (RH Inferred) | doors | Verified LH |
| 10 | Car Computer (MCU/FSD) | 1 | IP | Verified name |
| 11 | Gateway | 1 | n/a | Verified |
| 12 | TCU + bracket | 1 | n/a | Verified |
| 13 | Restraint Control Module | 1 | n/a | Verified |
| 14 | Device cluster | 1 | n/a | Verified |
| 15 | Steering column control module | 1 | column | Verified |
| 16 | Steering actuators front/rear, feedback actuator | 3 | steering | Verified |
| 17 | Trailer ECU | 1 | rear | Verified |
| 18 | Supermanifold controller | 1 | thermal | Verified |
| 19 | USB controller + USB hub | 1+1 | console | Verified |
| 20 | Charge port controller (Gen 4) | 1 | charge port | Verified |
| 21 | Ethernet RJ45 diagnostic module | 1 | IP | Verified |
| 22-30 | Cameras: bi-cam windshield (2), B-pillar (2), fender flare (2), rear (1), fascia (1), cabin (1) | 9 | see sect. 3 | Verified |
| 31 | Cabin radar | 1 | cabin | Verified |
| 32 | Windshield camera fan | 1 | windshield | Verified |
| 33-36 | Antennas GPS, Wi-Fi, AM/FM/HD, satellite | 4 | n/a | Verified |
| 37-44 | BLE end points (front/rear, interior, rear, 4 wheel wells) | ~8 | see list | Verified |
| 45 | Telephony microphone | 1+ | LH | Verified |
| 46-49 | Speakers: full range, rear header, super horn, pedestrian warning | multiple | n/a | Verified |
| 50 | Low tone horn | 1+ | LH | Verified |
| 51 | Wiper motor | 1 | windshield | Verified |
| 52-53 | B/C-pillar exterior door switches | per door | pillars | Verified |
| 54 | Frunk switch, safety lock switch, lamp | 3 | frunk | Verified |
| 55 | Tonneau motor(s) | LH (RH Inferred) | bed | Verified |
| 56 | Tailgate cinching latches, harness | LH ... | tailgate | Verified |
| 57 | Bed outlet door | 1 | bed | Verified |
| 58 | Seat track position sensor (driver) | 1 | seat | Verified |
| 59-63 | Airbags (5 listed) | 5 | see sect. 4 | Verified |
| 64 | Key card | 1+ | n/a | Verified |
| 65 | TPMS sensors | 4 | wheels | Verified |
| 66 | PCS (inverter/charger/DC-DC) + ACJB | 1+1 | ancillary bay | Verified listing |
| 67 | Fuses Eaton EVK22-60-T, Littelfuse 828-30 | n/a | ancillary | Verified |
| 68 | Window regulator 48V Q-Motor | per door | doors | Verified |
| 69 | Outlets 120 V (4) + 240 V (1) | 5 | cabin/bed | Reported |
| 70 | 48 V accessory feeds (roof, frunk) | 2 | roof/frunk | Reported |
| 71 | Coax cables (side repeater, front LH/RH, jumper) | several | n/a | Verified |
| 72 | Ferrite core, shunt jumper harness | 1+1 | device cluster | Verified |
| 73 | Headlamps, front lightbar | 2+1 | front | Verified |

This list has ~73 line items (roughly 100+ physical parts when quantities are expanded); the 120+ target was not reached because procedure pages were unreadable.

## 7. Small parts likely missing in a basic model (Inferred)
Blue 48 V connectors and blue tape on wiring, ground/chassis studs, harness clips and routing clamps on MV backbone, ferrite core, coax jumpers for cameras, camera heater/fan, windshield camera cover, PCB-integrated pinless-housing controller connectors, BLE end points in wheel wells, frunk and roof 48 V feed connectors, super-manifold wiring, HV header doubler, DC inlet busbars, MV locking cover circlip, USB hub, RJ45 diagnostic module.
