import base64

import binascii
from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64FileField
import mimetypes


class AudioBase64FileField(Base64FileField):
    def get_file_extension(self, filename, decoded_file):
        # Utiliser le type MIME pour obtenir l'extension de fichier
        file_extension = mimetypes.guess_extension(self.file_mime_type)
        if file_extension:
            return file_extension.replace(".", "")
        return "bin"

    def to_internal_value(self, base64_data):
        if base64_data is None:
            return None

        if isinstance(base64_data, str):
            if "data:" in base64_data and ";base64," in base64_data:
                # Séparer l'en-tête du contenu encodé
                header, base64_data = base64_data.split(";base64,")
                try:
                    self.file_mime_type = header.split("data:")[1]
                except IndexError:
                    self.file_mime_type = "application/octet-stream"
            else:
                self.file_mime_type = "application/octet-stream"

            # Décoder le fichier
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error):
                self.fail("invalid_file")

            # Obtenir le nom et l'extension du fichier
            file_name = self.get_file_name("file")
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "{0}.{1}".format(file_name, file_extension)

            data = ContentFile(decoded_file, name=complete_file_name)
            return data
        else:
            self.fail("invalid_file")
