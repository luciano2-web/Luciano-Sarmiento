#!/usr/bin/env python3
"""
update_levels.py — Detección automática de niveles de colaboradores (Félix/GatoGPT).

Lee CONTRIBUTORS.json, procesa el evento que lo dispara (PR merged, issue
cerrado, o recálculo programado), aplica las reglas de CONTRIBUTOR_LEVELS.md
y regenera:
  - CONTRIBUTORS.json  (fuente de verdad)
  - CONTRIBUTORS.md    (tabla humana)
  - README.md          (badges, entre los marcadores BADGES)

Reglas automáticas (hasta nivel 3):
  Nivel 1 👾 Pixel    : >= 1 PR merged
  Nivel 2 🐝 Flyer   : >= 3 PRs merged
  Nivel 3 🐧 Penguin : >= 5 PRs merged
Niveles 4-7 son manuales (decisión del mantenedor).
Baja de nivel por inactividad > 90 días (solo si nivel fue automático).
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(REPO_ROOT, "CONTRIBUTORS.json")
CONTRIB_MD = os.path.join(REPO_ROOT, "CONTRIBUTORS.md")
README_MD = os.path.join(REPO_ROOT, "README.md")
INACTIVITY_DAYS = 90
LEVEL_NAMES = {
    0: ("🐱", "Kiten (Owner)"),
    1: ("👾", "Pixel"),
    2: ("🐝", "Flyer"),
    3: ("🐧", "Penguin"),
    4: ("🦝", "Raccoon"),
    5: ("🦊", "Fox"),
    6: ("🐺", "Wolfy"),
    7: ("🦉", "Buhny"),
}
AUTO_RULES = {1: 1, 2: 3, 3: 5}  # nivel: PRs merged mínimos


def now():
    return datetime.now(timezone.utc)


def load():
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def save(data):
    data["updated_at"] = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_contributor(data, login):
    if login.lower() == "luciano2-web":
        for c in data["contributors"]:
            if c["login"].lower() == "luciano2-web":
                c["role"]="owner"; c["level"]=0; c["manual"]=True; c["name"]="Luciano Sarmiento"
                return c
        c = {"login":"luciano2-web","name":"Luciano Sarmiento","emoji":"🐱","role":"owner","level":0,"prs_merged":0,"issues_closed":0,"reviews":0,"last_contribution":None,"joined":"2026-11-08","manual":True,"note":"Kiten — Owner. Inmutable."}
        data["contributors"].insert(0,c)
        return c
    for c in data["contributors"]:
        if c["login"].lower() == login.lower():
            return c
    c = {
        "login": login, "name": login, "emoji": "", "role": "contributor",
        "level": 0, "prs_merged": 0, "issues_closed": 0, "reviews": 0,
        "last_contribution": None, "joined": now().strftime("%Y-%m-%d"),
        "manual": False, "note": "",
    }
    data["contributors"].append(c)
    return c


def auto_level(prs_merged):
    """Nivel automático máximo según reglas (nunca > 3)."""
    level = 0
    for lvl, needed in AUTO_RULES.items():
        if prs_merged >= needed:
            level = lvl
    return level


def process_event(data):
    """Aplica el evento actual y devuelve una lista de cambios."""
    event = os.environ.get("EVENT_NAME", "manual")
    changes = []
    login = None

    if event == "pull_request_target":
        if os.environ.get("PR_MERGED", "false") == "true":
            login = os.environ.get("PR_AUTHOR", "")
    elif event == "issues":
        # un issue cerrado por el propio autor cuenta como triage suave
        login = os.environ.get("ISSUE_AUTHOR", "")

    if login and login.lower() != "luciano2-web":
        c = get_contributor(data, login)
        if event == "pull_request_target":
            c["prs_merged"] += 1
        elif event == "issues":
            c["issues_closed"] += 1
        c["last_contribution"] = now().strftime("%Y-%m-%d")
        if not c["manual"]:
            old = c["level"]
            new = max(c["level"], auto_level(c["prs_merged"]))
            if new > old:
                c["level"] = new
                emoji, name = LEVEL_NAMES[new]
                changes.append(f"{login} sube a nivel {new} {emoji} {name}")
    return changes


def demote_inactive(data):
    """Baja un nivel a contribuidores inactivos > 90 días (solo automáticos)."""
    changes = []
    limit = now() - timedelta(days=INACTIVITY_DAYS)
    for c in data["contributors"]:
        if c.get("login","").lower()=="luciano2-web": continue
        if c.get("manual") or c["level"] <= 0 or not c.get("last_contribution"):
            continue
        last = datetime.strptime(c["last_contribution"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if last < limit:
            c["level"] -= 1
            changes.append(f"{c['login']} baja a nivel {c['level']} por inactividad")
    return changes


def badge_line(c):
    if c.get("role") == "owner":
        return f"| 🐱 **{c['name']} (Kiten)** | Owner — creador del proyecto | 🐱 Kiten |"
    emoji, name = LEVEL_NAMES.get(c["level"], ("", "?"))
    return f"| [@{c['login']}](https://github.com/{c['login']}) | {c['prs_merged']} PRs · {c['issues_closed']} issues | {emoji} {name} |"


def regenerate_docs(data):
    # --- CONTRIBUTORS.md ---
    rows = "\n".join(badge_line(c) for c in data["contributors"])
    md = (
        "# Colaboradores de Felix / GatoGPT\n\n"
        "Gracias a todas las personas que han contribuido a este proyecto.\n\n"
        "> 🤖 Este archivo se actualiza automáticamente por \.github/workflows/levels.yml.\n\n"
        "## Colaboradores\n\n"
        "| Usuario | Contribuciones | Nivel |\n|---|---|---|\n"
        f"{rows}\n\n"
        "→ Ver [CONTRIBUTOR_LEVELS.md](CONTRIBUTOR_LEVELS.md) para las reglas de progresión.\n"
    )
    with open(CONTRIB_MD, "w", encoding="utf-8") as f:
        f.write(md)

    # --- README badges (entre marcadores) ---
    badges = "\n".join(badge_line(c) for c in data["contributors"])
    section = f"<!-- BADGES-START -->\n| Usuario | Contribuciones | Nivel |\n|---|---|---|\n{badges}\n<!-- BADGES-END -->"
    with open(README_MD, encoding="utf-8") as f:
        readme = f.read()
    if "<!-- BADGES-START -->" in readme and "<!-- BADGES-END -->" in readme:
        start = readme.index("<!-- BADGES-START -->")
        end = readme.index("<!-- BADGES-END -->") + len("<!-- BADGES-END -->")
        readme = readme[:start] + section + readme[end:]
        with open(README_MD, "w", encoding="utf-8") as f:
            f.write(readme)


def main():
    data = load()
    changes = process_event(data)
    changes += demote_inactive(data)
    regenerate_docs(data)
    save(data)
    for ch in changes:
        print(f"LEVEL-CHANGE: {ch}")
    if not changes:
        print("No hay cambios de nivel en este evento.")


if __name__ == "__main__":
    sys.exit(main())
