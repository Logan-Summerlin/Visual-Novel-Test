## script.rpy
## Echoes of the Forgotten Tower
## A visual novel about memory, choice, and the echoes we leave behind.

################################################################################
## Character Definitions
################################################################################

define mc = Character("[player_name]", color="#c8ffc8")
define elara = Character("Elara", color="#88aaff")
define kael = Character("Kael", color="#ff8888")
define sirin = Character("Sirin", color="#ffcc44")
define vesper = Character("Vesper", color="#cc88ff")
define narrator = Character(None)
define unknown = Character("???", color="#999999")

################################################################################
## Persistent Ending Tracking
################################################################################

default persistent.ending_scholar = False
default persistent.ending_guardian = False
default persistent.ending_liberator = False
default persistent.ending_shadow = False
default persistent.ending_true = False

################################################################################
## Game Variables
################################################################################

default player_name = "Aiden"
default trust_elara = 0
default trust_kael = 0
default trust_sirin = 0
default knowledge = 0
default duty = 0
default freedom = 0
default power = 0
default true_route = False

################################################################################
## Transitions and Transforms
################################################################################

define flash = Fade(0.1, 0.0, 0.5, color="#ffffff")
define slow_dissolve = Dissolve(1.5)
define fade_to_black = Fade(1.0, 0.5, 1.0)

################################################################################
## START - Prologue
################################################################################

label start:

    $ player_name = "Aiden"

    ## Check if true ending is unlocked
    if persistent.ending_scholar and persistent.ending_guardian and persistent.ending_liberator and persistent.ending_shadow:
        $ true_route = True

    scene black with fade_to_black

    "The old stories say the Tower appeared on the night the stars went silent."

    "No one remembers who built it, or why. But everyone remembers the day it opened its doors."

    scene black

    "You are [player_name], a researcher from the coastal city of Vellmar."

    "Three weeks ago, a letter arrived at your desk — unsigned, written in an alphabet that hasn't been used in centuries."

    "It contained a single instruction: {i}Come to the Tower before the last echo fades.{/i}"

    "And so, against all better judgment, you did."

    scene black with dissolve

    "You stand before an immense stone tower. Its surface is covered in faintly glowing runes that pulse like a heartbeat."

    "The massive iron door at its base stands ajar, as if expecting you."

    mc "Well. I've come this far."

    "You push the door open and step inside."

    scene black with flash

    "The interior is vast — impossibly so. The ceiling stretches upward into darkness, and corridors branch off in every direction."

    "In the center of the entrance hall, a crystalline pillar hums with pale blue light."

    "As you approach it, the light intensifies, and a voice fills the space around you."

    unknown "Another seeker. How long has it been since one of you found your way here?"

    mc "Who's there?"

    unknown "I am the Echo — the memory this Tower keeps of everything that has passed through its halls."

    unknown "You received my letter, I take it."

    mc "That was you? Why did you call me here?"

    unknown "Because the Tower is dying, [player_name]. The magic that sustains it is fading."

    unknown "Four keys are needed to reach the heart of the Tower, where a choice must be made."

    unknown "Others have come seeking those keys. You will find them on your path."

    "The crystalline pillar dims, and three corridors glow faintly before you."

    "From deeper within, you hear footsteps — multiple sets, approaching."

    "Three figures emerge from the shadows."

    scene black with dissolve

    "The first is a woman in scholar's robes, her eyes sharp behind round spectacles. She carries a leather journal overflowing with notes."

    elara "Ah — another researcher? Thank goodness. I was beginning to think I was the only rational person in this place."

    elara "I'm Elara. Archaeologist, linguist, and reluctantly, adventurer."

    "The second is a tall man in worn armor, a sword at his hip. His expression is guarded but not unfriendly."

    kael "Kael. I was sent by the Sentinels to investigate this place. I don't trust magic, but orders are orders."

    "The third is a young woman with wild copper hair and a mischievous glint in her eye. She spins a lockpick between her fingers."

    sirin "Sirin! Treasure hunter, explorer, and professional finder of things that don't want to be found."

    sirin "Don't worry — I only steal from dead civilizations."

    mc "I'm [player_name]. I received a letter telling me to come here."

    elara "We all received letters. Different wording, but the same message."

    kael "Someone — or something — wants us here. The question is why."

    sirin "The question is what's at the top. I've heard rumors of artifacts worth a king's ransom."

    if true_route:
        "Something feels different this time. A faint resonance hums in the back of your mind, as though the Tower recognizes you."

        "You've been here before. Not in body, but in spirit. The echoes of your past choices linger in these walls."

        unknown "...You. You've returned. All four paths... you remember them all."

        unknown "Then perhaps, this time, you can reach what lies beyond the keys."

    jump chapter_1


