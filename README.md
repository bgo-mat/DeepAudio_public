# E-commerce sample audio Backend

## English

### Run the API
At the repository root, run:

```bash
docker compose up -d
```

Then open:

```
http://localhost:8000/api/schema/swagger-ui/#/
```

To check request timings:

```
http://localhost:8000/silk/
```

### Tools & Technologies

- Python 3.12 with Django 5 and Django REST framework
- PostgreSQL database
- Redis & Celery for asynchronous tasks
- drf-spectacular for OpenAPI documentation
- Stripe for payments
- Brevo (SendinBlue) for transactional mails
- OpenAI integration for pack description and naming
- boto3 with S3 storage
- pydub for audio processing
- Docker Compose for development

## Français

### Lancer l'API
À la racine du dépôt, exécutez :

```bash
docker compose up -d
```

Puis rendez-vous sur :

```
http://localhost:8000/api/schema/swagger-ui/#/
```

Pour visualiser les temps d'exécution des requêtes :

```
http://localhost:8000/silk/
```

### Outils et technologies

- Python 3.12 et Django 5 avec Django REST framework
- Base de données PostgreSQL
- Redis et Celery pour les tâches asynchrones
- drf-spectacular pour la documentation OpenAPI
- Stripe pour les paiements
- Brevo (SendinBlue) pour les emails transactionnels
- OpenAI pour générer noms et descriptions de pack
- boto3 avec stockage S3
- pydub pour le traitement audio
- Docker Compose pour lancer l'ensemble du projet
