"""
Altasreef AI Tutor -- /explain API.

A standalone FastAPI app, deliberately independent of the private Altasreef
production backend (which stays closed-source -- see README). It exposes:

  POST /explain   -- wrong-answer explanation, retrieval-only (matcher.py)
  POST /ilal      -- step-by-step اعلال derivation chain (taaleelat_rules.py),
                      currently covers اجوف واوی roots in باب نصر only
  GET  /sample    -- a few real seeded questions (Surah 114 data) for the
                      judge-facing demo page to call against with no login
  GET  /surah114  -- the full Surah 114 occurrence-level tagging (every word,
                      every ayah), the same data the private app's Word
                      Viewer reads, redacted to just this one surah
  GET  /codes     -- the integer-code -> label mapper needed to decode
                      /surah114's coded fields (word_class, gender, ... etc)

No user data, no production database, no secrets. CORS is wide open on
purpose -- this is a public, no-auth demo API, not a production service.
"""
import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from matcher import explain as explain_lookup
import taaleelat_rules

app = FastAPI(title="Altasreef AI Tutor", description="Retrieval-only wrong-answer explanations for Quranic Arabic morphology")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "demo_scenarios.json")
SURAH114_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "surah_114_sample.json")
CODES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tag_codes.json")


class ExplainRequest(BaseModel):
    dim: str
    correct_value: str
    given_value: str
    word: str
    root: str = ""
    ref: str = ""
    lang: str = "en"


class IlalRequest(BaseModel):
    root_word: str
    baab_name: str = "نصر"
    tense: str = "ماضی"
    lang: str = "ur"


@app.post("/explain")
def explain_endpoint(req: ExplainRequest):
    return explain_lookup(
        req.dim, req.correct_value, req.given_value,
        word=req.word, root=req.root, ref=req.ref, lang=req.lang,
    )


@app.post("/ilal")
def ilal_endpoint(req: IlalRequest):
    rows = taaleelat_rules.get_full_gardaan_taaleelat(req.root_word, req.baab_name, req.tense, lang=req.lang)
    if not rows:
        return {"matched": False, "reason": "unsupported_combination"}
    return {"matched": True, "rows": rows}


@app.get("/sample")
def sample():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.get("/surah114")
def surah114():
    with open(SURAH114_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.get("/codes")
def codes():
    with open(CODES_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def root():
    return {"service": "altasreef-ai-tutor", "endpoints": ["/explain", "/ilal", "/sample", "/surah114", "/codes"]}
