from celery import shared_task
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from allauth.account.models import EmailConfirmation
from app.models import Pack
from app.serializers import PackSerializer
from django.utils import timezone

User = get_user_model()
api_key = settings.BREVO_API_KEY
frontend_url = settings.FRONTEND_URL
mail_pro = settings.MAIL_PRO


@shared_task
def envoyer_email_verification(context):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # Récupérer l'utilisateur à partir de l'e-mail
    try:
        user = User.objects.get(email=context["user_email"])
    except User.DoesNotExist:
        print(
            f"Utilisateur avec l'e-mail {context['user_email']} n'existe pas.",
            flush=True,
        )
        return

    # Rendre le template de l'e-mail
    subject = "Veuillez confirmer votre adresse e-mail"
    html_content = render_to_string("emails/verification_email.html", context)
    sender = {"name": "sample-boutique", "email": mail_pro}
    to = [{"email": user.email, "name": user.email}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, subject=subject, sender=sender
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        # Mettre à jour le champ 'sent' dans EmailConfirmation
        try:
            email_confirmation = EmailConfirmation.objects.get(
                key=context["email_confirmation_key"]
            )
            email_confirmation.sent = timezone.now()
            email_confirmation.save()
        except EmailConfirmation.DoesNotExist:
            print(
                f"EmailConfirmation avec la clé {context['email_confirmation_key']} n'existe pas.",
                flush=True,
            )
        except Exception as e:
            print(f"Erreur lors de la mise à jour du champ 'sent' : {e}", flush=True)

    except ApiException as e:
        print(
            f"Exception lors de l'envoi de l'e-mail de vérification : {e}", flush=True
        )


@shared_task
def envoyer_email_debut_abonnement(user_id, subscription_plan):
    user = User.objects.get(id=user_id)
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    context = {
        "user_email": user.email,
        "name": user.email,
        "site_url": settings.FRONTEND_URL,
        "subscription_plan": subscription_plan,
    }

    subject = "Bienvenue dans votre nouvel abonnement"
    html_content = render_to_string("emails/debut_abonnement.html", context)
    sender = {"name": "sample-boutique", "email": mail_pro}
    to = [{"email": user.email, "name": user.email}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, subject=subject, sender=sender
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(
            "Exception lors de l'envoi de l'e-mail de début d'abonnement : %s\n" % e,
            flush=True,
        )


@shared_task
def envoyer_email_fin_abonnement(user_id, subscription_plan):
    user = User.objects.get(id=user_id)
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    context = {
        "user_email": user.email,
        "name": user.email,
        "site_url": settings.FRONTEND_URL,
        "subscription_plan": subscription_plan,
    }

    subject = "Votre abonnement a expiré"
    html_content = render_to_string("emails/fin_abonnement.html", context)
    sender = {"name": "sample-boutique", "email": mail_pro}
    to = [{"email": user.email, "name": user.email}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, subject=subject, sender=sender
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(
            "Exception lors de l'envoi de l'e-mail de fin d'abonnement : %s\n" % e,
            flush=True,
        )


@shared_task
def envoyer_email_reactivation(context):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    user_email = context.get("user_email")
    reactivation_key = context.get("reactivation_key")
    site_url = context.get("site_url")
    reactivation_url = context.get("reactivation_url")

    # Récupérer l'utilisateur à partir de l'e-mail
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        print(
            f"Utilisateur avec l'e-mail {user_email} n'existe pas.",
            flush=True,
        )
        return

    # Rendre le template de l'e-mail
    subject = "Réactivation de votre compte"
    html_content = render_to_string(
        "emails/reactivation_email.html",
        {
            "user_email": user_email,
            "reactivation_key": reactivation_key,
            "reactivation_url": reactivation_url,
            "site_url": site_url,
        },
    )
    sender = {"name": "Sample Boutique", "email": mail_pro}
    to = [{"email": user.email, "name": user.get_full_name() or user.email}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, html_content=html_content, subject=subject, sender=sender
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(
            f"Exception lors de l'envoi de l'e-mail de réactivation : {e}", flush=True
        )


@shared_task
def send_newsletter():
    # Récupérer les 5 derniers packs
    last_five_packs = Pack.objects.order_by("-created_at")[:5]

    serializer = PackSerializer(last_five_packs, many=True)
    serialized_packs = serializer.data

    # Récupérer les utilisateurs qui acceptent la newsletter
    users = User.objects.filter(accept_newsletter=True, is_active=True)
    # Préparer le contenu de l'email
    subject = "Découvrez les 5 derniers packs sortis !"
    site_url = frontend_url

    # Configuration de l'API Brevo
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
    sender = {"name": "Sample Boutique", "email": mail_pro}

    # Préparer le contenu HTML de l'email
    html_content = render_to_string(
        "emails/newsletter.html", {"packs": serialized_packs, "site_url": site_url}
    )

    # Envoyer l'email à chaque utilisateur
    for user in users:
        to = [{"email": user.email, "name": user.email}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to, html_content=html_content, subject=subject, sender=sender
        )

        try:
            api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            print(
                f"Exception lors de l'envoi de l'e-mail à {user.email} : {e}",
                flush=True,
            )
