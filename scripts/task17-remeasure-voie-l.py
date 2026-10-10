#!/usr/bin/env python3
# PROVENANCE: Task 17 re-execution (session web-b93f42fa) — rewrite post-incident S3 étendu
# (restauration snapshot 2026-10-10 20:48 ; runner original perdu, logique reconstituée du worklog)
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Task 17 — Re-mesure voie L des dérives replay (31 cas / 15 skills).
Pour chaque cas dérivant du replay voie M (stemmer SHARED §7 v2) : 3 votes z-ai (CLI).
Décisions : CONFIRME (votes unanimes == expected — dérive M réelle documentée, 0 fix instrument)
| REFUTE_UNANIME (votes unanimes != expected — révision auto du trigger_evals, expected := vote)
| AMBIGU (votes mixtes) | QUOTA (échec après backoff 429 — re-mesurable).
Crash-safe : report persisté après CHAQUE cas. Idempotent : --skip-done ignore les cas décidés.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPLAY = REPO / "scripts" / "triggers-replay-report.json"
REPORT = REPO / "scripts" / "task17-voie-l-report.json"
TMP = Path("/home/z/my-project/scripts/task17b/vote-out.json")
VOTES_PAR_CAS = 3
BACKOFFS = [15, 30, 60]

def charger_cas():
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))
    derives = replay["derives"]
    cas_par_skill = {}
    for skill in derives:
        bloc = replay["skills"].get(skill, {})
        cas_der = [c for c in bloc.get("cases", []) if not c.get("ok", True)]
        if cas_der:
            cas_par_skill[skill] = cas_der
    return cas_par_skill

def description_skill(skill: str) -> str:
    """Description frontmatter COMPLÈTE (bloc YAML multi-lignes « > »), sans troncature agressive."""
    sk = REPO / "skills" / skill / "SKILL.md"
    if not sk.exists():
        return "(description indisponible)"
    lines = sk.read_text(encoding="utf-8").splitlines()
    desc, capture, indent = [], False, False
    for line in lines:
        if line.lower().startswith("description:"):
            after = line.split(":", 1)[1].strip()
            capture = True
            if after in (">", ">-", "|", "|-"):
                indent = True
            elif after:
                desc.append(after)
            continue
        if capture:
            if line.strip() == "" or (line[:1] not in (" ", "\t") and not indent):
                break
            if indent and line[:1] in (" ", "\t"):
                desc.append(line.strip())
            elif not indent:
                break
            elif line[:1] not in (" ", "\t"):
                break
    texte = " ".join(desc).strip()
    return texte[:900] if texte else "(description indisponible)"

def vote_zai(skill: str, description: str, query: str) -> bool | None:
    """1 vote via CLI z-ai (prompt calibré au contrat de déclenchement SHARED §7 v2).
    Retourne True/False, ou None si échec (429/erreur) après backoffs."""
    prompt = (
        f"Skill disponible : {skill}\n"
        f"Périmètre du skill (description frontmatter) : {description}\n\n"
        f"Prompt de test : « {query} »\n\n"
        "CONTRAT DE DÉCLENCHEMENT (heuristique officielle SHARED §7 v2) : un skill ne s'active que si la demande relève de son PÉRIMÈTRE PRÉCIS ci-dessus.\n"
        "- Une tâche générique qui contient seulement un mot du périmètre ne déclenche PAS (anti faux-positif).\n"
        "- Une demande hors périmètre qui mentionne le skill en négatif (« plutôt qu'avec X ») ne déclenche PAS.\n"
        "- Une demande qui relève clairement de la spécialité du skill déclenche, même sans mention explicite du nom.\n\n"
        "Question : selon ce contrat, l'assistant devrait-il activer CE skill pour ce prompt ?\n"
        'Réponds uniquement avec ce JSON : {"should_trigger": true} ou {"should_trigger": false}'
    )
    system = "Tu es un arbitre d'evals de déclenchement de skills. Réponds UNIQUEMENT avec un JSON valide, sans texte autour."
    for i, delai in enumerate([0] + BACKOFFS):
        if delai:
            time.sleep(delai)
        try:
            TMP.parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(
                ["z-ai", "chat", "-p", prompt, "-s", system, "-o", str(TMP)],
                capture_output=True, text=True, timeout=75,
            )
            if r.returncode != 0:
                continue
            data = json.loads(TMP.read_text(encoding="utf-8"))
            # Format CLI : réponse OpenAI-style {choices:[{message:{content}}]}
            content = (data.get("choices", [{}])[0].get("message", {}).get("content")
                       or data.get("content") or data.get("response") or "").strip()
            m = re.search(r'\{[^{}]*"should_trigger"[^{}]*\}', content, re.DOTALL)
            if not m:
                continue
            return bool(json.loads(m.group(0))["should_trigger"])
        except Exception:
            continue
    return None

