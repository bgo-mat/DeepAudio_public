import mimetypes
import zipfile
import tempfile
import os
import base64

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from pydub import AudioSegment
from app.models import Genre, Type, SubType
from app.permissions import IsAdminUserRole
from app.views.External_API.open_ai_call import OpenAIService


class UploadPackPreviewView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # [IsAuthenticated, IsAdminUserRole]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open_ai_call = OpenAIService()
        self.data_for_ai = []

    def post(self, request, format=None):
        enable_ai_description = (
            self.request.query_params.get("enable_ai_description", "false").lower()
            == "true"
        )
        enable_ai_name = (
            self.request.query_params.get("enable_ai_name", "false").lower() == "true"
        )

        # Récupérer le fichier uploadé
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response(
                {"error": "Aucun fichier n'a été uploadé."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérifier si le fichier est un zip
        if not zipfile.is_zipfile(uploaded_file):
            return Response(
                {"error": "Le fichier uploadé n'est pas un fichier zip valide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Créer un répertoire temporaire pour extraire le zip
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Extraire le zip
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall(tmpdirname)

            # Traiter les fichiers
            pack_data = self.process_pack(
                tmpdirname, enable_ai_description, enable_ai_name
            )

        return Response(pack_data, status=status.HTTP_200_OK)

    def process_pack(self, directory, enable_ai_description, enable_ai_name):
        # Initialiser les données du pack
        pack_info = {"pack": {}, "audio": []}

        # Variables pour la durée totale et le nombre de fichiers
        total_duration = 0
        num_files = 0

        # Nom du pack (nom du dossier racine)
        root_dirs = [
            name
            for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))
        ]
        if root_dirs:
            pack_name = root_dirs[0]
            self.data_for_ai.append(pack_name)
            pack_info["pack"]["pack_name"] = pack_name
            pack_path = os.path.join(directory, pack_name)
        else:
            pack_name = "Pack_Uploaded"
            pack_info["pack"]["pack_name"] = pack_name
            pack_path = directory  # Traiter les fichiers directement

        # Traiter les fichiers audio
        # D'abord, rechercher et traiter 'mix.wav' s'il existe
        mix_file_path = None
        for dirpath, dirnames, filenames in os.walk(pack_path):
            for filename in filenames:
                if filename.lower() == "mix.wav":
                    mix_file_path = os.path.join(dirpath, filename)
                    break
            if mix_file_path:
                break

        if mix_file_path:
            preview_audio = self.process_preview_audio_file(mix_file_path)
            if preview_audio:
                pack_info["pack"]["preview"] = preview_audio["audio_file"]

        # Ensuite, traiter les autres fichiers audio (excluant 'mix.wav')
        for dirpath, dirnames, filenames in os.walk(pack_path):
            for filename in filenames:
                if filename.lower() == "mix.wav":
                    continue  # Déjà traité
                if filename.lower().endswith((".wav", ".mp3")):
                    file_path = os.path.join(dirpath, filename)
                    # Traiter le fichier audio
                    audio_data = self.process_audio_file(file_path, dirpath, pack_path)
                    if audio_data:
                        pack_info["audio"].append(audio_data)
                        num_files += 1
                        # Calculer la durée totale
                        total_duration += audio_data.get("duration_seconds", 0)

        # Mettre à jour les informations du pack
        pack_info["pack"]["number_of_files"] = num_files
        pack_info["pack"]["total_duration"] = self.format_duration(total_duration)

        # Collecter tous les genres des fichiers audio
        all_genres = set()
        for audio in pack_info["audio"]:
            all_genres.update(audio.get("genres", []))

        pack_info["pack"]["genres"] = list(all_genres) if all_genres else []

        # Création description
        self.data_for_ai.append(pack_info["pack"]["genres"])
        self.data_for_ai.append(pack_info["pack"]["pack_name"])

        if enable_ai_description:
            pack_info["pack"]["description"] = self.open_ai_call.get_description(
                self.data_for_ai
            )
        else:
            pack_info["pack"]["description"] = ""

        # call creation name
        if enable_ai_name:
            pack_info["pack"]["pack_name"] = self.open_ai_call.get_name(
                self.data_for_ai
            )

        return pack_info

    def process_preview_audio_file(self, file_path):
        file_info = {}

        # Lire le fichier audio et l'encoder en Base64
        try:
            with open(file_path, "rb") as f:
                audio_content = f.read()
                encoded_audio = base64.b64encode(audio_content).decode("utf-8")
                # Obtenir le type MIME du fichier
                mime_type = (
                    mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                )
                # Créer l'URI de données (data URI)
                data_uri = f"data:{mime_type};base64,{encoded_audio}"
                file_info["audio_file"] = data_uri
        except Exception as e:
            print(
                f"Erreur lors de la lecture du fichier audio preview {file_path}: {e}"
            )
            file_info["audio_file"] = None

        return file_info

    def process_audio_file(self, file_path, dirpath, pack_path):
        # Obtenir le chemin relatif pour extraire les noms de dossiers
        relative_path = os.path.relpath(dirpath, pack_path)
        folder_names = relative_path.split(os.sep) if relative_path != "." else []

        # Extraire les métadonnées du nom de fichier et des noms de dossiers
        filename = os.path.basename(file_path)
        file_info = {"song_name": filename}

        # Utiliser pydub pour obtenir la durée
        try:
            audio = AudioSegment.from_file(file_path)
            duration = len(audio) / 1000.0  # Durée en secondes
            file_info["duration_seconds"] = duration
        except Exception as e:
            duration = 0
            file_info["duration_seconds"] = 0

        # Extraire bpm et key du nom du fichier
        name_without_extension = filename.rsplit(".", 1)[0]
        name_parts = name_without_extension.split("_")
        bpm = None
        key = None
        scale = None

        # Recherche de 'BPM' et extraction du BPM
        for idx, part in enumerate(name_parts):
            if "BPM" in part.upper():
                # Extraire le BPM qui se trouve avant 'BPM'
                bpm_candidate = part.upper().replace("BPM", "")
                if not bpm_candidate and idx > 0:
                    bpm_candidate = name_parts[idx - 1]
                try:
                    bpm = int(bpm_candidate)
                except (ValueError, TypeError):
                    bpm = None
                # La key est le segment suivant après 'BPM'
                if idx + 1 < len(name_parts):
                    key_candidate = name_parts[idx + 1]
                    key = key_candidate
                break  # On arrête après avoir trouvé 'BPM'

        # Récupérer la scale comme le dernier mot avant l'extension
        if name_parts:
            scale_candidate = name_parts[-1]
            # Vérifier que le scale_candidate n'est pas déjà le key ou le bpm
            if scale_candidate != key and scale_candidate != str(bpm):
                scale = scale_candidate
            if scale_candidate == "NA":
                scale = None

        file_info["bpm"] = bpm if bpm else ""
        file_info["key"] = key if key else ""
        file_info["scale"] = scale if scale else ""

        phrases = self.parse_filename(filename)
        subtypes = SubType.objects.all()
        types = Type.objects.all()
        genres = Genre.objects.all()
        found_genres = set()
        found_subtypes = []
        found_types = set()

        # Rechercher les SubTypes correspondants
        for phrase in phrases:
            matching_subtypes = subtypes.filter(name__iexact=phrase)
            for subtype_obj in matching_subtypes:
                if subtype_obj.name not in found_subtypes:
                    found_subtypes.append(subtype_obj.name)
                    found_types.add(subtype_obj.type.name)

        file_info["subtypes"] = found_subtypes if found_subtypes else []
        file_info["types"] = list(found_types) if found_types else []

        # Rechercher les Types correspondants
        for phrase in phrases:
            matching_types = types.filter(name__iexact=phrase)
            for type_obj in matching_types:
                if type_obj.name not in file_info.get("types", []):
                    file_info.setdefault("types", []).append(type_obj.name)

        # Déterminer le genre à partir des noms de dossiers
        genres_query = Q()
        for phrase in phrases:
            genres_query |= Q(name__iexact=phrase)

        matching_genres = genres.filter(genres_query)
        print("Genres correspondants :", matching_genres)

        for genre_obj in matching_genres:
            found_genres.add(genre_obj.name)

        file_info["genres"] = list(found_genres) if found_genres else []

        self.data_for_ai.append(file_info["types"])
        self.data_for_ai.append(file_info["subtypes"])

        # Lire le fichier audio et l'encoder en Base64
        try:
            with open(file_path, "rb") as f:
                audio_content = f.read()
                encoded_audio = base64.b64encode(audio_content).decode("utf-8")
                # Obtenir le type MIME du fichier
                mime_type = (
                    mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                )
                # Créer l'URI de données (data URI)
                data_uri = f"data:{mime_type};base64,{encoded_audio}"
                file_info["audio_file"] = data_uri
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier audio {file_path}: {e}")
            file_info["audio_file"] = None

        # Retourner les informations du fichier
        return file_info

    def format_duration(self, seconds):
        # Formater la durée en minutes et secondes
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}min{remaining_seconds}s"

    def parse_filename(self, filename):
        filename = filename.rsplit(".", 1)[0]
        parts = filename.split("_")
        words = []
        for part in parts:
            # Vérifier si la partie contient un entier
            if any(char.isdigit() for char in part):
                break
            words.append(part)
        # Générer les combinaisons et inclure les mots individuels
        combinations = set()
        n = len(words)
        for i in range(n):
            for j in range(i + 1, n + 1):
                combination = " ".join(words[i:j])
                combinations.add(combination)
        return list(combinations)
