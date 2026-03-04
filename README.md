# MiniStudio -- Environnement de développement structuré (FastAPI & React)

## Description

MiniStudio est un environnement de développement personnel construit
avec **FastAPI (Python)** et **React (Vite)**.

Il permet d'expérimenter :

-   Architecture backend modulaire
-   API REST structurée
-   Persistance des données
-   Automatisation via CI/CD
-   Dockerisation complète

Le projet sert de laboratoire d'architecture backend et d'organisation
applicative.

------------------------------------------------------------------------

## Stack technique

### Backend

-   FastAPI (Python)
-   Architecture modulaire
-   Pytest

### Frontend

-   React (Vite)
-   Tailwind CSS

### Infrastructure

-   Docker
-   Docker Compose
-   GitHub Actions (CI/CD)

------------------------------------------------------------------------

## Fonctionnalités principales

-   API REST organisée par modules
-   Système de persistance des données
-   Tests automatisés
-   Pipeline CI/CD
-   Structure évolutive

------------------------------------------------------------------------

## Installation locale

``` bash
git clone https://github.com/rachid-hammami/MiniStudio.git
cd MiniStudio
pip install -r requirements.txt
uvicorn fastapi_app.main:app --reload
```

------------------------------------------------------------------------

## Documentation technique

La documentation complète (architecture détaillée, modules, historique
versions) est disponible dans le dossier `/docs`.

------------------------------------------------------------------------

Projet maintenu par **Rachid Hammami**.
