# Chum Storm

A survivors-style horde game: sea cats keep showing up demanding dinner, and you auto-toss fish (and much more) to keep the horde fed. Last 15:00 and the **Dinner Bell** rings.

## Run the game
Serve the folder over HTTP (opening the file directly can block the art from loading):
- **VS Code:** install **Live Server**, right-click `index.html` → *Open with Live Server*.
- **Python:** run `start-local-server.bat` (needs Python), then open http://localhost:8000.
- **GitHub Pages:** publish the repository root from `main`.

## Cat art
**Town cats (area 1)** come from **`assets/cats/town_cats.webp`**: Orange Tabby, Brown Tabby, Grey Tabby, Black, White, Cream, Calico, Tortoiseshell, Tuxedo, Siamese, Ragdoll, and Black & White Cats, on the same 4 × 3 layout with a label under each cat. The Cream Cat is the town's boss, the **Big Cream Cat**. If the sheet is missing, plain round cats in each fur colour stand in.

**Sebastian, the Royal Ragdoll Cat** (the last cat of Cat Town) is **`assets/cats/royal_ragdoll.webp`**, a single picture cut out the same way. Catching him is the mission of your **second Cat Town run**:
1. **The request:** when you come back from your first run, **Princess Rosalind** (the signora, with a crown) is waiting at the harbor. Sebastian has run off; he won't touch fish and hisses at anyone who comes near. She gives you her caviar plates.
2. **Finding him:** a "MISSION: CATCH SEBASTIAN" card opens the run, and he turns up a little way off. A blue 👑 arrow with the distance points the way.
3. **You can't chase him down:**
   - Get close and he **hisses** ("HSSSSS!") and bolts, a bit faster than you.
   - Linger near him and his 👁 suspicion meter fills up until he runs off.
4. **Caviar traps:**
   - Press **F** (or the 🍽️ CAVIAR button) to put a plate down where you stand. You can have 3 out at once; putting down another picks up the oldest.
   - When nobody's near, he sneaks up to a plate. If you hang around the plate he's after, he smells you and gives up on it for a while (😾).
5. **The bite:** when he starts eating:
   - You get an alert banner and a flash.
   - The plate pulses gold, and a **GO!** marker over him shows how much meal is left.
   - Off screen, the arrow turns gold and says **EATING!**
6. **The swoop:** reach him while he eats (the dodge helps). Dawdle close by for more than about a second and he spots you and runs; if he finishes the plate, he slips away and you need another.
7. **The rescue:** touch him while he's eating and he's yours. **Cat Town is complete**, **Willow Park opens**, and the Princess pays **300 🪙** at the harbor.

**Rules:** weapons don't hurt him and he never hurts you. Tune it with `ROYAL` in `index.html`.

**Area 2 unlock:** Willow Park opens once you've found **every cat in Cat Town**, Sebastian included.

**Sea cats** (areas 2 and 3):
The sea-cat sheet lives at **`assets/cats/sea_cats.webp`** (4 columns × 3 rows on white, with a name label under each cat; a `sea_cats.png` works too). The game slices it when it loads: it removes the white background from the edges inward (so white fur and eyes stay) and keeps only the biggest shape in each cell, which drops the labels. In reading order the cells are:

| Row | Cats |
|---|---|
| 1 | Octopus · Squid · Shark · Sea Bass |
| 2 | Sea Angel · Axolotl · Orca · Nudibranch |
| 3 | Jellyfish · Clownfish · Sea Urchin · Narwhal |

To swap in new art, replace the sheet with one in the same layout. If it is missing, the cats fall back to the old pixel sprites.

## Your fisher's look
The **Look** tab is a character creator: skin tone, expression, hair, top, bottom, jacket and one extra (bow, goggles, cap, headphones, bag…), plus 🎲 *Surprise me*. Your look is used for every fisher in runs. It squashes and stretches as you walk, and its face reacts: it cries when hit, gets starry eyes on level-up or when you find an artifact, laughs at the foghorn, grins at dug-up treasure, and looks worried below 30% HP. Your character has a white outline so they stand out in the crowd. The parts come from the character sheet at **`assets/player/avatar_sheet.webp`** (or `.png`). Each item is found by growing outward from a seed at its spot in the sheet (`AV_PANELS`), so items that overlap a neighbour are split cleanly. Clothes are scaled per category to the base body (`AV_SCALE`) and pinned to measured body landmarks (`AV_BODY`). Hair is lined up by its own fringe line, just above the eyes (`AV_BROW`); faces are lined up by the chin; accessories have their own spots (`AV_ACC`). Layer order is body → clothes → head → hair → hats, so collars tuck under the chin and headphone cups sit behind the head. Without the sheet, the old pixel fisherman is used.

**Wardrobe expansion.** Four more sheets add to the paper doll. Each item is cut out by growing from its spot on the sheet, so touching items split cleanly, and small loose bits like "!!", sparkles or ZZZ stay with their face.
- **`assets/player/faces.webp`:** 45 expression heads
- **`assets/player/hair.webp`:** 35 hairstyles
- **`assets/player/tops.webp`:** 35 tops, capes and jackets (the skull tee is left out)
- **`assets/player/accessories.webp`:** about 60 accessories (the fish-bone clip and the effect icons are left out).

