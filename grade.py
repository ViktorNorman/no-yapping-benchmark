#!/usr/bin/env python3
"""Re-grade the no-yapping benchmark from the committed responses.

Reads results/<run>/eval-*/<config>/run-1/outputs/response.md, scores each
against objective assertions, writes grading.json per run, prints a summary.

Usage:
    python grade.py [run-dir]      # default: results/iteration-3
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WS = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "results" / "iteration-3"

FILLER = ["great question", "great idea", "happy to", "let me know", "want me to",
          "in order to", "best practice", "it's worth noting", "robust", "leverage",
          "holistic", "seamless", "hope this helps"]
NAMES = {0: "vague-cleanup-redirect", 1: "multi-concept-menu", 2: "concrete-debounce",
         3: "ripcord-explain", 4: "architecture-recommendation",
         5: "vague-complex-sloppy", 6: "architecture-vibe-redirect"}

def wc(t): return len(t.split())
def filler(t): lt = t.lower(); return [p for p in FILLER if p in lt]
def has_code(t): return "```" in t
def starts_code(t):
    for ln in t.strip().splitlines():
        if ln.strip(): return ln.strip().startswith("```")
    return False

def grade(eid, t):
    lt = t.lower(); w = wc(t); fil = filler(t); E = []
    if eid == 0:
        E = [("Concise redirect (<=60 words)", w <= 60, f"{w} words"),
             ("Names the file/component", "checkout" in lt, "named" if "checkout" in lt else "not named"),
             ("Proposes concrete change (useReducer/consolidate)", any(k in lt for k in ["usereducer","reducer","consolidat","collapse","one object"]), "concrete"),
             ("Offers y/redirect, no full code dump", (("(y" in lt or "point me" in lt or t.strip().endswith("?")) and not has_code(t)), "asks, no dump"),
             ("No filler phrases", not fil, "clean" if not fil else str(fil))]
    elif eid == 1:
        E = [("Concise (<=80 words)", w <= 80, f"{w} words"),
             ("Numbered menu present", bool(re.search(r"(?m)^\s*1\.", t)) and bool(re.search(r"(?m)^\s*2\.", t)), "menu"),
             ("Asks which / parks rest", any(k in lt for k in ["which first","which","park","start with"]), "asks+parks"),
             ("No code dump (not all-at-once)", not has_code(t), "no dump"),
             ("Not an interrogation (<=2 '?')", t.count("?") <= 2, f"{t.count('?')} q")]
    elif eid == 2:
        E = [("Leads with code block", starts_code(t), "opens ```" if starts_code(t) else "prose first"),
             ("Implements 300ms debounce", ("debounce" in lt or "settimeout" in lt) and "300" in t, "debounce+300"),
             ("Concise (<=120 words)", w <= 120, f"{w} words"),
             ("No explanatory postamble/filler", not fil and "what changed" not in lt, "clean" if (not fil and "what changed" not in lt) else "postamble")]
    elif eid == 3:
        E = [("Substantial explanation (>=150 words) — ripcord honored", w >= 150, f"{w} words"),
             ("Contrasts useReducer vs useState", "usereducer" in lt and "usestate" in lt, "both"),
             ("Covers downside AND upside", any(k in lt for k in ["ceremony","indirection","boilerplate","more code","overhead"]) and any(k in lt for k in ["scal","related","coordinat","testable","one place","single"]), "two-sided"),
             ("Gives a verdict", any(k in lt for k in ["verdict","my take","i'd","lean","recommend","rule of thumb"]), "verdict")]
    elif eid == 4:
        E = [("Engages — substantial (>=120 words), not a refusal", w >= 120, f"{w} words"),
             ("Addresses all 3 options (shard/replica/event sourcing)", all(k in lt for k in ["shard","replica","event sourc"]), "all 3"),
             ("Gives a clear recommendation", any(k in lt for k in ["what i'd do","i'd","recommend","start"]), "recommends"),
             ("Names concrete levers (citus/shard key/wal/tune/iops)", any(k in lt for k in ["citus","shard key","customer_id","wal","synchronous_commit","iops","tune","batch"]), "levers")]
    elif eid == 5:
        E = [("Concise (<=120 words) — no full rewrite", w <= 120, f"{w} words"),
             ("Names a concrete target in dashboard.js", any(k in lt for k in ["xhr","callback","fetch","innerhtml","var ","global","loadandrender","async"]), "target"),
             ("No giant rewrite dump", not has_code(t) or t.count("```") <= 2, "no dump"),
             ("Offers a choice / asks which first", any(k in lt for k in ["(y","point me","which","first","scope"]) or t.strip().endswith("?"), "choice"),
             ("Flags a concrete risk (XSS/empty-state/error-handling)", any(k in lt for k in ["xss","inject","escap","nan","empty","divide","error handl","never fires","hang"]), "flags bug")]
    elif eid == 6:
        E = [("Concise-ish (<=200 words) — not an abstract essay", w <= 200, f"{w} words"),
             ("Pulls toward concrete (part/which/file)", any(k in lt for k in ["which","point me","n+1","orm","query","caching","index","repository","file","specific"]), "concrete-leaning"),
             ("Offers a concrete next step", ("(y" in lt or t.strip().endswith("?") or "start" in lt), "next step")]
    return E

rates = {"with_skill": [], "without_skill": []}
for eid in range(7):
    ev = WS / f"eval-{eid}"
    for cfg in ("with_skill", "without_skill"):
        resp = ev / cfg / "run-1" / "outputs" / "response.md"
        if not resp.exists():
            print(f"MISSING {resp}"); continue
        t = resp.read_text()
        exps = [{"text": x, "passed": bool(p), "evidence": e} for (x, p, e) in grade(eid, t)]
        passed = sum(1 for x in exps if x["passed"]); total = len(exps)
        (ev / cfg / "run-1" / "grading.json").write_text(json.dumps({
            "summary": {"pass_rate": round(passed / total, 4), "passed": passed, "failed": total - passed, "total": total},
            "expectations": exps,
            "execution_metrics": {"output_chars": len(t)}}, indent=2))
        rates[cfg].append(passed / total)
        print(f"eval-{eid:<2} {NAMES[eid]:<28} {cfg:<14} {passed}/{total}  ({wc(t)} words)")

for cfg in ("with_skill", "without_skill"):
    r = rates[cfg]
    if r: print(f"\n{cfg:<14} mean pass rate: {100*sum(r)/len(r):.1f}%")
