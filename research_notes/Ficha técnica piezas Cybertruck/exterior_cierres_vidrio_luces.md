# Cybertruck exterior: closures, glass, lighting, trim, bed, hardware (parts breakdown)

Conventions. BASE = `https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/` (every procedure URL = BASE + GUID file). Confidence: Verified = Tesla Service Manual page read directly; Reported = secondary source; Inferred = my deduction. The manual lists only the LH side for most procedures (RH assumed mirrored, Inferred). Manual pages are marked DRAFT by Tesla. Some manual pages (wiper motor, charge port, Powergate fascia, Active grille shutter, 1209 mirror regulator, tow-eye cap) returned HTTP 403 or were not fetched; those are flagged as gaps. Fetched procedure pages were ~100k chars of boilerplate, I could not read the final ~20-45k characters of each section index (likely only footers/cross-refs).

Section index pages (Verified): [Manual TOC](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/index.html). Section GUIDs: 1001 Bumper/Fascia `GUID-A76646E7-DF66-4716-BFE4-8770F4D37695`, 1010 Body Panels `GUID-03E5CC62-C5C2-49FA-A3BE-6E9C1310C0E8`, 1020 Glass `GUID-79DFDD24-B74D-4765-BA26-995C9D75BA3B`, 1120 Tonneau `GUID-D284C287-577D-42B9-9D6D-6E33E689938D`, 1133 Closure assist/hinges `GUID-CA414463-1C4F-4F5E-82E8-F714AD66BEE9`, 1150 Door glass/regulators `GUID-830DA2E9-792D-40E7-ACCB-FC090D619987`, 1170 Seals `GUID-CA7A555B-BAC8-4B28-9BD0-1B110F79C1CC`, 12 Exterior fittings `GUID-B1EC1800-938E-4623-8459-B4723361D57C`, 1740 Exterior lights `GUID-B6D2B838-A8BD-473E-A074-2367E2D9648B` (all under BASE).

Trim note: the manual tags many parts "(Long Range)" vs "(Standard)"/untagged, i.e. AWD/Cyberbeast vs the later Long Range RWD-type build; "Post 11/4/2024" marks a running change (new sail applique / tonneau rail). The Cyberbeast generally follows the untagged/Standard variants (Inferred; the manual does not label Cyberbeast explicitly in what I read).

---

## 1. What are the exact part names and counts per the Service Manual (exterior, closures, glass, lighting, body hardware)?

### Takeaway
The Service Manual exposes ~250 distinct exterior procedure titles (one per serviceable part), which gives an official part-name list. Fastener data exist only in individual procedure pages; those I read are tabulated below. The manual gives names and torque but almost no dimensions or materials.

### Cited Findings

**A. Body panels (1010) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-03E5CC62-C5C2-49FA-A3BE-6E9C1310C0E8.html))
Part names (qty 1 per side unless noted; RH mirrored = Inferred):
1. Bed Side Outer Assembly LH/RH (Long Range and standard variants)
2. Bed Side Applique Corner Bracket LH/RH
3. Rear Under Body Rear Fascia Bracket LH/RH
4. Dash Absorber LH/RH
5. Door Front LH/RH (stainless skin door; R&I and R&R procedures)
6. Door Rear LH/RH
7. Fender Assembly Front LH/RH
8. Front Fascia Lower Dummy LP Cover (dummy license plate cover)
9. Lamp Step Bracket LH/RH
10. Powergate Fascia
11. Powergate Hood ("Powergate" = frunk lid/hood)
12. Powergate manual release
13. Stud Plate Hinge Upper/Lower, Front door LH/RH (4 per side set front+rear: Front-Upper, Front-Lower, Rear-Upper, Rear-Lower; marked NEW)
14. Tailgate Assembly
15. Trim Cantrail Roof Rail LH/RH
16. Panel Alignment Specifications (gap/flush spec page, `GUID-4869C70E-5CBF-48B6-A7C6-03E006DA85E7`)

