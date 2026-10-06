"""
RESEARCH TRAIL, NOT A SHIPPED FEATURE -- kept here to document why the final
architecture (retrieval-only, see app/matcher.py) was chosen over this
live-LLM-generation approach. This script will not run as-is in this repo:
it expects quran_words.json/tag_codes.json from the private production
backend (not published here, see README's "Repo boundary" section) for
optional irab_wajah grounding. Point BACKEND_DATA at your own copy of those
files (or a local Altasreef checkout) to actually run it.

Standalone pilot test for AI-generated wrong-answer explanations, via OpenRouter.

Run this yourself with your own OPENROUTER_API_KEY set in the environment.
It does NOT touch the running app or any database -- it only reads the local
pilot_dataset.json (built from a real production sample) and quran_words.json
(for optional irab_wajah grounding), and calls a model through OpenRouter's
OpenAI-compatible API (https://openrouter.ai/api/v1/chat/completions).

Usage (PowerShell):
    cd ai_explanations
    pip install requests
    $env:OPENROUTER_API_KEY="sk-or-v1-...."
    python test_explanations.py                 # runs the 4 hand-picked representative cases
    python test_explanations.py --all            # runs all 30 pilot examples
    python test_explanations.py --limit 10        # runs first 10
    python test_explanations.py --model anthropic/claude-sonnet-5   # compare a pricier model

Get an OpenRouter key at https://openrouter.ai/keys (after signing in to your
existing account).
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent
BACKEND_DATA = BASE.parent / "backend" / "data"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# The 4 examples we hand-wrote gold explanations for, matched by (dim, root, matched_word)
REPRESENTATIVE = [
    ("gender", "فسد", "لَفَسَدَتَا"),
    ("root", "كفر", "کَفَرُوۡا"),
    ("case", "حصن", "الۡمُحۡصَنٰتِ"),
    ("seven_types", "خرج", "خَرَجۡتَ"),
]

DIM_LABELS = {
    "tense": "Tense", "person": "Person", "gender": "Gender", "number": "Number",
    "voice": "Voice", "mood": "Mood", "pattern": "Pattern (باب/derived form)",
    "seven_types": "Root Type (سبعہ انواع)", "root": "Root Letters",
    "noun_type": "Noun Type (اسم فاعل / اسم مفعول)", "definiteness": "Definiteness",
    "case": "Case (اعراب)",
}

SYSTEM_PROMPT = """You are an Arabic morphology (علم الصرف) tutor explaining Quran-based grammar
questions to a student who answered incorrectly.

You will be given: the real verse, the target word, its root, ONE grammatical
dimension, the correct value, and the student's wrong value. You may also be
given the word's tagged grammatical role (i'rab) in the sentence, if available.

Rules:
1. Explain ONLY the one dimension given. Ignore every other field, even if
   also wrong -- never speculate about the student's other mistakes.
2. Two tiers of claim, and you must keep them visibly separate:
   - TIER A (stated as plain fact): anything directly derivable from the
     word's own spelling, its root, its i'rab role (if given), or the literal
     text of the ONE verse provided.
   - TIER B (must be hedged): anything else -- who/what a pronoun or dual
     subject refers to, surrounding context not in the verse given, tafsir,
     or any other claim from your own background knowledge of the Quran.
     Every Tier B sentence MUST begin with one of these exact lead-ins:
     "Traditionally, this refers to..." / "For context (beyond this verse
     alone): ..." / "This is commonly understood as...". Never state a Tier B
     claim in the same unhedged voice as a Tier A one.
3. Ground the core explanation (Tier A) in something concrete: the word's
   actual letters or ending shape, or its grammatical role in the sentence if
   the dimension is case/mood and spelling alone is ambiguous.
4. 2-4 sentences total. Encouraging tone, no filler ("Great question!" etc).
5. Respond in {language}.
6. If you are not confident even a Tier A claim is correct from the given
   facts alone, say what's certain and flag the rest as uncertain -- never
   guess confidently.
