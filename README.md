# NVD CVE Retriever (WIP)

## Description
**NVD CVE Retriever est un outil en ligne de commande pour récupérer des informations sur les vulnérabilités récentes à partir de la base de données NVD *(National Vulnerability Database)*.**

## Installation
Pour installer et utiliser cet outil, assurez-vous d'avoir **python>=3.9** installé sur votre système ou d'utiliser un **venv/anaconda**, puis suivez ces étapes :

1. Clonez le dépôt :
    
    ```bash
    git clone https://github.com/zxtNX/nvd_cve_retriever.git
    ```

2. Accédez au répertoire du projet :
    
    ```bash
    cd nvd_cve_retriever
    ```
3. Installez le package :
    
    ```bash
    pip install .
    ```

## Configuration
Avant de commencer à utiliser **NVD CVE Retriever**, vous devez configurer votre **clé API NVD**, cela se fait directement lors de votre premier lancement du programme :

```bash
C:\Users\reddandy\nvd_cve_retriever> nvd_cve_retriever
Veuillez entrer votre clé API NVD : ***********
```

Après cela, vous aurez un fichier d'environnement pour votre configuration qui sera créé à l'emplacement suivant :
* ``C:\Users\{username}\AppData\Roaming\nvd_cve_retriever\config\.env`` pour **Windows**
* ``/home/{username}/.nvd_cve_retriever/config/.env`` pour **Unix/Linux/macOS**

Ce fichier contiendra alors votre clé API NVD, ainsi que le chemin vers la version de l'API que vous utiliserez lors des requêtes que fera l'outil pour récupérer les CVEs *(par défaut API v2 utilisée)*.

Vous pouvez également rajouter ce fichier manuellement en créant les bons répertoires et en rajoutant les bonnes valeurs, comme par exemple :

````bash
NVD_API_KEY=votre_clé_api_ici
NVD_API_URL=https://services.nvd.nist.gov/rest/json/cves/2.0
````

## Utilisation
Pour utiliser **NVD CVE Retriever**, exécutez la commande suivante dans votre terminal :

````bash
nvd_cve_retriever [options]
````

### Options
* **-d, --days :** Nombre de jours depuis aujourd'hui pour chercher les nouvelles CVEs. Par défaut à 1.
* **-v, --verbose :** Augmente la verbosité des logs.
* **-o, --output :** Spécifie un chemin de répertoire de sortie personnalisé pour les résultats.

Cas d'usage pour récupérer les CVEs des 3 derniers jours avec des logs détaillés :

````bash
nvd_cve_retriever -d 3 -v
````
Vous pourrez par la suite retrouver le détails des outputs dans un fichier JSON et TXT soit via le répertoire que vous auriez spécifié dans le cas où vous utiliseriez l'option ``-o`` ou alors dans l'emplacement par défaut :
* ``C:\Users\{username}\AppData\Roaming\nvd_cve_retriever\outputs`` pour **Windows**
* ``/home/{username}/.nvd_cve_retriever/outputs`` pour **Unix/Linux/macOS**

## Debugging

Les logs se situent dans le même dossier parent que celui des outputs ou du dossier de configuration, soit : 
* ``C:\Users\{username}\AppData\Roaming\nvd_cve_retriever\logs`` pour **Windows**
* ``/home/{username}/.nvd_cve_retriever/logs`` pour **Unix/Linux/macOS**
