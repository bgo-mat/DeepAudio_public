from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.contrib.auth import get_user_model

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_SECRET_KEY
TWITTER_CLIENT_ID = settings.TWITTER_CONSUMER_KEY
TWITTER_CLIENT_SECRET = settings.TWITTER_CONSUMER_SECRET
SITE_DOMAIN = settings.SITE_DOMAIN
SITE_NAME = settings.SITE_NAME
admin_username = settings.ADMIN_USERNAME
admin_email = settings.ADMIN_EMAIL
admin_password = settings.ADMIN_PASSWORD

User = get_user_model()


class Command(BaseCommand):
    help = "Configure les sites et les applications sociales initiales"

    def handle(self, *args, **kwargs):
        self.create_default_site()
        self.create_social_apps()

    def create_default_site(self):
        site_domain = SITE_DOMAIN
        site_name = SITE_NAME
        site, created = Site.objects.get_or_create(
            domain=site_domain, defaults={"name": site_name}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Default site created."))
        else:
            self.stdout.write("Default site already exists.")

    def create_social_apps(self):
        providers = [
            {
                "provider": "google",
                "name": "Google",
                "client_id": GOOGLE_CLIENT_ID,
                "secret": GOOGLE_CLIENT_SECRET,
                "key": "",
            },
            {
                "provider": "twitter",
                "name": "Twitter",
                "client_id": TWITTER_CLIENT_ID,
                "secret": TWITTER_CLIENT_SECRET,
                "key": "",
            },
        ]

        for provider_info in providers:
            provider = provider_info["provider"]
            name = provider_info["name"]
            client_id = provider_info["client_id"]
            secret = provider_info["secret"]
            key = provider_info["key"]

            social_app, created = SocialApp.objects.get_or_create(
                provider=provider,
                name=name,
                defaults={
                    "client_id": client_id,
                    "secret": secret,
                    "key": key,
                },
            )
            if created:
                site = Site.objects.get(domain=SITE_DOMAIN)
                social_app.sites.add(site)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"SocialApp pour {provider} créé et associé au site."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"SocialApp pour {provider} existe déjà.")
                )


# def create_admin_user(self):
#
#       if not admin_password:
#          self.stdout.write(
#             self.style.ERROR(
#                "Le mot de passe administrateur n'est pas défini. Veuillez définir 'ADMIN_PASSWORD' dans les variables d'environnement."
#           )
#      )
#     return

#        user, created = User.objects.get_or_create(
#           username=admin_username,
#          defaults={
#             "email": admin_email,
#            "is_staff": True,
#           "is_superuser": True,
#      },
# )

#        if created:
#           user.set_password(admin_password)
#          user.save()
#         self.stdout.write(
#                self.style.SUCCESS(
#                   f"Utilisateur admin '{admin_username}' créé avec succès."
#              )
#         )
#    else:
#       self.stdout.write(
#          self.style.WARNING(
#             f"L'utilisateur admin '{admin_username}' existe déjà."
#        )
#   )