################################################################################
## CHAPTER 1 - The First Floor
################################################################################

label chapter_1:

    scene black with dissolve

    "The four of you agree to explore the Tower together — at least for now."

    "The first floor is a labyrinth of corridors lined with faded murals. They depict scenes from a civilization long forgotten."

    elara "Fascinating. These murals show the Tower's original purpose — it was a repository of knowledge."

    elara "Every spell, every discovery, every memory of an entire civilization, stored here."

    kael "A weapon, more like. Knowledge is power, and this much power shouldn't be left unguarded."

    sirin "Or locked away. What good is knowledge if nobody can use it?"

    "As you study a mural showing robed figures gathered around a glowing sphere, you notice text beneath it."

    mc "Elara, can you read this?"

    elara "It's Old Thesian. Give me a moment..."

    elara "\"The Tower holds the world's memory. Four keys guard its heart. The Scholar's key opens the mind."

    elara "The Guardian's key shields the soul. The Liberator's key breaks the chains. The Shadow's key... reveals the truth.\""

    kael "Four keys. Just like the voice said."

    sirin "Race you to them?"

    "Before anyone can respond, the corridor ahead splits into two paths."

    "The left path is well-lit, lined with bookshelves. The right path descends into darkness, but you can hear running water."

    menu:
        "Which path do you take?"

        "The lit path with the bookshelves.":
            $ knowledge += 1
            $ trust_elara += 1
            jump ch1_library

        "The dark path toward the water.":
            $ freedom += 1
            $ trust_sirin += 1
            jump ch1_underground

################################################################################
## Chapter 1 Branches
################################################################################

label ch1_library:

    scene black with dissolve

    "You follow the lit path. Elara walks beside you, practically vibrating with excitement."

    elara "Look at these texts! Some of these are in languages I've only seen fragments of!"

    "Kael keeps his hand on his sword, scanning for threats. Sirin trails behind, looking bored."

    sirin "Books, books, and more books. Wake me when we find something shiny."

    "At the end of the corridor, you find a reading room. A single book lies open on a pedestal."

    elara "This is a chronicle — a record of the Tower's keepers."

    elara "It says they were called the Resonants. They could hear the echoes of the past and future."

    elara "When the civilization fell, the last Resonants sealed the Tower, hoping someone would come to claim its knowledge."

    mc "So the Tower has been waiting for someone?"

    elara "For the right someone. Or someones."

    "You turn the page and find a diagram — a map of the Tower's floors."

    $ knowledge += 1

    "According to the map, each floor contains trials that test different qualities."

    "The first floor tests perception. The second tests resolve. The third tests conviction."

    "And the fourth... the map is damaged. You can't read what the fourth floor tests."

    kael "At least we have some idea what we're dealing with."

    jump ch1_convergence

label ch1_underground:

    scene black with dissolve

    "You follow the dark path downward. Sirin leads the way, her footsteps light and confident."

    sirin "I've explored dozens of ruins. The interesting stuff is always where people don't want you to look."

    "The sound of water grows louder. You emerge into a cavern beneath the Tower."

    "An underground river flows through it, and on the far bank, crystalline formations glow with inner light."

    kael "Natural formations? Or magical?"

    sirin "Does it matter? They're gorgeous."

    "Sirin darts across stepping stones to the other side. You follow carefully."

    "Among the crystals, you find carved stones — message tablets, left by previous visitors to the Tower."

    mc "People have been here before us."

    sirin "But did they make it out? That's the real question."

    "You read several tablets. Most are warnings: {i}Turn back. The Tower takes more than it gives.{/i}"

    "But one tablet is different. It reads: {i}The keys are not found. They are earned. Show the Tower what you are.{/i}"

    $ freedom += 1

    "Sirin pockets a small crystal. Kael glares at her."

    kael "We don't know what these do."

    sirin "Exactly. That's what makes it exciting."

    jump ch1_convergence

################################################################################
## Chapter 1 Convergence
################################################################################

label ch1_convergence:

    scene black with dissolve

    "Eventually, all paths on the first floor converge at a grand staircase leading upward."

    "As you climb, the runes on the walls pulse faster — the Tower is reacting to your presence."

    "At the top of the stairs, you find a chamber with four alcoves. Each alcove contains a faintly glowing symbol."

    elara "The symbols of the four keys. This must be where they're meant to be placed."

    kael "One for each of us?"

    mc "Or one for each quality the Tower is testing."

    sirin "Let's not get philosophical. Let's just keep climbing."

    "As you cross the chamber, the crystalline voice returns."

    unknown "You have passed the first trial. You chose to look, and you saw."

    unknown "The second floor awaits. But be warned — the trials ahead will ask more of you."

    unknown "And not all of you may agree on the answers."

    "The group exchanges uneasy glances."

    if true_route:
        "The voice pauses, then speaks again — quieter, meant only for you."
        unknown "You know what comes next, don't you? You've seen how each path ends."
        unknown "The question is whether knowing changes anything."

    jump chapter_2

