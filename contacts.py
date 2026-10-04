#!/usr/bin/env python3
"""
Gestionnaire de Contacts - Projet 05 de la Forteresse YUAN.
CRUD complet avec persistance JSON.
"""

import json
import sys
import uuid
from pathlib import Path
from datetime import datetime


CONTACTS_FILE = Path(__file__).parent / "contacts.json"


# ============================================================
# PERSISTANCE
# ============================================================

def charger_contacts():
    """Charge les contacts depuis contacts.json."""
    if not CONTACTS_FILE.exists():
        return []
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def sauvegarder_contacts(contacts):
    """Sauvegarde les contacts dans contacts.json."""
    try:
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"[AVERTISSEMENT] Impossible de sauvegarder : {e}", file=sys.stderr)


# ============================================================
# AFFICHAGE
# ============================================================

def afficher_titre(titre):
    """Affiche un titre encadre."""
    print()
    print("=" * 60)
    print(f"  {titre}")
    print("=" * 60)


def afficher_contact(contact, index=None):
    """Affiche un contact formaté."""
    prefix = f"{index}. " if index else "  "
    print(f"{prefix}{contact['nom']}")
    print(f"     Téléphone : {contact.get('telephone', '(non renseigné)')}")
    print(f"     Email     : {contact.get('email', '(non renseigné)')}")
    print(f"     Créé le   : {contact.get('date_creation', '?')[:10]}")
    print()


def afficher_contacts(contacts):
    """Affiche tous les contacts triés."""
    afficher_titre(f"Contacts ({len(contacts)})")
    
    if not contacts:
        print("  Aucun contact. Ajoute-en un !")
        return
    
    # Trier par nom
    contacts_tries = sorted(contacts, key=lambda c: c["nom"].lower())
    
    for i, contact in enumerate(contacts_tries, 1):
        afficher_contact(contact, i)


# ============================================================
# CRUD
# ============================================================

def demander_texte(prompt, obligatoire=True):
    """Demande un texte avec validation."""
    while True:
        valeur = input(prompt).strip()
        if valeur or not obligatoire:
            return valeur
        print("  Ce champ est obligatoire.")


def contact_existe(contacts, nom):
    """Vérifie si un contact avec ce nom existe."""
    return any(c["nom"].lower() == nom.lower() for c in contacts)


def ajouter_contact(contacts):
    """Ajoute un nouveau contact."""
    afficher_titre("Ajouter un contact")
    
    nom = demander_texte("Nom : ")
    
    if contact_existe(contacts, nom):
        print(f"[ERREUR] Un contact nommé '{nom}' existe déjà.")
        return False
    
    telephone = demander_texte("Téléphone (optionnel) : ", obligatoire=False)
    email = demander_texte("Email (optionnel) : ", obligatoire=False)
    
    contact = {
        "id": str(uuid.uuid4()),
        "nom": nom,
        "telephone": telephone,
        "email": email,
        "date_creation": datetime.now().isoformat(),
    }
    
    contacts.append(contact)
    sauvegarder_contacts(contacts)
    
    print(f"\n[BINGO] Contact '{nom}' ajouté !")
    return True


def rechercher_contact(contacts):
    """Recherche un contact par nom."""
    afficher_titre("Rechercher un contact")
    
    if not contacts:
        print("  Aucun contact.")
        return None
    
    terme = demander_texte("Nom à rechercher : ").lower()
    
    resultats = [c for c in contacts if terme in c["nom"].lower()]
    
    if not resultats:
        print(f"Aucun contact trouvé pour '{terme}'.")
        return None
    
    print(f"\n{len(resultats)} résultat(s) :\n")
    for contact in resultats:
        afficher_contact(contact)
    
    return resultats


def choisir_contact(contacts, action):
    """Laisse l'utilisateur choisir un contact parmi la liste."""
    afficher_titre(f"{action} un contact")
    
    if not contacts:
        print("  Aucun contact.")
        return None
    
    contacts_tries = sorted(contacts, key=lambda c: c["nom"].lower())
    
    for i, contact in enumerate(contacts_tries, 1):
        print(f"  {i}. {contact['nom']} ({contact.get('telephone', 'sans tel')})")
    
    print("  0. Annuler")
    
    while True:
        try:
            choix = input("\nTon choix : ").strip()
            if choix == "0":
                return None
            idx = int(choix) - 1
            if 0 <= idx < len(contacts_tries):
                return contacts_tries[idx]
            print("Choix invalide.")
        except ValueError:
            print("Entre un nombre.")


def modifier_contact(contacts):
    """Modifie un contact existant."""
    contact = choisir_contact(contacts, "Modifier")
    if not contact:
        return False
    
    afficher_titre(f"Modifier '{contact['nom']}'")
    print(f"  (laisse vide pour garder la valeur actuelle)\n")
    
    nouveau_nom = input(f"Nom [{contact['nom']}] : ").strip()
    nouveau_tel = input(f"Téléphone [{contact.get('telephone', '')}] : ").strip()
    nouveau_email = input(f"Email [{contact.get('email', '')}] : ").strip()
    
    if nouveau_nom:
        if nouveau_nom.lower() != contact["nom"].lower() and contact_existe(contacts, nouveau_nom):
            print(f"[ERREUR] Un contact nommé '{nouveau_nom}' existe déjà.")
            return False
        contact["nom"] = nouveau_nom
    
    if nouveau_tel:
        contact["telephone"] = nouveau_tel
    
    if nouveau_email:
        contact["email"] = nouveau_email
    
    contact["date_modification"] = datetime.now().isoformat()
    
    sauvegarder_contacts(contacts)
    print(f"\n[BINGO] Contact '{contact['nom']}' modifié !")
    return True


def supprimer_contact(contacts):
    """Supprime un contact."""
    contact = choisir_contact(contacts, "Supprimer")
    if not contact:
        return False
    
    confirmation = input(f"\nConfirmer la suppression de '{contact['nom']}' ? (o/N) : ").strip().lower()
    
    if confirmation != "o":
        print("Suppression annulée.")
        return False
    
    contacts.remove(contact)
    sauvegarder_contacts(contacts)
    print(f"\n[BINGO] Contact '{contact['nom']}' supprimé !")
    return True


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():
    """Menu principal."""
    contacts = charger_contacts()
    
    while True:
        afficher_titre("GESTIONNAIRE DE CONTACTS")
        print(f"  {len(contacts)} contact(s) enregistré(s)")
        print()
        print("  1. Ajouter un contact")
        print("  2. Lister tous les contacts")
        print("  3. Rechercher un contact")
        print("  4. Modifier un contact")
        print("  5. Supprimer un contact")
        print("  6. Quitter")
        print("=" * 60)
        
        choix = input("Ton choix : ").strip()
        
        if choix == "1":
            ajouter_contact(contacts)
        elif choix == "2":
            afficher_contacts(contacts)
        elif choix == "3":
            rechercher_contact(contacts)
        elif choix == "4":
            modifier_contact(contacts)
        elif choix == "5":
            supprimer_contact(contacts)
        elif choix == "6":
            print("\nAu revoir !")
            break
        else:
            print("Choix invalide.")


def main():
    """Point d'entrée."""
    print()
    print("=" * 60)
    print("  GESTIONNAIRE DE CONTACTS v1.0")
    print("  Projet 05 - Forteresse YUAN")
    print("=" * 60)
    
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nInterrompu. Au revoir !")
        return 1
    except Exception as e:
        print(f"\n[FATAL] {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())