**B. Bumper/fascia (1001) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-A76646E7-DF66-4716-BFE4-8770F4D37695.html)): Active Grille Shutter; Body Side Bracket LH Rear Fascia; Cover-Camera-Lower-Fascia-Front; Foam Seal Side Front Grille; Foam Seal Upper/Lower Front Grille; Front Center Applique Assembly; Front End Carrier Plastic Assembly; Front Energy Absorber / Front Bumper Beam Assembly; Front Fascia Fairing Assembly LH/RH; Front Fascia; Front Lower Grille; Frunk Switch; Lower Tow Eye Cap LH/RH (front grille); Rear Energy Absorber Cast Bumper Assembly LH/RH; Rear Energy Absorber Center Bracket; Rear Energy Absorber Fascia Step Bracket Center; Rear Fascia; Step Bracket Center LH/RH Rear Fascia; Support Bracket Center and LH/RH Front Energy Absorber; Trailer Hitch Cover.

**C. Glass (1020, 1150, 1170) — Verified** ([1020](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-79DFDD24-B74D-4765-BA26-995C9D75BA3B.html)): Windshield Assembly (separate variant "w/ Off Road Lightbar"); Windshield edge seal front and LH/RH; Fixed Glass Roof Assembly; Roof glass rear edge seal; Fixed Backlite Glass (rear window); Moving Glass Door Front LH/RH and Rear LH/RH (4); Primary Seal door front/rear; Quarter Glass Front LH/RH (fixed small front quarter glass); Seal Header LH/RH; Seal Quarter Glass Front. Chip repair and clean-forward-camera procedures exist.

**D. Closures hardware (1133) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-CA414463-1C4F-4F5E-82E8-F714AD66BEE9.html)): Hood latch + latch actuator (frunk/Powergate latch); Powergate Hinge LH/RH; Hood Strut LH/RH; Powergate Striker; Door Latch Front/Rear (x4 per truck); Door Presenter Front/Rear (x4, powered door pop-out); Door Striker Rear; Hinge Upper Front/Rear door; Hinge Lower Front/Rear door (4 hinges per side set = 2 per door, so 8 total); Check Strap Front/Rear (4 total); Tailgate: Bumpstop, Cable Strap, Cinching Latch LH/RH, Striker LH/RH, Hinge Body Side RH/LH, Strut Damper (LH), Torsion Rod LH/RH, Latch and Striker.

**E. Door glass/regulators (1150) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-830DA2E9-792D-40E7-ACCB-FC090D619987.html)): Closeout Panel Front/Rear door; Window Regulator Front/Rear door; "Window Regulator, 48V Q-Motor" (regulator motor uses 48 V); Moving Glass adjust procedures.

**F. Seals (1170) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-CA7A555B-BAC8-4B28-9BD0-1B110F79C1CC.html)): Aero Seal Powergate LH/RH; Edge Seal Rear Roof Glass; Glass Run Seal Front Door A-Pillar; Seal Tailgate LH/RH; Secondary Seal Front/Rear door; Waist Belt Seal Inner and Outer, Front and Rear door (4 per door side set = 8 per truck); Water Management Seal Tonneau Center LH/RH.

**G. Tonneau (1120) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-D284C287-577D-42B9-9D6D-6E33E689938D.html)): Applique Lower/Upper Tonneau; Bushing Slat and Seal; Cam Block LH/RH; Chain Link; Closeout Seal; Corner Bracket LH/RH; Deflector Clip LH/RH; Flat Cassette Assembly LH/RH; Foam Datum Pad; Hinge Pivot Applique LH/RH; Horizon Rail Assembly LH/RH; Tonneau Horizontal Rail LH/RH; Mid Slat; Sealing Slat; Slat System (full slat set); Tonneau Applique; Tonneau Lower Assembly; Tonneau Motor Assembly LH/RH (motors are per side); NVH Barrier Assembly; Tonneau Rail LH/RH (post 11/4/2024 version); Manual release (slats); Manual Release Tailgate; Strut Bed Cargo Tub. Chain-driven (Chain Link) with cam blocks, so the cover is a motor+chain+slat system.

