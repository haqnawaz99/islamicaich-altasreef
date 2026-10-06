"""
Taaleelat (تعلیلات) rules for Arabic verb conjugations.

Copied/ported from the quran_nlp_web project's
app/services/conjugation/taaleelat_rules.py (2026-10-05) -- that project is
kept fully separate (not committed alongside this one), but the algorithm
itself is tracked here. See CLAUDE.md if this grows into a wired-up feature.

Fully root-generic: given any اجوف واوی root (ف-و-ل shape, و in the middle
position), this derives the step-by-step grammatical transformation for a
given conjugation index -- it is not tied to a specific word like قول.
Currently covers باب نصر only (the only باب اجوف واوی supports today in the
source project), for ماضی معروف and مضارع معروف (and their منفی variants).
امر معروف is intentionally not covered yet.
"""

# ── Diacritic/letter constants (subset actually needed by this algorithm) ──
fatha = "َ"
kasra = "ِ"
alif  = "ا"
yaa   = "ی"
waw   = "و"
noon  = "ن"
Zamma = "ُ"
jazam = "ْ"
maa   = "م" + fatha + alif   # "مَا" -- ماضی negation particle
laa   = "ل" + fatha + alif   # "لَا" -- مضارع negation particle
hamzaMazmoom = alif + Zamma  # "اُ" -- امر کی اصل شکل پر ہمزۃ الوصل بالضمہ

# Ending markers per conjugation index (0-13), matching the source project's
# 14-person model (غائب 6 + حاضر 6 + متکلم 2 -- دوہری/جمع متکلم combined,
# same convention this project's own CLAUDE.md documents for ماضی).
AlaamatMaazi = [
    fatha, "َا", "ُوْا", "َتْ", "َتَا", "ْنَ", "ْتَ", "ْتُمَا", "ْتُمْ", "ْتِ", "ْتُمَا", "ْتُنَّ", "ْتُ", "ْنَا"
]
AlaamatMuzaraStart = [
    "یَ", "یَ", "یَ", "تَ", "تَ", "یَ", "تَ", "تَ", "تَ", "تَ", "تَ", "تَ", "اَ", "نَ"
]
AlaamatMuzaraEnd = [
    "ُ", "َانِ", "ُوْنَ", "ُ", "َانِ", "ْنَ", "ُ", "َانِ", "ُوْنَ", "ِیْنَ", "َانِ", "ْنَ", "ُ", "ُ"
]
UrduZameerTitle = [
    "واحد مذکر غائب", "تثنیہ مذکر غائب", "جمع مذکر غائب",
    "واحد مونث غائب", "تثنیہ مونث غائب", "جمع مونث غائب",
    "واحد مذکر حاضر", "تثنیہ مذکر حاضر", "جمع مذکر حاضر",
    "واحد مونث حاضر", "تثنیہ مونث حاضر", "جمع مونث حاضر",
    "واحد مذکر/مونث متکلم", "تثنیہ/جمع مذکر/مونث متکلم"
]

# امر only exists for حاضر persons (indices 6-11) -- there is no غائب or
# متکلم امر in Arabic. Endings per index, matching the real Arabic forms
# (قُلْ، قُولَا، قُولُوْا، قُولِیْ، قُولَا، قُلْنَ).
AMR_HAAZIR_INDICES = [6, 7, 8, 9, 10, 11]
AMR_ENDINGS = {
    6:  jazam,                          # قُلْ
    7:  fatha + alif,                   # قُولَا
    8:  Zamma + waw + jazam + alif,     # قُولُوْا
    9:  kasra + yaa + jazam,            # قُولِیْ
    10: fatha + alif,                   # قُولَا (dual has no gender distinction)
    11: jazam + noon + fatha,           # قُلْنَ
}
# Endings that themselves start with a sakin letter -- these are the ones
# that collide with the already-sakin واو after نقل (التقاءِ الساکنین) and so
# need the extra حذفِ حرفِ علت step; the rest keep their واو.
AMR_SPECIAL_INDICES = {6, 11}