New pieces are scaled by their own sheet's typical size, so old and new pieces mix freely. The Wardrobe (in the Big Fish Shop) has 12 tabs: Face, Hair, Top, Bottom, Jacket, **Hat & Ears**, **Glasses**, **Neck**, **Bag**, **Wings & Tails**, **In Hand** and Extra. Each accessory slot can be worn at once:
- **Hat & Ears:** hats, ears, crowns and hair clips, drawn over the hair
- **Glasses:** worn on the face
- **Neck:** scarves, collars and the bandana
- **Bag:** at the hip
- **Wings & Tails:** wings, tails and the backpack, drawn behind the body
- **In Hand:** the fishing rod, wand, net, lantern, camera, bouquet and more.

🎲 *Surprise me* and the harbor locals pick from all of it. Adding `?debug#dolls` (optionally with `&part=face`, `hair`, `top`, `head`, `eyes`, `neck`, `bag`, `back` or `hand`) shows every piece on the doll, for checking the fit.

## Environment art
There are three areas, each with its own ground:
- **Cat Town** has cobbles with manhole covers, puddles, flower pots and weeds.
- **Willow Park** has grass with swaying tufts; its floor uses the grass colours from **`assets/env/env_sheet.webp`**.
- **Sunny Beach** has sand with ripples, starfish, shells and pebbles.

The environment sheet is otherwise only used for the breakable props: a pink pot in town, a flower crate in the park and a teal pot on the beach. The bones panel and the skull sign are not used.

## The opening story
The first time the game starts, an animated opening plays **in Cat Town itself**, in the piazza where every run begins. The run is set up but frozen while the story plays on top of the real map, in sunset light under string lights:
1. A little seaside town somewhere in Italy.
2. Townspeople enjoy their evening in the piazza: the lemon seller, a musician serenading a waitress, a gelato kid, the florist, granny, the gondolier and the chef.
3. **But this town has one big problem…** The lights flicker, everyone panics and runs home (SLAM!), and dusk falls.
4. **The town is run by cats.** A few peek in from the edges, then they pour into the square, and the Big Cream Cat shows up too.
5. It's **DINNER TIME!** The cats all jump and meow.
6. **Then you step out of your fish shop:** the fish shop owner, the only one up for the challenge. The cats make room and you hold the fish up high: "Save the town. Feed every single cat!"

**Straight into the first map:** when the story ends (or you skip it), the run simply starts right there. The cats that came for dinner are the first ones to feed. When that first run is over, the results screen only offers **⚓ Back to the fish shop**, which opens the harbor for the first time with a short "Your fish shop" welcome. From then on you sail out from the harbor as usual.

**Controls:** tap, Space or Enter goes to the next line. **Skip** (or Esc) and **Let's feed them!** both start the Cat Town run. A replay from the 🎬 button goes back to the harbor instead.

**Seeing it again:** it only plays once (`save.seenIntro`). Replay it with the 🎬 button next to "The Harbor", or add `?intro` to the URL.

## The fisher, the townsfolk and the Italian town kit
- **You: the fisher.** `assets/player/fisher_turnaround.webp` (front, three-quarter, side and back views) is you in runs, the harbor and the story.
  - **Look:** the view follows the way you're heading, with a thick white outline (`OUTLINE_PX`) and squash & stretch when walking. You're drawn bigger than before (`PLAYER_H`).
  - **Fixed outfit:** the Wardrobe just shows your fisher walking (beanie, striped shirt, overalls and boots).
  - **The chibi rig is off:** the head + hair from `chibi_parts.psd` on the `chibi_body.webp` body, with the hair picker, is still in the code. Set `CHIBI_ENABLED = true` to bring it back; `?debug#chibi` shows it.- **Townspeople:** `assets/npc/townsfolk.webp` (4 × 4) has the chef, waitress, old fisherman, fishmonger, gelato seller, gondolier, nun, granny, painter, musician, lemon seller, florist, sailor, gelato kid, signora and newsboy. They are the story's locals and the harbor's request-givers; locals saved before the sheet get one picked from their outfit.
- **Town kit:** `assets/env/italian_town.webp`.
  - **The harbor's buildings** come from the kit, bigger than before. Only the Big Fish Shop keeps its own art.
    - The **Big Fish Shop** is where your **Tackle & Skills** are, with your **Cat Home** upstairs (the 🏠 button in its panel). The bottom bar's Home, Tackle and Skills buttons lead there too.
    - The Italian houses and the trattoria are scenery.
    - The **Pet Store** is the gelato shop.
  - **The harbor street** has bunting strung between the houses, flower pots along the quay, a lemon tree by the fish shop and the Italian flag by your boat. These are the `kit:` entries in `HB_DECOR` and `HB_BUILDINGS`.
  - **Everyone the same height:** you, the locals and Old Gil are the same height in the harbor (`HB_PERSON_H`). In the story, the townsfolk are as tall as you (`PLAYER_H`).  - **Cat Town:** keeps its own clean cobbled look. The only kit pieces there are the row of shops where every run (and the story) starts: the trattoria, your fish shop and the gelato shop.
  - **Old Gil:** he is the old fisherman with the pipe from the townsfolk sheet.
  - **Checking the cuts:** `?debug#kit` shows every cut piece.

