from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models import Pack
from app.permissions import IsAdminUserRole
from app.serializers.pack import PackSerializer
from rest_framework.viewsets import GenericViewSet, mixins


class UploadPackViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Pack.objects.all()
    serializer_class = PackSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    http_method_names = ["post", "options"]
