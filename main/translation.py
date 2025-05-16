from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SUPPORTED_LANGUAGES = [
    ('cor', 'Cornish'),
    ('glv', 'Manx'),
    ('bre', 'Breton'),
    ('iku', 'Inuktitut'),
    ('kal', 'Kalaallisut'),
    ('rom', 'Romani'),
    ('oci', 'Occitan'),
    ('lad', 'Ladino'),
    ('sme', 'Northern Sami'),
    ('hsb', 'Upper Sorbian'),
    ('csb', 'Kashubian'),
    ('zza', 'Zazaki'),
    ('chv', 'Chuvash'),
    ('liv', 'Livonian'),
    ('tsd', 'Tsakonian'),
    ('srm', 'Saramaccan'),
    ('bis', 'Bislama'),
]

def translate_text(text, target_language):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}. Preserve the formatting."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text
