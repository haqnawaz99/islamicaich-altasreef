# واقعية التشغيل والاستكمال — Sustainability / Operating Plan

## What already exists and keeps running regardless of the hackathon outcome

The host platform, Altasreef (morphology.haqnawaz.org), is a live, actively
maintained production service — not a hackathon prototype that disappears after
judging. It has real infrastructure (Postgres, systemd, CI/CD via GitHub
Actions, SSL via Let's Encrypt), real users, and an owner who has operated it
daily for months. This submission's feature is additive to that platform, not
a one-off demo that has nowhere to live afterward.

## Immediate next steps if selected

1. **Merge into the production repo.** This repo is intentionally a standalone
   extraction for public judging; `/explain` and `/ilal` are designed to be
   dropped into the existing `backend/routes/` as a real route once reviewed,
   reusing the same auth/rate-limit pattern every other Altasreef route already
   follows (see the private repo's own `limiter.py` convention).
2. **Human review of every rule** before it reaches a real student — see
   `reliability_plan.md` §7. This is a hard gate, not a formality.
3. **Wire into both existing clients**, not a new surface: the web app's
   `EvaluationQuestion.jsx` (wrong-dim branch) and the Android app's
   `evaluation_screen.dart` (same insertion pattern) — both already exist,
   both are live, both have real users today.

## Ongoing maintenance cost

- **Rule DB growth is incremental, not a rewrite.** The same production export
  (`export_wrong_answer_breakdown.py`) can be re-run periodically (monthly, or
  triggered by a real usage milestone) to find the next-highest-frequency
  uncovered confusion, and a new rule is one JSON entry plus a human review —
  no architecture change needed as coverage grows.
- **No ongoing LLM API cost** — the retrieval-only design means there is no
  per-explanation inference bill to budget for, unlike a live-generation
  approach. The only cost is authoring time, which scales with real teaching
  value (each new rule serves real recorded confusion, not a guess).
- **No new infrastructure to operate long-term.** The production merge target
  already has hosting, monitoring, and deploy automation in place.

## What would need deliberate investment, not assumed to happen automatically

- Expanding `/ilal` beyond اجوف واوی/باب نصر to other weak-verb classes is real
  linguistic authoring work, not a mechanical extension — scoped as a
  deliberate future task, not promised here.
- Full i18n parity (the rule DB currently ships English + Arabic Tier-A text;
  the live platform is quadrilingual) needs the same human-review gate applied
  per language before being trusted as a certification-level feature.
