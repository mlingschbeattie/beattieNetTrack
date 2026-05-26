# Demo Flow Runbook

Use this runbook to present the LMS with a complete functional loop:

1. Lesson
2. Activity
3. Lab
4. Review quiz

Each flow below is pre-wired to track/module mappings and validated.

## Demo Prep (2-3 min)

1. Open the LMS home page.
2. Confirm track cards load.
3. Confirm progress storage is clear (optional for fresh demo):
   - Browser devtools -> Application -> Local Storage
   - Remove key: `beattie_progress_v1`
4. Keep one tab open to the target track page for fast recovery.

## Flow A: PC Technician - Hardware Troubleshooting (8-10 min)

### Objective
Show practical diagnostic workflow under ticket pressure.

### Sequence
1. Lesson:
   - `/lessons/pct-troubleshooting-hardware`
2. Activity:
   - `/workspace/activity/pct-hardware-ticket-debrief`
3. Lab:
   - `/labs/pct-hardware-triage-lab`
4. Review quiz:
   - `/quizzes/pct-troubleshooting-hardware`

### Live Talk Track
1. In lesson: emphasize "symptom first, theory second, verification before closeout."
2. In activity: narrate triage order and why each step is low-risk/high-signal.
3. In lab: complete all validated steps and call out closure-note quality.
4. In quiz: submit and show score/progress behavior.

## Flow B: PC Technician - Windows Security (8-10 min)

### Objective
Show endpoint hardening + incident triage as a complete technician workflow.

### Sequence
1. Lesson:
   - `/lessons/pct-windows-security`
2. Activity:
   - `/workspace/activity/pct-windows-incident-triage`
3. Lab:
   - `/labs/pct-windows-security-hardening-lab`
4. Review quiz:
   - `/quizzes/pct-windows-security`

### Live Talk Track
1. In lesson: focus on containment, baseline controls, and communication.
2. In activity: explain what triggers cleanup vs reimage decisioning.
3. In lab: show hardening checks (containment, Defender, startup triage, BitLocker).
4. In quiz: show retained knowledge check with pass threshold.

## Flow C: Cybersecurity Foundations - CIA + Risk (8-10 min)

### Objective
Show foundational security reasoning moving from concepts to action.

### Sequence
1. Lesson:
   - `/lessons/intro-to-cybersecurity`
2. Activity:
   - `/workspace/activity/cfs-cia-triad-classifier`
3. Lab:
   - `/labs/cfs-security-baseline-lab`
4. Review quiz:
   - `/quizzes/cfs-intro-cybersecurity-review`

### Live Talk Track
1. In lesson: classify by confidentiality, integrity, availability first.
2. In activity: justify primary CIA category when multiple are impacted.
3. In lab: map incident -> risk priority -> immediate control -> layered defense.
4. In quiz: close with competency signal and progression.

## Optional Track Entry Points

- PC Technician track: `/tracks/pc-technician`
- Cybersecurity Foundations track: `/tracks/cybersecurity-foundations`

## Troubleshooting During Demo

1. If a page fails to render:
   - Return to track page and reopen item from module card.
2. If progress appears stale:
   - Refresh once; if needed clear `beattie_progress_v1` and retry.
3. If a lab check fails unexpectedly:
   - Re-read the exact expected wording in prompt hints and retry.

## Timing Plan (30 min total)

1. Intro + context: 3 min
2. PC Hardware flow: 8 min
3. Windows Security flow: 8 min
4. Cybersecurity Foundations flow: 8 min
5. Wrap + Q&A: 3 min

## Validation Snapshot

Last verified in repo before this runbook:

1. `npm run validate:tracks` passed
2. `npm run lint` passed (no errors)
