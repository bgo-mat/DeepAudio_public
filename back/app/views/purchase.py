from rest_framework.viewsets import GenericViewSet, mixins
from app.models import Purchase
from app.serializers import PurchaseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.commons.pagination import CustomPagination


class PurchaseViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            grouped_data = {"pack": [], "sound": []}
            for purchase in serializer.data:
                if purchase["pack"] is not None:
                    grouped_data["pack"].append(purchase)
                elif purchase["sound"] is not None:
                    grouped_data["sound"].append(purchase)
            return self.get_paginated_response(grouped_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