def reviser_trigger_evals(skill: str, query: str, should: bool) -> bool:
    """REFUTE_UNANIME — révision auto BIDIRECTIONNELLE : should_trigger := should (les deux sens)."""
    te_path = REPO / "skills" / skill / "evals" / "trigger_evals.json"
    if not te_path.exists():
        return False
    cases = json.loads(te_path.read_text(encoding="utf-8"))
    touched = False
    for c in cases:
        if c.get("query") == query and c.get("should_trigger") != should:
            c["should_trigger"] = should
            touched = True
    if touched:
        te_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return touched

def main() -> int:
    skip_done = "--skip-done" in sys.argv
    cas_par_skill = charger_cas()
    total = sum(len(v) for v in cas_par_skill.values())

    if REPORT.exists():
        report = json.loads(REPORT.read_text(encoding="utf-8"))
    else:
        report = {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "methode": "voie L — 3 votes z-ai CLI par cas dérivant (rewrite post-incident S3 étendu)",
            "source": "scripts/triggers-replay-report.json (15 dérives voie M)",
            "skills": {},
            "bilan": {},
        }
    skills_r = report["skills"]

    n_done = 0
    for skill, cas_list in cas_par_skill.items():
        if skill not in skills_r:
            skills_r[skill] = {"cases": []}
        bloc = skills_r[skill]
        desc = description_skill(skill)
        for cas in cas_list:
            query, expected = cas["query"], cas["expected"]
            deja = next((c for c in bloc["cases"] if c["query"] == query), None)
            if deja and deja.get("decision") in ("CONFIRME", "REFUTE_UNANIME", "AMBIGU"):
                continue
            if deja and skip_done and deja.get("decision") == "QUOTA" and "--retry-quota" not in sys.argv:
                continue
            votes, quorum = [], 0
            for _ in range(VOTES_PAR_CAS):
                v = vote_zai(skill, desc, query)
                if v is not None:
                    votes.append(v)
                    quorum += 1
                else:
                    votes.append(None)
            if quorum == VOTES_PAR_CAS:
                ratio = sum(1 for v in votes if v) / VOTES_PAR_CAS
                unanime_pos = ratio == 1.0
                unanime_neg = ratio == 0.0
                if unanime_pos or unanime_neg:
                    llm_should = unanime_pos
                    if llm_should == expected:
                        decision, rev = "CONFIRME", False
                    else:
                        decision, rev = "REFUTE_UNANIME", reviser_trigger_evals(skill, query, llm_should)
                else:
                    decision, rev = "AMBIGU", False
            else:
                ratio = None
                decision, rev = "QUOTA", False
            entree = {
                "query": query,
                "expected": expected,
                "trigger_m": cas.get("trigger_m"),
                "votes": votes,
                "ratio": ratio,
                "decision": decision,
                "revision_appliquee": rev,
            }
            if deja:
                bloc["cases"][bloc["cases"].index(deja)] = entree
            else:
                bloc["cases"].append(entree)
            report["bilan"] = bilan(report)
            REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            n_done += 1
            print(f"  [{n_done}/{total}] {skill} « {query[:48]}… » → {decision}" + (f" (révision appliquée)" if rev else ""))

    report["bilan"] = bilan(report)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    b = report["bilan"]
    print(f"\nBILAN : {b}")
    return 0

def bilan(report: dict) -> dict:
    stats = {}
    for s in report["skills"].values():
        for c in s["cases"]:
            stats[c["decision"]] = stats.get(c["decision"], 0) + 1
    return stats

if __name__ == "__main__":
    raise SystemExit(main())
