# Phase 5 — AI Question Generation Engine

**Status:** Roadmap — not started  
**Prerequisite:** Phase 3 (Supabase) complete, app fully functional  
**CoachClient stub:** `src/lib/coachClient.ts` — already wired, needs activation  
**Anthropic API:** Called via Supabase Edge Function (keeps API key server-side)

---

## The Goal

Generate net-new CompTIA Network+ practice questions that:
- Are scenario-based, not recall-only
- Have one clearly correct answer and three plausible, instructive distractors
- Map to a specific N10-009 (and N10-008) objective
- Include an explanation for why each wrong answer is wrong
- Pass schema validation before any human ever reviews them
- Are reviewed and approved by the instructor before going live

This is not a replacement for CYBER.ORG content. It's a force multiplier — unlimited
novel practice questions for exam prep, generated on demand, reviewed by a human,
released to students.

---

## Why the Explanation Field Matters

The quiz schema already supports `explanation` on every question:

```yaml
- id: q1
  type: single
  prompt: "A technician notices..."
  options:
    - "A. Replace the NIC"
    - "B. Check DNS configuration"
    - "C. Reboot the switch"
    - "D. Update the firmware"
  correctIndex: 1
  explanation: "The user can ping by IP but not by hostname, which isolates
    the failure to name resolution (Layer 7 / DNS). NIC replacement (A) is
    ruled out because IP connectivity works. The switch (C) is fine for the
    same reason. Firmware (D) is a change-management action, not a
    diagnostic step."
```

CYBER.ORG quizzes don't have explanations — students just see right/wrong.
AI-generated questions populate this field on every question. That's the
learning moment: not just "you got it wrong" but "here's exactly why B is
right and why A sounds right but isn't."

---

## Architecture

```
Instructor requests questions
        ↓
[Question Generator UI] — React island, instructor-only
        ↓
POST to Supabase Edge Function: generate-questions
        ↓
Edge Function calls Anthropic API (claude-sonnet-4-20250514)
        ↓
Returns validated question JSON
        ↓
[Review Queue UI] — instructor approves / edits / rejects each question
        ↓
Approved questions written to Supabase questions table
        ↓
[optional] Export to MDX for permanent inclusion in quiz files
```

The API key never touches the browser. The Edge Function is the only thing
that calls Anthropic. This is the pattern the CoachClient stub was designed for.

---

## Question Generation Prompt (v1 draft)

This is the system prompt for the generation call. Refined over time.

```
You are a CompTIA Network+ exam question writer with 10 years of
certification exam development experience.

Generate {count} multiple-choice questions for the following:
- Certification: CompTIA Network+ ({exam_version})
- Objective: {objective_id} — {objective_title}
- Difficulty: {difficulty}  (Beginner | Intermediate | Advanced)
- Student context: High school, second year, PC fundamentals complete

QUESTION REQUIREMENTS:
- Scenario-based. Start with "A technician...", "A network admin notices...",
  "A user reports...", or similar. Not "What is X?"
- One clearly correct answer
- Three distractors that are plausible but wrong for specific, teachable reasons
- Distractors must not be obviously absurd — they should represent common
  misconceptions or related-but-wrong concepts
- No trick questions. No "all of the above" / "none of the above"
- Appropriate to the difficulty level:
    Beginner: recall + simple application
    Intermediate: scenario requiring 1-2 reasoning steps
    Advanced: scenario requiring elimination, multiple factors, or edge cases

EXPLANATION REQUIREMENTS:
- Explain why the correct answer is correct (1-2 sentences)
- Explain why each wrong answer is wrong (1 sentence each)
- Total explanation: 4-6 sentences
- Write for a student, not an examiner

OUTPUT FORMAT: Valid JSON array only. No preamble, no markdown fences.
Schema per question:
{
  "id": "gen_{uuid}",
  "type": "single",
  "prompt": "string",
  "options": ["A. text", "B. text", "C. text", "D. text"],
  "correctIndex": 0,
  "explanation": "string"
}
```

---

## Validation Pipeline

Generated questions pass through validation before the instructor ever sees them:

### Automated checks (schema + logic)
- JSON parses without error
- All required fields present (`id`, `type`, `prompt`, `options`, `correctIndex`, `explanation`)
- `options` has exactly 4 items
- `correctIndex` is 0–3
- `prompt` is scenario-based (starts with persona or situation, not "What is")
- `explanation` mentions all four answer options
- No duplicate questions (fuzzy match against existing question bank)

