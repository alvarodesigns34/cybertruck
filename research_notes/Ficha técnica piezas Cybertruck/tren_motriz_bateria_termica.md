# Cybertruck Cyberbeast: powertrain, high-voltage battery and thermal management (part-by-part research notes)

Scope note: about 15 tool calls were used. Several key sources could not be read (Tesla owner's manual spec pages returned HTTP 403 on tesla.com; the Munro/Lean Design battery page 404'd; InsideEVs battery-passport page returned 502; the service manual drive-unit and HV-battery procedures were not individually opened). The 150+ item target was NOT reached with verified data. Items below are tagged Verified (primary Tesla document), Reported (teardown or press), or Inferred. Masses, dimensions and most fastener torques for the drive units and battery are not public in what I could read; they are listed under Gaps.

## 1. Powertrain: motors, inverters, gearboxes, ratios, power and torque

### Takeaway
The Cyberbeast has three motors: one front permanent-magnet synchronous motor and two rear induction motors, all with a single-speed fixed gear at 15.02:1 per the owner's manual. Headline output is 845 hp and 10,296 lb-ft (wheel torque) per aggregator listings. Teardown detail is qualitative; no masses, per-motor kW or inverter ratings were found.

### Cited Findings
- Item PT-01, Front motor (1x, front axle): one AC permanent magnet synchronous motor, liquid-cooled, variable frequency drive. Confidence: Verified — [Tesla Owner's Manual (regional copy, en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html)
- PT-02, Rear motors (2x, one per rear wheel): AC induction motors, liquid-cooled, variable frequency drive. Verified — [Tesla Owner's Manual (en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html); Reported identical by Munro — [Autopian motor teardown](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-03, Transmission: single-speed fixed gear, overall ratio 15.02:1 front and rear for the Cyberbeast; reverse limited to 15 mph (24 km/h). Verified — [Tesla Owner's Manual (en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html)
- PT-04, Conflict: the same manual table lists the Premium AWD rear gear ratio as "2" with independent gearsets at 15.02:1, which looks like a typo; and its front/rear motor types for Premium AWD are listed as front induction, rear PM, which is the reverse of what other coverage describes for the dual-motor truck. Flag: unresolved — [Tesla Owner's Manual (en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html)
- PT-05, Long Range / RWD variant: one rear PM synchronous motor, ratio 15.02:1. Verified — [Tesla Owner's Manual (en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html)
- PT-06, Peak output: 845 hp (621 kW), 10,296 lb-ft (13,959 Nm) torque, 2.6 s 0-60 mph, 123 kWh total / 111.9 kWh usable listed. Reported (spec aggregator, not Tesla primary) — [ArenaEV Cyberbeast specs](https://www.arenaev.com/tesla_cybertruck_cyberbeast_2023-specs-57.php); 845 hp and 2.6 s also in [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-07, Front drive unit inverter: integrated, packaged at the end of the gear mechanism (Turnbull believes this keeps delicate parts out of the way in a crash). Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-08, Front PM rotor: carries magnets; laminations partly retained by an aluminum endplate that does not reach full rotor diameter, leaving magnets exposed (suspected oil cooling of magnets). Monoblock (not segmented) magnets. Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-09, Front stator: stacked hairpin coils. Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-10, Front electromagnet-actuated clutch providing a locking-differential function on the front axle. Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-11, Front gear housing: cast housing with a pin that engages a notch in large bearing outer races (prevents race spin, allows slip fit). Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-12, Rear drive unit inverters (2x): one per induction motor, packaged on the back of each motor. Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-13, Rear induction rotors (2x): no magnets; rectangular channels through rotor centre believed (unconfirmed) to be for oil cooling. Rear motors freewheel with low spin losses, so no disconnect clutch. Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-14, Rear motor shafts (2x): cold-headed. Reported — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-15, Commonality: all variants share one PM rotor/stator, one induction rotor/stator, one inverter design and one gearset; the PM motor is very similar to the Model Y Performance motor; rotor/stator smaller than Model 3's. Reported (Tesla engineers via Munro) — [Autopian Munro/Tesla interview](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/)
- PT-16, Munro estimate: front motor costs about as much as both rear motors combined (rare-earth magnets). Reported opinion — [Autopian](https://www.theautopian.com/heres-what-manufacturing-experts-found-when-they-tore-into-the-tesla-cybertrucks-motors/)
- PT-17, Curb weight conflicts: 6,669 lb (KBB), 6,843 lb (ArenaEV/early specs), 6,901 lb (Car and Driver as cited in a comparison article). Flag conflict — [KBB 2026 specs](https://www.kbb.com/tesla/cybertruck/2026/specs/); [ArenaEV](https://www.arenaev.com/tesla_cybertruck_cyberbeast_2023-specs-57.php)
- PT-18, Why two motor types: owner-forum theory that the induction motors switch off at cruise and the PM motor runs efficiently. Speculation, not official — [CybertruckOwnersClub thread](https://www.cybertruckownersclub.com/forum/threads/why-two-motor-types-in-cyberbeast.10295/post-206734)
- PT-19, Service manual references to a "front drive unit breather fitting" and HV coolant hoses routed behind the front drive unit. Verified — [Service Manual: Hose - Supply - HV Battery](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-34BAA5A1-C6A0-4463-9B21-B3BA3CA5D154.html)
- PT-20, Service procedures reference an "inverter-to-heat-exchanger hose", implying a drive-unit oil/coolant heat exchanger plumbed to the inverter loop (search snippet only). Reported — [Service Manual index result](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-FAC16ECE-F2C6-48CC-879C-666C2A9DD363.html)
- PT-21, Steer-by-wire front uses two motors; rear steering uses one motor (adjacent system, not powertrain). Reported — [Autopian Munro/Tesla interview](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/)

### Inferences
- Inferred: each of the three drive units contains an oil pump, oil-to-coolant heat exchanger, gear train (input/intermediate/output shafts), bearings, seals, half shafts with CV joints, breather and mounts; no source above gives quantities or masses. Rear units are likely a single combined housing (or two paired casings) with a shared cradle, but this is unconfirmed.
- Inferred: if the 15.02:1 ratio is the same for PM and induction units, motor-speed-to-wheel-speed scaling is identical, which fits the "one gearset" statement.
- Inferred: inverters are probably SiC-based (not confirmed anywhere in the fetched material).

### Gaps
- Per-motor kW/torque, inverter current ratings, drive-unit masses, housing materials, gear tooth counts, oil type/volume, half-shaft dimensions and mount fasteners: not found.
- Service Manual drive-unit pages (section 3xxx) were not opened; fetch via search "Cybertruck Service Manual drive unit remove install".

## 2. High-voltage battery pack

### Takeaway
Reported pack is 4680 cells, roughly 1,344 total (192S7P or alternative 224S6P), about 123 kWh, cell-to-pack with green structural foam and mica. Nominal voltage conflicts: owner's manual says 700 V DC nominal; Munro and Tesla engineers describe an 800 V architecture with a DPDT switch for 400 V charging.

### Cited Findings
- BT-01, Cells: 4680 format (46 x 80 mm nominal format), identified visually. About 48 cells long (possibly 49), four blocks, seven cells wide, roughly 1,344 total. Back-of-envelope, not verified. Reported — [Autopian pack teardown](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/)
- BT-02, 1,344 cells yielding about 123 kWh (about 91.5 Wh/cell) cited to Tesla impact report via InsideEVs search summary; 192S7P layout per Lean Design. Reported — [InsideEVs battery passport](https://insideevs.com/news/724981/tesla-cybertruck-battery-passport-4680cell/); [Lean Design](https://leandesign.com/?p=3390)
- BT-03, Alternative 224S6P from regulatory filings (same cell count). Reported/speculative — [Autopian pack teardown](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/)
- BT-04, Cell voltages: about 4.2 V full, 3.4 V empty, 3.6 V nominal; pack range about 600-900 V; called 800 V nominal. Reported — [Autopian pack teardown](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/)
- BT-05, CONFLICT on nominal voltage: owner's manual lists high voltage battery as liquid-cooled lithium-ion, 700 V DC nominal. Verified (primary) — [Tesla Owner's Manual (en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html); contradicts 800 V in [Autopian pack teardown](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/). (192 x 3.6 V = 691 V, which fits the 700 V manual figure better.)
- BT-06, Pack energy: 123 kWh total, 111.9 kWh usable (aggregator). Reported — [ArenaEV](https://www.arenaev.com/tesla_cybertruck_cyberbeast_2023-specs-57.php)
- BT-07, Architecture: cell-to-pack, no replaceable modules; cells glued with foam; replacement means replacing the pack. Reported — [Autopian pack teardown](https://www.theautopian.com/experts-teardown-a-cybertruck-and-show-how-tesla-made-it-fire-and-water-resistant/)
- BT-08, Structural foam: bright green, stiff; structural support, thermal-runaway mitigation, vibration damping. Reported — same source.
- BT-09, Mica sheet layer over the vent trough; cell bottoms push through during runaway to vent downward. Reported — same source.
- BT-10, Cooling: single coolant channel along one edge of the cell rows (Tesla may restrict flow to equalize). Reported — same source.
- BT-11, Underbody clearance beneath cells about 1.3 in (about 33 mm); empty side-impact gap (Model Y fills with foam). Reported — same source.
- BT-12, Top vent: single-use high-capacity vent; orange snap-on lid blows off, leaving a black spark-arrestor part. Plus a moisture-trapping breather vent for pressure equalization. Reported — same source.
- BT-13, Flood ports (stacked wafer discs absorb moisture, drains coolant leaks from penthouse area) and a second spring-loaded flood port on the pack side. Reported — same source.
- BT-14, Wade/Scuba mode: air-suspension compressor feeds a line that pressurizes the pack cavity. Reported — same source.
- BT-15, HV contacts widely separated and shielded by foam; welded cell links described as fragile. Reported — same source.
- BT-16, "Penthouse" section at pack top houses coolant/electrical interface (referenced through flood-port drainage). Reported — same source.
- BT-17, Pack voltage-switching: dual-pole dual-throw switch configures two blocks in series (800 V) or parallel (400 V) so Supercharger connects directly to terminals; charge port supports up to 11.5 kW bidirectional AC. Reported (Baglino quote) — [Autopian Munro/Tesla interview](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/)
- BT-18, Battery operating-storage limit: not above 65 C or below -30 C ambient for more than 24 h. Verified — [Tesla Owner's Manual (en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html)
- BT-19, Cell teardown (UCSD, second-gen "Cybercell"): thinned can, welded lid, tabless electrodes, about 30% lighter. Reported — [Notebookcheck](https://www.notebookcheck.net/First-Cybertruck-4680-battery-teardown-shows-how-Tesla-managed-to-increase-its-energy-density.875816.0.html)
- BT-20, Pack described as half empty (Wes Morrill "half full" remark); doubling capacity not proven. Reported — [InsideEVs](https://insideevs.com/news/715634/tesla-cybertruck-battery-pack-half-empty/); [Electrek](https://electrek.co/?p=357943)
- BT-21, Range extender: structurally mounted in the bed, about 11.5 kW OBC; capacity disputed (iFixit says about +50 kWh; other sources say unreleased). Cyberbeast claimed 440+ mi with extender. Reported/conflict — [iFixit](https://www.ifixit.com/Device/Tesla_Cybertruck); [Capital One](https://ane-west1.capitalone.com/cars/learn/finding-the-right-car/what-to-know-about-the-tesla-cybertrucks-range-extender/2976)

### Inferences
- Inferred: a battery pack contains tray (likely aluminum), lid/cover, perimeter seals, busbars, pyro fuse, main contactors (plus DPDT series/parallel contactors), BMS boards, cell-voltage sense harness, HV connectors (to PCS and to drive units), temperature sensors, coolant cooling ribbon/plate and a service disconnect-style interlock. None have quantities, materials or torques in the sources read.
- Inferred: 192S x 3.6 V = 691 V supports the manual's "700 V nominal" and suggests the "800 V" label refers to the architecture/max-voltage class, not nominal.
- Inferred: 1,344 cells x 4680 (about 0.133 L each) gives roughly 179 L of cell volume; mass of cells likely roughly 1,344 x about 355 g, order of 480 kg, unverified.

### Gaps
- Pack mass, outer dimensions, tray/lid materials, bolt counts and torques, busbar material/size, pyro fuse and contactor part numbers, BMS layout, HV connector specs: not found. Munro/Lean Design pack article (munrocommercial.com/?p=3390) and InsideEVs passport page were not retrievable.
- Service manual HV battery sections not opened.

## 3. Thermal management (Supermanifold, coolant, refrigerant, HVAC)

### Takeaway
The service manual confirms a Supermanifold-based architecture (Octovalve-class) with a cooling fan module, chiller, powertrain bypass and battery loops, and a "Penta" HVAC line. Coolant/refrigerant charge volumes are mostly absent; only the 15 L fill-container minimum and POE oil are documented.

### Cited Findings
- TM-01, Supermanifold: 1x, bolted to vehicle with 2 bolts (33 Nm) and to the "megabeam" with 2 bolts (33 Nm); carries a harness connector (2 electrical connectors noted). Verified — [Service Manual: Hose - Supply - HV Battery](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-34BAA5A1-C6A0-4463-9B21-B3BA3CA5D154.html)
- TM-02, Hoses on Supermanifold: battery supply, battery return, powertrain supply, chiller-to-battery (x2), powertrain bypass, radiator inlet, radiator outlet, radiator-to-manifold hose. Verified — same page and [Service Manual: Pentaport AC Lines](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-38F1B41A-55D7-497E-902D-F27700522487.html)
- TM-03, Battery coolant supply and return hose bundle: hose clips x2 and edge clips x2; routed behind front drive unit. Verified — same.
- TM-04, Cooling fan module (CFM): 1x, 4 bolts at 10 Nm, 2 electrical connectors. Verified — [Service Manual](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-34BAA5A1-C6A0-4463-9B21-B3BA3CA5D154.html)
- TM-05, Fore crossmember to front subframe: 2 bolts, 90 Nm. Verified — same.
- TM-06, Penta HVAC line assembly: nut to Supermanifold 36 Nm (13 mm); 5 seal washers on manifold side, lubricated with RB100EV POE oil. Verified — same.
- TM-07, A/C line assembly: bolt to Supermanifold 22 Nm (13 mm); bracket bolt 8 Nm (10 mm); Supermanifold-to-compressor A/C line uses seal washers. Verified — same.
- TM-08, Car computer coolant hoses (x2) plus grommet: the computer (HW) is liquid-cooled and plumbed through the Supermanifold. Verified — same.
- TM-09, Front aero shield: 11 bolts, 10 mm, 6 Nm. Frunk assembly: 6 bolts at 12 Nm. Rear underhood apron: 9 clips. Verified — [Service Manual: Pentaport AC Lines](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-38F1B41A-55D7-497E-902D-F27700522487.html)
- TM-10, Coolant reservoir ("coolant bottle") with cap, vacuum refill cap, overflow hose; vacuum refill to 60-70 cmHg; at least 15 L of coolant prepared for refill; level between NOM and MAX. Verified — same page.
- TM-11, Two Schrader valves on A/C lines and two A/C service ports with caps. Verified — same.
- TM-12, Refrigerant oil: POE (RB100EV used for washers); service note threshold 1.01 oz (30 mL) oil loss. Refrigerant type and charge amount are not stated on the page ("recharge to vehicle specification"). Verified — same.
- TM-13, Thermal routines: Thermal Fill Drain, Coolant Air Purge (pumps about 10 min; about 7000 RPM pump speed indicates air lock), Heat Pump Commissioning, Thermal Performance test. Indicates heat-pump system and electric coolant pumps. Verified — same.
- TM-14, Service procedures require disconnecting MV (48 V) battery connector and FRL connector, waiting 2 minutes. Verified — same.
- TM-15, 48 V low-voltage battery rated 4 Ah; electronics powered by 48 V "mid voltage" architecture. Verified — [Tesla Owner's Manual (en_CA)](https://www.tesla.cn/ownersmanual/cybertruck/en_ca/GUID-32CD64C8-5661-45A8-BFB6-35603858F7FB.html); [Service Manual search result](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-FAC16ECE-F2C6-48CC-879C-666C2A9DD363.html)
- TM-16, Jump-start switch-tank converter boosts 12 V to 48 V. Reported — [Autopian Munro/Tesla interview](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/)
- TM-17, Charger/DC-DC: secondary source says the PCS combines the on-board AC charger with redundant DC-DC converters stepping HV to 48 V ("PCS2" name not verified). Reported, low quality — [e-vehicleinfo](https://e-vehicleinfo.com/global/tesla-cybertruck-using-48v-wiring-harness-not-12v/) (page itself failed to load; only search snippet)
- TM-18, AC charging 11.5 kW at 240 V / 48 A. Reported — [Notebookcheck](https://www.notebookcheck.net/470-mile-Cybertruck-range-available-with-extender-accessory-as-5-Powershare-outlets-run-owners-tools-or-home.776037.0.html)

### Inferences
- Inferred: the system includes front radiator, powertrain pump(s), battery pump(s), chiller (refrigerant-coolant heat exchanger), electric compressor, condenser/heat exchanger, active grille shutters or equivalent, PTC or heat-pump heating and coolant temperature/pressure sensors ("PT sensor kit" mentioned in the service page, 25 mm socket). Counts and specs not sourced.
- Inferred: the 15 L coolant-prep minimum suggests a total system fill in the low-teens of litres, unverified.

### Gaps
- Refrigerant type (R-1234yf is typical but not confirmed for Cybertruck), refrigerant charge, coolant type and total volume, pump/valve counts, compressor and radiator dimensions, Octovalve-vs-Supermanifold part naming: not found. A search for these returned only Kia manuals.

## 4. Charging, on-board electronics and small parts

### Takeaway
Little primary data was retrieved. Charge port is NACS with 11.5 kW AC; DC fast charge connects directly to pack via DPDT arrangement. Most small parts (brackets, clips, harness, sensors) are only visible via service-manual fastener lists.

### Cited Findings
- CH-01, Charge port: bidirectional power up to 11.5 kW; Supercharger connects directly to battery terminals at 400 V or 800 V. Reported — [Autopian Munro/Tesla interview](https://www.theautopian.com/heres-what-manufacturing-expert-sandy-munro-learned-when-he-spoke-with-the-tesla-cybertrucks-engineers-and-designers/)
- CH-02, Low-voltage hardware is 48 V (window, wiper motors redesigned). Reported — same source.
- CH-03, Parts commonly absent from a basic model, evidenced by service-manual lists: hose clips (x2) and edge clips (x2) on battery hose bundle; spring clips (3x and 1x on A/C hoses); seal washers (5 on Penta line plus 2 on compressor line); bolt caps (2x) and bumpstops (2x) on frunk; breather fitting; hose grommet; A/C line bracket; CFM connectors (x2); Supermanifold connectors (x2). Verified — [Service Manual: Pentaport AC Lines](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-38F1B41A-55D7-497E-902D-F27700522487.html); [Service Manual: Hose - Supply - HV Battery](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-34BAA5A1-C6A0-4463-9B21-B3BA3CA5D154.html)

### Inferences
- Inferred: further items to model include HV cables (pack to PCS, pack to each drive unit, charge port to PCS), orange HV conduit, HVIL harness, motor phase cables (3 sets), drive-unit mounts/bushings, half-shaft boots, and sensor set (coolant temp/pressure, oil temp, resolver or position sensors). All unsourced.

### Gaps
- Service-manual sections for PCS, charge port, HV cables, HVIL, Supercharging; Tesla Cybertruck impact-report cell counts; patents. Not retrieved within the call budget.
- Recommended next fetches: service.tesla.com/docs/Cybertruck/ServiceManual/en-us/ index (sections 1830 Cooling, 3xxx Drive Unit, 1xxx HV Battery), and munrocommercial.com Cybertruck battery articles.
