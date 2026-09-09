# beattieNetTrack — Authoring Standard
*Add this to CLAUDE.md or reference it in the Code tab before Phase B.*
*Every lesson body must be written to this standard — not the CYBER.ORG source material's voice.*
*Sections 1–7 cover lesson prose. Sections 8–10 cover questions, quizzes, and labs, and are
binding on every assessment in the repo.*

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

---

## Questions — The Atom

Every question in this repo is graded the same way and carries the same obligation:
**a wrong answer must teach.** The schema supports an `explanation` on every question,
and `QuizRunner` shows it only when the student gets it wrong. A question without one
wastes the single best teaching moment the format offers.

**Every question requires an `explanation`.** No exceptions. Write it as the sentence you
would say to a student who just picked wrong — name why their answer was tempting and
what distinguishes the right one. Not a restatement of the correct option.

**Test mechanism, not vocabulary.** "What does DHCP stand for?" is worthless. "A laptop
gets 169.254.x.x after a reboot — what failed?" tests whether they understand what DHCP
*does*. If a question can be answered by someone who memorised a glossary and understands
nothing, rewrite it.

**Distractors must be diagnostic.** Every wrong option should correspond to a specific,
real misconception — the mistake an actual student actually makes. If you are inventing
filler options to reach four, you have not thought hard enough about how people get this
wrong. Filler distractors make a question easier, not fairer.

**Choose the type by what the student must produce:**

| Type | Use it when | Example |
|---|---|---|
| `single` | Judgement between competing plausible actions | "Which do you fix first?" |
| `multi` | Completeness matters — partial knowledge should fail | "Select every port that must be open" |
| `short` | The literal string *is* the skill | A command, a port, a broadcast address, a binary value |

`multi` grades as an exact set match — miss one correct option or add one wrong one and it
is marked wrong. That is deliberate. It is the only type that cannot be beaten by
elimination, so use it wherever "knowing most of it" should not be a pass.

`short` removes the options entirely. Use it for anything the student should be able to
produce cold: `chmod 640`, `255.255.255.0`, `587`, `11010110`. Put every reasonable
spelling in `acceptedAnswers` — the grader normalises punctuation and spacing, not synonyms.

**Never write:**
- "All of the above" / "None of the above" — they test test-taking, not knowledge
- Negation traps — "Which is NOT..." reads as a trick and fails students who understood
- Questions whose answer is given verbatim in a nearby option
- Two options that are defensibly correct

---

## Quizzes — Checkpoints and Reviews

There are two kinds and they do different jobs.

**Lesson checkpoint** — sits at the same `order` as its lesson, immediately after it.
**10–15 questions.** Covers that lesson only.

**Module review** — sits at the end of a module, after every lesson and lab in it.
**15–20 questions, drawn across the whole module.** This is the one that produces
retention: a student who crammed one lesson and dumped it cannot pass a review that
reaches back three lessons.

**Both require a mix of types.** A quiz that is 100% `single` is a recognition test, and a
student can pass a 70% threshold on four-option questions with partial knowledge and decent
elimination instincts. Target roughly:

- **60% `single`** — scenarios and judgement
- **25% `multi`** — where completeness matters
- **15% `short`** — exact recall of things that must be produced from memory

Five questions is not an assessment. Nobody learns a topic by answering five multiple-choice
questions, and nobody demonstrates mastery of one either.

`passThreshold` stays at 70 unless there is a specific reason. Add `hints` for a quiz a
student may reasonably get stuck on, and a `checklist` where the quiz has a workflow.

---

## Labs — Performance, Not Recognition

**A lab is where the student does the thing.** If every step is a `choice` validator, it is
a quiz wearing a lab costume — and most of the labs in this repo currently are. That is the
single biggest quality gap in the curriculum.

**Hard rule: no more than half a lab's steps may use `choice`.** A lab that cannot meet
that is either mis-scoped or should have been a quiz.

**Reach for a typed validator whenever the student can produce the artifact:**

| Validator | Use it for |
|---|---|
| `exact` | One correct string — a command, a value, a flag |
| `oneOf` | Several equally correct forms — `chmod 640` or `chmod u=rw,g=r,o=` |
| `regex` | A structured answer with variable content — a finding that must name two things |

`choice` is legitimate for a genuine judgement call where free text would test phrasing
rather than understanding — "which do you contain first?" — and every `choice` step **must**
carry a `rationale`, so a wrong pick still teaches.

**8–12 steps.** Four or five steps is a warm-up, not a lab. An `estimatedMinutes` of 20 with
five multiple-choice steps is a lie; the student is done in three.

**Steps must build.** A lab is a scenario that progresses — the value computed in step 3 is
used in step 6, the decision in step 4 changes what step 7 asks. Independent steps in a list
are a quiz with extra formatting. This is what makes it a lab.

**Every step carries:** a `prompt` with enough context to act on, a `hint` for the step
where students predictably stall, and a `successMessage` that confirms *why* it was right
rather than just saying "Correct."

**End with production, not selection.** The last step should have the student write
something — a closure note, a finding, a command they would run next — validated with
`regex`. It is the closest this format gets to asking them to think in their own words.

---

## Applying This to Existing Content

Content authored before this standard does not meet it. When you touch an existing quiz or
lab, bring it up to standard rather than matching what is already there — otherwise the
drift that produced 1,346 `single` questions out of 1,348 simply continues.

*This guide applies to all tracks. Adjust warmth by difficulty level but never adjust
directness, concreteness, or respect for the student's intelligence.*
