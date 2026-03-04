from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.docs import get_redoc_html
import os

app = FastAPI(title="MiniStudio API", version="1.1.0")

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes statiques ---
if not os.path.exists("memory"):
    os.makedirs("memory")
app.mount("/memory", StaticFiles(directory="memory"), name="memory")


# --- Fonction : Génération du schéma OpenAPI compact ---
def generate_compact_openapi(app, keep_tags: list[str] | None = None, remove_docs=True):
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # ✅ Ajout du serveur par défaut si absent
    if "servers" not in schema or not schema["servers"]:
        schema["servers"] = [
            {"url": "https://ministudio.store", "description": "Instance Cloudflare"}
        ]

    # 🔹 Filtrage facultatif des tags
    if keep_tags:
        filtered_paths = {}
        for path, methods in schema.get("paths", {}).items():
            new_methods = {}
            for method, info in methods.items():
                tags = info.get("tags", [])
                if any(tag in keep_tags for tag in tags):
                    new_methods[method] = info
            if new_methods:
                filtered_paths[path] = new_methods
        schema["paths"] = filtered_paths

    # 🔹 Suppression de certains champs pour réduire la taille du schéma
    if remove_docs:

        def prune(obj):
            if isinstance(obj, dict):
                obj.pop("summary", None)
                obj.pop("examples", None)
                obj.pop("description", None)
                for v in obj.values():
                    prune(v)
            elif isinstance(obj, list):
                for e in obj:
                    prune(e)

        prune(schema)

        # ✅ Correction : Ajout automatique d'une description si manquante dans les réponses
    for path, methods in schema.get("paths", {}).items():
        for method, data in methods.items():
            responses = data.get("responses", {})
            for code, resp in responses.items():
                if isinstance(resp, dict) and "description" not in resp:
                    resp["description"] = f"Response {code}"

    # ✅ Ajout automatique d'un schéma de corps minimal pour certaines routes POST
    for path, methods in schema.get("paths", {}).items():
        for method, data in methods.items():
            if method.lower() == "post" and "requestBody" not in data:
                if any(key in path for key in ["write", "read", "delete"]):
                    data["requestBody"] = {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "filename": {"type": "string"},
                                        "content": {"type": "string"},
                                    },
                                    "required": ["filename", "content"],
                                }
                            }
                        },
                    }

    return schema


# --- Endpoint : schéma compact ---
@app.get("/openapi_compact.json", include_in_schema=False)
def openapi_compact():
    return JSONResponse(generate_compact_openapi(app))


# --- Docs Swagger et Redoc ---
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi_compact.json", title="MiniStudio - Swagger UI"
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi_compact.json", title="MiniStudio - ReDoc"
    )


# voici la modif ;)


# --- Page d'accueil ---
# --- Page d'accueil ---
@app.get("/", response_class=HTMLResponse)
async def root():
    html = """
    <html>
        <head>
            <title>MiniStudioGPT API v1.4.3</title>
            <style>
                body {
                    font-family: system-ui, sans-serif;
                    background-color: #0f172a;
                    color: #e2e8f0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                h1 { font-size: 2.5em; margin-bottom: 0.3em; color: #38bdf8; }
                p { font-size: 1.1em; color: #94a3b8; }
                a { color: #38bdf8; text-decoration: none; font-weight: bold; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>🚀 MiniStudioGPT API v1.4.3</h1>
            <p>Builder Integration Active – Lecture étendue + Apply-Code</p>
            <p>📘 <a href="/openapi_compact.json">Voir le schéma OpenAPI compact</a></p>
            <p>🧠 <a href="/docs">Accéder à Swagger UI</a></p>
        </body>
    </html>
    """
    return HTMLResponse(html)


# --- Import des routes ---
from fastapi_app.endpoints_project import router as project_router
from fastapi_app.endpoints.endpoints_cortex import router as cortex_router

app.include_router(project_router, tags=["MiniStudioGPT Project"])
app.include_router(cortex_router, tags=["Cortex"])

from fastapi_app.cortex.cortex_feedback_service import router as cortex_feedback_router
app.include_router(cortex_feedback_router, tags=["Cortex Feedback"])

# --- Point d'entrée ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


# --- Import pour le projet FastAPI Notes ---
from fastapi import HTTPException
from fastapi_app.models import Note
from fastapi_app.storage import load_notes, add_note, delete_note


# --- Routes FastAPI Notes ---
@app.get("/notes", response_model=list[Note], tags=["FastAPI Notes"])
def get_notes():
    """Récupère la liste complète des notes."""
    return load_notes()


@app.post("/notes", response_model=Note, tags=["FastAPI Notes"])
def create_note(note: Note):
    """Ajoute une nouvelle note."""
    new_note = add_note(note.title, note.content)
    return new_note


@app.delete("/notes/{note_id}", tags=["FastAPI Notes"])
def remove_note(note_id: int):
    """Supprime une note selon son identifiant."""
    success = delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Note {note_id} introuvable")
    return {"message": f"Note {note_id} supprimée avec succès"}