## Controls
- Move: WASD / arrow keys, or touch anywhere and drag (floating joystick)
- Weapons fire automatically; desktop mouse-drag aims Fish Toss and Catnip Spray
- **Dodge: Space** (or the 💨 DODGE button left of the item slots). A snappy dash of about 175 px the way you're moving, or the way you face if standing still. Most of the distance comes in the first half, and you can steer it a little. You lean hard into it, stretch on take-off, and squash on landing; speed lines and blue afterimages trail behind you. You can't be hurt mid-dodge or for a moment after landing. Dodging something that would have hit you is a **perfect dodge**: a tiny freeze, a flash and "Dodge!". It recharges in about 0.75 s (a blue ring under your feet and on the button). Press Space a moment early and the dodge fires as soon as it's ready. Tune it with `ROLL` in `index.html`.
- Pause: ⏸ button, Esc or P
- One-time items: **1 / 2 / 3** (or **Q** for the first), or tap the item slots at the bottom right. Party Treats fire instantly. Yarn Balls and Cucumbers are **placed by hand**: pick one, then click / tap where it should land (an aiming circle shows its area, time slows while you aim, and you can reach up to 480 px away). Pressing the same number again places it at the circle; Esc, right-click or tapping the slot again cancels.

## Cat Town's layout
Cat Town is blocked out as a little Italian town, built from simple 3D shapes (boxes, cylinders and ball-shaped treetops) that stand up on the tilted ground. The layout repeats every `TOWN_TILE` pixels, so it never ends.
- **The piazza** (where you start):
  - A big round stone square with a large tiered **fountain**, with water arcs, ripples and sparkles.
  - Benches and lamp posts around it.
  - The trattoria, your fish shop and the gelato shop along its north side.
- **Streets and houses:**
  - A paved east–west main street, a north street, and a north–south avenue.
  - Rows of houses face the streets: pastel walls, windows with green shutters and flower boxes, an arched door and a terracotta roof. Some wear the Italian village art.
  - Gaps between the houses leave lanes to walk through, and trees line the main street.
- **The park** (south-east): grass, trees, a pond with ripples, flower beds, benches and a lamp along a winding path.
- **The garden** (south-west): rows of raised flower beds and lemon trees on grass, with crossing paths.

**It never gets in the way:**
- Nothing blocks you or the cats.
- Any house, tree, shop or the fountain fades to see-through while you or a cat is behind it.
- Manholes and weeds stay off the grass, the garden and the piazza.

**Editing it:** the layout is the `TOWN` list in `index.html` (`ground` for streets and grass, `things` for what stands up). `BOX3D.Z` sets how much tall things lean with the camera.
## How a run works
**The 3D look:** the run maps look like a tilted, gently curved 3D diorama.
- **The ground** (floor, decorations, zones, plates, shots):
  - It's drawn flat, then a small WebGL pass tilts it so it falls away toward the top.
  - The same pass adds a subtle fish-eye curve and a soft haze in the distance, in the area's own tint.
  - The result shows on `#glc`, the canvas underneath.
