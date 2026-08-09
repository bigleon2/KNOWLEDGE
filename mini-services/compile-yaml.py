#!/usr/bin/env python3
"""
Compile le projet KNOWLEDGE en YAML.
Exporte toutes les entrées de connaissances et configs en un fichier YAML portable.
"""

import json
import urllib.request
import yaml  # type: ignore
from datetime import datetime

API_KNOWLEDGE = "http://localhost:3000/api/knowledge"
API_CONFIG = "http://localhost:3000/api/config"
OUTPUT = "/home/z/my-project/download/knowledge-export.yaml"


def fetch(url):
    resp = urllib.request.urlopen(url, timeout=10)
    return json.load(resp)


def compile_yaml():
    print("📦 Compilation du projet KNOWLEDGE en YAML...")

    # Fetch data
    entries = fetch(API_KNOWLEDGE)
    configs = fetch(API_CONFIG)

    # Build structure
    document = {
        "project": {
            "name": "KNOWLEDGE",
            "version": "1.0.0",
            "description": "Mémoire persistante pour l'écosystème d'orchestration DJ/Python/PDF/Image/Audio",
            "author": "François",
            "compiled_at": datetime.now().isoformat(),
            "stats": {
                "knowledge_entries": len(entries),
                "config_entries": len(configs),
                "categories": sorted(set(e["category"] for e in entries)),
                "agents_count": 12,
                "skills_count": 71,
            },
        },
        "profile": {},
        "knowledge": [],
        "config": [],
    }

    # ── Profile (extract from knowledge + config) ──
    profile_configs = [c for c in configs if c["category"] == "profile"]
    document["profile"] = {
        c["key"].replace("user.", ""): c["value"]
        for c in profile_configs
    }

    # ── Knowledge entries ──
    category_order = ["profile", "agent", "skill", "protocol", "trigger", "rule", "other"]
    entries_sorted = sorted(entries, key=lambda e: (
        category_order.index(e["category"]) if e["category"] in category_order else 99,
        {"critical": 0, "important": 1, "normal": 2, "secondary": 3}.get(e["priority"], 4),
        e["title"],
    ))

    for e in entries_sorted:
        entry_yaml = {
            "title": e["title"],
            "content": e["content"],
            "category": e["category"],
            "tags": [t.strip() for t in e["tags"].split(",") if t.strip()],
            "priority": e["priority"],
            "source": e["source"],
            "pinned": e["pinned"],
            "updated": e["updatedAt"][:10],
        }
        document["knowledge"].append(entry_yaml)

    # ── Config entries ──
    for c in configs:
        config_yaml = {
            "key": c["key"],
            "value": c["value"],
            "category": c["category"],
            "description": c["description"],
        }
        document["config"].append(config_yaml)

    # Write YAML
    with open(OUTPUT, "w", encoding="utf-8") as f:
        yaml.dump(
            document,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )

    print(f"✅ YAML compilé : {OUTPUT}")
    print(f"   {len(entries)} connaissances")
    print(f"   {len(configs)} configs")
    print(f"   {len(profile_configs)} propriétés profil")


if __name__ == "__main__":
    compile_yaml()
