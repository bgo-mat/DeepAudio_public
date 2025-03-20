from django.utils import timezone
import datetime
from app.constantes import UserRoles
from app.models import Subscription, SubscriptionPlan, Transaction, User
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from app.tasks import envoyer_email_debut_abonnement, envoyer_email_fin_abonnement


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Payload invalide
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Signature invalide
        return HttpResponse(status=400)

    # Gérer les différents types d'événements
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_checkout_session(session)
    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        handle_invoice_payment_succeeded(invoice)
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        handle_subscription_deleted(subscription)
    elif event["type"] == "customer.subscription.created":
        subscription = event["data"]["object"]
        handle_subscription_created(subscription)
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        handle_subscription_updated(subscription)

    return HttpResponse(status=200)


def handle_checkout_session(session):
    customer_id = session.get("customer")
    email = session.get("customer_details", {}).get("email")

    try:
        user = User.objects.get(email=email)
        if not user.stripe_customer_id:
            user.stripe_customer_id = customer_id
            user.save()
    except User.DoesNotExist:
        print(f"Utilisateur avec l'email {email} n'existe pas", flush=True)
    except Exception as e:
        print(f"Exception dans handle_checkout_session: {e}", flush=True)


def handle_invoice_payment_succeeded(invoice):
    subscription_id = invoice["subscription"]
    try:
        subscription = Subscription.objects.get(
            stripe_subscription_id=subscription_id, active=True
        )
        next_payment_timestamp = invoice.get("next_payment_attempt")
        if next_payment_timestamp:
            subscription.next_payment_date = datetime.datetime.fromtimestamp(
                next_payment_timestamp, tz=datetime.timezone.utc
            )
        else:
            # Utilisez 'current_period_end' de l'abonnement Stripe
            stripe_subscription = stripe.Subscription.retrieve(subscription_id)
            subscription.next_payment_date = datetime.datetime.fromtimestamp(
                stripe_subscription.current_period_end, tz=datetime.timezone.utc
            )
        subscription.save()

        # Mise à jour des crédits si nécessaire
        if subscription.plan.credits_per_month:
            subscription.user.tokens += subscription.plan.credits_per_month
            subscription.user.save()

        # Enregistrer la transaction
        Transaction.objects.create(
            user=subscription.user,
            plan=subscription.plan,
            amount=subscription.plan.amount,
            transaction_type="subscription",
            payment_method="stripe",
            transaction_id=invoice["id"],
            status="succeeded",
        )

    except Subscription.DoesNotExist:
        print(
            f"Abonnement avec stripe_subscription_id {subscription_id} n'existe pas",
            flush=True,
        )
    except Exception as e:
        print(f"Exception dans handle_invoice_payment_succeeded: {e}", flush=True)


def handle_subscription_created(subscription):
    customer_id = subscription.get("customer")
    subscription_id = subscription.get("id")
    plan_id = subscription["plan"]["product"]

    try:
        user = User.objects.get(stripe_customer_id=customer_id)
    except User.DoesNotExist:
        print(f"Aucun utilisateur avec stripe_customer_id {customer_id}", flush=True)
        return

    try:
        subscription_plan = SubscriptionPlan.objects.get(stripe_prod_id=plan_id)

        # Mettre à jour le rôle de l'utilisateur
        user.roles = subscription_plan.subscription_type
        user.save()

        # Créer ou mettre à jour l'abonnement de l'utilisateur
        sub, created = Subscription.objects.update_or_create(
            user=user,
            defaults={
                "plan": subscription_plan,
                "stripe_subscription_id": subscription_id,
                "active": True,
                "next_payment_date": datetime.datetime.fromtimestamp(
                    subscription["current_period_end"], tz=datetime.timezone.utc
                ),
            },
        )

        # Envoyer un email de début d'abonnement
        envoyer_email_debut_abonnement(user.id, subscription_plan.subscription_type)

    except SubscriptionPlan.DoesNotExist:
        print(
            f"SubscriptionPlan avec stripe_prod_id {plan_id} n'existe pas", flush=True
        )
    except Exception as e:
        print(f"Exception dans handle_subscription_created: {e}", flush=True)


def handle_subscription_updated(subscription):
    customer_id = subscription.get("customer")
    subscription_id = subscription.get("id")
    plan_id = subscription["plan"]["product"]

    try:
        user = User.objects.get(stripe_customer_id=customer_id)
    except User.DoesNotExist:
        print(f"Aucun utilisateur avec stripe_customer_id {customer_id}", flush=True)
        return

    try:
        subscription_plan = SubscriptionPlan.objects.get(stripe_prod_id=plan_id)

        # Mettre à jour le rôle de l'utilisateur
        user.roles = subscription_plan.subscription_type
        user.save()

        # Mettre à jour l'abonnement de l'utilisateur
        sub, created = Subscription.objects.update_or_create(
            user=user,
            defaults={
                "plan": subscription_plan,
                "stripe_subscription_id": subscription_id,
                "active": True,
                "next_payment_date": datetime.datetime.fromtimestamp(
                    subscription["current_period_end"], tz=datetime.timezone.utc
                ),
            },
        )

    except SubscriptionPlan.DoesNotExist:
        print(
            f"SubscriptionPlan avec stripe_prod_id {plan_id} n'existe pas", flush=True
        )
    except Exception as e:
        print(f"Exception dans handle_subscription_updated: {e}", flush=True)


def handle_subscription_deleted(subscription):
    try:
        subscription_id = subscription["id"]
        sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
        sub.active = False
        sub.save()
        user = sub.user
        user.roles = UserRoles.VISITOR
        user.save()
        envoyer_email_fin_abonnement(user.id, sub.plan.subscription_type)
    except Subscription.DoesNotExist:
        print("Subscription does not exist in delet sub", flush=True)
        pass
    except Exception as e:
        print(f"Exception in delet sub : {e}", flush=True)
        pass
