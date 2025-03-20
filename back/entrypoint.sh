#!/bin/sh

# Attendre que la base de données soit disponible
echo "Attente de la disponibilité de la base de données..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Base de données disponible!"

echo "Création des migrations..."
python manage.py makemigrations

# Exécuter les migrations
echo "Exécution des migrations..."
python manage.py migrate

# Charger les données initiales
echo "Chargement des données initiales..."
python manage.py loaddata genres.yaml types.yaml subType.yaml subscription_plans.json

# Exécuter la commande de management personnalisée pour configurer les Sites et SocialApps
echo "Configuration des données initiales..."
python manage.py setup_initial_data

# Vérifier la variable IN_PROD
if [ "$IN_PROD" = "True" ]; then
    echo "Mode Production"
    # Démarrer Gunicorn
    exec gunicorn deepBack.wsgi:application --bind 0.0.0.0:$PORT
else
    echo "Mode Développement"
    # Démarrer le serveur de développement Django
    exec python manage.py runserver 0.0.0.0:$PORT
fi