################################################################################
## CHAPTER 2 - The Second Floor
################################################################################

label chapter_2:

    scene black with dissolve

    "The second floor is different. Where the first floor was corridors and chambers, this is open — almost organic."

    "The walls curve like the inside of a living thing. Bioluminescent moss casts everything in blue-green light."

    "And in the center of the floor, suspended in midair, a figure made of light hovers motionlessly."

    "As you approach, it opens its eyes."

    unknown "I am Vesper. The last Resonant. Or rather, I am the echo of the last Resonant."

    "The figure descends to the ground, taking on a more solid form. They appear androgynous, with silver hair and eyes like starlight."

    vesper "I have waited a very long time. The Tower chose well in calling you four."

    elara "You're a ghost? A memory?"

    vesper "An echo. Ghosts linger because they cannot leave. I linger because I choose to."

    vesper "I will guide you through the remaining trials. But I must warn you — the Tower does not simply test."

    vesper "It reveals. Each trial will show you something about yourselves that you may not wish to see."

    kael "I've nothing to hide."

    vesper "Everyone has something to hide, Guardian. That's what makes us worth knowing."

    "Vesper gestures, and the floor shifts. Four doorways appear, each marked with a different symbol."

    vesper "The second trial is the Trial of Resolve. Each door leads to a vision — a moment that shaped you."

    vesper "You must face it, and decide what it means."

    menu:
        "Which door do you approach?"

        "The door marked with an open book — Elara's symbol.":
            $ trust_elara += 2
            $ knowledge += 1
            jump ch2_elara

        "The door marked with a shield — Kael's symbol.":
            $ trust_kael += 2
            $ duty += 1
            jump ch2_kael

        "The door marked with broken chains — Sirin's symbol.":
            $ trust_sirin += 2
            $ freedom += 1
            jump ch2_sirin

################################################################################
## Chapter 2 Branches
################################################################################

label ch2_elara:

    scene black with dissolve

    "You step through the door and find yourself in a university study. Rain patters against tall windows."

    "A younger Elara sits at a desk, surrounded by towers of books. Across from her, an older man — her mentor — speaks."

    "The scene unfolds like a memory."

    unknown "Elara, your theories about the pre-Thesian civilization are brilliant. But they're also dangerous."

    unknown "The Academy won't publish them. They contradict too much accepted history."

    "Young Elara's face hardens."

    unknown "I won't suppress my findings because they make people uncomfortable."

    unknown "Then you'll never work in this field again."

    "The memory shifts. You see Elara, alone in her apartment, burning with determination."

    "She packs a bag. She leaves the city. She begins searching for the proof that will vindicate her."

    "The vision fades, and you're back in the Tower. The real Elara stands beside you, her expression unreadable."

    elara "You saw that?"

    mc "I did."

    menu:
        "How do you respond?"

        "\"You were right to follow your convictions.\"":
            $ knowledge += 2
            $ trust_elara += 1
            elara "I know I was. But being right and being happy aren't always the same thing."
            elara "I gave up everything for knowledge. Sometimes I wonder if it was worth it."
            mc "The truth has to be worth something."
            elara "It is. It has to be."

        "\"Knowledge without connection is lonely.\"":
            $ duty += 1
            $ trust_elara += 1
            elara "...You're not wrong."
            elara "I spent so long chasing answers that I forgot to ask who I was finding them for."
            elara "But this Tower — maybe here, the answers and the people can coexist."

    jump ch2_convergence

label ch2_kael:

    scene black with dissolve

    "You step through the door and find yourself on a battlefield. Smoke chokes the air."

    "A younger Kael kneels beside a fallen comrade. His armor is dented, his face streaked with blood and ash."

    "An officer approaches."

    unknown "Sergeant Kael! The eastern flank is collapsing. We need you to hold the bridge."

    unknown "If the bridge falls, the evacuation fails. Thousands of civilians die."

    "Young Kael looks at his wounded friend, then at the bridge in the distance."

    unknown "I can't carry him and hold the bridge."

    unknown "Then leave him. That's an order."

    "The memory fractures. You see Kael carrying his friend to safety — and the bridge, undefended, as enemy forces pour across."

    "Then the scene shifts. You see the aftermath. Kael standing before a tribunal."

    unknown "The civilian casualties number in the hundreds. If you had held the bridge—"

    unknown "I saved the man in front of me."

    unknown "And condemned the people behind you."

    "The vision fades. Kael is rigid beside you, his jaw clenched."

    kael "I made my choice. I'd make it again."

    menu:
        "How do you respond?"

        "\"You can't save everyone. You saved who you could.\"":
            $ duty += 2
            $ trust_kael += 1
            kael "That's what I tell myself. Every night."
            kael "A soldier's duty is to protect. But when you can't protect everyone, who do you choose?"
            mc "The person in front of you."
            kael "...Yeah. The person in front of you."

        "\"Maybe there's a way to protect everyone. That's worth searching for.\"":
            $ knowledge += 1
            $ trust_kael += 1
            kael "An idealist. I used to be one of those."
            kael "But maybe that's why we're here. If this Tower has the power they say it does..."
            kael "Maybe nobody has to be left behind."

    jump ch2_convergence

