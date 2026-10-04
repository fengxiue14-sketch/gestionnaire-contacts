# Gestionnaire de Contacts

Cinquième projet de la **Forteresse YUAN**.

## Objectif

CRUD complet en Python avec persistance JSON.

## Fonctionnalités

- Ajouter un contact (nom, téléphone, email)
- Lister tous les contacts (triés alphabétiquement)
- Rechercher un contact (par nom, insensible à la casse)
- Modifier un contact existant
- Supprimer un contact (avec confirmation)
- Persistance automatique dans `contacts.json`
- IDs uniques (UUID v4)
- Validation : pas de doublons de nom

## Installation

Aucune dépendance externe. Python 3.10+ requis.

## Usage

```bash
python contacts.py