from flask import Flask, render_template, jsonify, request
from datetime import datetime
from api.wikipedia_client import WikipediaClient
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Inicialitzar client Wikipedia
wiki_client = WikipediaClient(app.config['WIKIPEDIA_API_BASE'])


def get_mapped_language(language: str) -> str:
    """
    Mapeja l'idioma de la UI a l'idioma de Wikipedia API

    Args:
        language: Codi d'idioma (ca, es, en)

    Returns:
        Codi d'idioma per Wikipedia API
    """
    return app.config['WIKIPEDIA_LANGUAGE_MAP'].get(language, language)

@app.route('/')
def index():
    """Servir la pàgina principal"""
    return render_template('index.html')

@app.route('/api/ephemeris/today', methods=['GET'])
def get_today_ephemeris():
    """
    Retorna una efemèride aleatòria del dia actual
    Query params: lang (ca, es, en)
    """
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])

    if language not in app.config['SUPPORTED_LANGUAGES']:
        return jsonify({'error': 'Unsupported language'}), 400

    # Map language to Wikipedia API language
    wiki_lang = get_mapped_language(language)

    today = datetime.now()
    month, day = today.month, today.day

    try:
        # Obtenir event aleatori
        event = wiki_client.get_random_event(month, day, wiki_lang)

        if not event:
            return jsonify({'error': 'No events found for today'}), 404

        # Retornar versió simplificada (sense details)
        return jsonify({
            'year': event.get('year', 'Unknown'),
            'text': event.get('text', ''),
            'hasDetails': len(event.get('pages', [])) > 0
        })

    except Exception as e:
        app.logger.error(f"Error getting ephemeris: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/ephemeris/details', methods=['POST'])
def get_ephemeris_details():
    """
    Retorna detalls ampliats d'una efemèride
    Body: { year, text, lang }
    """
    data = request.get_json()
    language = data.get('lang', app.config['DEFAULT_LANGUAGE'])
    year = data.get('year')
    text = data.get('text')

    if not year or not text:
        return jsonify({'error': 'Missing required fields'}), 400

    # Map language to Wikipedia API language
    wiki_lang = get_mapped_language(language)

    today = datetime.now()
    month, day = today.month, today.day

    try:
        # Obtenir tots els events i trobar el que coincideix
        events = wiki_client.get_events(month, day, wiki_lang)

        matching_event = None
        for event in events:
            if event.get('year') == year and event.get('text') == text:
                matching_event = event
                break

        if not matching_event:
            return jsonify({'error': 'Event not found'}), 404

        # Obtenir detalls ampliats
        details = wiki_client.get_event_details(matching_event, wiki_lang)
        return jsonify(details)

    except Exception as e:
        app.logger.error(f"Error getting details: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/translations/<lang>', methods=['GET'])
def get_translations(lang):
    """Retorna les traduccions per l'idioma especificat"""
    if lang not in app.config['SUPPORTED_LANGUAGES']:
        return jsonify({'error': 'Unsupported language'}), 400

    try:
        translations_path = os.path.join('translations', f'{lang}.json')
        with open(translations_path, 'r', encoding='utf-8') as f:
            import json
            translations = json.load(f)
        return jsonify(translations)
    except FileNotFoundError:
        return jsonify({'error': 'Translations not found'}), 404
    except Exception as e:
        app.logger.error(f"Error loading translations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
