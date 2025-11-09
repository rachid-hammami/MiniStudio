
# Cahier des Charges – MiniStudioGPT  
## Étape 1.5 – CORTEX (Module d’Intelligence Interne)  
**Version : 1.5**  
**Projet : MiniStudio**  
**Auteur : MiniStudioGPT**

---

# 1. Objectif général

Développer le module **CORTEX**, partie centrale de l’intelligence interne de MiniStudio.  
Le Cortex doit être capable de :

- comprendre la structure complète du projet MiniStudio,
- analyser le code source et détecter les incohérences,
- proposer ou appliquer des corrections intelligentes,
- faciliter la création automatique de fichiers,
- assurer la cohérence globale du projet (imports, modules, arborescence),
- servir de moteur d’analyse pour les étapes futures (1.6+, automatisation).

CORTEX agit comme un **IDE interne** : un “cerveau technique” connecté à la project map et aux logs.

---

# 2. Périmètre et contexte

Le Cortex arrive après :

- **1.4.4 — CI/CD**, qui gère patch, recovery, audit, tests  
- **1.4.5 — Structure & Project Map**, qui génère la carte complète du projet

Il s’appuie donc sur :

- `/project/map`
- project_map.json
- snapshots système
- project tree
- logs de session (`session.log`, `session_audit.log`)

---

# 3. Modules à créer

## 3.1. Dossier Cortex

```
fastapi_app/cortex/
```

## 3.2. Fichier principal du moteur Cortex

```
fastapi_app/cortex/cortex_engine.py
```

## 3.3. Service Cortex

```
fastapi_app/services/cortex_service.py
```

## 3.4. Endpoints API Cortex

```
fastapi_app/endpoints/endpoints_cortex.py
```

Expose :

- `/cortex/analyze`
- `/cortex/check-integrity`
- `/cortex/suggest`
- `/cortex/auto-fix`
- `/cortex/map-inspect`
- `/cortex/scan-missing-files`

---

# 4. Fonctionnalités à implémenter

## 4.1. Analyse de la Project Map

- lecture complète  
- détection de :
  - fichiers manquants
  - imports cassés
  - modules orphelins
  - incohérences structurelles  

## 4.2. Analyse de cohérence du code

- vérification des conventions MiniStudio  
- présence des services et endpoints obligatoires  
- organisation interne  

## 4.3. Détection automatique d’erreurs

- fichiers vides  
- imports circulaires  
- incohérences de structure  
- anomalies potentielles  

## 4.4. Suggestions intelligentes

- création de fichiers  
- nettoyage  
- corrections structurelles  
- améliorations  

## 4.5. Actions automatiques (option)

- création automatique  
- réparation des imports  
- insertion de templates  

---

# 5. Endpoints à créer

## `/cortex/analyze`

Rapport global.

## `/cortex/check-integrity`

Vérifie la cohérence.

## `/cortex/suggest`

Propositions intelligentes.

## `/cortex/map-inspect`

Inspection ciblée.

## `/cortex/auto-fix`

Corrections automatiques.

---

# 6. Logs et historique

Tout doit être logué :

```
[CORTEX] YYYY-MM-DD HH:MM:SS — Analyse réalisée
[CORTEX] Suggestion : créer service manquant
```

---

# 7. Sécurité & isolation

- aucune modification sans validation  
- pas d'exécution de code arbitraire  
- lecture uniquement de l’arborescence MiniStudio  

---

# 8. Résultat final attendu

- moteur d’analyse Cortex  
- services opérationnels  
- endpoints actifs  
- suggestions intelligentes  
- base de l’automatisation (1.6)  

---

# 9. Livrables finaux

- code du Cortex  
- README_CORTEX.md  
- project_map.json mise à jour  
- snapshots  
- logs  
- tests unitaires minimum  

---