### Instructor review queue
Each generated question shows:
- The question and all options with correct answer highlighted
- The explanation
- The objective it maps to
- One-click Approve / Edit / Reject
- Edit mode: instructor can fix any field before approving
- Rejected questions are logged (helps improve the generation prompt over time)

### Approved questions
- Written to Supabase `generated_questions` table with status `approved`
- Tagged with `source: ai-generated`, `reviewed_by`, `reviewed_at`
- Optionally exported to MDX via `scripts/export-approved-questions.mjs`

---

## Database Schema (Supabase — Phase 5)

```sql
create table generated_questions (
  id uuid primary key default gen_random_uuid(),
  track text not null,
  module_id text not null,
  objective text not null,           -- e.g. "N10-009 1.1"
  difficulty text not null,
  prompt text not null,
  options jsonb not null,            -- ["A. ...", "B. ...", "C. ...", "D. ..."]
  correct_index integer not null,
  explanation text not null,
  status text not null default 'pending',  -- pending | approved | rejected
  reviewed_by text,
  reviewed_at timestamptz,
  created_at timestamptz default now(),
  generation_prompt_version text     -- tracks which prompt version produced this
);

-- Row Level Security: only authenticated instructors can read/write
alter table generated_questions enable row level security;
```

---

## Objective Coverage Map

Priority order for generation — highest CompTIA exam weight first:

| Priority | Objective | Domain | Weight |
|---|---|---|---|
| 1 | N10-009 5.x | Troubleshooting | 24% |
| 2 | N10-009 1.x | Networking Concepts | 23% |
| 3 | N10-009 2.x | Network Implementation | 20% |
| 4 | N10-009 3.x | Network Operations | 19% |
| 5 | N10-009 4.x | Network Security | 14% |

Generate questions in this order. Students need the most practice on the
highest-weight domains.

---

## Exam Simulation Mode

Once the question bank is large enough (target: 10+ questions per objective),
enable full exam simulation:

- 90 questions, 90 minutes (mirrors actual exam)
- Questions drawn from approved bank, weighted by domain percentage
- No question repeats within a session
- Results broken down by domain (shows students their weak areas)
- Score displayed as x/900 (matches CompTIA scoring)
- Missed questions show explanation after exam ends

This is the feature that separates beattieNetTrack from every other prep tool
a student might use. It's not Quizlet. It's a full certification rehearsal.

---

## Implementation Notes

1. **CoachClient stub** (`src/lib/coachClient.ts`) — already exists, just needs
   the Edge Function URL and activation. Read this file before starting Phase 5.

2. **Prompt versioning** — store the generation prompt version with each question.
   When you improve the prompt, old questions are still tagged with their origin.
   Lets you A/B compare question quality across prompt versions.

3. **Human review is non-negotiable** — no AI-generated question goes live without
   instructor sign-off. This is both a quality gate and a legal/academic integrity
   requirement. The review queue UI must be frictionless or it won't get used.

4. **Start with one objective** — don't generate across all objectives at once.
   Pick N10-009 1.1 (OSI model), generate 10 questions, review all 10, refine
   the prompt based on what's wrong. Then scale.

5. **Export to MDX** — approved questions can be exported into existing quiz MDX
   files, making them permanent content rather than database-only. This is the
   bridge between AI-generated and hand-crafted content.

---

## Success Criteria

Phase 5A (Instructor Batch) is complete when:
- [ ] CoachClient activated, Edge Function deployed
- [ ] Generation UI available to instructor (not students)
- [ ] Automated validation catches schema errors before review queue
- [ ] Review queue functional — approve/edit/reject per question
- [ ] 50+ approved questions in the bank across all 5 domains
- [ ] Exam simulation mode functional (90Q / 90min / domain breakdown)
- [ ] Export to MDX script working

---

## Phase 5B — Adaptive Student Mode

**Status:** Roadmap — design complete, not started  
**Prerequisite:** Phase 5A complete (approved question bank must exist for fallback)

---

### Two Modes, One Engine

**Mode A — Instructor Batch (original spec above)**  
Instructor requests questions → AI generates → instructor reviews → approved questions enter permanent bank → students see them in quizzes and exam simulation.  
Quality gate: human review required before student exposure.

