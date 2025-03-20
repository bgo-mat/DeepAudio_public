from openai import OpenAI
from django.conf import settings


class OpenAIService:
    def __init__(self, api_key=None, model="gpt-4-turbo"):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model
        print("icicicicicici ======>",self.api_key, flush=True)
        self.client = OpenAI(api_key=self.api_key)

    def get_description(self, all_data):
        all_data_str = "".join(str(x) for x in all_data)

        prompt = (
            "Based on the following list of filenames, "
            "create an appealing and persuasive description "
            "for a music sample pack. The description should be "
            "in English, entice potential users, and include"
            " relevant keywords for optimal search engine visibility"
            " in the music samples domain. Do not mention any specific"
            " audio filenames, keys, or BPMs. Instead, infer the overall"
            " style, genre, and instruments from the filenames and "
            "discuss the pack in general terms. List of filenames:  " + all_data_str
        )

        content_system = (
            "You are an expert copywriter specialized in"
            " the music industry. Your task is to create engaging, "
            "concise, and SEO-optimized descriptions for music sample packs. "
            "You will analyze a list of audio file names to determine the style, "
            "genre, and instruments featured in the pack. Use relevant keywords to "
            "enhance searchability and appeal to potential buyers. Ensure the description "
            "is written in fluent English, is persuasive, and highlights the unique features "
            "of the sample pack."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": content_system},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,  # Limitez la longueur de la réponse
                n=1,  # Nombre de réponses générées
                stop=None,  # Arrêtez la génération de la réponse à un token de fin
                temperature=0.9,  # Contrôle de la créativité de la réponse (entre 0 et 1)
            )

            generated_content = response.choices[0].message.content
            return generated_content
        except Exception as e:
            print(e)
            return

    def get_name(self, all_data):
        all_data_str = "".join(str(x) for x in all_data)

        prompt = (
            "Based on the following list of filenames,"
            " generate an appealing and memorable name "
            "for a music sample pack. The name should be "
            "in English, capture the overall style, genre, "
            "and instruments inferred from the filenames, "
            "and include relevant keywords to enhance search "
            "engine optimization in the music samples market. "
            "Do not reference specific audio filenames, keys, "
            "or BPMs; focus on the general characteristics and "
            "vibe of the pack. Return just the pack name"
            "List of filenames:  " + all_data_str
        )

        content_system = (
            "You are an AI assistant specialized "
            "in creating catchy and relevant names "
            "for music sample packs. Your names should "
            "reflect the style, genre, and instruments "
            "inferred from a list of filenames. Ensure "
            "the names are memorable, appealing to potential "
            "users, and optimized with relevant keywords for "
            "search engine visibility in the music samples domain."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": content_system},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=20,  # Limitez la longueur de la réponse
                n=1,  # Nombre de réponses générées
                stop=None,  # Arrêtez la génération de la réponse à un token de fin
                temperature=0.9,  # Contrôle de la créativité de la réponse (entre 0 et 1)
            )

            generated_content = response.choices[0].message.content
            return generated_content
        except Exception as e:
            print(e)
            return
