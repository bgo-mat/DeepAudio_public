from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.models import Subscription


class GetSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            subscription = Subscription.objects.get(user=request.user, active=True)
            data = {
                "plan": {
                    "name": subscription.plan.name,
                    "amount": subscription.plan.amount,
                    "payment_frequency": subscription.plan.payment_frequency,
                },
                "start_date": subscription.start_date,
                "trial_end": subscription.next_payment_date
                if subscription.next_payment_date
                else None,
                "next_payment_date": subscription.next_payment_date,
            }
            return Response(data, status=200)
        except Subscription.DoesNotExist:
            return Response(
                {
                    "error": "No active subscription found. If you believe this is an error, please contact us."
                },
                status=404,
            )
        except Exception as e:
            return Response(
                {
                    "error": "An unexpected error has occurred. Please try again or contact us if the error persists."
                },
                status=500,
            )
