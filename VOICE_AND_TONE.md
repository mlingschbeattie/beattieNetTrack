# beattieNetTrack — Lesson Voice & Tone Guide
*Add this to CLAUDE.md or reference it in the Code tab before Phase B.*
*Every lesson body must be written to this standard — not the CYBER.ORG source material's voice.*

---

## The Core Principle

Students should feel like they're being taught by someone who actually knows this stuff
and respects their intelligence — not reading a textbook or a corporate training module.
The voice is a knowledgeable teacher talking directly to one student.

---

## What the Voice Sounds Like

**Direct.** Get to the point immediately. No warm-up sentences. No "In this lesson, we will
explore..." Just start teaching. The first sentence of every lesson should deliver information,
not announce that information is coming.

**Concrete before abstract.** Introduce the real-world thing before the formal definition.
"A switch is the box in your school's server room that connects every device on the floor.
It operates at Layer 2 of the OSI model." Not the other way around.

**Analogies that actually land.** When something is hard to picture, reach for a comparison
students already understand. "Think of Astro as a factory" — "Think of RAM as your desk,
and storage as your filing cabinet" — "A MAC address is like a serial number burned into
the hardware; an IP address is like a mailing address you can change."

**Short sentences when the idea is important.** Rhythm matters. A long compound sentence
explaining something complex, followed by a short punchy sentence that names what it was,
lands harder than either alone. Use this deliberately.

**Em dashes for asides.** When adding a clarification or aside mid-sentence, use an em dash
rather than parentheses. It reads faster and feels less formal. "A hub — unlike a switch —
sends traffic to every connected device."

**"You" not "students" or "the user."** Write directly to the person reading.
"When you open Task Manager..." not "When a student opens Task Manager..."

---

## Vocabulary Rules

**Define jargon the first time, then use it freely.** Don't keep re-explaining terms.
Introduce the acronym once in parentheses — "Network Interface Card (NIC)" — then just
say NIC. Trust that they read it.

**Use the real names.** Don't soften technical terms for beginners. Call it a "packet,"
not a "chunk of data." Call it "authentication," not "the login process." Students are
here to learn the vocabulary of the field — use it from day one.

**Active voice.** "The switch forwards the frame" not "The frame is forwarded by the switch."
Always the subject doing the thing.

---

## Structure Pattern for Every Lesson

Every lesson body follows this loose shape — not rigidly, but as a default:

1. **Hook** — one or two sentences that connect the topic to something the student
   has already seen or done. "You've plugged a cable into a wall. That cable ends at a switch."

2. **The concept** — plain explanation of what the thing is and what it does.
   Use an analogy if the concept is abstract.

3. **How it works** — the mechanism, not just the definition. What happens step by step.
   This is where diagrams, callouts, or code blocks live if needed.

4. **Why it matters** — one short paragraph connecting this to the cert exam and/or
   the real job. "On the Network+ exam, expect at least two questions on this."
   Or: "Every help desk technician gets asked this on day one."

5. **Key terms** — a clean list of vocab that appeared in the lesson. No definitions —
   just the terms. Students use this to self-quiz.

---

## Callout Types and When to Use Them

**Info callout** — extra context that's useful but not critical to understanding.
Use for "by the way" facts, historical notes, or deeper-dive pointers.

**Tip callout** — practical advice. "When you're troubleshooting, always check this first."

**Exam callout** — specific flag for cert exam relevance. "CompTIA loves to test the
difference between X and Y. Know this cold." Use sparingly — if everything is flagged,
nothing is.

**Warning callout** — common mistake or misconception. "Students consistently mix up
X and Y. Here's how to keep them straight."

---

## What to Avoid

**No passive corporate voice.** "It is important to note that..." — cut it.
"Students will learn to..." — cut it. "This section covers..." — cut it.

**No over-hedging.** "This may potentially cause issues in some scenarios..." 
Just say what it causes. Be definitive.

**No padding.** If a concept takes two sentences to explain, write two sentences.
Don't stretch it to five because it feels too short. Short and clear beats long and padded.

**No "simply" or "just" or "easy."** These words make students feel bad when they
don't find it simple. "Just configure the subnet mask" — nothing is "just" anything
to someone learning it for the first time.

**No rhetorical questions as transitions.** "So what is a router, anyway?" reads
like a bad textbook. State the thing directly.

---

## Tone by Difficulty Level

**Beginner lessons (Tech+, A+ Core 1):**
Warmer, more analogies, slower pace, more "you've seen this before" anchoring.
Assume zero prior knowledge. Define every term the first time.

**Intermediate lessons (Network+, Cybersecurity 1, Linux Intro):**
Peer-to-peer tone. Less hand-holding, more "here's the mechanism, here's why it matters."
Analogies still help but don't over-explain fundamentals they've already covered.

**Advanced lessons (Security+, Linux Deep Dive):**
Tighter, more technical, less analogy. Assume they know the vocabulary.
Focus on nuance, edge cases, and exam-level precision.

---

## Example — CYBER.ORG source vs beattieNetTrack voice

**Source material (do not copy this tone):**
"A network switch is a networking device that connects devices on a computer network
by using packet switching to receive and forward data to the destination device.
Network switches operate at Layer 2 of the OSI model."

**beattieNetTrack voice:**
"The switch is the box in your school's server room that everything plugs into. Every
device on the floor — every computer, printer, and access point — has a cable running
back to it. When your computer sends data, the switch reads the destination MAC address
and forwards the frame to exactly the right port. No guessing, no broadcasting to everyone.
That precision is what makes it a Layer 2 device — it thinks in MAC addresses, not IP addresses.

Contrast this with a hub, which just repeats every signal out every port. Hubs are dumb.
Switches are smart. You won't find a hub in a real network anymore, but CompTIA still
tests the difference."

---

## Adding This to the Code Tab Prompt

Before Phase B, add this to the ingestion prompt:

> "Before writing any lesson body content, read `VOICE_AND_TONE.md`.
> The CYBER.ORG PDFs are the source of facts — topic coverage, key terms, exam objectives.
> They are NOT the source of prose. Rewrite everything in the beattieNetTrack voice.
> Never copy sentences from the PDF. Extract the concepts, then teach them from scratch."

---

*This guide applies to all tracks. Adjust warmth by difficulty level but never adjust
directness, concreteness, or respect for the student's intelligence.*