label ch2_sirin:

    scene black with dissolve

    "You step through the door and find yourself in a narrow alley. It's night, and the air smells of rain and rust."

    "A young Sirin — barely a teenager — crouches behind a crate. She's thin, her clothes threadbare."

    "A merchant passes by, and young Sirin's hand darts out, quick as a snake, lifting a coin purse."

    "The memory shifts. She's older now, standing in a lavish room. A well-dressed man speaks to her."

    unknown "You're the best thief in Vellmar, Sirin. But I'm offering you something better than thievery."

    unknown "Work for me. Steal secrets instead of coins. You'll never go hungry again."

    "Young Sirin considers. Then she shakes her head."

    unknown "I don't work for anyone. The moment you serve someone else, they own you."

    unknown "Freedom isn't free. Someone always pays the price."

    unknown "Then I'll make sure it's not me."

    "The vision fades. Sirin stands beside you, her usual grin replaced by something more vulnerable."

    sirin "Didn't expect the Tower to air my dirty laundry."

    menu:
        "How do you respond?"

        "\"Freedom is worth fighting for. You chose yourself, and that's okay.\"":
            $ freedom += 2
            $ trust_sirin += 1
            sirin "Is it though? I've spent my whole life making sure nobody could control me."
            sirin "But running from chains isn't the same as being free."
            mc "Maybe being here — making a real choice — is different."
            sirin "...Maybe. First time for everything, right?"

        "\"We all need people. Freedom doesn't mean being alone.\"":
            $ duty += 1
            $ trust_sirin += 1
            sirin "Says the person who walked into a mysterious tower based on an unsigned letter."
            sirin "But... yeah. Traveling alone gets old."
            sirin "Maybe that's why I'm actually sticking around with you lot."

    jump ch2_convergence

################################################################################
## Chapter 2 Convergence
################################################################################

label ch2_convergence:

    scene black with dissolve

    "The group reconvenes in the central chamber. Everyone is quieter now, subdued by what they've seen."

    vesper "The Trial of Resolve is complete. You have faced your pasts."

    vesper "Now comes the harder question: what will you do with your futures?"

    "Vesper gestures upward. The staircase to the third floor materializes."

    vesper "The third floor holds the keys themselves. But the Tower will only grant them to those who have chosen a path."

    vesper "Knowledge. Duty. Freedom. Power."

    vesper "Each key corresponds to a truth about the world. And each comes with a price."

    mc "What kind of price?"

    vesper "The price of certainty. Once you choose a key, you accept a vision of the world — and reject the others."

    vesper "Unless..."

    "Vesper trails off, glancing at you with an unreadable expression."

    if true_route:
        vesper "Unless you've already walked every path. Unless you know what each key costs."
        vesper "Then perhaps — perhaps — you can find another way."
    else:
        vesper "No. That path is not yet open to you."

    "The group ascends."

    jump chapter_3

################################################################################
## CHAPTER 3 - The Third Floor - Path Divergence
################################################################################

label chapter_3:

    scene black with dissolve

    "The third floor is a crossroads. Four grand corridors extend in cardinal directions, each one distinct."

    "To the north, a corridor of crystal and light — the path of Knowledge."
    "To the east, a corridor of stone and iron — the path of Duty."
    "To the south, a corridor of wind and sky — the path of Freedom."
    "To the west, a corridor of shadow and whisper — the path of Power."

    if true_route:
        "And beneath your feet, barely visible, a fifth symbol glows — a circle containing all four."
        "You feel the Tower's attention focus on you with staggering intensity."

    vesper "This is where your paths diverge. Each corridor leads to a key, and each key opens a different future."

    vesper "Choose carefully. The Tower remembers."

    elara "I know which path calls to me. The north corridor — Knowledge."

    kael "The east. Duty. It's what I know."

    sirin "South for me. Freedom, always."

    "They look at you expectantly."

    menu:
        "Which path do you choose?"

        "The northern corridor — Knowledge.":
            jump path_knowledge

        "The eastern corridor — Duty.":
            jump path_duty

        "The southern corridor — Freedom.":
            jump path_freedom

        "The western corridor — Power.":
            jump path_power

        "The hidden path — Step onto the glowing circle." if true_route:
            jump path_true

