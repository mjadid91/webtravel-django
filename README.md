# 🌍 WebTravel - Gestion de Voyages (Django)

WebTravel est une application web de gestion et de réservation de voyages développée avec le framework Django. Ce projet a été réalisé dans le cadre du BUT Informatique à l'IUT d'Orsay.

L'application permet aux utilisateurs de parcourir un catalogue de voyages, de gérer un panier et de consulter leur historique de commandes. Une interface d'administration dédiée permet aux gestionnaires (Staff) de piloter les destinations, les étapes et les clients.

## 🚀 Fonctionnalités Principales

### 👤 Espace Utilisateur & Client

- **Authentification complète** : Inscription, connexion, déconnexion et réinitialisation de mot de passe par email
- **Gestion du profil** : Modification des informations personnelles et de la photo d'avatar
- **Catalogue de voyages** : Consultation des destinations disponibles et détails des étapes
- **Système de Panier** : Ajout/suppression de voyages, gestion des quantités et calcul automatique du total
- **Commandes** : Validation du paiement (simulation) et historique détaillé des achats passés

### 🛠️ Espace Administration (Staff)

- **Dashboard dédié** : Vue d'ensemble pour la gestion globale
- **Gestion du catalogue** : Création, modification et suppression des voyages et des villes
- **Gestion des étapes** : Organisation du parcours détaillé pour chaque voyage (villes et durée en jours)
- **Suivi client** : Consultation de la liste des clients inscrits et de l'historique de toutes les commandes passées sur la plateforme

## 🎨 Design & Interface

Le projet utilise un Design System "Neo-Travel" moderne basé sur Bootstrap 5 avec :

- Un thème sombre premium (Dark Mode)
- Des effets de Glassmorphism sur la barre de navigation
- Des animations fluides d'apparition (Fade-in)
- Une interface entièrement responsive

## 🛠️ Stack Technique

- **Back-end** : Django 5.x
- **Front-end** : HTML5, CSS3 (Custom Styles), Bootstrap 5, Bootstrap Icons
- **Base de données** : SQLite (par défaut)
- **Gestion des médias** : Stockage des photos de profil et des images de voyages

## 📦 Installation et Lancement

### 1. Cloner le dépôt

```bash
git clone https://git.iut-orsay.fr/r5a05tp5b/mjadid/webtravel.git
cd webtravel
```

### 2. Configuration de l'environnement

```bash
# Créer l'environnement virtuel
python -m venv env

# Activer l'environnement
# Sur Windows :
env\Scripts\activate
# Sur macOS/Linux :
source env/bin/activate
```

### 3. Installation des dépendances et migrations

```bash
pip install django pillow
python manage.py migrate
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

**Accès** : 👉 http://127.0.0.1:8000/

## 📂 Structure du Projet

```
webtravel/
│── applitravel/       # Cœur de l'application (Voyages, Villes, Étapes)
│── applicompte/       # Gestion des comptes utilisateurs et profils
│── applipanier/       # Logique du panier, des commandes et de l'administration
│── images/            # Répertoire de stockage des médias (images voyages et avatars)
│── manage.py
└── README.md
```

## 👥 Auteur

**Mohamed JADID** - Projet développé dans le cadre du **BUT Informatique** à l'**IUT d'Orsay**.

## 📄 Licence

Ce projet est développé à des fins éducatives.

## 🤝 Contributions

Les contributions sont les bienvenues !

Pour contribuer :

1. Fork du projet
2. Création d'une branche (`feature/ma-feature`)
3. Commit (`git commit -m "Ajout de ma feature"`)
4. Push
5. Pull Request