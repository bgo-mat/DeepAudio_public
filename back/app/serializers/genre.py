from rest_framework import serializers
from app.models import Genre
from app.commons.pagination import GenreResponsePagination


class GenreSerializer(serializers.ModelSerializer):
    sound_count = serializers.IntegerField(source="sound_set.count", read_only=True)

    class Meta:
        model = Genre
        fields = ["id", "name", "image", "sound_count"]


class GenreSerializerRetrieve(serializers.ModelSerializer):
    pack = serializers.SerializerMethodField()
    sound = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ["id", "name", "image", "pack", "sound"]

    def get_pack(self, obj):
        from app.serializers.pack import PackSerializer

        packs = obj.pack_set.all()

        paginator = GenreResponsePagination()
        paginator.page_query_param = "pack_page"
        page = paginator.paginate_queryset(packs, self.context["request"])

        serializer = PackSerializer(page, many=True, context=self.context)

        return paginator.get_paginated_response(serializer.data).data

    def get_sound(self, obj):
        from app.serializers.sound import SoundSerializer

        sounds = obj.sound_set.all()

        paginator = GenreResponsePagination()
        paginator.page_query_param = "sound_page"
        page = paginator.paginate_queryset(sounds, self.context["request"])

        serializer = SoundSerializer(page, many=True, context=self.context)

        return paginator.get_paginated_response(serializer.data).data
