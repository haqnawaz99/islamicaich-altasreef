"""
Retrieval-only matcher for wrong-answer explanations.

No LLM call, no text generation anywhere in this module -- it looks up a
pre-authored template by exact (dim, correct_value, given_value) key, falls
back to a wildcard template for the one documented system-limitation case
(the متکلم تثنیہ جمع ambiguity), and otherwise abstains explicitly. This is
the whole point of the "retrieval, not generation" architecture: there is no
code path in this file that can produce text nobody wrote in advance.
"""
import json
import os

RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "rules", "wrong_answer_rules.json")

with open(RULES_PATH, encoding="utf-8") as f:
    _DATA = json.load(f)

# Exact-key index: (dim, correct, given) -> rule
_EXACT = {}
# Wildcard index: dim -> list of rules where correct or given is "*"
_WILDCARD = {}

for rule in _DATA["rules"]:
    dim, correct, given = rule["dim"], rule["correct"], rule["given"]
    if correct == "*" or given == "*":
        _WILDCARD.setdefault(dim, []).append(rule)
    else:
        _EXACT[(dim, correct, given)] = rule


def _fill(template: str, *, word, root, ref, correct, given):
    return (
        template.replace("{word}", word or "")
        .replace("{root}", root or "")
        .replace("{ref}", ref or "")
        .replace("{correct_label}", correct or "")
        .replace("{given_label}", given or "")
    )


def explain(dim: str, correct_value: str, given_value: str, *, word: str, root: str, ref: str, lang: str = "en"):
    """
    Returns {"matched": True, "rule_id": ..., "tier_a": str, "is_system_limitation_disclosure": bool}
    or {"matched": False, "reason": "no_rule"} -- the explicit abstain case.
    """
    if correct_value == given_value:
        return {"matched": False, "reason": "not_actually_wrong"}

    rule = _EXACT.get((dim, correct_value, given_value))
    matched_as_wildcard = False

    if rule is None:
        for candidate in _WILDCARD.get(dim, []):
            if (candidate["correct"] in ("*", correct_value)) and (candidate["given"] in ("*", given_value)):
                # Only fire the wildcard when the value it's actually about
                # (تثنیہ جمع) is really on one side -- a "*" alone should
                # never swallow an unrelated confusion this rule set hasn't
                # authored content for yet.
                if "تثنیہ جمع" in (correct_value, given_value):
                    rule = candidate
                    matched_as_wildcard = True
                    break

    if rule is None:
        return {"matched": False, "reason": "no_rule"}

    tier_a_template = rule["tier_a"].get(lang, rule["tier_a"]["en"])
    tier_a = _fill(tier_a_template, word=word, root=root, ref=ref, correct=correct_value, given=given_value)

    return {
        "matched": True,
        "rule_id": f"{dim}:{correct_value}:{given_value}",
        "matched_as_wildcard": matched_as_wildcard,
        "tier_a": tier_a,
        "is_system_limitation_disclosure": rule.get("is_system_limitation_disclosure", False),
    }
