# 🧠 MiniStudioGPT — Cahier des Charges v1.6 : Cortex Feedback Loop (Mémoire & Apprentissage Cognitif)

## 📅 Contexte général
Ce cahier des charges définit la feuille de route technique pour la **version v1.6 du projet MiniStudioGPT**, appelée **CORTEX Feedback Loop**.  
Il s’appuie directement sur la base solide établie dans les versions précédentes :
- **v1.4.6 — Cortex Sync Layer** : synchronisation mémoire et audit.
- **v1.5 — Cortex Engine** : moteur d’analyse, de suggestion et de correction automatique.

L’objectif de la **v1.6** est de faire évoluer le CORTEX d’un moteur d’analyse à un **système cognitif apprenant et adaptatif** capable de comprendre, d’évaluer et d’améliorer son propre comportement dans le temps.

---

## 🧠 1️⃣ Objectif principal
Mettre en place une **boucle de rétroaction cognitive** ("Feedback Loop") permettant au CORTEX de :
1. **Observer** ses propres actions (analyze, suggest, auto-fix, applycode).  
2. **Apprendre** des résultats de ses analyses passées.  
3. **S’ajuster** automatiquement pour améliorer sa précision et sa cohérence.  
4. **Documenter** son apprentissage dans des rapports auto-générés.

---

## 🧩 2️⃣ Description fonctionnelle

### 🔹 2.1. Modules à développer

| Module | Description | Fichiers impliqués |
|---------|--------------|--------------------|
| **Cortex Feedback Core** | Noyau logique gérant la collecte et l’analyse des feedbacks | `cortex_feedback.py` |
| **Feedback Service Layer** | Service FastAPI pour manipuler les données de feedback | `cortex_feedback_service.py` |
| **Memory Integration** | Extension du `cortex_memory.py` pour le stockage des feedbacks vectorisés | `cortex_memory.py` |
| **Docs Auto-Reporter** | Génère automatiquement des rapports cognitifs Markdown | `/docs/Cortex_History_Report.md` |
| **CI/CD Feedback Runner** | Étend la pipeline YAML pour déclencher le feedback post-build | `.github/workflows/cortex_feedback.yml` |

---

### 🔹 2.2. Données manipulées
Les retours du CORTEX seront stockés dans :
```
memory/
├── cortex_feedback.json        ← Nouvel historique d’apprentissage
├── memoire.json                ← Mémoire principale Cortex
├── session_audit.log           ← Journal des actions
├── feedback_vectorstore/       ← (Optionnel) FAISS/Chroma pour recherche sémantique
└── reports/
    ├── Cortex_History_Report.md
    └── Cortex_Feedback_Stats.md
```

### 🔹 2.3. Structure du fichier `cortex_feedback.json`
```json
{
  "version": "1.6",
  "timestamp": "2025-11-09T18:42:00Z",
  "feedback_events": [
    {
      "endpoint": "/cortex/analyze",
      "context": "fastapi_app/endpoints_cortex.py",
      "status": "success",
      "patterns_detected": ["Empty file", "Docker naming issue"],
      "correction_applied": true,
      "confidence_score": 0.92,
      "tags": ["[FEEDBACK]", "[LEARNING]"]
    }
  ],
  "patterns_summary": {
    "recurring_issues": ["__init__.py empty", "docker file name"],
    "improvement_rate": 14.3,
    "avg_confidence": 0.86
  }
}
```

---

## ⚙️ 3️⃣ Endpoints API à implémenter

| Méthode | Route | Description |
|----------|--------|-------------|
| `POST` | `/cortex/feedback/log` | Enregistre un événement d’apprentissage (action + résultat) |
| `GET` | `/cortex/feedback/stats` | Retourne les statistiques globales d’amélioration |
| `GET` | `/cortex/feedback/trends` | Analyse l’évolution des anomalies et leur correction |
| `POST` | `/cortex/memory/query` | Recherche sémantique dans la mémoire vectorielle (FAISS) |
| `GET` | `/cortex/health` | Retourne l’état cognitif global (intégrité, stabilité, score apprentissage) |

---

## 🧬 4️⃣ Comportement attendu

1. Chaque action Cortex (analyze, suggest, auto-fix, applycode) déclenche un **événement feedback**.  
2. Ces événements sont centralisés dans `cortex_feedback.json`.  
3. Le système agrège les patterns récurrents et ajuste ses suggestions futures.  
4. Un **rapport automatique** est généré sous `/docs/Cortex_History_Report.md`.  
5. La pipeline CI/CD déclenche la collecte et l’analyse du feedback après chaque déploiement.  

---

## 🧠 5️⃣ Intelligence adaptative (Extensions proposées)
### 🔸 Score de confiance dynamique
Chaque correction et suggestion doit inclure un **champ `confidence_score`** (0–1).  
Ce score influence la pondération des futures recommandations.

### 🔸 Analyse prédictive (préparation v1.7)
Le CORTEX doit identifier des **tendances temporelles** :
- fichiers les plus souvent corrigés,
- types d’anomalies récurrentes,
- causes principales d’erreurs.

### 🔸 Visualisation des feedbacks
Créer des graphiques (Markdown ou HTML léger) représentant :
- fréquence des corrections par module,  
- taux d’amélioration par version,  
- score global d’intelligence cognitive.  

---

## 🔄 6️⃣ Intégration CI/CD (GitHub Actions)
### YAML additionnel : `.github/workflows/cortex_feedback.yml`
Étapes à ajouter :
1. Exécuter `/cortex/analyze` → `/cortex/feedback/log`  
2. Générer le rapport Markdown sous `docs/`  
3. Commit automatique du rapport (`git push origin feedback-loop`)  
4. Publier le statut dans la console CI  
5. Déclencher `/cortex/health` pour validation finale

---

## 🧩 7️⃣ Livrables attendus

| Type | Fichier / Endpoint | Description |
|------|--------------------|--------------|
| Code | `cortex_feedback.py` | Moteur principal d’analyse de feedback |
| API | `/cortex/feedback/*` | Interface REST complète du module feedback |
| Données | `memory/cortex_feedback.json` | Historique global des actions Cortex |
| Rapport | `docs/Cortex_History_Report.md` | Rapport Markdown auto-généré |
| CI/CD | `.github/workflows/cortex_feedback.yml` | Workflow de boucle cognitive |

---

## 📈 8️⃣ Objectif final
> Rendre MiniStudioGPT **autonome dans son apprentissage**.  
> Le Cortex doit non seulement détecter les problèmes, mais aussi apprendre de ses corrections pour améliorer sa pertinence et documenter ses progrès dans le temps.

---

## 🧾 9️⃣ Annexes & amélioration continue
- Intégration future de **FAISS / Chroma** pour recherche sémantique.  
- Ajout d’un module de visualisation interactive (v1.7).  
- Amélioration du moteur de pondération cognitive.  
- Mise en place du **Cortex Predictive Engine (v2.0)**.

---

**Auteur :** Code GPT & Rachid  
**Version :** 1.6  
**Nom de version :** Cortex Feedback Loop  
**Date de rédaction :** 2025-11-09  
**Statut :** Cahier des charges validé et enrichi  