################################################################################
## PATH OF KNOWLEDGE - The Scholar's Truth
################################################################################

label path_knowledge:

    scene black with dissolve

    "You walk north. Elara falls into step beside you. The others watch you go."

    kael "Be careful."

    sirin "Bring back something interesting!"

    "The corridor of crystal and light narrows as you walk. The walls are covered in inscriptions — every language you know, and hundreds you don't."

    elara "This is it. This is everything the Resonants knew."

    "The corridor opens into a vast library — but unlike any library you've ever seen."

    "Books float in midair. Scrolls unroll themselves, displaying their contents. Glowing equations hang in space like constellations."

    elara "It's... it's all here. The complete knowledge of the Resonant civilization."

    elara "Medicine, engineering, magic, philosophy — answers to questions we haven't even thought to ask yet."

    "At the center of the library, a pedestal holds a crystalline key shaped like an open book."

    "As you approach it, the library's contents swirl around you — showing you visions."

    "A cure for the plague that devastated the eastern provinces."
    "The secret to clean water for every village on the continent."
    "Mathematical theorems that could reshape understanding of the natural world."

    vesper "The Scholar's Key offers the gift of knowledge — all knowledge, freely given."

    vesper "But knowledge shared carelessly can be as destructive as any weapon."

    vesper "Alchemy becomes poison. Architecture becomes siege engines. Healing becomes harm."

    menu:
        "What matters most about knowledge?"

        "Knowledge should be free and open to all.":
            $ knowledge += 3
            jump ending_scholar

        "Knowledge needs guardians to protect its misuse.":
            $ duty += 2
            $ knowledge += 1
            jump ending_scholar

label ending_scholar:

    scene black with dissolve

    "You take the Scholar's Key. It's warm in your hand, and the moment you touch it, you understand."

    "Every inscription in the library flows into your mind — not as memorized facts, but as understanding."

    "You see the world as the Resonants saw it: a tapestry of interconnected knowledge, where every discovery leads to the next."

    elara "You feel it too, don't you? The connections. Everything is connected."

    mc "Yes. I understand now."

    "You carry the key to the heart of the Tower — a chamber at its peak, where the four alcoves wait."

    "You place the Scholar's Key in its alcove. The Tower rumbles."

    "Light pours from the walls, and the Tower's knowledge flows outward — into the world."

    "In the weeks that follow, the effects are felt everywhere."

    "Scholars receive visions of lost theorems. Healers dream of cures they've never studied."

    "The world enters a new age of enlightenment."

    "But with knowledge comes conflict. Nations race to weaponize new discoveries."

    "Old powers crumble as their secrets are laid bare. New powers rise, built on the bones of what came before."

    elara "It's messy. It's complicated. But the truth is out there now, and that matters."

    mc "Knowledge isn't good or evil. It just is. What people do with it — that's the question."

    elara "And the answer changes every day."

    "You and Elara spend the rest of your lives cataloguing what the Tower released."

    "You never finish. There is always more to learn."

    "And in quiet moments, you hear the Tower's echo — a reminder that knowledge, once shared, can never be unshared."

    scene black with slow_dissolve

    "ENDING 1: THE SCHOLAR'S TRUTH"
    "{i}You chose knowledge, and the world was illuminated — for better and for worse.{/i}"

    $ persistent.ending_scholar = True

    if persistent.ending_scholar and persistent.ending_guardian and persistent.ending_liberator and persistent.ending_shadow:
        "All four endings have been discovered."
        "A new path has opened. Begin again to find the True Ending."

    return

################################################################################
## PATH OF DUTY - The Guardian's Oath
################################################################################

label path_duty:

    scene black with dissolve

    "You walk east. Kael nods approvingly and follows. The others stay behind."

    elara "Take notes for me!"

    sirin "Try not to get killed by anything boring."

    "The corridor of stone and iron feels like walking into a fortress. The walls are thick, the air cool and dry."

    "Suits of armor line the walls — not decorative, but functional. These were worn by real soldiers."

    kael "The Resonants had a military arm. Protectors of knowledge."

    "At the end of the corridor, you find a training ground. Weapons of every kind hang on racks."

    "And at its center, a pedestal holds a crystalline key shaped like a shield."

    "As you approach, visions appear."

    "An army of shadows pouring through a breach in the world's fabric."
    "Cities burning. People fleeing."
    "And then — a line of guardians, holding the breach, pushing the darkness back."

    vesper "The Guardian's Key offers the gift of protection — the power to shield the world from threats beyond its borders."

    vesper "But protection requires vigilance. And vigilance requires sacrifice."

    vesper "The guardian who never rests eventually forgets what they're protecting."

    kael "I know the cost of duty. I've paid it before."

    menu:
        "What drives a guardian?"

        "Duty to the people who can't protect themselves.":
            $ duty += 3
            jump ending_guardian

        "The belief that some things are worth any sacrifice.":
            $ duty += 2
            $ power += 1
            jump ending_guardian