- **Things that stand up** (cats, you, the house blocks, lamps, flower pots, the story's actors) are drawn on top.
  - They stay upright and aren't squashed.
  - Each stands at its spot on the curved ground and is sized by its distance (`billboard()`).
  - They're depth-sorted, so a cat behind a house is hidden by it.
- **House blocks:** the piazza's trattoria, fish shop and gelato shop are real boxes.
  - The front face shows the Italian village art.
  - The side walls are in the facade's colour, with a terracotta roof on top.
  - You see a building's side as you walk past it.
- **No cut-off ground:** the ground is drawn zoomed out by just enough (`tiltOverscan()`) that the tilt and curve always have ground to show, so it fills the screen edge to edge. The view bounds grow with it, so cats spawn beyond what you can see.
- **Tilt-shift blur:** a light blur at the top and bottom of the screen (`#tiltshift`).
- **Aiming:** mouse aim and placing items are mapped back through the curve and tilt, so they land where you point.
- **Without WebGL:** the ground is tilted by redrawing it in thin rows, with no curve.
- **Tuning:** `TILT` in `index.html`. `k` is the lean, `focus` the row that keeps its size, and `fish` the lens curve (0 = none). `BOX3D` controls the house blocks.
| Type | Colour | What it is |
|---|---|---|
| 🎯 **New projectile** | Blue | A weapon you don't have yet |
| ⬆️ **Projectile upgrade** | Orange | The next level of a weapon you have; a new trick (Lv 4 / 7) glows gold |
| 📈 **Stat upgrade** | Green | A passive bonus |

Each card also shows:
- **Level pips:** where you are and the level you'd get, like "Lv 1 → 2 / 8".
- **A pink "+1 PROJECTILE" tag:** when the pick adds a projectile.
- **15-minute runs.** Each area has a minute-by-minute wave table plus scripted events: crowds and schools sweeping across the screen, encirclements, elite cats, and a boss at 3:30, 8:30 and 13:30 (the Big Cream Cat in town, the Narwhal Cat on the beach, and the two take turns in the park). Every 5 minutes is a day/night cycle.
- **Three areas, 24 cats (+2 bosses), each type with its own behaviour.** Each wave slot is a role. The area decides which cat fills it, and the town cat plays the same role as a sea cat:
  - **Tougher as you go:** every new cat type has more HP than the one before it, in the order they first show up: Octopus 10 → Sea Bass 18 → Urchin 26 → Squid 38 → Axolotl 55 → Shark 75 → Nudibranch 105 → Sea Angel 120 → Orca 190 → bosses 3,000. Crowds and schools stay light. XP rises to match, and town cats copy the sea cat whose role they play.
  - **Signature moves** (from the attack concept sheet). Each has a tell first:
    - Orange Tabby: *Zoomies*. Brown Tabby: *Scratch Combo*.
    - Black Cat: *Shadow Pounce*, melting into purple smoke and reappearing on a landing circle.
    - Calico: *Lucky Paw*, a giant paw dropping from the sky. Tortoiseshell: *Whirlwind Claws*.
    - Tuxedo: homing *Fish Missiles*. Siamese: *Energy Beam*, with a glowing aim line. Ragdoll: *Hairball Shot*, coughing "hack!" and shedding sticky fur.
    - Black & White: *Rolling Tackle*. Shark: *Dash Slash*.
    - Orca and both bosses: *Glomp*, crouching, leaping and landing on a red circle.
  - **Area 1 · Cat Town:** 12 house cats. Orange Tabby wiggles; Brown Tabby pounces; Grey Tabby and White Cats come in gangs; Black Cat hisses out a claw ring; Tuxedo flicks 3 hairballs; Calico lobs hairballs; Siamese circles you; Black & White charges; Tortoiseshell belly-flops; Ragdoll sheds sticky fur.
  - **Area 2 · Willow Park:** 12 animal cats from **`assets/cats/park_cats.webp`** (4 × 3, same layout as the other sheets), each in a sea-cat role:
    - Fox, Raccoon, Red Panda, Owl, Platypus, Koala and Tanuki Cats
    - Quokka and Penguin Cats, which come in crowds
    - Deer Cat, which charges and slashes
    - Wolf Cat, which glomps
    - the boss, the **Big Bear Cat**
  - **Park specials** from **`assets/cats/park_special.webp`** change the ground you fight on:
    - **Apple Cat:** drops apples that leave slippery, slowing juice.
    - **Pigeon Cat:** blows a feather gust lane that shoves you along it.
    - **Working Cat:** builds a worksite of cones, a barrier and crates that block your way for 12 s.
    - **Looooong Stray Cat:** very long, bites along its whole body, and leaves fur piles you can't walk through.
  - The specials join the park from minutes 1, 3, 5 and 7. Both park sheets are in; `?debug#cats` shows every cat as the game cuts it.
  - **Area 3 · Sunny Beach:** the 12 sea cats.
  - Every attack is telegraphed on the ground with an outline + gradient that fills up before it lands. The sea cats:
  - Octopus Cat wiggles toward you; Sea Bass Cat rests, then darts.
  - Sea Urchin Cat puffs up and fires a ring of spikes (the spike lines grow out first).
  - Squid Cat backs off and squirts a 3-ink spread (aim lines first); Sea Angel Cat circles you firing bubble volleys.
  - Shark Cat locks a red charge lane, then dashes down it: step out of the lane.
  - Axolotl Cat lobs bubbles where you're standing (a blue circle fills, then it lands); Orca Cat belly-flops in a red circle when it's close.
  - Nudibranch Cat leaves sticky purple slime that slows you and stings.
  - Jellyfish and Clownfish Cats wobble past in schools. The Narwhal Cat boss cycles hairball rings, a turning spiral and a giant telegraphed slam.
  - Elites are big, gold-glowing versions that drop treasure and a one-time item. The first time you spot a new cat, the banner tells you what it does.
- **Find every cat:** a cat type you've never fed wears a bouncing **?** tag (plus a banner the first time one appears). The Cat Home shelf and the results screen show silhouettes of the cats you haven't met, with a hint about where and when each one turns up.
- **Leveling:** fed cats drop XP stars. Each level offers 3 choices (4 with luck): new weapons, weapon levels, or passive items. Every level-up offers at least one upgrade for a weapon you own. Choices that add a projectile glow pink with a **🎯 +PROJECTILE** ribbon.
- **Missions:** three missions run at once in the panel at the top left, each worth bonus gold the moment it's done. Each row shows what to do (with the cat's picture for cat missions), a progress bar with the count, and a gold **REWARD** pill. Cats a mission wants wear a gold dashed ring at their feet. A banner introduces the missions at the start of a run and announces each new one; the row bounces when it makes progress. Examples: *Feed 17 Sea Bass Cats*, *Feed 60 cats*, *Grab 4 power-ups*, *Don't get hit for 30 s*, *Reach level 8*, *Dig up a treasure spot*, *Use 2 one-time items*, *Feed a big (elite) cat*. A finished mission is replaced by a slightly harder one; the header tallies missions done and gold earned, and the results screen lists them.
- **Mission callouts:**
  - **Finishing a mission:** a big *MISSION COMPLETE!* card drops in, showing the mission and its reward, and coins fly into your gold counter.
  - **Cat missions:** feeding a cat a mission wants pops its count (e.g. 📜 5/12) where it was fed.
  - **Almost done:** missions at 75% or more glow and say *almost!*
