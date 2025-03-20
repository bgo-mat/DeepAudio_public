from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from app.constantes import UserRoles
from app.models import Subscription
import stripe
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY


class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            subscription = Subscription.objects.get(user=user, active=True)
            stripe_subscription_id = subscription.stripe_subscription_id

            # Récupérer l'abonnement depuis Stripe
            stripe_subscription = stripe.Subscription.retrieve(stripe_subscription_id)

            # Obtenir la date de fin de l'essai (trial_end)
            trial_end_timestamp = stripe_subscription.get("trial_end")
            trial_end = (
                datetime.fromtimestamp(trial_end_timestamp, tz=dt_timezone.utc)
                if trial_end_timestamp
                else None
            )

            current_time = timezone.now()

            if trial_end and current_time < trial_end:
                # L'utilisateur est encore dans la période d'essai, annuler immédiatement
                stripe.Subscription.delete(stripe_subscription_id)
                # Mettre à jour l'abonnement dans la base de données
                subscription.active = False
                subscription.save()
                # Mettre à jour le rôle de l'utilisateur
                user.roles = UserRoles.VISITOR
                user.save()
                return Response(
                    {
                        "message": "Your subscription has been cancelled immediately. No fees will be charged."
                    },
                    status=200,
                )
            else:
                if subscription.plan.subscription_type == "PREMIUM":
                    # L'utilisateur est hors de la période d'essai, annuler à la fin de la période actuelle
                    stripe.Subscription.modify(
                        stripe_subscription_id, cancel_at_period_end=True
                    )
                else:
                    # Mettre à jour l'abonnement dans la base de données
                    subscription.active = False
                    subscription.save()
                    # Mettre à jour le rôle de l'utilisateur
                    user.roles = UserRoles.VISITOR
                    user.save()
                    stripe.Subscription.delete(stripe_subscription_id)
                # Mettre à jour l'abonnement dans la base de données
                subscription.cancel_at_period_end = (
                    True  # Ajouter ce champ si nécessaire
                )
                subscription.save()
                return Response(
                    {
                        "message": "Your subscription will be cancelled at the end of the current period."
                    },
                    status=200,
                )

        except Subscription.DoesNotExist:
            return Response(
                {
                    "error": "No active subscription found. If you believe this is an error, please contact us."
                },
                status=404,
            )
        except stripe.error.StripeError as e:
            return Response(
                {
                    "error": f"Error while cancelling the subscription: {str(e)}. Please try again or contact us if the error persists."
                },
                status=500,
            )
        except Exception as e:
            return Response(
                {
                    "error": f"An unexpected error has occurred: {str(e)}. Please try again or contact us if the error persists."
                },
                status=500,
            )