"""


def load_quran_words():
    path = BACKEND_DATA / "quran_words.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_tag_codes():
    path = BACKEND_DATA / "tag_codes.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_ref(ref: str):
    """'An-Nur 24:4' -> (24, 4)"""
    m = re.search(r"(\d+):(\d+)", ref)
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2))


def find_irab_wajah(quran_words, tag_codes, ref: str, matched_word: str, lang: str):
    surah, ayah = parse_ref(ref)
    if surah is None:
        return None
    # matched_word from evaluation_answers can include a leading ل/و/ف particle
    # not present as its own token in quran_words.json -- try exact match first,
    # then a suffix match (word_text is a substring at the end of matched_word).
    candidates = [w for w in quran_words if w.get("surah") == surah and w.get("ayah") == ayah]
    for w in candidates:
        wt = w.get("word_text", "")
        if wt and (wt == matched_word or matched_word.endswith(wt)):
            code = w.get("irab_wajah")
            if code is not None and str(code) in tag_codes.get("irab_wajah", {}):
                label = tag_codes["irab_wajah"][str(code)].get(lang)
                if label and label != "—":  # em-dash placeholder = untagged
                    return label
    return None


def build_prompt(example: dict, quran_words, tag_codes, lang: str):
    dim = example["dim"]
    dim_label = DIM_LABELS.get(dim, dim)
    irab = find_irab_wajah(quran_words, tag_codes, example["ref"], example["matched_word"], lang)

    lines = [
        f"Dimension: {dim_label}",
        f"Word: {example['matched_word']}",
        f"Root: {example['root']}",
        f"Verse: {example['verse']}",
        f"Reference: {example['ref']}",
    ]
    if irab:
        lines.append(f"Grammatical role in sentence (i'rab): {irab}")
    lines.append(f"Correct answer: {example['correct_value']}")
    lines.append(f"Student's answer: {example['given_value']}")
    lines.append("")
    lines.append(f'Explain why "{example["correct_value"]}" is correct for {dim_label}, '
                  f'not "{example["given_value"]}".')
    return "\n".join(lines), irab


def call_openrouter(api_key: str, model: str, system: str, user: str):
    resp = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            # Optional but recommended by OpenRouter for their leaderboard/analytics -- harmless to include
            "HTTP-Referer": "https://morphology.haqnawaz.org",
            "X-Title": "Morphology LMS - AI explanation pilot",
        },
        json={
            "model": model,
            "max_tokens": 400,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
        timeout=60,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text}")
    data = resp.json()
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return text, usage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="run all 30 pilot examples")
    parser.add_argument("--limit", type=int, default=None, help="run only the first N examples")
    parser.add_argument("--model", default="anthropic/claude-haiku-4.5",
                         help="OpenRouter model slug, e.g. anthropic/claude-haiku-4.5 or anthropic/claude-sonnet-5")
    parser.add_argument("--lang", default="en", choices=["en", "ar", "ur", "fr", "fa"])
    args = parser.parse_args()

    lang_names = {"en": "English", "ar": "Arabic", "ur": "Urdu", "fr": "French", "fa": "Persian"}
    lang_name = lang_names[args.lang]

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: set OPENROUTER_API_KEY first, e.g.")
        print('  $env:OPENROUTER_API_KEY="sk-or-v1-...."')
        sys.exit(1)

    with open(BASE / "pilot_dataset.json", encoding="utf-8") as f:
        pilot = json.load(f)

    quran_words = load_quran_words()
    tag_codes = load_tag_codes()

    if args.all:
        examples = pilot
    elif args.limit:
        examples = pilot[: args.limit]
    else:
        examples = []
        for dim, root, word in REPRESENTATIVE:
            match = next((p for p in pilot if p["dim"] == dim and p["root"] == root
                          and p["matched_word"] == word), None)
            if match:
                examples.append(match)
        if not examples:
            examples = pilot[:4]

    system = SYSTEM_PROMPT.format(language=lang_name)

    total_prompt = total_completion = 0
    for i, ex in enumerate(examples, 1):
        user_msg, irab = build_prompt(ex, quran_words, tag_codes, args.lang)
        print("=" * 70)
        print(f"[{i}/{len(examples)}] dim={ex['dim']}  word={ex['matched_word']}  ref={ex['ref']}")
        print(f"correct={ex['correct_value']}  given={ex['given_value']}"
              + (f"  irab={irab}" if irab else "  (no irab tagged)"))
        print("-" * 70)

        try:
            text, usage = call_openrouter(api_key, args.model, system, user_msg)
        except Exception as e:
            print(f"FAILED: {e}")
            continue

        print(text.strip())
        total_prompt += usage.get("prompt_tokens", 0)
        total_completion += usage.get("completion_tokens", 0)
        print()

    print("=" * 70)
    print(f"Total: {len(examples)} calls, {total_prompt} prompt tokens, {total_completion} completion tokens")
    print("(Check openrouter.ai/activity for exact $ spent -- OpenRouter's own dashboard "
          "is the source of truth on cost, since pricing can include a small platform margin "
          "on top of the underlying model's own rate.)")


if __name__ == "__main__":
    main()