- **Cats left to discover:** the HUD chip shows the total and how many are in this area (e.g. ❓ 33 to discover · 5 here), with silhouettes of this area's undiscovered cats underneath.
  - **Run start:** a *CATS TO DISCOVER* card lists them.
  - **New cat:** feeding one gives a *NEW CAT DISCOVERED!* card with how many are left.
  - **Elsewhere:** the harbor top bar and the area pop-up's stage list show the counts too.
- **HUD:** level badge, HP (with numbers) and XP bars, timer, gold and cats fed across the top; weapons, passives and missions on the left; projectile count, active Frenzy / Party Treats timers and how many cat types are still left to discover on the right; one-time item slots bottom right.
- **Weapon tricks:** every weapon learns a new trick at **Lv 4** and **Lv 7** (cards that unlock one get a gold **★ NEW TRICK** ribbon, other cards show the next trick coming). Evolved weapons keep both. Stars on the HUD weapon icons count tricks learned.

  | Weapon | Lv 4 | Lv 7 |
  |---|---|---|
  | 🐟 Fish Toss | Ricochet: fish bounce to a second cat | Golden Catch: every 4th throw adds a golden fish (3× damage, pierces all) |
  | 🌿 Catnip Spray | Catnip Patch: leaves a slowing patch | Both Ways: also sprays behind you |
  | 🔴 Bobber Orbit | Splashdown: hits splash nearby cats | Endless Line: bobbers never stop |
  | 🪣 Chum Bucket | Sticky Chum: cats crawl, take +50% | Chum Burst: puddles pop for 3× damage |
  | 🥛 Milk Splash | Big Wave: shoves cats far back | Four Ways: also splashes up and down |
  | ⚓ Anchor Drop | Aftershock: a shockwave ring follows | Dragnet: aims at the biggest crowd and drags cats in |

- **Area outlines:** every area weapon (spray wedge, aura, puddles, splashes, anchors, orbit path) shows its exact reach as an outline + gradient. Fish get bigger as Fish Toss levels up.
- **Evolutions:** max a weapon, own its partner passive, then open a treasure box:

  | Weapon | + Passive | → Evolution |
  |---|---|---|
  | 🐟 Fish Toss | 🍽️ Second Serving | 🐠 Salmon Run |
  | 🌿 Catnip Spray | 🕸️ Wide Net | ☁️ Catnip Cloud |
  | 🔴 Bobber Orbit | 📏 Long Line | 🌀 Whirlpool |
  | 🪣 Chum Bucket | 🧲 Chum Magnet | 🦈 Feeding Frenzy |
  | 🥛 Milk Splash | 💚 Fresh Catch | 🍦 Cream Tide |
  | ⚓ Anchor Drop | 🎏 Bigger Bait | 🚢 Shipwreck |

### Loot hunting
- **Projectiles are precious.** The pink **🎯×N** counter in the HUD shows how many projectiles each weapon throws, and it pops when the number goes up. They come slowly on purpose: Second Serving (up to 2), 🪱 **Bait Bundles** (+1 each, up to 2 per run, only from 4:00), the 🪝 Golden Hook and 🎣 Twin Rod artifacts (not before 5:00, and the second not before 10:00), 🔥 **Frenzy** (+1 for 8 s, from 3:00), a couple of weapon levels, and the Angler skill branch.
- **Treasure spots:** about every 45 s an **X marks the spot** appears 650–900 px away, with a screen-edge arrow and a distance readout. Reach it within 45 s to dig it up: it throws out an artifact or a treasure box, plus two power-ups.
- **Artifacts** last the whole run: Golden Hook and Twin Rod (+1 projectile each), Lucky Pearl (luck), Old Compass (treasure spots twice as often), Ship's Bell (cooldown), Coral Charm (regen), Spyglass (area and pickup range), Mermaid Figurehead (damage). They show in the HUD and on the results screen.
- **Power-ups** (mostly from breakable props) each have their own colour, badge shape, label, light pillar and pickup effect: 🥫 **+30 HP**, 🧲 **MAGNET**, 📯 **BLAST!**, 💰 **+GOLD**, 🔥 **FRENZY**, 🪱 **+1 PROJECTILE**. The odds shift during a run: the first 5 minutes are heavy on 🧲 magnets, while Frenzy, Blast and Bait Bundles only start dropping later. Power-ups glow through the night and get edge arrows when off screen.
- **One-time items** (from breakable props, treasure spots and elites; carry up to 3, shown bottom right):
  - 🍤 **Party Treats:** every cat rushes at you for 6 s (cats from off screen pile in too), and cats fed meanwhile give double XP. Great late in a run with big area weapons.
  - 🧶 **Yarn Ball:** place it; every cat within its dashed circle sprints to it (much faster than they chase you) and plays with it for 7 s instead of biting.
  - 🥒 **Cucumber:** place it; no explosion and no damage. It sits there for 7 s and cats are too scared to come inside its circle: any that do leap and run back out. A safe spot to stand in.
  - A full bag leaves new items on the ground until you use one. While a placed item is in the air, its landing area is outlined.