# Indices (0-13) whose ending attaches directly to a sakin letter, which is
# what actually forces the extra اعلال step (التقاء الساکنین) beyond the
# basic transformation every other index gets.
#   ماضی:   غائب واحد/تثنیہ/جمع + مونث غائب واحد/تثنیہ (0-4) need only قلب
#           (واو -> الف). Everything from جمع مونث غائب onward (5-13 --
#           حاضر and متکلم all attach a sakin-starting suffix) needs the
#           full قلب -> حذف -> پیش کی علامت chain.
#   مضارع:  only جمع مونث غائب/حاضر (5, 11) attach نَ directly to the stem,
#           triggering حذفِ حرفِ علت. Every other index keeps the واو
#           (only نقل happens), including جمع مذکر (ونَ) and حاضر مونث
#           واحد (ینَ), where the stem doesn't end in a bare sakin.
MAZI_SPECIAL_INDICES = set(range(5, len(AlaamatMaazi)))
MUZARE_SPECIAL_INDICES = {5, 11}

RULE_TEXT = {
    "mazi_qalb": {
        "ur": "اگر واو مفتوح کے پہلے فتحہ ہو تو واو کو الف میں تبدیل کیا جاتا ہے",
        "en": "If و (waw) with fatha is preceded by fatha, it is converted to ا (alif)",
        "ar": "إذا كان الواو المفتوح يسبقه فتحة، يُحوّل إلى ألف",
    },
    "mazi_hazf": {
        "ur": "جب دو ساکن متصل ہوں تو الف کو حذف کیا جاتا ہے",
        "en": "When two consecutive sakin letters occur, the alif is dropped",
        "ar": "عندما يكون هناك حرفان ساكنان متتاليان، يُحذف الألف",
    },
    "mazi_damma_mark": {
        "ur": "پہلے حرف کو زبر کی بجائے پیش دی جاتی ہے تاکہ ظاہر ہو کہ حذف شدہ حرف اصل میں واو تھا",
        "en": "قَ is replaced with قُ (damma) to show that the dropped letter was originally و (waw)",
        "ar": "يتم استبدال الفتحة بالضمة على الحرف الأول لإظهار أن الحرف المحذوف كان أصلاً واو",
    },
    "muzare_naql": {
        "ur": "حرفِ علت (واو) متحرک ہو اور اس سے پہلے والا حرف ساکن ہو تو واو کی حرکت ماقبل ساکن حرف کی طرف منتقل کر دی جاتی ہے، اور واو خود ساکن ہو جاتا ہے",
        "en": "The vowel on the weak letter (و) is transferred to the preceding sakin letter (نقل), and و itself becomes sakin",
        "ar": "تُنقل حركة حرف العلة (الواو) إلى الحرف الساكن الذي قبله، ويصير الواو نفسه ساكناً",
    },
    "muzare_hazf": {
        "ur": "جب دو ساکن حروف متصل ہو جائیں تو درمیانی حرفِ علت (واو) کو حذف کر دیا جاتا ہے",
        "en": "When two consecutive sakin letters occur, the weak letter (و) between them is dropped",
        "ar": "عندما يلتقي ساكنان، يُحذف حرف العلة (الواو) الواقع بينهما",
    },
    # Exact wording already used for قُلۡ's own manually-tagged ilal_chain in
    # quran_words_test.json -- reused here verbatim so the algorithmically
    # generated chain for every other حاضر صیغہ reads consistently with it.
    "amr_naql": {
        "ur": "نقل — واو کی حرکت ماقبل ساکن حرف کی طرف منتقل کرنا",
        "en": "Naql — the vowel on و (waw) is transferred to the preceding sakin letter",
        "ar": "النقل — نقل حركة الواو إلى الحرف الساكن الذي قبلها",
    },
    "amr_hamza": {
        "ur": "اگلا حرف متحرک ہونے کی وجہ سے ہمزہ وصل کا حذف",
        "en": "Since the next letter is now voweled, the ہمزۃ الوصل (connecting hamza) is dropped",
        "ar": "حذف همزة الوصل لأن الحرف التالي أصبح متحركاً",
    },
    "amr_hazf": {
        "ur": "دو ساکن حروف جمع ہونے کی وجہ سے حرفِ علت (واو) کا حذف",
        "en": "Because two sakin letters would collide, the weak letter (و) is dropped",
        "ar": "حذف حرف العلة (الواو) لالتقاء ساكنين",
    },
}


