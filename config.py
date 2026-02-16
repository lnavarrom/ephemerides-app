import os
from datetime import datetime

class Config:
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True

    # Wikipedia API
    WIKIPEDIA_API_BASE = 'https://{lang}.wikipedia.org/api/rest_v1/feed/onthisday/{type}/{month:02d}/{day:02d}'

    # Supported languages for UI
    SUPPORTED_LANGUAGES = ['ca', 'es', 'en']
    DEFAULT_LANGUAGE = 'ca'

    # Wikipedia API language mapping (some languages not supported by onthisday API)
    # Catalan (ca) will use Spanish (es) for Wikipedia data
    WIKIPEDIA_LANGUAGE_MAP = {
        'ca': 'es',  # Català usa espanyol per les dades de Wikipedia
        'es': 'es',
        'en': 'en'
    }

    # Cache settings (opcional per futura optimització)
    CACHE_TIMEOUT = 3600  # 1 hora en segons
