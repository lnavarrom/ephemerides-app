"""
Tests d'integració per als endpoints de l'API Flask
"""
import pytest
import responses
from datetime import datetime


class TestHealthEndpoint:
    """Tests per l'endpoint de health check"""

    def test_health_check_returns_ok(self, client):
        """Test: /health retorna status ok"""
        response = client.get('/health')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'timestamp' in data

    def test_health_check_has_valid_timestamp(self, client):
        """Test: /health timestamp és vàlid"""
        response = client.get('/health')
        data = response.get_json()

        # Verificar que el timestamp es pot parsejar
        timestamp = datetime.fromisoformat(data['timestamp'])
        assert isinstance(timestamp, datetime)


class TestMainPageEndpoint:
    """Tests per la pàgina principal"""

    def test_main_page_accessible(self, client):
        """Test: / és accessible"""
        response = client.get('/')

        assert response.status_code == 200
        assert b'text/html' in response.content_type.encode()

    def test_main_page_contains_title(self, client):
        """Test: / conté el títol"""
        response = client.get('/')

        assert b'Efem' in response.data  # "Efemèrides"
        assert b'Hist' in response.data  # Part de "Històriques"
        assert b'app-title' in response.data  # Classe del títol


class TestEphemerisTodayEndpoint:
    """Tests per l'endpoint d'efemèrides del dia"""

    @responses.activate
    def test_get_ephemeris_catalan(self, client):
        """Test: GET /api/ephemeris/today?lang=ca retorna efemèride"""
        # Mock Wikipedia API (CA usa ES)
        responses.add(
            responses.GET,
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/{datetime.now().month:02d}/{datetime.now().day:02d}',
            json={'events': [
                {'year': 1866, 'text': 'Test event', 'pages': [{'title': 'Test'}]}
            ]},
            status=200
        )

        response = client.get('/api/ephemeris/today?lang=ca')

        assert response.status_code == 200
        data = response.get_json()
        assert 'year' in data
        assert 'text' in data
        assert 'hasDetails' in data

    @responses.activate
    def test_get_ephemeris_spanish(self, client):
        """Test: GET /api/ephemeris/today?lang=es retorna efemèride"""
        responses.add(
            responses.GET,
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/{datetime.now().month:02d}/{datetime.now().day:02d}',
            json={'events': [
                {'year': 1959, 'text': 'Evento de prueba', 'pages': []}
            ]},
            status=200
        )

        response = client.get('/api/ephemeris/today?lang=es')

        assert response.status_code == 200
        data = response.get_json()
        assert data['year'] == 1959

    @responses.activate
    def test_get_ephemeris_english(self, client):
        """Test: GET /api/ephemeris/today?lang=en retorna efemèride"""
        responses.add(
            responses.GET,
            f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{datetime.now().month:02d}/{datetime.now().day:02d}',
            json={'events': [
                {'year': 1923, 'text': 'Test event', 'pages': []}
            ]},
            status=200
        )

        response = client.get('/api/ephemeris/today?lang=en')

        assert response.status_code == 200
        data = response.get_json()
        assert data['year'] == 1923

    def test_get_ephemeris_unsupported_language(self, client):
        """Test: idioma no suportat retorna 400"""
        response = client.get('/api/ephemeris/today?lang=fr')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @responses.activate
    def test_get_ephemeris_no_events_found(self, client):
        """Test: gestió quan no hi ha events"""
        responses.add(
            responses.GET,
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/{datetime.now().month:02d}/{datetime.now().day:02d}',
            json={'events': []},
            status=200
        )

        response = client.get('/api/ephemeris/today?lang=ca')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestEphemerisDetailsEndpoint:
    """Tests per l'endpoint de detalls d'efemèrides"""

    @responses.activate
    def test_get_details_success(self, client):
        """Test: POST /api/ephemeris/details retorna detalls"""
        today = datetime.now()
        responses.add(
            responses.GET,
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/{today.month:02d}/{today.day:02d}',
            json={'events': [
                {
                    'year': 1492,
                    'text': 'Test event',
                    'pages': [{
                        'title': 'Test Page',
                        'extract': 'Test description',
                        'content_urls': {'desktop': {'page': 'https://test.com'}}
                    }]
                }
            ]},
            status=200
        )

        response = client.post('/api/ephemeris/details',
                                json={'year': 1492, 'text': 'Test event', 'lang': 'es'})

        assert response.status_code == 200
        data = response.get_json()
        assert 'description' in data
        assert 'links' in data

    def test_get_details_missing_fields(self, client):
        """Test: detalls sense year o text retorna 400"""
        response = client.post('/api/ephemeris/details',
                                json={'lang': 'es'})

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @responses.activate
    def test_get_details_event_not_found(self, client):
        """Test: event no trobat retorna 404"""
        today = datetime.now()
        responses.add(
            responses.GET,
            f'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/{today.month:02d}/{today.day:02d}',
            json={'events': [
                {'year': 2000, 'text': 'Different event', 'pages': []}
            ]},
            status=200
        )

        response = client.post('/api/ephemeris/details',
                                json={'year': 1492, 'text': 'Non-existent', 'lang': 'es'})

        assert response.status_code == 404


class TestTranslationsEndpoint:
    """Tests per l'endpoint de traduccions"""

    def test_get_translations_catalan(self, client):
        """Test: GET /api/translations/ca retorna traduccions"""
        response = client.get('/api/translations/ca')

        assert response.status_code == 200
        data = response.get_json()
        assert 'app' in data
        assert 'title' in data['app']

    def test_get_translations_spanish(self, client):
        """Test: GET /api/translations/es retorna traduccions"""
        response = client.get('/api/translations/es')

        assert response.status_code == 200
        data = response.get_json()
        assert 'app' in data

    def test_get_translations_english(self, client):
        """Test: GET /api/translations/en retorna traduccions"""
        response = client.get('/api/translations/en')

        assert response.status_code == 200
        data = response.get_json()
        assert 'app' in data

    def test_get_translations_unsupported_language(self, client):
        """Test: idioma no suportat retorna 400"""
        response = client.get('/api/translations/de')

        assert response.status_code == 400