- **Treasure boxes come in three tiers:** gold (1 reward), purple **Rare** (3 rewards, may contain an artifact) and rainbow **Legendary** (5 rewards, always an artifact if one is left, triple gold). Bosses always drop Rare or better. Each tier has its own look in the world and on the opening screen.

## Between runs
- **The Harbor.** The game opens, and every run ends, on the street outside your fish shop. Walk left and right (**A / D** or the arrow keys, or tap where to go). Walk up to a building and press **E** / **Space** / **↑** (or tap it) to go in:
  The street is built from the harbor kit at **`assets/env/harbor_sheet.webp`**:
  - **Buildings:** the Big Fish Shop (your shop, with its own sign) and three houses for the Cat Home, Tackle & Skills and the Pet Store.
  - **Street dressing:** lamp posts, a bench, flower boxes, plant pots, an A-board, a signpost and a banner pole.
  - **On the pier:** crates, a fish scale, buoys, a life ring, rope and an anchor.
  - **Ground:** stone paving for the quay, planks for the pier and brick for the sea wall.
  - **Sky and sea:** the sun, clouds and a lighthouse.
  The cream panels on the sheet count as background when it's cut up. Until the sheet loads, the old drawn street shows instead.
  - 🏠 **Cat Home**: visit and squish your cats
  - 🎣 **Tackle & Skills**: the skill tree
  - 🐟 **Chum Storm Fish Co.** (your shop): the wardrobe for your fisher's look
  - 🐾 **Pet Store**: furniture for the Cat Home
  - 🐠 **Old Gil's Fish** on the pier: buy fish for your bucket
  - ⛵ **Your boat** at the end of the pier: go fishing (see below).
  - 🗺️ **Out of town** at the far left of the street: a yellow **Areas** sign with arrows on the cobbles. Walk past it (or press **E** by it, or tap **Areas** in the bottom bar) and a pop-up shows every area, your fishers and what is in your fish bucket. Pick and press **Let's go!** to start a run.
  - Your collected cats laze around in front of the shop (tap one to squish it).
- **Locals with requests.** Now and then a local walks up with a ❗ and asks for something. Requests carry across runs (up to 3 at once) and show in the Requests panel, both in the harbor and during runs:
  - find and feed a specific cat, often one you've never met
  - feed a number of one cat type
  - feed the Narwhal Cat
  - dig up some treasure spots
  - survive to a set time on a stage
  When one is done, the local waits in the harbor with a 🪙 bubble. Talk to them to collect the gold.
