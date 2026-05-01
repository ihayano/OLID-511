# Project Intermesh — Character & Dialogue Reference
<!-- INTERNAL USE ONLY — not intended for players -->

All dialogue and narrative text listed in logical play order, organized by character.
Source of truth: `content/strings.json`. UI prose and system lines are excluded.

---

## Character Roster

| Character | Role | Location / Encounter | Appears |
|-----------|------|----------------------|---------|
| Dr. Ansari | University professor, observatory gatekeeper | Campus Science Building | Act II (player's choice) |
| Luz | Valley West resident | Valley West | Act II (player's choice) |
| Diego | Valley West resident, Luz's partner | Valley West | Act II (player's choice) |
| Yoshiko | Classmate, driver, logistics partner | International Grocery | Act II (player's choice) |
| Dalia | Apartment resident, community garden steward | Tesseract Apartments | Act II (player's choice) |
| Geo | Radio station contact | Radio Station | Act II (player's choice) |
| Yasmin | Women's Health Clinic contact | Women's Health Clinic | Act II (player's choice) |
| Nina | Neighbor, mutual aid encounter | Mid-deployment (after first site) | Act II, fires once |
| The Stray Cat | Unnamed stray | Mid-deployment (cat carrier required) | Act II, fires once |

---

## Act I — The Workbench
*No named characters appear. System narration only.*

---

## Act II — Community Deployment

Deployment order is player-chosen. Encounters fire after the player's first completed deployment, regardless of which site was chosen first.

---

### Dr. Ansari
**Location:** Campus Science Building
**Elevation:** Maximum (best line-of-sight in town)
**Condition:** Player must have at least 1 device available

**Intro (narrator):**
> Destination: Campus Science Building.
> Dr. Ansari leans in the observatory doorway, unimpressed by panic and very impressed by evidence.

**Ansari's opening line:**
> "Give me one reason this belongs on my roof," he says.

**Prompt:** *Make your case.*

---

**Branch A — Appeal to telemetry and survival data** *(roof install; requires WisMesh Repeater)*
> Ansari nods once. "That is an actual argument." He unlocks the roof hatch for you.

**Branch B — Make an emotional plea** *(dorm window fallback)*
> He refuses roof access. You settle for a dorm window and lose the best line-of-sight in town.

**Branch C — Use pure radio jargon** *(dorm window fallback)*
> He refuses roof access. You settle for a dorm window and lose the best line-of-sight in town.

**Branch D — Skip this site** *(no deploy)*
> You leave the science building dark. Full town coverage is no longer achievable.

---

### Luz & Diego
**Location:** Valley West
**Elevation:** Low (hills create dead zones)
**Condition:** Player must have at least 1 device available

**Intro (narrator):**
> Destination: Valley West.
> Luz and Diego meet you on their porch while hills crowd every approach to the neighborhood.
> A standard device will struggle here unless you spend more on the link.

**Prompt:** *Choose the Valley West deployment package.*

---

**Branch A — Basic device placement** *(dead zone risk)*

*Luz:*
> The house line joins the mesh, and Luz hands you a warm mug from the kitchen. The western edge still drops packets into silence.

**Branch B — Device + high-gain antenna** *(dead zone cleared)*

*Diego:*
> Diego helps you sight the antenna line. The western district finally links cleanly to the main network.

**Branch C — Device + solar repeater** *(best outcome)*
> The repeater drinks afternoon sun and throws packets across the low ground like a promise.
*(No named character line — narrator only)*

**Branch D — Skip**
> You keep your cash, but the valley edge falls off the map.
*(No named character line)*

---

### Yoshiko
**Location:** International Grocery
**Elevation:** Medium
**Condition:** Player must have at least 1 device available

**Intro (narrator):**
> Destination: International Grocery.
> Yoshiko eyes your gear, then your empty wallet, then tosses you her keys.

**Yoshiko's line:**
> "You give a device to the store, I drive you wherever else you need to go," she says.

**Prompt:** *Accept Yoshiko's deal?*

---

**Branch A — Give a device for logistics support** *(Yoshiko becomes free driver for out-of-town sites)*
> Yoshiko tops off her tank and waves you in. The market goes live, and your out-of-town travel rides are now free.

**Branch B — Skip International Grocery** *(Yoshiko keeps her keys)*
> You pass on International Grocery. The next deployments stay slower and more expensive in spirit, if not on paper.

**Note:** If Yoshiko's deal was accepted and player later visits Valley West or Women's Health Clinic, the travel prompt is replaced with:
> Yoshiko gives you a free ride to {title}. No travel fee charged.

---

### Dalia
**Location:** Tesseract Apartments
**Elevation:** Medium
**Condition:** Player must have at least 1 device available

**Intro (narrator):**
> Destination: Tesseract Apartments.
> Dalia meets you by the community garden with a crate of peppers, canned beans, and one stubborn smile.

**Prompt:** *Give a device for food and rooftop access?*

---

**Branch A — Give a device to the apartment community** *(+3 supplies)*
> The garden device comes online. Dalia sends you off with extra supplies from the rooftop harvest.

**Branch B — Skip**
> You keep moving. Dalia watches you go with a basket that could have mattered later.

---

### Geo
**Location:** Radio Station
**Elevation:** Medium (tower greatly extends reach)
**Condition:** Player must have at least 1 device available

**Intro (narrator):**
> Destination: Radio Station.
> Geo unlocks a side gate and points toward the tower with a grin that says he would climb it himself if you asked.

**Prompt:** *How bold do you get?*

---

**Branch A — Climb the tower** *(requires WisMesh Repeater; best coverage gain)*
> The tower sways, your hands shake, and the new relay paints a clean arc across the city center.
*(Narrator only — Geo spotting is referenced in the log note but has no spoken line)*

**Branch B — Mount it inside the lobby** *(safe, reduced reach)*
> You take the safe route. Geo does not judge you, but the coverage map absolutely does.

**Branch C — Skip**
> You leave the station behind. The town loses a strong mid-grid relay point.

---

### Yasmin
**Location:** Women's Health Clinic
**Elevation:** Medium (dense foliage requires better antenna)
**Condition:** Player must have at least 1 device available. Out-of-town site — requires $10 ride or walking.

**Intro (narrator):**
> Destination: Women's Health Clinic.
> Yasmin leads you behind the building where trees and wet branches turn the air into a green wall.
> Dense foliage here demands better hardware than a naked stock antenna.

**Prompt:** *Choose the clinic deployment package.*

---

**Branch A — Basic device placement** *(foliage still causes dead zone)*
> Yasmin thanks you anyway. The clinic joins the map, but every tree between you and town remains an enemy.

**Branch B — Device + high-gain antenna** *(dead zone cleared)*
> The upgraded antenna slices through the foliage. Women's Health Clinic now has a reliable lifeline.
*(Narrator only — Yasmin has no additional spoken line)*

**Branch C — Skip**
> You save the money. The clinic vanishes behind branches and static.

---

### Nina
**Encounter:** Mid-deployment mutual aid — fires after the player's first completed site deployment
**Condition:** Always fires once (flag: `state.minaEncounterFired`). Grant option disabled if no devices remain.

**Intro (narrator):**
> Nina — from your engineering class — stops you on your way back.
> Her family hasn't heard from her since the alerts started. She asks if you have a spare device — she wants to join the mesh and reach them.

**Prompt:** *Give Nina one of your devices?*

---

**Branch A — Give her a device** *(costs 1 device, earns +1 supplies)*
> Nina's face changes the moment the device lights up. She hands you a jar of honey from her kitchen. The mesh just got one person wider.

**Branch B — You cannot spare one**
> You keep moving. Nina watches you go. The mesh stays exactly as planned, and so does the silence on her street.

---

### The Stray Cat
**Encounter:** Mid-deployment — fires after first completed site deployment
**Condition:** Only triggers if player purchased the Portable Cat Carrier (`state.catCarrier === true`). Coin-flip outcome is independent of player choice.

**Intro (narrator):**
> A rustle in the shadows. Something small is watching you.
> A stray cat sits at the edge of the alley, tail twitching.

**Prompt:** *What do you do?*

*Options:*
- Try to pick it up — *Reach out slowly and hope for the best.*
- Whisper "psss psss psss" — *The universal language.*

---

**Outcome A — Cat joins (50% chance, independent of choice chosen)**
> The cat sniffs the air once, then walks straight to you and headbutts your shin.
> You have a companion.

*[ASCII art of cat displays for 4 seconds]*

**Outcome B — Cat scratches and runs (50% chance, independent of choice chosen)**
> The cat flattens its ears, swipes at your hand, and bolts into the dark. You have a small scratch and a lesson.

---

## Act III — Diagnostics
*No named characters appear. System narration only.*

**Storm alert (narrator):**
> Storm alert: derecho leading edge detected.
> Grid instability spikes. Lights flicker across the city and then vanish sector by sector.
> Project Intermesh becomes the only thing still awake.

---

## Endings — Narrator Only
*No named characters appear.*

| Ending | Trigger conditions |
|--------|--------------------|
| A — The Resilient Utopia | Coverage ≥ 30%, encrypted, supplies > 0, no dead zones, science requirement met |
| B — The Fractured Lifeline | Encrypted, coverage ≥ 22%, but dead zones present or science missed |
| C — The Open Frequency | Not encrypted, coverage ≥ 22% |
| D — The Dark Age | Coverage < 20%, supply shortage, hardware or signal failures |

---

## Cross-Reference: Character × Encounter Type

| Character | Spoken Dialogue | Named in Narrator | Supplies Impact | Device Impact | Blocks/Unlocks |
|-----------|----------------|-------------------|-----------------|---------------|----------------|
| Dr. Ansari | Yes — 1 line | Yes | — | −1 | Roof install requires WisMesh |
| Luz | Yes — 1 line | Yes | — | −1 | — |
| Diego | Yes — 1 line | Yes | — | −1 | — |
| Yoshiko | Yes — 1 line | Yes | +1 (sugar deploy) | −1 | Unlocks free travel |
| Dalia | No | Yes | +3 (deploy) | −1 | — |
| Geo | No spoken | Yes | — | −1 | Tower requires WisMesh |
| Yasmin | Yes — 1 line | Yes | — | −1 | — |
| Nina | No | Yes | +1 (grant) | −1 (grant) | — |
| Stray Cat | No | No | — | — | Requires cat carrier |
