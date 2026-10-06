const pptxgen = require("pptxgenjs");

// Organizer-required template: Readex Pro, navy/coral/green palette, 45/24/18pt sizes
const NAVY = "1B2183";
const CORAL = "EA6150";
const GREEN = "2CEF2C";
const TINT = "F2F4FF";
const WHITE = "FFFFFF";
const INK = "1A1A2E";
const MUTED = "5B5F7A";

const THEME = {
  name: "Altasreef",
  headFontFace: "Readex Pro",
  bodyFontFace: "Readex Pro",
  colors: {
    dk1: INK, lt1: WHITE, dk2: NAVY, lt2: TINT,
    accent1: NAVY, accent2: CORAL, accent3: GREEN, accent4: MUTED, accent5: NAVY, accent6: CORAL,
    hlink: CORAL, folHlink: NAVY,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5

const PAGE_W = 13.3, PAGE_H = 7.5;
const MARGIN = 0.6;

function footer(slide, pageNum) {
  slide.addText("Altasreef AI Tutor  —  Islamic AI Challenge 2026, Track 3", {
    x: MARGIN, y: PAGE_H - 0.42, w: 8, h: 0.3, fontSize: 10, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  slide.addText(String(pageNum), {
    x: PAGE_W - 1.0, y: PAGE_H - 0.42, w: 0.5, h: 0.3, fontSize: 10, color: MUTED, align: "right", fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
}

function circleIcon(slide, x, y, d, bg, glyph, glyphColor) {
  slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
  slide.addText(glyph, {
    x, y, w: d, h: d, align: "center", valign: "middle",
    fontSize: d * 28, bold: true, color: glyphColor, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
}

function card(slide, x, y, w, h, opts) {
  slide.addShape("roundRect", { x, y, w, h, rectRadius: 0.1, fill: { color: WHITE }, line: { type: "none" },
    shadow: { type: "outer", color: "1B2183", opacity: 0.12, blur: 8, offset: 3, angle: 90 } });
}

// ── Slide 1: Title ──────────────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addImage({ path: "C:/Haqnawaz/Quran/Programming/morphology_app/assets/icon/icon_512.png", x: MARGIN, y: 0.7, w: 1.1, h: 1.1 });
  s.addText("ALTASREEF AI TUTOR", {
    x: MARGIN, y: 2.3, w: 11.5, h: 1.0, fontSize: 45, bold: true, color: WHITE, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  s.addText("Grounded, Multilingual Explanations for Quranic Arabic Morphology", {
    x: MARGIN, y: 3.25, w: 11.5, h: 0.6, fontSize: 24, color: TINT, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  s.addShape("line", { x: MARGIN, y: 4.1, w: 0, h: 0, line: { type: "none" } }); // no accent stripe
  s.addText("Track 3 — Interactive Experiences & Learning Journeys for Islam", {
    x: MARGIN, y: 4.5, w: 11, h: 0.4, fontSize: 18, color: CORAL, bold: true, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  s.addText("Team Altasreef  ·  Final Submission  ·  Oct 4–6, 2026 build window", {
    x: MARGIN, y: 5.0, w: 11, h: 0.4, fontSize: 18, color: TINT, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  s.addText("Live demo: islamicaich-altasreef.netlify.app   •   Repo: github.com/haqnawaz99/islamicaich-altasreef", {
    x: MARGIN, y: 6.6, w: 12, h: 0.4, fontSize: 14, color: GREEN, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
})();

// ── Slide 2: The Problem ────────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("A Score Doesn't Teach Grammar", { x: MARGIN, y: 0.5, w: 11.5, h: 0.8, fontSize: 36, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("Every certification level scores a mistake — but nothing explains what the correct form is, or why.", {
    x: MARGIN, y: 1.25, w: 11.5, h: 0.5, fontSize: 16, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  // Big stat callout
  card(s, MARGIN, 2.1, 4.0, 3.3);
  s.addText("49 → 12", { x: MARGIN, y: 2.4, w: 4.0, h: 1.0, align: "center", fontSize: 44, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("real wrong answers on one Quran word collapsed into just 12 repeating mistake patterns — not random noise.", {
    x: MARGIN + 0.3, y: 3.5, w: 3.4, h: 1.7, align: "center", fontSize: 15, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const rows = [
    ["Feedback stops at \u201Cincorrect\u201D", "A right/wrong marker alone gives a learner nowhere to go next."],
    ["Traditional terms are a barrier", "Learners outside the classical method (نحو، صرف، اعراب) can guess right without understanding why."],
    ["Errors are structured, not random", "Exactly what a grounded, pre-authored explanation layer is built to serve."],
  ];
  let ry = 2.1;
  rows.forEach(([t, d], i) => {
    circleIcon(s, 4.6, ry + 0.05, 0.5, TINT, String(i + 1), NAVY);
    s.addText(t, { x: 5.3, y: ry, w: 7.3, h: 0.35, fontSize: 17, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: 5.3, y: ry + 0.38, w: 7.3, h: 0.6, fontSize: 14, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    ry += 1.1;
  });
  footer(s, 2);
})();

// ── Slide 3: Disclosed baseline ─────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: TINT };
  s.addText("Altasreef — Already Live, Not a Prototype", { x: MARGIN, y: 0.5, w: 11.5, h: 0.8, fontSize: 36, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("Disclosed per the challenge's own rules as pre-existing work, dated before Oct 4, 2026.", {
    x: MARGIN, y: 1.25, w: 11.5, h: 0.5, fontSize: 16, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const stats = [
    ["7", "certification levels, scored against real Quranic verses"],
    ["4", "interface languages — EN / AR / UR / FR, full RTL support"],
    ["11,000+", "tagged Quran verb/noun rows, real occurrence data"],
    ["Live", "on Google Play, in active use by real students"],
  ];
  const cw = 2.85, gap = 0.25, startX = MARGIN;
  stats.forEach(([n, d], i) => {
    const x = startX + i * (cw + gap);
    card(s, x, 2.2, cw, 2.9);
    s.addText(n, { x, y: 2.5, w: cw, h: 0.9, align: "center", fontSize: 36, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.2, y: 3.5, w: cw - 0.4, h: 1.4, align: "center", fontSize: 13, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  });

  s.addText("Only new work built during the Oct 4–6 window is submitted for judging.", {
    x: MARGIN, y: 5.5, w: 11.5, h: 0.5, fontSize: 15, italic: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  footer(s, 3);
})();

// ── Slide 4: The Gap ────────────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("Today, There Is No AI Layer At All", { x: MARGIN, y: 0.5, w: 11.5, h: 0.8, fontSize: 36, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("This challenge's Oct 4–6 window is exactly where the AI layer goes in — not a re-skin of an existing feature.", {
    x: MARGIN, y: 1.25, w: 11.5, h: 0.5, fontSize: 16, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const items = [
    ["Conjugation is rule-based", "A deterministic engine generates verb forms — not learned, not AI."],
    ["Scoring is fixed heuristics", "\u201CWeak area\u201D detection is bucket counts over past answers, nothing adaptive or generative."],
    ["Every mistake says just \u201Cincorrect\u201D", "Zero natural-language feedback anywhere in the certification flow."],
  ];
  const cw = 3.65, gap = 0.3;
  items.forEach(([t, d], i) => {
    const x = MARGIN + i * (cw + gap);
    card(s, x, 2.3, cw, 3.3);
    circleIcon(s, x + 0.3, 2.6, 0.6, TINT, String(i + 1), NAVY);
    s.addText(t, { x: x + 0.3, y: 3.4, w: cw - 0.6, h: 0.8, fontSize: 17, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.3, y: 4.2, w: cw - 0.6, h: 1.2, fontSize: 14, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  });
  footer(s, 4);
})();

// ── Slide 5: The Idea ───────────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: TINT };
  s.addText("Grounded Explanations — Retrieval, Not Generation", { x: MARGIN, y: 0.5, w: 12.1, h: 0.8, fontSize: 33, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("Every wrong answer is matched to a pre-authored rule template by exact key — never generated by a model.", {
    x: MARGIN, y: 1.3, w: 11.5, h: 0.5, fontSize: 16, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const steps = [
    ["Wrong Answer", "The dimension, the student's value, and the correct value — plus the real word/root/verse."],
    ["Exact Rule Lookup", "A deterministic match against 43 pre-authored templates spanning 12 grammar dimensions."],
    ["Explanation or Honest Abstain", "A match fills in the specific word/verse and renders in EN/AR/UR. No match → says so, plainly."],
  ];
  const cw = 3.65, gap = 0.3;
  steps.forEach(([t, d], i) => {
    const x = MARGIN + i * (cw + gap);
    card(s, x, 2.25, cw, 3.4);
    circleIcon(s, x + (cw - 0.7) / 2, 2.55, 0.7, i === 2 ? GREEN : NAVY, String(i + 1), WHITE);
    s.addText(t, { x: x + 0.25, y: 3.45, w: cw - 0.5, h: 0.6, align: "center", fontSize: 17, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.25, y: 4.1, w: cw - 0.5, h: 1.4, align: "center", fontSize: 13, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    if (i < 2) {
      s.addText("→", { x: x + cw, y: 3.5, w: gap, h: 0.6, align: "center", fontSize: 24, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    }
  });
  s.addText("No LLM ever generates the explanation text — zero hallucination surface, by construction.", {
    x: MARGIN, y: 5.9, w: 11.8, h: 0.5, fontSize: 16, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  footer(s, 5);
})();

// ── Slide 6: Why we rejected live generation ────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("We Tested Generation First — And Rejected It", { x: MARGIN, y: 0.5, w: 11.8, h: 0.8, fontSize: 33, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("Pilot benchmark: a live LLM's raw conjugation output for one root (140 forms) vs. our verified, rule-based gold-standard data.", {
    x: MARGIN, y: 1.3, w: 11.8, h: 0.6, fontSize: 15, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const stats = [["45%", "exact match"], ["53.6%", "ignoring diacritics"], ["50.7%", "English translation accuracy"]];
  const cw = 3.6, gap = 0.3;
  stats.forEach(([n, l], i) => {
    const x = MARGIN + i * (cw + gap);
    card(s, x, 2.2, cw, 2.1);
    s.addText(n, { x, y: 2.4, w: cw, h: 1.0, align: "center", fontSize: 40, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(l, { x, y: 3.4, w: cw, h: 0.6, align: "center", fontSize: 14, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  });

  card(s, MARGIN, 4.65, 11.5, 1.85);
  s.addText("A trust bar that low is unacceptable for Islamic educational content. So the shipped explanation layer never generates grammar — it only ever returns text a human wrote and reviewed in advance, selected by exact key match.", {
    x: MARGIN + 0.35, y: 4.9, w: 10.8, h: 1.4, fontSize: 16, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  footer(s, 6);
})();

// ── Slide 7: What we built ──────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: TINT };
  s.addText("Three Built Features, One Public Repo", { x: MARGIN, y: 0.5, w: 11.8, h: 0.8, fontSize: 36, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("All built and deployed during the Oct 4–6 window — github.com/haqnawaz99/islamicaich-altasreef", {
    x: MARGIN, y: 1.25, w: 11.8, h: 0.5, fontSize: 15, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const feats = [
    ["/explain", "43 rules across all 12 tested grammar dimensions, in English/Arabic/Urdu — prioritized by real production frequency, pulled live from 5,215 real student answers."],
    ["/ilal", "Full گردان (conjugation table) + step-by-step تعلیل derivation chain, root-generic — verified against قول/قوم/كون — in all 3 languages."],
    ["Surah 114 Viewer", "Every word, every ayah, fully tagged (root, case, i'rab) — real data, dual-script (Uthmani/IndoPak) display, merged into one interactive page."],
  ];
  const cw = 3.65, gap = 0.3;
  feats.forEach(([t, d], i) => {
    const x = MARGIN + i * (cw + gap);
    card(s, x, 2.1, cw, 4.3);
    circleIcon(s, x + 0.3, 2.4, 0.55, [NAVY, CORAL, GREEN][i], String(i + 1), WHITE);
    s.addText(t, { x: x + 0.3, y: 3.1, w: cw - 0.6, h: 0.5, fontSize: 18, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.3, y: 3.65, w: cw - 0.6, h: 2.6, fontSize: 13, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  });
  footer(s, 7);
})();

// ── Slide 8: Originality & fit with Track 3's own success criteria ──────
(() => {
  const s = pres.addSlide();
  s.background = { color: TINT };
  s.addText("Why This Is a Learning Journey, Not Just a Feature", { x: MARGIN, y: 0.5, w: 11.8, h: 0.9, fontSize: 32, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("Track 3: Interactive Experiences & Learning Journeys for Islam — التجارب التفاعلية والرحلة المعرفية", {
    x: MARGIN, y: 1.35, w: 11.8, h: 0.5, fontSize: 14, italic: true, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const left = [
    ["A wrong answer becomes a journey, not a dead end", "Tap “why” on a mistake → see the grammar rule → open its full تعلیل derivation → explore the real verse it came from. Four real learning surfaces from one tap, not a static correction."],
    ["Originality is the restraint, not the novelty", "Most AI-tutor pitches reach for live generation by default. The original move here was testing it, measuring it (45% exact match), and choosing deterministic retrieval instead — a harder, less flashy, more trustworthy design decision."],
  ];
  const right = [
    ["Grounded in the learner's own real mistakes", "Every rule exists because a real student made that exact error in production — not a hypothetical FAQ list."],
    ["One coherent system, not three bolted-on demos", "Explanation, derivation, and verse exploration share one data model and one language toggle — designed together, not stitched together."],
  ];

  function col(items, x) {
    let ry = 2.2;
    items.forEach(([t, d]) => {
      card(s, x, ry, 5.5, 2.0);
      s.addText(t, { x: x + 0.3, y: ry + 0.2, w: 4.9, h: 0.6, fontSize: 15, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
      s.addText(d, { x: x + 0.3, y: ry + 0.8, w: 4.9, h: 1.1, fontSize: 12.5, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
      ry += 2.3;
    });
  }
  col(left, MARGIN);
  col(right, MARGIN + 5.9);
  footer(s, 8);
})();

// ── Slide 9 (was 8): Reliability & safety plan ───────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("Reliability & Scientific Safety Plan", { x: MARGIN, y: 0.5, w: 11.8, h: 0.8, fontSize: 36, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("خطة الموثوقية والسلامة العلمية — mapped directly onto the organizer's own scientific reference package.", {
    x: MARGIN, y: 1.25, w: 11.8, h: 0.5, fontSize: 15, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const rows = [
    ["مقاومة الهلوسة — Hallucination resistance", "No code path can generate explanation text. An unmatched case returns an explicit abstain, never a guess."],
    ["قطعي / اجتهادي — Tier A / Tier B split", "Every rule is Tier A only: a plain fact derivable from the word's own spelling, root, or the literal verse text."],
    ["الشفافية — Transparency", "Every response shows its exact rule_id. The single most common \u201Cwrong answer\u201D in production is a real scoring ambiguity — disclosed as a known system limitation, not defended as a student error."],
    ["Reliability / attribution", "Rule priority is not guessed — it's ranked by real frequency, pulled live from 5,215 production answers before a single rule was written."],
    ["Human review gate", "All 43 rules are flagged for review by the project's own Sarf instructor (9 years teaching علم الصرف) before being treated as final — confirmed complete."],
  ];
  let ry = 2.05;
  rows.forEach(([t, d]) => {
    circleIcon(s, MARGIN, ry + 0.02, 0.4, TINT, "✓", GREEN);
    s.addText(t, { x: MARGIN + 0.6, y: ry, w: 10.9, h: 0.35, fontSize: 15, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: MARGIN + 0.6, y: ry + 0.33, w: 10.9, h: 0.55, fontSize: 12.5, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    ry += 0.98;
  });
  footer(s, 9);
})();

// ── Slide 9: Live demo ──────────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText("Live, Judge-Testable — No Login Required", { x: MARGIN, y: 0.9, w: 12.1, h: 0.8, fontSize: 36, bold: true, color: WHITE, fontFace: "Readex Pro", isTextBox: true, margin: 0 });

  card(s, MARGIN, 2.1, 11.5, 1.5);
  s.addText("islamicaich-altasreef.netlify.app", { x: MARGIN, y: 2.3, w: 11.5, h: 1.1, align: "center", valign: "middle", fontSize: 30, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });

  const infos = [
    ["Frontend", "Static demo page, deployed on Netlify"],
    ["Backend", "FastAPI, deployed on Render (free tier)"],
    ["Source", "github.com/haqnawaz99/islamicaich-altasreef"],
  ];
  const cw = 3.65, gap = 0.3;
  infos.forEach(([t, d], i) => {
    const x = MARGIN + i * (cw + gap);
    s.addText(t, { x, y: 4.1, w: cw, h: 0.4, fontSize: 16, bold: true, color: GREEN, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x, y: 4.55, w: cw, h: 0.6, fontSize: 13, color: TINT, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  });

  s.addText("Note: the free Render tier spins down when idle — the very first request after inactivity can take 30–60s to wake up. Normal, not a bug.", {
    x: MARGIN, y: 5.6, w: 11.5, h: 0.7, fontSize: 13, italic: true, color: TINT, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  footer(s, 10);
})();

// ── Slide 10: Build timeline ─────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: TINT };
  s.addText("October 4–6 — Built, Tested, Deployed", { x: MARGIN, y: 0.5, w: 11.8, h: 0.8, fontSize: 36, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });

  const days = [
    ["Day 1 — Oct 4", "Pulled real production wrong-answer frequency (5,215 answers). Authored the first rule set, built the retrieval matcher and /explain endpoint, stood up the first demo page."],
    ["Day 2 — Oct 5", "Expanded to all 12 dimensions (43 rules). Built /ilal (full گردان + تعلیل chain) and the Surah 114 verse viewer. Merged all three into one trilingual, dual-script page."],
    ["Day 3 — Oct 6", "Fixed language-toggle and font bugs across every module, deployed backend (Render) and frontend (Netlify), end-to-end live verification, reliability/sustainability docs, submission packaging."],
  ];
  const cw = 3.65, gap = 0.3;
  days.forEach(([t, d], i) => {
    const x = MARGIN + i * (cw + gap);
    card(s, x, 1.6, cw, 4.9);
    circleIcon(s, x + 0.3, 1.9, 0.55, NAVY, String(i + 1), WHITE);
    s.addText(t, { x: x + 0.3, y: 2.6, w: cw - 0.6, h: 0.5, fontSize: 17, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: x + 0.3, y: 3.15, w: cw - 0.6, h: 3.2, fontSize: 13, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  });
  footer(s, 11);
})();

// ── Slide 11: Sustainability ─────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("Operating & Sustainability Plan", { x: MARGIN, y: 0.5, w: 11.8, h: 0.8, fontSize: 36, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("واقعية التشغيل والاستكمال — this extends a live, actively-maintained platform, not a hackathon prototype with nowhere to live.", {
    x: MARGIN, y: 1.25, w: 11.8, h: 0.6, fontSize: 15, color: MUTED, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });

  const rows = [
    ["Merges into production", "Reviewed rules move into the real Altasreef backend, reusing its existing auth/rate-limit conventions — not a parallel system to maintain."],
    ["Zero ongoing LLM cost", "Retrieval-only means no per-explanation inference bill to budget for as usage grows."],
    ["Incremental growth, not a rewrite", "The same production export used to prioritize the first 43 rules can be re-run anytime to find the next highest-impact gap."],
    ["No new infrastructure required", "The production merge target already has hosting, monitoring, and CI/CD in place."],
  ];
  let ry = 2.1;
  rows.forEach(([t, d]) => {
    circleIcon(s, MARGIN, ry + 0.02, 0.45, TINT, "•", NAVY);
    s.addText(t, { x: MARGIN + 0.65, y: ry, w: 10.8, h: 0.4, fontSize: 17, bold: true, color: NAVY, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(d, { x: MARGIN + 0.65, y: ry + 0.4, w: 10.8, h: 0.6, fontSize: 13.5, color: INK, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    ry += 1.15;
  });
  footer(s, 12);
})();

// ── Slide 12: Team + closing ──────────────────────────────────────────────
(() => {
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addImage({ path: "C:/Haqnawaz/Quran/Programming/morphology_app/assets/icon/icon_512.png", x: MARGIN, y: 0.6, w: 0.9, h: 0.9 });
  s.addText("Team Altasreef", { x: MARGIN, y: 1.7, w: 11.5, h: 0.8, fontSize: 40, bold: true, color: WHITE, fontFace: "Readex Pro", isTextBox: true, margin: 0 });

  const team = [
    ["Haq Nawaz", "Technical Lead — NLP/AI"],
    ["Muhammad Wajih Uz Zaman", "Backend"],
    ["Kashif Sohail", "DevOps"],
    ["Hafiz Muhammad Haris", "Frontend"],
  ];
  const cw = 2.85, gap = 0.25;
  team.forEach(([n, r], i) => {
    const x = MARGIN + i * (cw + gap);
    s.addShape("roundRect", { x, y: 2.8, w: cw, h: 1.5, rectRadius: 0.1, fill: { color: "2A2FA0" }, line: { type: "none" } });
    s.addText(n, { x: x + 0.15, y: 2.95, w: cw - 0.3, h: 0.7, fontSize: 15, bold: true, color: WHITE, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
    s.addText(r, { x: x + 0.15, y: 3.55, w: cw - 0.3, h: 0.6, fontSize: 13, color: TINT, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  });

  s.addText("Thank you", { x: MARGIN, y: 4.8, w: 11.5, h: 0.7, fontSize: 28, bold: true, color: CORAL, fontFace: "Readex Pro", isTextBox: true, margin: 0 });
  s.addText("Live demo: islamicaich-altasreef.netlify.app   •   Repo: github.com/haqnawaz99/islamicaich-altasreef", {
    x: MARGIN, y: 5.55, w: 11.8, h: 0.4, fontSize: 15, color: GREEN, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
  s.addText("Altasreef AI Tutor  —  Islamic AI Challenge 2026, Track 3", {
    x: MARGIN, y: 6.9, w: 10, h: 0.3, fontSize: 10, color: TINT, fontFace: "Readex Pro", isTextBox: true, margin: 0,
  });
})();

(async () => {
  await pres.writeFile({ fileName: "altasreef_final_submission_deck.pptx" });
  const { applyTheme } = require("C:/Users/Haq/.claude/skills/synced/d792c46f-6e47-4b60-9ebc-cb91f4eb031e_48025eb4-205e-4666-b563-bd6bdfacd782/pptx/scripts/apply_theme.js");
  await applyTheme("altasreef_final_submission_deck.pptx", THEME);
  console.log("done");
})();
