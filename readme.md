# MLOps Application

Application MLOps avec architecture client-serveur pour le déploiement et la gestion de modèles de machine learning.

## 📋 Prérequis

Avant de lancer l'application, assurez-vous d'avoir installé :

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 ou supérieure)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29 ou supérieure)
- Git

## 🚀 Installation et Lancement

### 1. Cloner le repository

```bash
git clone https://github.com/Abdourahmane2/mlops.git
cd mlops
```

### 2. Lancer l'application avec Docker Compose

La méthode la plus simple pour lancer l'application est d'utiliser Docker Compose :

```bash
docker-compose up --build
```

Cette commande va :
- Construire les images Docker pour le client et le serveur
- Démarrer les conteneurs
- Configurer le réseau entre les services

### 3. Accéder à l'application

Une fois les conteneurs lancés, l'application devrait être accessible :

- **Client (Frontend)** : `http://127.0.0.1:8501/` 
- **Server (Backend/API)** : `http://localhost:8000/docs#/` 


## 🛠️ Commandes Utiles

### Lancer en mode détaché (en arrière-plan)

```bash
docker-compose up -d
```

### Arrêter l'application

```bash
docker-compose down
```

### Arrêter et supprimer les volumes

```bash
docker-compose down -v
```

### Voir les logs

```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f server
docker-compose logs -f client
```

### Rebuild les images

```bash
docker-compose build --no-cache
```

### Redémarrer un service spécifique

```bash
docker-compose restart server
# ou
docker-compose restart client
```

## 📁 Structure du Projet

```
mlops/
├── client/              # Application frontend
├── server/              # Application backend/API
├── TD/                  # Travaux dirigés et documentation
├── docker-compose.yml   # Configuration Docker Compose
└── README.md           # Ce fichier
```



### Personnaliser docker-compose.yml

Vous pouvez modifier le fichier `docker-compose.yml` pour :
- Changer les ports exposés
- Ajouter des volumes
- Configurer des variables d'environnement
- Ajouter des services (base de données, Redis, etc.)




## 📚 Développement

### Mode développement

Pour le développement avec rechargement automatique :

```bash
docker-compose up
```

Les volumes sont généralement configurés pour permettre le rechargement à chaud des modifications.

### Exécuter des commandes dans un conteneur

```bash
# Accéder au shell du serveur
docker-compose exec server bash

# Accéder au shell du client
docker-compose exec client sh
```



## 📊 MLOps - Fonctionnalités

Cette application MLOps inclut typiquement :

- ✅ Entraînement de modèles
- ✅ Versionnement de modèles
- ✅ Déploiement de modèles
- ✅ Monitoring et logging
- ✅ API REST pour les prédictions
- ✅ Interface utilisateur pour la gestion

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request


## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

## 🔗 Liens Utiles

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [MLOps Best Practices](https://ml-ops.org/)