**Mode B — Adaptive Student Mode**  
Student completes a lesson or quiz → system generates a fresh challenge question in real time → student answers immediately → question is consumed and discarded (or queued for instructor review).  
Quality gate: automated validation only — no human in the loop per question, but multiple safety layers prevent bad content from reaching students.

---

### Why Adaptive Without Human Review Is Acceptable Here

The risk with AI-generated content: factually wrong, misleading, or confusing questions that a student believes and internalizes incorrectly.

The mitigation strategy:

**Grounding** — the generation prompt includes the actual lesson text as context. The AI generates questions about content the student just read, not from general knowledge. Hallucination risk drops dramatically when the model is summarizing source material it was given rather than recalling from training.

**Strict schema validation** — automated checks catch structural problems before the question is shown. A question that fails validation is silently discarded and replaced with a question from the approved bank.

**Low stakes** — adaptive questions are formative, not summative. They don't affect XP, grades, or completion status. A wrong question is annoying, not harmful.

**Student reporting** — every adaptive question has a "flag this question" button. Flagged questions go to the instructor review queue. Three flags auto-retire a question from the adaptive pool.

**Fallback** — if generation fails or produces nothing that passes validation, the system falls back to a random approved question from the bank. The student never sees a failure state.

---

### Architecture

```
Student completes lesson/quiz
        ↓
[AdaptiveChallenge island] — React, client-only
        ↓
POST to Supabase Edge Function: generate-adaptive-question
  payload: { lessonSlug, moduleId, track, studentWeakAreas }
        ↓
Edge Function:
  1. Fetches lesson MDX content from storage (or passes slug)
  2. Calls Anthropic API with lesson content as context
  3. Validates response against schema
  4. If valid → returns question to client
  5. If invalid → fetches fallback from approved bank
        ↓
Student sees question, answers, gets immediate feedback with explanation
        ↓
Question logged to adaptive_questions table with student response
        ↓
If flagged → moves to instructor review queue
```

---

### Generation Prompt — Adaptive Mode

The key difference from batch mode: the lesson content is injected as context.

```
You are generating a single formative assessment question for a student who just
finished reading the following lesson content:

---LESSON CONTENT START---
{lesson_text}
---LESSON CONTENT END---

Generate ONE multiple-choice question that:
- Tests understanding of a concept from this specific lesson content above
- Is scenario-based ("A technician...", "A student notices...", "You are configuring...")
- Has one clearly correct answer supported by the lesson content
- Has three plausible distractors representing common misconceptions
- Includes an explanation citing why each answer is right or wrong
- Is appropriate for difficulty level: {difficulty}

CRITICAL RULES:
- Only test content that appears in the lesson above
- Do not introduce concepts not covered in the lesson
- The correct answer must be unambiguously supported by the lesson text
- Do not ask "what is X" recall questions — ask application questions

OUTPUT: Valid JSON only. No preamble, no markdown fences.
{
  "prompt": "string",
  "options": ["A. text", "B. text", "C. text", "D. text"],
  "correctIndex": 0,
  "explanation": "string",
  "lessonSlug": "{lessonSlug}",
  "generatedAt": "{timestamp}"
}
```

**Why grounding works:** The model is given the source material and told to only test what's in it. This is a retrieval task, not a recall task. The model doesn't need to know whether 802.11ax supports 6 GHz — it reads that from the lesson content and asks a question about it. Hallucination requires the model to invent facts; grounded generation asks it to reflect facts back.

---

### Automated Validation Gates

Every generated question passes ALL of the following before reaching a student. Failure at any gate → silent discard → fallback to approved bank.

**Gate 1 — Schema**
- JSON parses without error
- All required fields present
- `options` has exactly 4 items
- `correctIndex` is 0–3
- `explanation` is present and > 50 characters

**Gate 2 — Content Safety**
- `prompt` does not start with "What is" or "Define" (recall, not application)
- `prompt` length > 40 characters (too short = too vague)
- No option is a substring of another option (copy-paste error)
- Options are not all the same length within 3 characters (likely templated garbage)