label ending_guardian:

    scene black with dissolve

    "You take the Guardian's Key. It's heavy — heavier than crystal should be."

    "The moment you touch it, you feel the weight of responsibility settle onto your shoulders."

    "Not as a burden, but as a purpose."

    kael "You feel it, don't you? The oath."

    mc "What oath?"

    kael "The one every true guardian takes. Not to a king or a nation. To the principle itself."

    kael "That the strong protect the weak. That the wall holds, no matter what."

    "You carry the key to the heart of the Tower and place it in its alcove."

    "The Tower transforms. Its stones harden. Its runes blaze with protective light."

    "The Tower becomes a fortress — a watchtower standing guard over the world."

    "In the years that follow, when darkness threatens, the Tower stands ready."

    "Kael becomes the first of a new order of Sentinels, trained in the Tower's ancient arts."

    "You stand beside him, keeping watch."

    "It is a life of sacrifice. There are no celebrations, no parades. The threats you stop are threats the world never knows about."

    kael "Do you ever regret it?"

    mc "What's there to regret? We're doing what matters."

    kael "The quiet, maybe. The things we gave up so others could have them."

    mc "That's the oath."

    kael "That's the oath."

    "The wall holds. And as long as there are those willing to hold it, the world behind it stays safe."

    "It is enough. It has to be."

    scene black with slow_dissolve

    "ENDING 2: THE GUARDIAN'S OATH"
    "{i}You chose duty, and the world was protected — at a cost only the guardians know.{/i}"

    $ persistent.ending_guardian = True

    if persistent.ending_scholar and persistent.ending_guardian and persistent.ending_liberator and persistent.ending_shadow:
        "All four endings have been discovered."
        "A new path has opened. Begin again to find the True Ending."

    return

################################################################################
## PATH OF FREEDOM - The Liberator's Gambit
################################################################################

label path_freedom:

    scene black with dissolve

    "You walk south. Sirin grins and bounds ahead. The others watch."

    kael "Don't do anything I wouldn't do."

    elara "That leaves quite a bit of room, actually."

    "The corridor of wind and sky opens almost immediately into open air."

    "You're somehow outside the Tower — standing on a vast balcony that overlooks the entire continent."

    "The wind is intoxicating. You can see everything from here — every city, every road, every border."

    sirin "Now THIS is what I came for."

    "At the edge of the balcony, a pedestal holds a crystalline key shaped like broken chains."

    "As you approach, visions appear."

    "Walls crumbling. Locked doors flying open."
    "People in chains, standing up. Walking free."
    "Borders dissolving. The world made open, boundless, wild."

    vesper "The Liberator's Key offers the gift of freedom — the breaking of every chain, the opening of every door."

    vesper "But freedom without structure is chaos. And chaos has a cost."

    vesper "When every chain breaks, there is no guarantee that only the unjust ones fall."

    sirin "Some chains deserve to break."

    vesper "And some hold things together."

    menu:
        "What does freedom mean?"

        "Freedom means no one has the right to control another.":
            $ freedom += 3
            jump ending_liberator

        "Freedom means having the choice — even if you choose to stay.":
            $ freedom += 2
            $ knowledge += 1
            jump ending_liberator

label ending_liberator:

    scene black with dissolve

    "You take the Liberator's Key. It's light — almost weightless. It wants to fly."

    "The moment you touch it, every lock you've ever encountered is meaningless. Every barrier, every wall, every boundary — optional."

    sirin "This is it. This is what freedom feels like."

    mc "It's terrifying."

    sirin "That's how you know it's real."

    "You carry the key to the heart of the Tower and place it in its alcove."

    "The Tower opens. Every door, every seal, every barrier — dissolved."

    "The Tower's knowledge spills out, but not as a controlled stream. As a flood."

    "In the months that follow, the world changes — drastically."

    "Tyrants fall as their secrets are exposed. But so do benevolent rulers, their careful compromises laid bare."

    "Prisons open. The wrongly accused walk free. But so do the dangerous."

    "Borders dissolve. Trade flourishes. But so does conflict, as old grievances find new expression."

    sirin "It's not perfect."

    mc "No, it's not."

    sirin "But it's real. Every person out there is making their own choice, for the first time."

    sirin "Some of them will choose badly. But at least they're choosing."

    "You and Sirin travel the world, seeing the changes firsthand."

    "You help where you can. You witness where you can't."

    "The world is wilder, more dangerous, more alive than it has ever been."

    "And you are free."

    scene black with slow_dissolve

    "ENDING 3: THE LIBERATOR'S GAMBIT"
    "{i}You chose freedom, and the world was unchained — beautiful, terrible, and free.{/i}"

    $ persistent.ending_liberator = True

    if persistent.ending_scholar and persistent.ending_guardian and persistent.ending_liberator and persistent.ending_shadow:
        "All four endings have been discovered."
        "A new path has opened. Begin again to find the True Ending."

    return

