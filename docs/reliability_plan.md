# خطة الموثوقية والسلامة العلمية — Reliability & Scientific Safety Plan

This maps the project directly onto the organizer's own scientific reference
package (المرجعية والحزمة العلمية والبيانات) and the screening rubric's largest
single category (20%).

## 1. Hallucination resistance (مقاومة الهلوسة) — abstain over invent

The organizer's own standard: *"عند غياب المرجع الكافي... تكون الأولوية للامتناع
أو التحفظ... لا لتوليد إجابة غير موثقة."*

Our answer is architectural, not a prompt instruction: **no code path in this
repository can generate explanation text.** `app/matcher.py` only ever returns
text that a human wrote in advance in `rules/wrong_answer_rules.json`, selected by
an exact `(dimension, correct_value, given_value)` key match. When no rule
matches, the API returns `{"matched": false, "reason": "no_rule"}` and the demo
page shows that abstention plainly — there is no fallback to an LLM call, no
paraphrasing, nothing generated.

We built and tested the alternative (`research/test_explanations.py`, a live
constrained-prompt LLM call) specifically to have a documented basis for
rejecting it, not as a hypothetical. The retrieval-only design was chosen
because it has zero hallucination surface *by construction*, not because we
only tuned the prompt hard enough.

## 2. Distinguishing definitive vs. interpretive claims (قطعي / اجتهادي)

Our domain is grammar, not fiqh, so the organizer's own قطعي/اجتهادي distinction
maps onto a parallel one we enforce in every authored rule: **Tier A** (a plain
fact directly derivable from the word's own spelling, root, or the literal verse
text — e.g. "this ending is the دhاضر marker, not the غائب one") versus **Tier B**
(anything requiring outside context — who a pronoun refers to, tafsir, broader
narrative). Every rule in `rules/wrong_answer_rules.json` is Tier A only by
design for this challenge's scope (pure morphology, no exegesis); the Tier A/B
split itself is carried over unchanged from the project's earlier pilot
(`research/test_explanations.py`'s `SYSTEM_PROMPT`) precisely so it's available
if/when a future rule needs to reference context beyond the verse itself.

## 3. Transparency (الشفافية) — including about our own system's limits

Two concrete disclosures ship in this submission, not just a generic "AI-assisted"
label:

- Every `/explain` response that matches a rule is labeled with its `rule_id` —
  a judge or a student can see exactly which pre-authored template fired, nothing
  is hidden behind a black box.
- The single most frequent "wrong answer" in real production data
  (`number: تثنیہ جمع ← جمع`, 145 of the top 1,627 sampled wrong answers) is a
  genuine ambiguity in Arabic's متکلم plural ending, not a real student mistake —
  our own data model scores it strictly. Rather than author a rule defending the
  strict score as correct, that rule is flagged
  `is_system_limitation_disclosure: true` and its text says so plainly to the
  student. We are disclosing a flaw in our own system as part of the submission,
  not just disclosing that AI is involved.

## 4. Reliability/attribution — grounded in real data, not assumption

Rule-authoring priority was not guessed. We pulled live production data (5,215
real `EvaluationAnswer` rows from the running Altasreef database, via
`backend/scripts/export_wrong_answer_breakdown.py`, run directly against the
production server on 2026-10-06) and ranked every real `(dimension,
correct_value, given_value)` confusion by actual frequency before writing a
single rule. The ~25 rules shipped cover over 80% of all real wrong answers ever
recorded, and the exact count is reproducible from that same export.

## 5. Not a fatwa, no independent religious ruling

This tool explains grammar, never religious rulings. It makes no claim about
tafsir, fiqh, or doctrine; `/ilal`'s derivation explanations and `/explain`'s
grammar explanations are both scoped strictly to morphology.

## 6. Privacy

No user-identifying data is used anywhere in this repository. The frequency
data behind rule prioritization is aggregate counts only (`(dimension,
correct_value, given_value) -> count`), with no student identity, session, or
individual answer ever read out of the aggregation query (see the export
script's own docstring).

## 7. Human review before being treated as final

`rules/wrong_answer_rules.json`'s `_meta.needs_human_review` is `true` on
purpose: the rules were drafted against documented morphology tables
(the project's own `taaleelat_rules.py` suffix/prefix tables), not independently
re-verified edge-case by edge-case. Final sign-off rests with the project's own
Arabic-morphology instructor (9 years teaching علم الصرف) before any rule here
is presented to a real student as authoritative.