**H. Exterior fittings (12) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B1EC1800-938E-4623-8459-B4723361D57C.html)):
- Wheel liners: Front LH/RH, Rear LH/RH
- Undertray/diffuser: Aeroshield Front, Aeroshield Rear, Rear Diffuser, Lower Tub Crossmember, Skid Plate (front), Skid Plate Rear, Skid Plate Stamping
- Badges and Films: no procedures listed (no serviceable badges/films published)
- License plate: Front License Plate Assembly, Front Bracket (retrofit)
- Mirrors: Exterior Mirror Assembly Electromechanical LH/RH; Mirror Glass Flat Electrochromic Dimming LH/RH; Skull Cap LH/RH
- Truck bed (23 titles): Bed Closeout Rear LH/RH; Bed Floor Assembly; Bed Side Wall LH/RH (+Upper, +Lower Long Range variants); Bed Tiedown Assembly Fore LH/RH; Forged Bed Tiedown Assembly; Bracket Upper Bed; Bumpstops Bed Cargo Tub; Inner Tailgate Cover; Door-Outlet-Bed (bed power outlet door); Damper Reinforcement Assembly Bed; False Wall Bed; Front Wall Assembly Truck Bed; Lid Bed Cargo Tub; Manual Release Cap Tailgate Cover; Seal Bed Cargo Tub; Under Bed Storage Assembly; X-Member Bed
- Exterior trim (1220, ~42 titles): Applique Backlite; Applique B-Pillar; Applique C-Pillar; Applique Closeout Lamp Rear; Applique Roof; Applique Sail Baffle; Applique Upper Fascia; Applique Wiper; Baffle Fender Front; Beauty Cover Lightbar LH/RH (+bracket); Bracket Applique Roof; Fender Flare Carriers (Fore-Front, Aft-Front, Fore-Rear, Aft-Rear, each LH/RH); Fender Flares Fore/Aft Rear; Closeout Applique B-Pillar, C-Pillar; Closeout Sail Baffle; Rocker Panel Rear Fairing; Rocker Panel Assembly; Rocker Step Reinforcement Front/Rear; Structural Off-Road Rocker; Mud Flap Front and Rear (LH/RH); Sail Applique LH/RH (two generations); Sail Applique Set (retrofit); Top Applique Tailgate
- Luggage trim (1224): Frunk Access Panel; Frunk Assembly; Frunk Lamp; Safety Lock Switch; Frunk Seal
- Underhood trim (1225): Underhood Apron LH/RH; Underhood Apron Rear
- Trailer hitch (1230): Tow Hitch
- Door triggers (1245): Exterior Door Switch Front (B-pillar) and Rear (C-pillar) (touch/button door openers; exterior door handles section 1145 lists no procedures, meaning no mechanical handle)
- Terrestrial Armor (1250): "Terrestrial Armor" off-road armor package (option)

**I. Exterior lights (1740) — Verified** ([section](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-B6D2B838-A8BD-473E-A074-2367E2D9648B.html)): Bed Light LH/RH (two variants); Headlamp Assembly LH/RH; Headlight adjust (wall method); License Plate Lamp; Rear Marker Lamp LH/RH; Reverse Lamp LH/RH; Tailgate Lamp; Lightbar Front; Tail Lamp Body Side LH/RH. Lightbar beauty covers are in 1220.

