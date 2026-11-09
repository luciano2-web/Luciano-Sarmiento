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
  Nivel 1 👾 Pixel  : >= 1 PR merged
  Nivel 2 🐝 Flyer  : >= 3 PRs merged
  Nivel 3 🐧 Penguin: >= 5 PRs merged
  Nivel 4+ son manuales (Raccoon, Fox, Wolfy, Buhny)

Kiten y Fénix son roles simbólicos del owner y no forman parte de la progresión
automática ni pueden alcanzarse por contribuciones.
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

OWNER_LOGIN = "luciano2-web"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(REPO_ROOT, "CONTRIBUTORS.json")
CONTRIB_MD = os.path.join(REPO_ROOT, "CONTRIBUTORS.md")
README_MD = os.path.join(REPO_ROOT, "README.md")
INACTIVITY_DAYS = 90
LEVEL_NAMES = {
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


def normalize_login(login):
    return (login or "").strip().lower()


def load():
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def save(data):
    data["updated_at"] = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_contributor(data, login):
    normalized = normalize_login(login)
    if not normalized:
        raise ValueError("login vacío")

    if normalized == OWNER_LOGIN:
        for c in data["contributors"]:
            if normalize_login(c.get("login", "")) == OWNER_LOGIN:
                c["login"] = "luciano2-web"
                c["name"] = "Luciano Sarmiento"
                c["emoji"] = "🐱"
                c["role"] = "owner"
                c["level"] = 0
                c["manual"] = True
                c["note"] = "Kiten — Owner del proyecto. Nivel simbólico, no se alcanza por contribuciones."
                return c

        contributor = {
            "login": "luciano2-web",
            "name": "Luciano Sarmiento",
            "emoji": "🐱",
            "role": "owner",
            "level": 0,
            "prs_merged": 0,
            "issues_closed": 0,
            "reviews": 0,
            "last_contribution": None,
            "joined": now().strftime("%Y-%m-%d"),
            "manual": True,
            "note": "Kiten — Owner del proyecto. Nivel simbólico, no se alcanza por contribuciones.",
        }
        data["contributors"].insert(0, contributor)
        return contributor

    for c in data["contributors"]:
        if normalize_login(c.get("login", "")) == normalized:
            return c

    contributor = {
        "login": login,
        "name": login,
        "emoji": "",
        "role": "contributor",
        "level": 0,
        "prs_merged": 0,
        "issues_closed": 0,
        "reviews": 0,
        "last_contribution": None,
        "joined": now().strftime("%Y-%m-%d"),
        "manual": False,
        "note": "",
    }
    data["contributors"].append(contributor)
    return contributor


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
        login = os.environ.get("ISSUE_AUTHOR", "")

    if not login:
        return changes

    normalized = normalize_login(login)
    if normalized == OWNER_LOGIN:
        return changes

    contributor = get_contributor(data, login)
    if contributor.get("manual"):
        return changes

    if event == "pull_request_target":
        contributor["prs_merged"] = int(contributor.get("prs_merged", 0)) + 1
    elif event == "issues":
        contributor["issues_closed"] = int(contributor.get("issues_closed", 0)) + 1

    contributor["last_contribution"] = now().strftime("%Y-%m-%d")
    old = int(contributor.get("level", 0) or 0)
    new = max(old, auto_level(int(contributor.get("prs_merged", 0))))
    if new > old:
        contributor["level"] = new
        emoji, name = LEVEL_NAMES[new]
        changes.append(f"{login} sube a nivel {new} {emoji} {name}")
    return changes


def demote_inactive(data):
    """Baja un nivel a contribuidores inactivos > 90 días (solo automáticos)."""
    changes = []
    limit = now() - timedelta(days=INACTIVITY_DAYS)
    for contributor in data["contributors"]:
        if normalize_login(contributor.get("login", "")) == OWNER_LOGIN:
            continue
        if contributor.get("manual") or contributor.get("level", 0) <= 0 or not contributor.get("last_contribution"):
            continue
        last = datetime.strptime(contributor["last_contribution"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        if last < limit:
            contributor["level"] -= 1
            changes.append(f"{contributor['login']} baja a nivel {contributor['level']} por inactividad")
    return changes


def badge_line(contributor):
    if contributor.get("role") == "owner":
        return f"| 🐱 **{contributor['name']} (Kiten)** | Owner — creador del proyecto | 🐱 Kiten |"

    level = int(contributor.get("level", 0) or 0)
    if level <= 0:
        return f"| [@{contributor['login']}](https://github.com/{contributor['login']}) | {contributor.get('prs_merged', 0)} PRs · {contributor.get('issues_closed', 0)} issues | — Sin nivel |"

    emoji, name = LEVEL_NAMES.get(level, ("", "?"))
    return f"| [@{contributor['login']}](https://github.com/{contributor['login']}) | {contributor.get('prs_merged', 0)} PRs · {contributor.get('issues_closed', 0)} issues | {emoji} {name} |"


def regenerate_docs(data):
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