def _steps(*keys):
    return [{"step": i + 1, "rule_text": RULE_TEXT[k]} for i, k in enumerate(keys)]


def ajwaf_wawi_mazi_forms(root_word, index, negate=False):
    """Original (pre-اعلال) form, intermediate forms, and rule steps for one
    ماضی معروف conjugation index of an اجوف واوی root -- باب نصر only."""
    fa, ain, laam = root_word
    prefix = (maa + " ") if negate else ""
    ending = AlaamatMaazi[index]

    original = fa + fatha + ain + fatha + laam + ending  # e.g. قَوَلَ / قَوَلْنَ

    if index not in MAZI_SPECIAL_INDICES:
        final = fa + fatha + alif + laam + ending  # قَالَ
        return prefix + original, [], prefix + final, _steps("mazi_qalb")

    step1 = fa + fatha + alif + laam + ending  # قَالْنَ -- قلب
    step2 = fa + fatha + laam + ending  # قَلْنَ -- حذفِ الف لالتقاءِ الساکنین
    final = fa + Zamma + laam + ending  # قُلْنَ -- پیشِ دلالت
    return (
        prefix + original,
        [prefix + step1, prefix + step2],
        prefix + final,
        _steps("mazi_qalb", "mazi_hazf", "mazi_damma_mark"),
    )


def ajwaf_wawi_muzare_forms(root_word, index, negate=False):
    """Original (pre-اعلال) form, intermediate forms, and rule steps for one
    مضارع معروف conjugation index of an اجوف واوی root -- باب نصر only."""
    fa, ain, laam = root_word
    prefix = (laa + " ") if negate else ""
    start = AlaamatMuzaraStart[index]
    end = AlaamatMuzaraEnd[index]

    original = prefix + start + fa + jazam + ain + Zamma + laam + end  # یَقْوُلُ / یَقْوُلْنَ

    if index not in MUZARE_SPECIAL_INDICES:
        final = prefix + start + fa + Zamma + ain + jazam + laam + end  # یَقُولُ -- نقل
        return original, [], final, _steps("muzare_naql")

    step1 = prefix + start + fa + Zamma + ain + jazam + laam + end  # یَقُوْلْنَ -- نقل
    final = prefix + start + fa + Zamma + laam + end  # یَقُلْنَ -- حذفِ واو لالتقاءِ الساکنین
    return original, [step1], final, _steps("muzare_naql", "muzare_hazf")


def ajwaf_wawi_amr_forms(root_word, index):
    """Original (pre-اعلال) form, intermediate forms, and rule steps for one
    امر معروف conjugation index (حاضر only, 6-11) of an اجوف واوی root --
    باب نصر. Mirrors the manually-derived قُلۡ chain already tagged in
    quran_words_test.json (اُقْوُلْ -> اُقُوْلْ -> قُوْلْ -> قُلْ) and reuses its
    exact rule wording, generalized to every حاضر صیغہ."""
    if index not in AMR_HAAZIR_INDICES:
        return None
    fa, ain, laam = root_word
    end = AMR_ENDINGS[index]

    original = hamzaMazmoom + fa + jazam + ain + Zamma + laam + end  # اُقْوُلْ / اُقْوُلَا / ...
    step1    = hamzaMazmoom + fa + Zamma + ain + jazam + laam + end  # اُقُوْلْ -- نقل
    step2    = fa + Zamma + ain + jazam + laam + end                 # قُوْلْ -- حذفِ ہمزہ

    if index not in AMR_SPECIAL_INDICES:
        return original, [step1], step2, _steps("amr_naql", "amr_hamza")

    final = fa + Zamma + laam + end  # قُلْ / قُلْنَ -- حذفِ حرفِ علت
    return original, [step1, step2], final, _steps("amr_naql", "amr_hamza", "amr_hazf")


def to_ilal_chain(original, intermediates, final, rules, lang="ur"):
    """Shapes a (original, intermediates, final, rules) result into the
    [{form, rule}] list IlalLadder.jsx (Word Viewer / Noun Tagger) already
    renders -- stage 0's rule is null (it's the اصل), every later stage's
    rule is the step that produced it from the previous stage."""
    forms = [original] + list(intermediates) + [final]
    chain = [{"form": forms[0], "rule": None}]
    for form, step in zip(forms[1:], rules):
        chain.append({"form": form, "rule": step["rule_text"].get(lang, step["rule_text"]["ur"])})
    return chain


