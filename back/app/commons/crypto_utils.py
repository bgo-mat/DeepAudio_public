from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os
from django.conf import settings

AES_KEY = base64.b64decode(settings.SOUND_CRYPT)


def encrypt_text(text):
    iv = os.urandom(16)  # Générer un IV aléatoire de 16 octets
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Appliquer le padding PKCS7
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()

    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # Retourner IV + ciphertext encodés en Base64
    return base64.b64encode(iv + encrypted).decode()
