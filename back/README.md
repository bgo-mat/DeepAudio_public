<h1>INSTRUCTIONS</h1>
run docker :

    docker compose up -d

Dans /admin : <br>
Add Site : nom du domaine
<br>
Add Social application 
<br>
<br>
<h1>Link</h1> : <br>
Swagger : http://localhost:8000/api/schema/swagger-ui/#/ <br>
Silk : http://localhost:8000/silk/

<h1>Stripe test local :</h1><br>
    commande:

        stripe listen --forward-to localhost:8000/api/webhook/ 
        stripe trigger checkout.session.completed 
        stripe trigger invoice.payment_succeeded 
        stripe trigger customer.subscription.deleted 

<h1>Connexion vps :</h1><br>
    commande :

    move .env : 
        -scp .env debian@57.128.178.248:/home/debian/
        -sudo mv /home/debian/.env /home/debian/deepAudio/back/ (dans vps)

    delete conteneur : 
        -docker rm -f deepaudio-backend deepaudio-db deepaudio-redis deepaudio-celery-beat deepaudio-celery 
        -docker rmi back-deepaudio:latest
        -docker image prune
        -docker volume rm back_deepaudio-pgdata
        -docker volume prune
        -docker container prune
    
    log docker : docker compose logs -f backend

<h1>Create admin : </h1><br>

    In vps : 
        docker exec -it deepaudio-backend python manage.py shell
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(email='matthias.begot@gmail.com')
        user.roles = 'ADMIN'
        user.save()

<h1>Create super user : </h1><br>

    In vps : 
    docker exec -it deepaudio-backend python manage.py shell
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_superuser(
         email='matias.begot@gmail.com',
         password='Lavieestbelle!44',
         username='root'  
    )

<h1>Test newsletter sending : </h1><br>

    python mange.py shell
    from app.tasks import send_newsletter
    send_newsletter()