- **Your fish bucket is your ammo.** It holds real species (the 30 fish from `fish_types.webp`), each in one of five grades: Common, Nice, Great, Rare (+1 pierce) and Legendary.
  - **Every fish Fish Toss throws comes out of the bucket**, picked at random from what's in it. The fish you see flying is the species that left your bucket, and it hits as hard as its grade: better fish do more damage and are bigger.
  - **What you catch is what you get:** hook a Pufferfish and Pufferfish go in your bucket. Hover a grade in the bucket to see which species you have.
  - **Every species has an ability** when Fish Toss throws it (`FISH_AB` in `index.html`). It's shown on the catch card, on fish pickups and at Old Gil's stall:
    - **Puff burst (AoE):** Pufferfish (widest) and Boxfish burst on impact and hit every cat around them.
    - **Zap:** the Eel zaps up to two more cats nearby.
    - **Stinger:** Lionfish and Stingray leave a stinging cloud that hurts cats inside it.
    - **School:** Sardines split into two little fish on the first hit.
    - **Lure light:** the Anglerfish steers itself towards the nearest cat.
    - **Piercing / Lance:** Salmon goes through one more cat, the Marlin through two more.
    - **Fierce:** Koi, Calico Koi, Red Betta and Moorish Idol have a 25% chance of a double-damage hit (CRIT!).
    - **Bouncy:** Blue Betta, Clownfish, Goby and Fancy Goby bounce on to another cat.
    - **Sticky:** Black Moor, Manta Ray and Flounder slow the cat they hit.
    - **Heavy:** Bluefin Tuna, Catfish and Sunfish knock cats back much harder.
    - **Speedy:** Mackerel, Trout and Blue Tang fly 40% faster.
    - **Lucky gold:** Goldfish and Golden Arowana have a 20% chance to drop a coin.
    - **Soothing:** Butterflyfish and Seahorse heal you a little with each hit.
    - Fish scraps and evolved weapons have no ability.
  - **Fish you don't throw stay** for the next run. The HUD's **Fish** pill shows how many are left; it turns red under 50.
  - **Empty bucket:** you throw **fish scraps**, which do 25% less damage.
  - **New saves** start with 300 Sardines. **Older saves** are scaled up to the new crate sizes once.
  - **Three ways to get fish:**
    - **Old Gil** sells crates: 100 Sardines for 40, 50 Mackerel for 90, 25 Bluefin Tuna for 180, 10 Swordfish for 320 (or ×5). The Golden Koi isn't for sale. You can **haggle** once per visit: a 55% chance of 20% off, otherwise prices go up 10%.
    - **Fishing off your boat:** a full-screen side view under the boat. It costs no gold and has no cooldown: fish as much as you like.
      - **Pick a bait:** Bread is free. Better bait is paid for with fish from your bucket: Worm costs 5 common fish, Shrimp 3 nice fish, Squid 2 great fish.
      - **Cast**, then **steer the hook** with the mouse, touch or arrow keys. The line stays out until something bites or you reel in (Space / Reel in).
      - **The deeper you go, the rarer the fish:** Shallows (common), Reef (nice), Open sea (great), Deep (rare) and Abyss (legendary).
      - **Fish that see the hook come and bite.** Fish see only what's in front of them.
      - **Rare fish swim away from weak bait.** Each bait is good up to a grade: Bread for common, Worm for nice, Shrimp for great, Squid for rare. Each grade above that makes a fish more likely to flee.
      - **Sneak up from behind:** touching any fish with the hook from behind snags it, whatever the bait.
      - **A bite is reeled in on its own.** The whole catch of that species goes in your bucket, for example 60–100 of a common fish or 3–5 of a legendary one; better bait lands a bit more.
      - **Fits any screen:** the sea fills the screen above the bait bar and gets taller on a phone in portrait.
    - **In the maps:** 🐟 **+FISH** pickups put a small catch in your bucket. ⬆️ **FISH UPGRADE** pickups (from 1:30) make every fish you throw for the rest of the run count as one grade better. The results screen shows how many fish you threw and found.
- **Fish types:** everything you throw is a real fish from **`assets/fx/fish_types.webp`** (30 species, from sardines to a golden arowana). Each fish grade adds more and fancier fish to the bucket Fish Toss picks from: 6 at first, 30 with the Golden Koi. Salmon Run throws salmon, Golden Catch throws a glowing golden arowana, and Tuxedo Cats' Fish Missiles are random fish.
- **Gold** collected in a run is kept, even if you're overrun. You spend it on two things:
- **Skill Tree:** three branches. Each node needs the one above it before you can buy it, and existing purchases carry over.
  - 🎣 **Angler** (damage → speed → area → duration → cooldown → +1 projectile → +1 more projectile)
  - ⚓ **Sailor** (max HP → regen → move speed → armor → Life Ring revive)
  - 🍀 **Fortune** (gold → pickup range → Treasure Nose → luck → XP)

  Skills are refundable at any time.
- **Cat Home decorations:** Catgrass, Cushion, Moon Lamp, Fish Tank, Cat Tower, Water Fountain, Fireplace and Window Hammock. Each adds **Comfort** (15 max). Comfort:
  - multiplies every affection gain (+6% per point)
  - raises how much affection petting and play can earn per visit
  - gives every cat a welcome-home affection gift after each run
  - makes cats go and lounge on the furniture (which earns extra affection)
