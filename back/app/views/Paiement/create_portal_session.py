import stripe
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY
frontend_url = settings.FRONTEND_URL


class PortalSessionCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            stripe_customer = request.user.stripe_customer_id
            if not stripe_customer:
                return Response(
                    {"error": "Utilisateur sans customer ID Stripe."}, status=400
                )

            checkout_session = stripe.billing_portal.Session.create(
                customer=stripe_customer,
                return_url=frontend_url,
            )

            return Response({"url": checkout_session.url})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
