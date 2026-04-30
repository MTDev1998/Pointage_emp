# Attendance System - Reconnaissance Faciale Premium

Ce projet est un système de gestion de présence (pointage) basé sur la reconnaissance faciale, utilisant Python, OpenCV et PyQt5 pour une interface moderne et intuitive.

## 🚀 Fonctionnalités

- **Interface Moderne** : Design sombre (Dark Mode) avec des animations fluides et une navigation intuitive.
- **Enregistrement des Employés** : Capture de visages simplifiée et stockage sécurisé dans une base de données MySQL.
- **Pointage par Reconnaissance Faciale** : Reconnaissance en temps réel avec validation par touche (Appuyez sur 'P').
- **Statistiques & Rapports** : Visualisation des heures de travail via des graphiques et export des données vers Excel.
- **Gestion Centralisée** : Modification et suppression des employés avec nettoyage automatique des données.

## 🛠️ Installation

### 1. Prérequis
Assurez-vous d'avoir Python 3.x installé, ainsi qu'un serveur MySQL (XAMPP recommandé).

### 2. Dépendances
Installez les bibliothèques nécessaires :
```bash
pip install opencv-python face_recognition PyQt5 mysql-connector-python pandas matplotlib openpyxl
```

### 3. Base de données
1. Créez une base de données nommée `employee_db` dans votre serveur MySQL.
2. Importez le fichier SQL fourni dans le dossier `BD/` (si disponible) ou créez les tables `employee` et `attendance`.

## 📖 Utilisation

1. **Lancement** : Exécutez `python HomeGui.py` pour ouvrir le menu principal.
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
© 2026 Attendance Management System - Développé avec ❤️
