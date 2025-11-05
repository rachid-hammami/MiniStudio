"""
MiniStudioGPT v1.4.4 - Docker Health Check Script
Auteur : Code GPT 🧠
Date : 2025-11-01
Usage :
    python check_docker_health.py
"""

import requests
import os
from datetime import datetime

LOCAL_URL = "http://localhost:8100/project/ping"
CLOUDFLARE_URL = "https://ministudio.store/project/ping"


def check_endpoint(url: str):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            version = data.get("server_version")
            if status == "ok" and version == "v1.4.4":
                return True, f"✅ OK ({version})", data
            else:
                return False, f"⚠️ Mauvaise réponse : {data}", data
        else:
            return False, f"❌ Code HTTP {response.status_code}", None
    except Exception as e:
        return False, f"❌ Erreur : {e}", None


def main():
    print("\n🔍 Vérification du conteneur MiniStudioGPT v1.4.4")
    print("=" * 55)

    # 1️⃣ Test local (Docker direct)
    ok_local, msg_local, data_local = check_endpoint(LOCAL_URL)
    print(f"\n📡 Test local ({LOCAL_URL}) : {msg_local}")

    # 2️⃣ Test Cloudflare (si tunnel actif)
    ok_cloud, msg_cloud, data_cloud = check_endpoint(CLOUDFLARE_URL)
    print(f"☁️  Test Cloudflare ({CLOUDFLARE_URL}) : {msg_cloud}")

    # 3️⃣ Résumé global
    print("\n🧾 Résumé")
    print("-" * 55)
    if ok_local:
        print("✅ Conteneur local : en ligne et fonctionnel")
    else:
        print("❌ Conteneur local : non accessible")

    if ok_cloud:
        print("✅ Tunnel Cloudflare : opérationnel")
    else:
        print("⚠️ Tunnel Cloudflare : injoignable (non bloquant)")

    # 4️⃣ Optionnel : vérifier la présence des logs critiques
    memory_path = os.path.join("memory", "session_audit.log")
    if os.path.exists(memory_path):
        size = os.path.getsize(memory_path)
        print(f"🧠 Log d’audit détecté ({size} octets)")
    else:
        print("⚠️ Aucun log d’audit trouvé dans /memory")

    print("\n🕒 Test terminé à", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 55)


if __name__ == "__main__":
    main()
