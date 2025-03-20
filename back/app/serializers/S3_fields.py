# serializers/fields.py

from rest_framework import serializers
import base64
import mimetypes
import binascii
from app.commons.s3_utils import S3Uploader


class S3Base64FileField(serializers.Field):
    def to_internal_value(self, data):
        if data is None:
            return None

        if isinstance(data, str):
            if "data:" in data and ";base64," in data:
                # Séparer l'en-tête du contenu encodé
                header, data = data.split(";base64,")
                file_mime_type = header.split("data:")[1]
            else:
                file_mime_type = "application/octet-stream"

            # Décoder le fichier
            try:
                decoded_file = base64.b64decode(data)
            except (TypeError, binascii.Error):
                self.fail("invalid_file")

            # Obtenir l'extension du fichier
            extension = mimetypes.guess_extension(file_mime_type)
            if extension is None:
                extension = ".bin"

            # Générer le nom du fichier
            file_name = self.get_file_name(extension)

            # Upload vers S3
            s3_uploader = S3Uploader()
            s3_key = s3_uploader.upload_file(decoded_file, file_name, file_mime_type)

            return s3_key
        else:
            self.fail("invalid_file")

    def to_representation(self, value):
        if value:
            s3_uploader = S3Uploader()
            url = s3_uploader.get_file_url(value)
            return url
        else:
            return None

    def get_file_name(self, extension):
        import uuid

        return f"{uuid.uuid4()}{extension}"


class S3Base64ImageField(S3Base64FileField):
    pass