**J. Fastener/torque data actually read (all Verified, procedure pages under BASE):**
- Front lightbar `GUID-4A605514-9F14-4377-A650-E152662396B1`: attached to Powergate by 2 nuts (3 Nm) + 2 bolts (4 Nm), 3 clips, 3 datums, 1 connector; 10 mm socket. Powergate fascia must come off first.
- LH headlamp `GUID-AA106AB5-27B0-48B1-86CA-A64E9D18F205`: 2 bolts 5 Nm (10 mm), 1 datum, 1 connector; access requires removing rear underhood apron, frunk assembly, and front center applique. Headlights need wall-method aim afterwards.
- Windshield assembly `GUID-28743D4C-E164-4741-8C95-D09F014DC857`: urethane-bonded with 4 tubes of urethane + primer (bead nozzle 8 mm x 14 mm); rear underhood apron 9 clips; front header trim 19 clips; wiper arm nut 18 mm, 45 Nm; wiper applique 2 clips + 2 datums; wiper nut cover cap; washer hose elbow; mirror stay arm cap + beauty cover; rearview mirror 1 screw T20 2 Nm; forward camera 4 screws T10 1 Nm; upper A-pillar panel 1 bolt 6 Nm each side; sun visors 2 bolts 6 Nm each; GNSS antenna; THS sensor; windshield heater harness; 4 edge seals + 2 datums; wiper arm to motor housing gap 3 mm +/-1 mm; wiper motor needs homing. Windshield is heated.
- Powergate hood `GUID-95384AD1-EF10-4818-8AAB-D95BD4C0E3BF`: 4 nuts 18 Nm (13 mm) + 1 connector, 6 harness clips; RH front wheel liner has 2 bolts 6 Nm to HV chinstrap + 1 push clip, 14 push clips (to fender flare carrier and fascia), 6 push clips/nuts (to body).
- Tailgate `GUID-FF063878-877C-49EC-BFE0-B51DAEF02984`: LH torsion rod bolt 25 Nm (13 mm), RH torsion rod fastener 50 Nm (Torx T45); spring clip on LH strut ball stud; 2 harness connectors + 1 harness clip; tailgate hinged on LH sleeve / RH slot, tilted ~45 degrees for removal.
- Front door `GUID-BDD33A91-1786-46E8-82C6-2AA75334F500`: 2 hinge fasteners 38 Nm (15 mm low profile), check strap bolt 23 Nm (Torx T40), A-pillar harness connector grommet.
- Door presenter `GUID-41B57474-80F4-47A5-8370-DAAA820F286F`: 2 bolts 13 Nm (Torx T30), 1 closure harness connector; sits behind door closeout panel.
- Exterior mirror `GUID-E5FC5791-2CCB-49E2-A210-2300460B0063`: 3 bolts (PN 1857466-00-B, single-use) 18 Nm (Torx T40), 3 retaining plugs holding door belt seal, 1 connector, door panel plug.
- Tail lamp `GUID-6A31AA5F-83BD-4CE3-B32C-DDDB56EA87F5`: 2 screws 5 Nm (Torx T30), 1 connector, datums; requires removing rear lamp closeout applique and rear bed closeout.
- Tow hitch `GUID-BD1223F7-BA44-4CD9-852C-7CABC4382CB2`: 6 x 18 mm bolts 198 Nm (single-use) to rear underbody casting + 4 upper bolts 44 Nm (15 mm) + 2 step-bracket bolts 16 Nm (13 mm) = 12 fasteners; trailer connector socket with harness clips; trailer ECU and rear center bracket.
- Fender (front) `GUID-BF8EBD82-4585-425A-9A61-117B82361D68`: 3 bolts to A-pillar + 2 bolts to upper fender beam, all 30 Nm (13 mm); 2 harness clips; fender mounting hole spec 8 mm with E-coat. 2 fender flare carriers (fore, aft) and roof rail cantrail trim also interface.
- Tonneau rail (post 11/4/2024) `GUID-5A374D49-E188-4AB9-B8CC-75B48347C047`: 9 bolts (10 mm) 9 Nm; sail applique held by 17 clips + 1 datum + 1 harness clip + 1 connector; applique corner bracket 1 bolt 9 Nm; water-management seal 1 clip; sail applique max 5 remove/reinstall cycles.
- Mud flap front LH `GUID-5070A3E5-A51D-4A86-B72F-10A852F30172`: 2 clips (to wheel arch liner) + 2 bolts 1.8 Nm (10 mm deep) to rocker.
- Front skid plate `GUID-B0F7244F-0D90-4781-A7C4-C4279FC261D9`: 8 bolts 4 Nm (10 mm), 4 push clips, 8 integral tabs; tow eye covers LH/RH removed first.