def get_full_gardaan_taaleelat(root_word, baab_name, tense):
    """
    Full conjugation table + per-صیغہ تعلیل for one tense, root-generic.

    Args:
        root_word: Three-letter root (e.g. "قول")
        baab_name: Baab pattern -- currently only "نصر" has rules
        tense: One of "ماضی", "مضارع", "امر"

    Returns:
        list of {"person_reference", "final_form", "ilal_chain"} -- 14 rows
        for ماضی/مضارع, 6 rows (حاضر only) for امر. Empty list if the
        combination isn't supported (e.g. a باب other than نصر).
    """
    if baab_name != "نصر" or len(root_word) != 3:
        return []
    fa, ain, laam = root_word
    if ain != waw:
        return []  # only اجوف واوی roots have rules today

    rows = []
    if tense == "ماضی":
        for i in range(len(AlaamatMaazi)):
            original, intermediates, final, rules = ajwaf_wawi_mazi_forms(root_word, i)
            rows.append({
                "person_reference": UrduZameerTitle[i],
                "final_form": final,
                "ilal_chain": to_ilal_chain(original, intermediates, final, rules),
            })
    elif tense == "مضارع":
        for i in range(len(AlaamatMuzaraStart)):
            original, intermediates, final, rules = ajwaf_wawi_muzare_forms(root_word, i)
            rows.append({
                "person_reference": UrduZameerTitle[i],
                "final_form": final,
                "ilal_chain": to_ilal_chain(original, intermediates, final, rules),
            })
    elif tense == "امر":
        for i in AMR_HAAZIR_INDICES:
            original, intermediates, final, rules = ajwaf_wawi_amr_forms(root_word, i)
            rows.append({
                "person_reference": UrduZameerTitle[i],
                "final_form": final,
                "ilal_chain": to_ilal_chain(original, intermediates, final, rules),
            })

    return rows


def get_taaleelat_rule(verb_type, fael_text, baab_name, root_word, conjugation_index):
    """
    Get the taaleelat (step-by-step اعلال) rule for one conjugation.

    Args:
        verb_type: Verb type (e.g., "اجوف واوی" or "ajwaf_wawi")
        fael_text: Fael type -- currently "ماضی معروف", "ماضی معروف نفی",
            "مضارع معروف", or "مضارع معروف نفی"
        baab_name: Baab pattern -- currently only "نصر" has rules
        root_word: Three-letter root (e.g., "قول") -- any اجوف واوی root works
        conjugation_index: Index of conjugation (0-13)

    Returns:
        dict with has_rule/original_form/final_form/intermediate_forms/rules,
        or None if no rule applies to this combination.

    Note: unlike the source-project version, this standalone copy does not
    recompute final_form against a live generator (there isn't one here) --
    its final_form is derived the same way original_form is, directly from
    the root letters and the rule logic above.
    """
    verb_type_mapping = {"ajwaf_wawi": "اجوف واوی", "sahih": "صحیح"}
    verb_type = verb_type_mapping.get(verb_type, verb_type)

    if verb_type != "اجوف واوی" or baab_name != "نصر":
        return None
    if len(root_word) != 3:
        return None
    if not (0 <= conjugation_index < len(UrduZameerTitle)):
        return None

    if fael_text in ("ماضی معروف", "ماضی معروف نفی"):
        original, intermediates, final_form, rules = ajwaf_wawi_mazi_forms(
            root_word, conjugation_index, negate=fael_text.endswith("نفی")
        )
    elif fael_text in ("مضارع معروف", "مضارع معروف نفی"):
        original, intermediates, final_form, rules = ajwaf_wawi_muzare_forms(
            root_word, conjugation_index, negate=fael_text.endswith("نفی")
        )
    else:
        return None

    return {
        "has_rule": True,
        "original_form": original,
        "final_form": final_form,
        "intermediate_forms": intermediates,
        "rules": rules,
        "conjugation_index": conjugation_index,
        "person_reference": UrduZameerTitle[conjugation_index],
    }
