from rest_framework import serializers


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(write_only=True, required=True)
    remember_me = serializers.BooleanField(default=False)