**K. Materials/dimensions that are published**
- Body skin: ~3 mm "ultra-hard 30X cold-rolled stainless" per Musk statement, likely modified 301 austenitic; mostly flat panels because cold rolling limits formability — [SAE Mobility Engineering](https://www.mobilityengineeringtech.com/component/content/article/44558-sae-ma-03878) and [SAE](https://www.sae.org/site/news/2020/06/tesla-cybertruck-stainless-steel). A 2026 blog claims door panels 1.8 mm and sail/hood 1.4 mm, low reliability, unconfirmed — [Basenor](https://www.basenor.com/blogs/news/cybertruck-is-bulletproof-to-handguns-shotguns-tommy-guns).
- Front wiper length: conflicting; 62 in (Autopian), ~50 in arm (Auto Connected Car News via secondary), ~4 ft / 1.22 m (analyst) — [Autopian](https://theautopian.com/if-you-were-a-fly-sitting-at-the-tip-of-the-tesla-cybertrucks-enormous-wiper-heres-how-fast-youd-be-traveling-when-it-wipes), [InsideEVs teardown](https://insideevs.com/news/718267/cybertruck-windshield-wiper-teardown/), [Drive Tesla Canada](https://driveteslacanada.ca/?p=83026). Single blade, die-cast base, washer fluid through the arm, 48 V motor (Reported). Sweep ~90 degrees (Autopian, Reported).
- NHTSA recall for wiper motor controller electrical overstress — [The Drive](https://www.thedrive.com/news/tech/nearly-every-tesla-cybertruck-has-been-recalled-again-this-time-for-sketchy-windshield-wipers).

### Inferences
- Total door-related parts: 4 doors x (skin, hinge x2, stud plates x2, latch, striker, presenter, check strap, window glass, regulator + 48 V motor, closeout panel, primary/secondary seal, 2 waist-belt seals, glass run seal, exterior switch, interior handle) is about 20 parts per door, ~80 for four doors.
- Hood is called Powergate, not frunk lid; the "frunk" is the cargo tub beneath (Frunk Assembly with access panel, lamp, seal, safety lock switch).
- Front lightbar is mounted on the Powergate (hood), so it opens with the hood; headlamps are separate corner units and, on the Windshield "Off Road Lightbar" variant, an optional roof/header lightbar exists.
- The lack of exterior door handle procedures and the existence of "Exterior Door Switch (B-pillar/C-pillar)" imply buttons at B/C pillars, not handles.
- Torque values 1-9 Nm on appliques/lamps indicate light plastic/aluminum trim, 30-40 Nm structural body bolts, 198 Nm hitch.

### Gaps
- Part numbers (PNs): only one PN was found (mirror bolt 1857466-00-B); the parts catalog (epc.tesla.com / parts.tesla.com) was not fetched and likely requires login; not verified.
- Fasteners for: wiper motor and linkage, charge port door, Active Grille Shutter, Powergate fascia, window regulator, cinching latches, hood latch, bed outlets, tonneau motor (403 error), front/rear fascia, rocker, fender flares, tiedowns, license plate lamp, reverse lamp, bed light, and others not opened. Each has a procedure page at BASE + GUID listed in sections above (GUIDs for those listed in the section index replies).
- Charge port (NACS) and wiper motor sections are not in the 10/11/12 indexes read; probably under 14xx/17xx (e.g. 1740/1730) or a 44xx charging chapter; not located.
- Real dimensions of lamp bar, glass panels, tonneau, bed, panel gauges per part: not found in the manual.
- Cameras and sensors on the exterior (front bumper camera, B-pillar repeaters, tailgate camera, ultrasonic/radar, rear-view) not enumerated here; only "Cover Camera Lower Fascia Front" and "Forward-facing camera" (windshield) appeared.

---

## 2. What do parts catalogs, Body Repair manual and teardown/video sources add?

### Takeaway
Little was retrievable in the effort budget: Tesla's catalog and tesla.com were not accessible (403 for tesla.com), and teardown coverage found was secondary only.

### Cited Findings
- Munro & Associates teardown found a die-cast wiper base; reported via [InsideEVs](https://insideevs.com/news/718267/cybertruck-windshield-wiper-teardown/) (Reported).
- Tesla originally tested a two-blade wiper and moved to a single blade, replacement ~$75 per [Drive Tesla Canada](https://driveteslacanada.ca/?p=83026) (Reported).
- Stainless exoskeleton is body-structure-integrated ("exoskeleton", not body on frame) — [Repairer Driven News](https://www.repairerdrivennews.com/2019/11/22/tesla-cybertruck-uses-stainless-steel-exoskeleton-rather-than-traditional-body-on-frame/) (Reported).
- The Service Manual includes procedure pages for the Terrestrial Armor package, Off Road structural rocker, and Off-Road Lightbar windshield variant, so these are optional/trim-specific parts (Verified, see section H/C above).

### Inferences
- Body Repair manual (separate Tesla doc) likely holds panel thickness, adhesive and weld-bond specs, but was not accessed.

### Gaps
- epc.tesla.com / parts.tesla.com contents, Body Repair manual, Owner's Manual dimension tables, YouTube teardown transcripts, forum threads: not retrieved.
- Tesla spec page (tesla.com/cybertruck) returned 403, so official overall dimensions were not confirmed in this pass.

---

## 3. Which small/hidden parts would a "complete" 3D model still be missing?

### Takeaway
The manual repeatedly cites clips, datums, harness clips, push nuts, plugs and seals that most models omit. Counts below are Verified from procedures.

### Cited Findings
- Sail applique: 17 clips + 1 datum + 1 harness clip + 1 connector per side; plus corner bracket + 1 bolt — [tonneau rail page](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-5A374D49-E188-4AB9-B8CC-75B48347C047.html).
- Front header trim: 19 clips, 1 magnet, 1 connector, 1 harness clip; rear underhood apron 9 clips; A-pillar forward trim 4 clips + 1 guide each; upper A-pillar 8 clips each; mid A-pillar 1 clip + 3 tabs each — [windshield page](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-28743D4C-E164-4741-8C95-D09F014DC857.html).
- Wheel liner (RH front): 1 + 14 + 6 push clips and 2 bolts — [Powergate hood page](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-95384AD1-EF10-4818-8AAB-D95BD4C0E3BF.html).
- Lightbar: 3 clips + 3 datums; headlamp: 1 datum; tail lamp: datums; skid plate: 8 tabs + 4 push clips; mud flap: 2 clips + 2 bolts — pages linked in section 1J.
- Windshield: 2 datums, 4 edge seals, rubber separator strip, glare shield 2 clips; urethane bead.
- Mirror: 3 retaining plugs, door panel plug, belt seal.
- Door: A-pillar harness grommet; check strap; hinge stud plates (NEW); Tonneau: bushing slat and seal, deflector clips, foam datum pad, NVH barrier, closeout seal, water management seal clip.
- Tow hitch: trailer ECU, rear center bracket, trailer connector socket.
- Fender: mounting hole 8 mm E-coated; 2 harness clips; fender flare carriers.

### Inferences
- Also typically missing (not documented here, Inferred): drain plugs/grommets in bed and frunk, tailgate wire-harness boots, license plate screws, washer nozzle, antenna(s), emblem adhesive pads, door seal clips, wiper washer reservoir lines, charge-port actuator and light.

### Gaps
- No complete count of body clips/fasteners for the vehicle exists in sources read.

---

## 4. Real dimensions of key parts

### Takeaway
Few dimensions are published; those found are fastener/gap-level or contested.

### Cited Findings
- Stainless sheet ~3 mm (SAE) vs 1.4-1.8 mm (Basenor blog, low confidence) — links in 1K.
- Wiper 50 / 62 in / ~4 ft (conflict) — links in 1K.
- Urethane bead nozzle 8 mm x 14 mm; wiper arm-to-housing gap 3 mm +/-1 mm; fender mounting hole 8 mm — [windshield page](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-28743D4C-E164-4741-8C95-D09F014DC857.html), [fender page](https://service.tesla.com/docs/Cybertruck/ServiceManual/en-us/GUID-BF8EBD82-4585-425A-9A61-117B82361D68.html).

### Inferences
- Gap/flush targets are in the manual's Panel Alignment Specifications page (not read); use it for door/hood/tailgate gap dimensions.

### Gaps
- Lightbar length, glass panel sizes, tonneau length, bed dimensions, overall vehicle dimensions: not obtained from a citable source in this pass (tesla.com blocked). Next step: read `GUID-4869C70E-5CBF-48B6-A7C6-03E006DA85E7` (panel alignment), the Owner's Manual specifications chapter, and the remaining procedure pages listed above.
