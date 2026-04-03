# 🎭 Système de Reconnaissance Faciale

Projet de reconnaissance faciale en temps réel utilisant OpenCV et la webcam. Le système permet de **collecter des visages**, **entraîner un modèle** et **identifier des personnes** en direct.

---

## 📁 Structure du projet

```
projet/
├── made_stock.py           # Capture et sauvegarde des images de visages
├── made_train.py           # Entraînement du modèle LBPH
├── reconnaissance_faciale.py  # Reconnaissance en temps réel
├── compile.bat             # Script d'automatisation (Windows)
├── data_image/             # Dossier des images d'entraînement (créé automatiquement)
│   └── <nom_sujet>/        # Sous-dossier par personne
├── labels.pickle           # Correspondance ID ↔ nom (généré par made_train.py)
└── trainner.yml            # Modèle entraîné (généré par made_train.py)
```

---

## ⚙️ Prérequis

### Dépendances Python

```bash
pip install opencv-python opencv-contrib-python numpy
```

> **Important :** `opencv-contrib-python` est nécessaire pour accéder au module `cv2.face` (LBPH).

### Fichier Haar Cascade

Le fichier `haarcascade_frontalface_alt2.xml` est inclus dans le package OpenCV. Le chemin par défaut dans le code est :

```
C:/Users/EG/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml
```

> Si votre installation est différente, modifiez ce chemin dans `made_stock.py` et `reconnaissance_faciale.py`.

---

## 🚀 Utilisation

### Option 1 — Via le script automatique (recommandé)

```batch
compile.bat <NOM_DU_SUJET>
```

**Exemple :**
```batch
compile.bat Alice
```

Ce script enchaîne automatiquement les 3 étapes :
1. Capture des images du sujet `Alice`
2. Entraînement du modèle sur toutes les images disponibles
3. Lancement de la reconnaissance en temps réel

> Si aucun nom n'est fourni, le script passe directement à l'entraînement puis à la reconnaissance.

---

### Option 2 — Étape par étape (manuel)

#### Étape 1 — Capturer les images d'un sujet

```bash
python made_stock.py <NOM_DU_SUJET>
```

**Contrôles lors de la capture :**

| Touche | Action |
|--------|--------|
| `s` | Activer / désactiver la sauvegarde des images |
| `q` | Quitter |

Les images sont sauvegardées dans `data_image/<NOM_DU_SUJET>/`. Répétez cette étape pour chaque personne à enregistrer.

---

#### Étape 2 — Entraîner le modèle

```bash
python made_train.py
```

Ce script parcourt le dossier `data_image/`, associe chaque sous-dossier à un identifiant numérique, et entraîne un modèle **LBPH (Local Binary Pattern Histogram)**. Il génère :
- `trainner.yml` — le modèle entraîné
- `labels.pickle` — la correspondance entre les IDs et les noms

---

#### Étape 3 — Lancer la reconnaissance

```bash
python reconnaissance_faciale.py
```

La webcam s'active et affiche en temps réel :
- Un **rectangle vert** autour des visages reconnus avec le nom de la personne
- Un **rectangle rouge** autour des visages inconnus avec la mention `inconnu`
- Le **score de confiance** (plus il est bas, meilleure est la correspondance)

Appuyez sur `q` pour quitter.

---

## 🧠 Fonctionnement technique

```
Webcam
  │
  ▼
Détection des visages (Haar Cascade)
  │  → Découpe la région du visage (ROI)
  │  → Redimensionne en 50×50 px (niveaux de gris)
  ▼
made_stock.py  ──────────────────────────────────▶  data_image/<sujet>/
                  Sauvegarde les images capturées

made_train.py  ──────────────────────────────────▶  trainner.yml
                  Lit les images, entraîne LBPH         labels.pickle

reconnaissance_faciale.py
  │  → Détecte les visages en live
  │  → Prédit l'identité via LBPH
  │  → Seuil de confiance ≤ 115 → personne connue
  └  → Seuil de confiance > 115 → "inconnu"
```

### Seuil de confiance

Le modèle LBPH retourne un score de confiance (distance). Plus il est **bas**, plus la correspondance est **fiable** :

| Score | Interprétation |
|-------|----------------|
| 0 – 50 | Très bonne correspondance |
| 50 – 115 | Correspondance acceptable (personne reconnue) |
| > 115 | Visage inconnu |

---

## 📝 Notes

- Plus vous capturez d'images par personne (et dans des conditions variées : éclairage, angle, expression), plus la reconnaissance sera précise.
- L'entraînement doit être **relancé** (`made_train.py`) à chaque ajout d'un nouveau sujet.
- Le projet fonctionne sous **Windows**. Sur Linux/macOS, adaptez les séparateurs de chemin dans `made_train.py` (`\\` → `/`).
