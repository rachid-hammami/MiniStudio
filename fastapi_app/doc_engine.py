from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
import re

router = APIRouter(prefix="/docs", tags=["Documentation"])

BASE_DIR = Path(__file__).resolve().parent.parent  # dossier racine du projet


def read_file(path: Path) -> str:
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Fichier non trouvé: {path.name}")
    return path.read_text(encoding="utf-8")


@router.get("/index")
async def get_index():
    """Retourne le contenu JSON de index.json"""
    index_path = BASE_DIR / "index.json"
    return json.loads(read_file(index_path))


@router.get("/status")
async def get_status():
    """Analyse la roadmap et renvoie un statut d'avancement"""
    roadmap_path = BASE_DIR / "docs" / "roadmap.md"
    content = read_file(roadmap_path)

    versions = re.findall(r"## (?:Version|📅 Version) (.+)", content)
    status = {"versions": []}

    for v in versions:
        percent = 0
        section = re.search(
            rf"## [^\n]*{re.escape(v)}[^\n]*\n((?:.|\n)*?)(?:## |$)", content
        )
        if section:
            lines = section.group(1).splitlines()
            total = sum(1 for l in lines if l.strip().startswith("-"))
            done = sum(1 for l in lines if "[x]" in l)
            percent = int((done / total) * 100) if total else 0

        status["versions"].append({"version": v.strip(), "progress": percent})

    return status


@router.get("/endpoints")
async def get_endpoints():
    """Fusionne fiche_endpoints.md et api_enrichie.md"""
    docs_path = BASE_DIR / "docs"
    fiche = docs_path / "fiche_endpoints.md"
    enrichie = docs_path / "api_enrichie.md"

    combined = f"# 📘 Endpoints combinés\n\n## Fiche principale\n\n{read_file(fiche)}\n\n---\n\n## API enrichie\n\n{read_file(enrichie)}"
    return {"merged_markdown": combined}
