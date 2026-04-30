# Attendance System - Reconnaissance Faciale Premium

Ce projet est un système de gestion de présence (pointage) basé sur la reconnaissance faciale, utilisant Python, OpenCV et PyQt5 pour une interface moderne et intuitive.

## ⚡ Démarrage Rapide

1. **Lancer la base de données** :
   ```powershell
   docker-compose up -d
   ```
2. **Lancer l'application** :
   ```powershell
   python HomeGui.py
   ```

## 🚀 Fonctionnalités

- **Interface Moderne** : Design sombre (Dark Mode) avec des animations fluides et une navigation intuitive.
- **Enregistrement des Employés** : Capture de visages simplifiée et stockage sécurisé dans une base de données MySQL.
- **Pointage par Reconnaissance Faciale** : Reconnaissance en temps réel avec validation par touche (Appuyez sur 'P').
- **Statistiques & Rapports** : Visualisation des heures de travail via des graphiques et export des données vers Excel.
- **Gestion Centralisée** : Modification et suppression des employés avec nettoyage automatique des données.

## 🛠️ Installation

### 1. Prérequis
- Python 3.x
- Docker & Docker Compose

### 2. Installation de l'environnement
Il est recommandé d'utiliser un environnement virtuel :
```powershell
# Création de l'environnement
python -m venv venv

# Activation (Windows)
.\venv\Scripts\activate

# Installation des dépendances
pip install -r requirements.txt
```

### 3. Base de données (Docker)
Le projet utilise Docker pour simplifier la gestion de MySQL. Le fichier `BD/employee_db.sql` est utilisé pour initialiser automatiquement la base.

## 📖 Utilisation

1. **Préparation** : Assurez-vous que le conteneur MySQL est actif avec `docker-compose up -d`.
2. **Lancement** : Exécutez `python HomeGui.py` pour ouvrir le menu principal.
2. **Ajout d'un Employé** : Allez dans "About User" -> "Add New". Suivez les instructions pour capturer le visage.
3. **Entraînement** : Le système s'entraîne automatiquement après l'ajout, mais vous pouvez aussi lancer `training.py`.
4. **Pointage** : 
   - Cliquez sur "Mark Attendance".
   - Placez l'employé devant la caméra.
   - Appuyez sur **'P'** pour valider le pointage.
5. **Rapports** : Cliquez sur "Show Details" pour voir l'historique et exporter les rapports.

## 📁 Structure du Projet

- `HomeGui.py` : Menu principal de l'application.
- `collect_data.py` : Module de capture d'images pour les nouveaux employés.
- `training.py` : Encodage des visages pour la reconnaissance.
- `attendance_recognition3.py` : Moteur de reconnaissance faciale en temps réel.
- `database.py` : Gestion centralisée des connexions MySQL.
- `styles.py` : Thème graphique global de l'application.
- `data/` : Dossier contenant les captures de visages (organisées par ID).

---
© 2026 Attendance Management System - Développé avec ❤️  BY MOUSSAOUI TAREK