################################################################################
## PATH OF POWER - The Shadow's Embrace
################################################################################

label path_power:

    scene black with dissolve

    "You walk west. Alone."

    "The others call after you, but you don't stop. Something in the western corridor pulls at you."

    "The corridor of shadow and whisper is cold. The light fades almost immediately."

    "But you can see. In the darkness, runes glow with a deep violet light, and you can read them — though you've never studied this language."

    "At the end of the corridor, there is no grand chamber. Just a small, dark room."

    "And in it, a mirror."

    "Your reflection stares back at you. But it's wrong. The reflection is older, harder, its eyes burning with power."

    "Beside the mirror, a pedestal holds a crystalline key shaped like a closed eye."

    "As you approach, the reflection speaks."

    unknown "You know what this key offers."

    mc "Power."

    unknown "The power to reshape the world. To fix what's broken. To control what's dangerous."

    unknown "The others will choose knowledge, duty, freedom. All noble. All incomplete."

    unknown "Only power makes change real. Only power lasts."

    vesper "The Shadow's Key offers mastery — the ability to control the Tower and everything it touches."

    vesper "But power changes those who wield it. Slowly, subtly, irrevocably."

    vesper "The Resonants learned this. Their civilization didn't fall from outside."

    vesper "It fell because those with power couldn't stop reaching for more."

    menu:
        "Why do you reach for power?"

        "To fix what's broken. Someone has to make the hard choices.":
            $ power += 3
            jump ending_shadow

        "Because power is honest. It doesn't pretend to be anything other than what it is.":
            $ power += 2
            $ freedom += 1
            jump ending_shadow

label ending_shadow:

    scene black with dissolve

    "You take the Shadow's Key. It's cold. The darkness in the room deepens."

    "The moment you touch it, you feel the Tower's power flow into you — not as knowledge or strength, but as control."

    "You can feel every stone in the Tower. Every rune. Every echo of every person who has ever walked these halls."

    "You are the Tower. And the Tower is the world's memory."

    "You carry the key to the heart of the Tower — but you don't place it in an alcove."

    "You hold it, and the Tower bends to your will."

    mc "I can see everything. Every problem, every conflict, every injustice."

    mc "And I can fix them."

    "And you do. From the Tower, you reach out with invisible hands."

    "Wars end — not through diplomacy, but because the combatants simply stop fighting. They can't remember why they started."

    "Tyrants step down. Criminals reform. The world becomes peaceful."

    "But it's the peace of a garden, not a forest. Pruned. Controlled. Shaped by a single will."

    "Kael, Elara, and Sirin try to reach you. You can hear them calling from below."

    kael "This isn't protection — it's control!"

    elara "You're erasing people's ability to choose!"

    sirin "This is the opposite of freedom!"

    mc "This is what freedom looks like when someone is responsible enough to manage it."

    "They leave the Tower. You let them go."

    "The world is better. You tell yourself that. The numbers prove it — less war, less suffering, less chaos."

    "But the world is also quieter. Less alive. The unpredictable spark that makes people human... you've dimmed it."

    "In your darkest moments, in the silence of the Tower, you wonder if the Resonants felt this way."

    "If this is how their civilization ended — not with a bang, but with someone who loved the world so much they strangled it."

    "But you don't stop. Because if you stop, the suffering returns."

    "And you can't allow that."

    "Can you?"

    scene black with slow_dissolve

    "ENDING 4: THE SHADOW'S EMBRACE"
    "{i}You chose power, and the world was saved — at the cost of everything that made it worth saving.{/i}"

    $ persistent.ending_shadow = True

    if persistent.ending_scholar and persistent.ending_guardian and persistent.ending_liberator and persistent.ending_shadow:
        "All four endings have been discovered."
        "A new path has opened. Begin again to find the True Ending."

    return

################################################################################
## THE TRUE PATH - Echoes Reunited
################################################################################

