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

Phase 5 is complete when:
- [ ] CoachClient activated, Edge Function deployed
- [ ] Generation UI available to instructor (not students)
- [ ] Automated validation catches schema errors before review queue
- [ ] Review queue functional — approve/edit/reject per question
- [ ] 50+ approved questions in the bank across all 5 domains
- [ ] Exam simulation mode functional (90Q / 90min / domain breakdown)
- [ ] Export to MDX script working
