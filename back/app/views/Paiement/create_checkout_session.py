import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from app.models import SubscriptionPlan
from app.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY
frontend_url = settings.FRONTEND_URL
trial_period_days = settings.TRIAL_SUB_PERIOD_DAY


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            price_id = request.data.get("price_id")  # ID du prix Stripe
            # Récupérer le plan dans la base de données
            subscription_plan = SubscriptionPlan.objects.get(stripe_price_id=price_id)

            if not request.user.stripe_customer_id:
                customer = stripe.Customer.create(email=request.user.email)
                request.user.stripe_customer_id = customer.id
                request.user.save()

            # **Nouveau code : Annuler l'ancien abonnement si nécessaire**
            try:
                # Vérifier si l'utilisateur a un abonnement actif
                subscription = Subscription.objects.get(user=request.user, active=True)
                # Annuler l'abonnement sur Stripe
                stripe.Subscription.delete(subscription.stripe_subscription_id)
                # Mettre à jour l'abonnement dans la base de données
                subscription.active = False
                subscription.save()
            except Subscription.DoesNotExist:
                # Pas d'abonnement actif, passer
                pass

            # Créer une nouvelle session de paiement
            checkout_session = stripe.checkout.Session.create(
                customer=request.user.stripe_customer_id,
                payment_method_types=["card", "paypal"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                success_url=frontend_url + "/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=frontend_url + "/cancel_sub",
                metadata={
                    "subscription_plan_id": subscription_plan.stripe_prod_id,
                },
                # Ajouter la période d'essai si nécessaire
                subscription_data={
                    "trial_period_days": trial_period_days
                    if subscription_plan.subscription_type == "PREMIUM"
                    else None
                },
            )

            return Response({"sessionId": checkout_session.id})
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Invalid plan"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
