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

Kitten pertenece exclusivamente a Luciano. Fénix está reservado y sin asignar;
solo una instrucción expresa de Luciano permitirá implementar su concesión.
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
                c["name"] = "luciano2-web"
                c["emoji"] = "🐱"
                c["role"] = "owner"
                c["level"] = 0
                c["manual"] = True
                c["note"] = "Kitten — Owner del proyecto. Nivel simbólico, no se alcanza por contribuciones."
                return c

        contributor = {
            "login": "luciano2-web",
            "name": "luciano2-web",
            "emoji": "🐱",
            "role": "owner",
            "level": 0,
            "prs_merged": 0,
            "issues_closed": 0,
            "reviews": 0,
            "last_contribution": None,
            "joined": now().strftime("%Y-%m-%d"),
            "manual": True,
            "note": "Kitten — Owner del proyecto. Nivel simbólico, no se alcanza por contribuciones.",
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


def record_change(contributor, old, reason):
    level = contributor["level"]
    emoji, name = ("🐱", "Kitten") if normalize_login(contributor["login"]) == OWNER_LOGIN else LEVEL_NAMES.get(level, ("", "Sin nivel"))
    entry = {
        "date": now().strftime("%Y-%m-%d"),
        "from": old, "to": level, "reason": reason,
        "message": f"@{contributor['login']}: {emoji} {name} (nivel {level}). {reason}",
        "issue_number": contributor.get("last_issue_number"),
    }
    history = contributor.setdefault("history", [])
    entry["id"] = f"{normalize_login(contributor['login'])}-{len(history) + 1}"
    history.append(entry)
    return entry["message"]


def enforce_reserved_roles(data):
    owner = get_contributor(data, OWNER_LOGIN)
    owner["rank"] = "Kitten"
    data["reserved_roles"] = {"fenix": {"assigned_to": None, "requires": "Instrucción expresa de luciano2-web"}}
    for c in data["contributors"]:
        if normalize_login(c["login"]) != OWNER_LOGIN:
            c["role"] = "contributor"
            c.pop("rank", None)
            c["level"] = max(0, min(7, int(c.get("level", 0))))


def process_event(data):
    """Recuerda cada PR/issue una sola vez, incluso al repetir el workflow."""
    event = os.environ.get("EVENT_NAME", "manual")
    if event == "pull_request_target" and os.environ.get("PR_MERGED") == "true":
        login, number, kind = os.environ.get("PR_AUTHOR"), os.environ.get("PR_NUMBER"), "pr"
    elif event == "issues" and os.environ.get("ISSUE_REASON") == "completed":
        login, number, kind = os.environ.get("ISSUE_AUTHOR"), os.environ.get("ISSUE_NUMBER"), "issue"
    else:
        return []
    if not login or not number or not number.isdigit():
        return []
    key = f"{kind}:{number}"
    events = data.setdefault("processed_events", [])
    if key in events:
        return []
    c = get_contributor(data, login)
    events.append(key)
    field = "prs_merged" if kind == "pr" else "issues_closed"
    c[field] = int(c.get(field, 0)) + 1
    c["last_contribution"] = now().strftime("%Y-%m-%d")
    c["last_issue_number"] = int(number)
    old = int(c.get("level", 0))
    if not c.get("manual") and normalize_login(login) != OWNER_LOGIN and kind == "pr":
        c["level"] = max(old, auto_level(c["prs_merged"]))
    # Cada aportación deja constancia del nivel actual, aunque no cambie.
    return [record_change(c, old, f"Contribución registrada: {key}.")]


def demote_inactive(data):
    """Como máximo una bajada por cada nuevo período de 90 días."""
    changes = []
    today = now().date()
    for c in data["contributors"]:
        if normalize_login(c.get("login")) == OWNER_LOGIN or c.get("manual") or c.get("level", 0) <= 0:
            continue
        dates = [c.get("last_contribution"), c.get("last_demotion")]
        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates if d]
        if not dates or (today - max(dates)).days < INACTIVITY_DAYS:
            continue
        old = c["level"]
        c["level"] -= 1
        c["last_demotion"] = today.isoformat()
        changes.append(record_change(c, old, "Baja por 90 días de inactividad."))
    return changes


def badge_line(contributor):
    if normalize_login(contributor.get("login")) == OWNER_LOGIN:
        return f"| 🐱 **{contributor['name']} (Kitten)** | Owner — creador del proyecto | 🐱 Kitten |"

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
    original = json.dumps(data, sort_keys=True, ensure_ascii=False)
    enforce_reserved_roles(data)
    changes = process_event(data)
    changes += demote_inactive(data)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## 🐱 Félix: niveles de colaboradores\\n\\n" + "\\n".join(changes or ["Sin cambios de nivel."]) + "\\n")
    updated = json.dumps(data, sort_keys=True, ensure_ascii=False)

    if updated == original:
        print("Sin cambios de contribución; no se actualizan marcas de tiempo.")
        return

    regenerate_docs(data)
    save(data)
    for ch in changes:
        print(f"LEVEL-CHANGE: {ch}")
    if not changes:
        print("Se guardaron cambios de contribución sin cambio de nivel.")


if __name__ == "__main__":
    sys.exit(main())
