import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RetrieveCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return Response(session)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