**Gate 3 — Grounding Check (lightweight)**
- At least one key term from the lesson appears in the question prompt
- The explanation is longer than the combined length of the options (short explanations = didn't actually explain anything)

**Gate 4 — Duplicate Check**
- Fuzzy match against last 20 questions shown to this student
- Prevents the same question appearing twice in a session

Fallback trigger: any gate failure → fetch random question from approved bank for this `lessonSlug`/`moduleId` → show that instead. Student sees no error.

---

### Database Schema — Additions

```sql
-- Adaptive questions log — every generated question, shown or not
create table adaptive_questions (
  id uuid primary key default gen_random_uuid(),
  lesson_slug text not null,
  module_id text not null,
  track text not null,
  prompt text not null,
  options jsonb not null,
  correct_index integer not null,
  explanation text not null,
  difficulty text not null,
  -- Student interaction
  shown_to uuid references auth.users,
  student_answer integer,          -- null if not answered
  was_correct boolean,
  time_to_answer_ms integer,
  -- Quality signals
  was_flagged boolean default false,
  flag_reason text,
  flag_count integer default 0,
  -- Generation metadata
  generation_prompt_version text,
  passed_validation boolean default true,
  fallback_used boolean default false,
  created_at timestamptz default now()
);

-- Row Level Security
alter table adaptive_questions enable row level security;

-- Students can only see their own responses
create policy "students see own adaptive responses"
  on adaptive_questions for select
  using (shown_to = auth.uid());

-- Instructors see all
create policy "instructors see all adaptive"
  on adaptive_questions for select
  using (
    exists (
      select 1 from user_roles
      where user_id = auth.uid() and role = 'instructor'
    )
  );
```

---

### Instructor Visibility

Adaptive questions are not invisible — they're just not blocking.

Instructor dashboard shows:
- Total adaptive questions generated this week
- Pass rate through validation gates (low pass rate = prompt needs work)
- Flag queue — student-flagged questions for review
- Per-lesson breakdown: correct vs. incorrect rate on adaptive questions (signals which lessons need more depth or better explanations)
- Option to promote a high-quality adaptive question to the approved bank

The feedback loop:
```
Student struggles with adaptive questions on lesson X
→ instructor sees low correct-answer rate in dashboard
→ instructor reviews the lesson content and the questions being generated
→ either improves the lesson or adds approved questions to reinforce the concept
→ adaptive generation improves because the source material improved
```

---

### Student Experience

After completing a lesson, the student sees:

```
┌─────────────────────────────────────────────┐
│  Quick Check — Lesson Complete              │
│                                             │
│  [Question text]                            │
│                                             │
│  ○ A. [option]                              │
│  ○ B. [option]                              │
│  ○ C. [option]                              │
│  ○ D. [option]                              │
│                                             │
│  [Submit Answer]          [Skip]            │
│                                             │
│  🚩 Flag this question                      │
└─────────────────────────────────────────────┘
```

After answering:
- **Correct:** green highlight + explanation + 5 XP awarded
- **Incorrect:** red highlight + correct answer highlighted + full explanation
- **Skip:** no penalty, proceeds to next lesson

The explanation is the learning moment — not just right/wrong, but why.

---

### Difficulty Adaptation — Phase 5.5 (Future)

Initial implementation uses fixed difficulty per lesson (matching the lesson's `difficulty` frontmatter field). Future enhancement:

- Track student's correct/incorrect rate per module
- If >80% correct → increase difficulty on next generation
- If <40% correct → decrease difficulty, flag for instructor
- Difficulty adjusts per student, per module, in real time

Requires `adaptive_questions` response data to accumulate across a few sessions before the system has enough signal. Design the schema for it now; implement the logic later.

---

### Implementation Order

1. **Phase 3** — Supabase integration, `lesson_completions` table, auth
2. **Phase 5A** — Instructor batch mode (original spec) — build approved bank first
3. **Phase 5B** — Adaptive mode — add Edge Function, `AdaptiveChallenge` island, validation pipeline, fallback logic
4. **Phase 5C** — Instructor dashboard for adaptive quality monitoring
5. **Phase 5.5** — Difficulty adaptation per student

Do not build 5B before 5A. The fallback mechanism requires an approved bank to fall back to. Building adaptive mode before the bank exists means every fallback returns nothing, which breaks the student experience.

---

### Success Criteria — Adaptive Mode

- [ ] Edge Function generates grounded questions from lesson content
- [ ] All 4 validation gates implemented and tested
- [ ] Fallback to approved bank works silently on any gate failure
- [ ] `AdaptiveChallenge` island renders after lesson completion
- [ ] Student flag button works, routes to instructor queue
- [ ] `adaptive_questions` table logging all interactions
- [ ] Instructor dashboard shows generation quality metrics
- [ ] Zero student-visible error states (all failures are silent fallbacks)
