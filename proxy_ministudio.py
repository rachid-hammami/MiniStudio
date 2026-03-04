from fastapi import FastAPI, Request, Response
import requests
import logging

# --- Configuration ---
CF_ACCESS_CLIENT_ID = "f783f0f990d8c074212dc346d8f6431a"
CF_ACCESS_CLIENT_SECRET = "5992eccfa0f5ddd9bcfb69ae5a63c2ef71fa9fcefbb9870895886cd538f20afe"
TARGET_DOMAIN = "https://studio.ministudio.store"  # ton domaine Cloudflare protégé

# --- Initialisation ---
app = FastAPI(title="MiniStudio Proxy", version="1.0")

# Activer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("proxy")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    """Relaye la requête vers le domaine Cloudflare en ajoutant les headers du Service Token."""
    try:
        # Construction de l’URL complète
        target_url = f"{TARGET_DOMAIN}/{path}"
        method = request.method
        body = await request.body()

        # Prépare les headers de Cloudflare Access
        headers = {
            "CF-Access-Client-Id": CF_ACCESS_CLIENT_ID,
            "CF-Access-Client-Secret": CF_ACCESS_CLIENT_SECRET,
        }

        # Ajouter les headers d’origine sauf le host
        for key, value in request.headers.items():
            if key.lower() != "host":
                headers[key] = value

        # Envoi de la requête à ton domaine protégé
        logger.info(f"🔁 {method} {target_url}")
        response = requests.request(method, target_url, headers=headers, data=body, timeout=15)

        # Retourne la réponse brute au client
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "application/json")
        )

    except Exception as e:
        logger.error(f"❌ Erreur proxy : {e}")
        return {"error": str(e)}
