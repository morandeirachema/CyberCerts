# The 15-minute debrief — outline and rehearsal script

The PNPT ends with a live debrief in which you explain and defend your methodology to
senior assessors (*verify current format on TCM*). It grades communication, prioritisation,
non-technical translation, methodology defence and remediation thinking — see
[reporting & the debrief](../topics/05-reporting-and-the-debrief.md). This page turns that
into something you can rehearse out loud, twice, before you book.

> Timings below are a rehearsal budget that fits a 15-minute slot with room for questions.
> They are this repo's suggestion, not a TCM requirement.

## The outline (about 10 minutes of talking, 5 for questions)

| Minute | Segment | What you say | What it proves |
|--------|---------|--------------|----------------|
| 0–1 | **Opening** | Who you are, what was in scope, the dates, the one-sentence outcome ("external foothold to domain compromise in N steps"). | You frame an engagement like a consultant. |
| 1–3 | **Executive summary** | Overall risk level; the three findings that matter most in business terms; the single fix that removes the most risk. No tool names. | Non-technical translation, prioritisation. |
| 3–8 | **The attack chain** | Walk the path in order: OSINT → external → foothold → AD exploitation → lateral movement → domain compromise. For each hop: what you found, why it worked, how you confirmed it, what you could have done differently. | Methodology defence. |
| 8–10 | **Remediation** | Prioritised fixes mapped to the chain: what breaks the chain earliest and cheapest; quick wins vs structural changes; the PAM-style controls (tiering, credential vaulting and rotation, least privilege, monitoring) where they apply. | Remediation thinking. |
| 10–15 | **Questions** | Answer what you did and why; say "I did not test that" when true; never invent. | Honesty and depth. |

## Rehearsal script (fill the blanks from your report)

```text
Opening
  "Between <dates> I assessed <scope>. Starting from open-source information only, I
   reached <end state> by <N> steps. I will give the business summary first, then the
   technical path, then what to fix."

Executive summary
  "Overall risk: <level>, because <one reason>.
   The three findings that matter: 1) <finding, impact> 2) <…> 3) <…>.
   The one change that removes the most risk: <fix>."

Attack chain (repeat per hop)
  "Step <n>: I found <what> using <phase, not tool>. It worked because <root cause>.
   I confirmed it by <evidence>. Alternative I considered: <path>."

Remediation
  "Fix first: <control> — it breaks the chain at step <n>.
   Then: <control>, <control>. Longer term: <structural change>."

Closing
  "That is the path and the fixes. Happy to take questions on any step."
```

## Questions to expect (rehearse answers)

- Why did you choose that path rather than another? What else did you try?
- How do you know the finding is real and not a false positive?
- What is the business impact if this were exploited by a real attacker?
- Which fix would you do first if the client had one week and no budget?
- What did you *not* test, and what would you recommend testing next?
- What would a defender have seen in the logs at each step, and which control would have
  stopped you? (the repo's [attack → defense matrix](../../../attack-to-defense-matrix.md))

## Rehearsal checklist

- [ ] First run-through, timed, alone, from the filled report: under 10 minutes of talking.
- [ ] Second run-through to a listener who asks the questions above; fix every stumble.
- [ ] You can name the root cause and the control for every hop without notes.
- [ ] The executive summary contains no tool names and takes under two minutes.

## Related

- [Study plan](study-plan.md) · [Report template](../../oscp/exam-prep/report-template.md) ·
  [Exam structure](../00-overview/exam-structure.md)

## Sources

- TCM Security — PNPT certification page (report and live debrief):
  https://certifications.tcm-sec.com/pnpt/
- The evaluation criteria and preparation advice: this repo's
  [reporting & the debrief](../topics/05-reporting-and-the-debrief.md) page. Segment timings
  are this repo's suggestion; *not specified in sources*.
