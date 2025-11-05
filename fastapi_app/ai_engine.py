import os
import re
import sqlite3
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()
DB_PATH = "memory/studio.db"

def clean_code_line(line: str) -> str:
    # Supprime les chaînes et les commentaires
    line = re.sub(r"#.*", "", line)
    line = re.sub(r"(['\"]{3})(.|\n)*?\\1", "", line)
    line = re.sub(r"(['\"])(?:(?=(\\\\?))\\2.)*?\\1", "", line)
    return line.strip()

def analyze_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    lang = "python" if file_path.endswith(".py") else "javascript"
    suggestions = []
    variables = set()

    ignore = {
        # mots-clés Python
        "def","class","return","import","from","as","if","elif","else","for","while",
        "try","except","with","True","False","None","and","or","not","in","is","print",
        "await","async","pass","break","continue","global","nonlocal","lambda","len",
        "range","open","enumerate","zip","list","dict","set","tuple","int","str","float",
        "bool","sum","min","max","any","all","map","filter","re","os","sqlite3","commit",
        "close","connect","cursor","execute","fetchall","Row","DB_PATH",
        # SQL et majuscules
        "INSERT","INTO","VALUES","IGNORE","OR","CREATE","TABLE","UPDATE","DELETE",
        "SELECT","FROM","WHERE","JOIN","LEFT","RIGHT","INNER","OUTER","ON",
    }

    with open(file_path, encoding="utf-8") as f:
        for num, raw in enumerate(f, 1):
            line = clean_code_line(raw)
            if not line:
                continue
            if line.startswith(("def ", "class ", "import ", "from ")):
                continue
            if re.match(r"^[A-Z0-9_]+$", line.strip()):
                continue

            assigns = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=", line)
            for a in assigns:
                variables.add(a)

            uses = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", line)
            for u in uses:
                if (
                    u not in variables
                    and u not in ignore
                    and not u.startswith("_")
                    and u.islower()
                ):
                    suggestions.append({
                        "file": file_path,
                        "line": num,
                        "type": "logic_warning",
                        "message": f"Variable '{u}' peut être utilisée avant sa définition.",
                        "suggestion": f"Vérifier l’ordre de définition de '{u}'.",
                        "language": lang
                    })

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for s in suggestions:
        cur.execute("""
            INSERT OR IGNORE INTO ai_suggestions
            (file, line, type, message, suggestion, status, created_at, language)
            VALUES (?, ?, ?, ?, ?, 'pending', datetime('now'), ?)
        """, (s["file"], s["line"], s["type"], s["message"], s["suggestion"], s["language"]))
    conn.commit()
    conn.close()
    return suggestions

@router.get("/ai/ping")
def ai_ping():
    return {"status": "ok", "message": "IA prête à analyser."}

@router.get("/ai/suggest")
def ai_suggest():
    base_dir = "fastapi_app"
    all_suggestions = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith((".py", ".js")):
                try:
                    all_suggestions.extend(analyze_file(os.path.join(root, f)))
                except Exception as e:
                    print(f"Erreur analyse {f}: {e}")
    return {"status": "done", "count": len(all_suggestions)}

@router.get("/ai/report")
def ai_report():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT file, type, message, language FROM ai_suggestions ORDER BY created_at DESC LIMIT 100")
    rows = cur.fetchall()
    conn.close()
    return JSONResponse({"reports":[{"file":r[0],"type":r[1],"message":r[2],"language":r[3]} for r in rows]})

@router.delete("/ai/clear")
def ai_clear():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM ai_suggestions")
    conn.commit()
    conn.close()
    return {"status": "cleared"}