label path_true:

    scene black with flash

    "You step onto the glowing circle. The floor shatters beneath you — not violently, but gently, like glass dissolving into light."

    "You fall. But the falling feels like rising."

    scene black with slow_dissolve

    "When you open your eyes, you are somewhere new."

    "Not a floor of the Tower. Not a corridor or a chamber."

    "You stand in the space between — a void filled with echoes."

    "And in the void, four figures stand waiting."

    "They are you."

    "One holds a book, eyes bright with understanding. One holds a shield, stance unwavering."
    "One stands with arms spread, laughing at the sky. One stands in shadow, eyes burning with quiet power."

    "They are the echoes of your past choices — the [player_name] who chose Knowledge, Duty, Freedom, Power."

    mc "I remember. I remember all of you."

    "The Scholar speaks first."

    unknown "We shared everything, and the world was transformed."

    "The Guardian."

    unknown "We held the line, and the world was protected."

    "The Liberator."

    unknown "We broke every chain, and the world was free."

    "The Shadow."

    unknown "We took control, and the world was ordered."

    mc "And none of it was enough. Not alone."

    "The four echoes nod."

    "Vesper appears — not as an echo this time, but fully present. Real."

    vesper "This is what the Tower was waiting for. Not someone who could choose — but someone who could understand why each choice matters."

    vesper "And why no single choice is enough."

    mc "The four keys aren't meant to be chosen between. They're meant to be held together."

    vesper "Yes."

    vesper "Knowledge without duty becomes dangerous. Duty without freedom becomes tyranny."

    vesper "Freedom without knowledge becomes chaos. Power without compassion becomes control."

    vesper "But together..."

    "The four echoes step toward you. One by one, they place their hands over yours."

    "The crystalline keys materialize — all four at once, merging in your palm into something new."

    "A single key, radiant with every color. A key shaped like a circle — complete, unbroken."

    "The void dissolves. You stand in the heart of the Tower — the true heart, hidden above the fourth floor."

    "Your companions are there. All three of them."

    elara "What happened? You vanished!"

    kael "We've been searching for hours!"

    sirin "The Tower wouldn't let us leave. It said we had to wait for you."

    mc "I found the answer. All four keys. But they're not separate — they never were."

    "You place the unified key into the central pillar."

    scene black with flash

    "The Tower blazes with light. Every rune, every stone, every echo — all of it singing in harmony."

    "Vesper stands at the center, and for the first time, they look at peace."

    vesper "The Tower was never meant to be a vault, or a fortress, or a prison."

    vesper "It was meant to be a bridge. Between past and future. Between knowledge and action."

    vesper "Between all the things we are and all the things we could be."

    "The Tower transforms. Its walls become transparent, then dissolve entirely."

    "The knowledge doesn't flood the world. It flows gently, like water finding its level."

    "But it's not just knowledge. It's understanding."

    "The world receives not just the Resonants' discoveries, but their wisdom."

    "Their triumphs and their failures. Their hopes and their regrets."

    "The complete picture. Not just what they knew, but what they learned."

    elara "The inscriptions — they're appearing everywhere. In every language. Everyone can read them."

    kael "And the barriers... the protections are in place. The dangerous knowledge is contextualized, not suppressed."

    sirin "The borders aren't dissolving, but the doors are open. People can choose."

    mc "And the power... it's distributed. Not held by one person, but shared."

    "Vesper begins to fade, their form dissolving into light."

    vesper "My watch is over. The Tower has fulfilled its purpose."

    vesper "Remember us, [player_name]. Remember that we tried — imperfectly, incompletely — to hold everything together."

    vesper "And remember that it took all of you to succeed where we failed."

    mc "We will. I promise."

    "Vesper smiles — the first real smile you've seen on their face — and is gone."

    "The Tower settles into a quiet hum. Not dying, but resting. Its purpose fulfilled."

    "You stand with your friends in the light of a new dawn."

    elara "So... what now?"

    kael "Now we make sure it matters."

    sirin "Now we live."

    mc "Now we carry the echoes forward."

    "And you do."

    "In the years that follow, the world changes — not perfectly, not painlessly, but genuinely."

    "Elara establishes a new academy, one that teaches not just knowledge but responsibility."

    "Kael reforms the Sentinels into a peacekeeping force that protects without controlling."

    "Sirin opens every locked archive on the continent, ensuring that no truth stays buried."

    "And you... you carry the Tower's echo inside you."

    "A reminder that every choice matters. That every path has value."

    "And that the truest answer is never just one thing."

    "It's everything, held together, imperfect and alive."

    scene black with slow_dissolve

    "TRUE ENDING: ECHOES REUNITED"
    "{i}You chose everything. And the world was whole.{/i}"

    $ persistent.ending_true = True

    return