- **Fishers:** six playable characters, each with a starting weapon and bonus — unlocked by surviving 5:00, reaching level 20, collecting 1,500 gold, feeding the Narwhal Cat, and clearing a full run.
- **Areas:** Cat Town → Willow Park (survive 10:00 in Cat Town) → Sunny Beach (survive 10:00 in Willow Park). Existing progress carries over: the old Meadow, Market and Pier saves count as Town, Park and Beach.
- **Cat Home:** every new type of cat you feed moves in for good. Tap **🏠 Visit your cats** to squish them: press to squash, hold to squash deeper, and let go to make them boing back (a long squish makes them hop). You can also carry them (hold and drag), use the 🔴 laser, toss 🧶 yarn, or buy 🐟 treats (5 gold). Affection fills **hearts (0–5)**, and each heart gives a small bonus in every run (each cat's bonus is shown on its card and in the Cat Home tab).

Progress is saved in the browser's localStorage (`chumstorm_save_v2`, `chumstorm_collection_v1`).

## UI pack
**`assets/ui/ui_pack.webp`** supplies:
- **Harbor menu bar:** its tab buttons (Home, Pets, Tackle, Skills, Shop, Explore, Missions) form the bar at the bottom of the harbor. Tapping one walks you into that building; Missions highlights your requests.
- **HUD icons:** the coin, fish, heart and lightning icons.
- **Locals:** the alert and coin badges over their heads.

Buttons, cards and level-up choices are restyled to match: chunky outlined yellow and green buttons, gold-rimmed cream panels and ribbon titles.

## Head + body characters
The character sheet is **`assets/player/characters.png`** (`.webp` / `.jpg` also work): 4 × 4 characters on a flat background. The game finds the gaps between the characters, then cuts each one apart:
- **Head:** everything above the chin, found where the face's skin runs out.
- **Torso:** the rest of the upper body, with the original owner's hair colour stripped from the chest so heads can be swapped. A few tufts of long hair can remain.
- **Arms:** whatever sticks out past the waist on each side, but only if it ends in a skin-coloured hand.
- **Legs:** the two columns at the bottom.

**Switched off for now:** the avatar is the PSD paper doll again (`HB_ENABLED = false` in `index.html`). The head + body cuts are still in the code: set the flag to `true` to bring back the **Head + Body** mode in the Wardrobe, where you pick any head and any body and walking swings the legs and arms. `?debug#chars` shows every cut for checking.

## Avatar = the PSD
**`assets/player/avatar_layers.psd`** is the avatar's source of truth:
- **What it controls:** only the pieces in it can be worn. Each is drawn with the layer's own pixels at the layer's own position, so moving, resizing, repainting or deleting layers in Photoshop all carry over.
- **Wardrobe:** the tabs and items show only what the PSD has, and saved outfits fall back to pieces that still exist.
- **Layer names:** must start with their id (`hair:12`, `head:3`). The hidden `#layout` layer maps the canvas onto the body.
- **Debug tools:** with `?debug`, the Wardrobe can **Export all layers as PSD** (a fresh file of every piece) or **Use a PSD** (load a file and save it as `avatar_layers.psd`).
- **Without the PSD:** the game falls back to the sheets and the built-in placement.

## Performance
- **Tilt-shift blur:** done inside the 3D camera's WebGL shader as a cheap 5-tap blur at the top and bottom of the view. A full-screen CSS `backdrop-filter` was much too slow on weaker graphics cards.
- **No extra frame copy:** the WebGL context no longer keeps its drawing buffer (`preserveDrawingBuffer:false`).
- **Automatic quality:** during a run the game watches the frame rate. If it stays under about 45 fps for 1 second, it drops one step and remembers it in `localStorage` (`chumstorm_quality`):
  - **0:** full quality
  - **1:** no tilt-shift blur and no lens curve
  - **2:** also fewer particles
  - **3:** also a flat camera (no 3D tilt)
- **Graphics switch:** the pause screen has **Auto / Fancy / Fast**. Auto steps down by itself, Fancy always uses full quality, and Fast always uses the flat camera with no blur and fewer particles. The choice is remembered (`chumstorm_quality_mode`).
- **Forcing a level:** add `?quality=0` … `?quality=3` to the URL to force a level, or `?quality=auto` to clear the saved level and mode.
- **Profiling:** with `?debug&prof`, `window.__prof` shows the average milliseconds per frame for update, render and each draw pass.

## Testing shortcuts
Add `?debug` to the URL: **L** level up · **T** skip 60 s · **C** spawn a treasure box · **U** spawn every power-up, an artifact and all three chest tiers, plus the three one-time items · **X** spawn a treasure spot now · **I** fill the item bag · **K** feed every cat · **H** heal · **G** +1000 gold (in the harbor) · **B** a local walks up now (in the harbor) · **P** the Princess comes for Sebastian (in the harbor; counts every other town cat as met for this visit) · **R** Sebastian appears now (in a Cat Town run with her request). Dispatch `new CustomEvent("cs-step", {detail: frames})` on `document` to advance the game or Cat Home by hand.
With `?debug`, `window.CS` in the browser console opens any screen or pop-up. For example: `CS.building('shop')`, `CS.talk('princess')`, `CS.pay()`, `CS.home()`, `CS.intro(25)`, `CS.run()`, `CS.levelUp()`, `CS.chest()`, `CS.pause()`, `CS.results()`, `CS.mission()`, `CS.discover('tortie')`, `CS.loot()`, `CS.banner()` and `CS.fish()` (fishing, in the harbor). `CS.bag()` shows the fish bucket, `CS.onlyFish(species, n)` fills the bucket with one species for testing abilities (not saved), and `CS.fishStep(dt)` advances the fishing game by hand. Screenshots of every screen are in **`docs/ui_screens/`** (open `index.html` there).

## Important files
- `index.html` — the whole game (HTML, CSS and JS in one file)
- `chum-storm.html` — matching standalone copy
- `assets/` — player, cat, fish and grass PNGs (`assets/cats/sea_cats.webp` is the sea-cat sheet)
