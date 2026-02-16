"""
Tests unitaris per al client de Wikipedia
"""
import pytest
import responses
from api.wikipedia_client import WikipediaClient
from config import Config


class TestWikipediaClient:
    """Tests per la classe WikipediaClient"""

    def test_client_initialization(self):
        """Test: El client s'inicialitza correctament"""
        client = WikipediaClient(Config.WIKIPEDIA_API_BASE)
        assert client.base_url_template == Config.WIKIPEDIA_API_BASE
        assert client.session is not None

    @responses.activate
    def test_get_events_returns_list(self, wiki_client):
        """Test: get_events retorna una llista d'events"""
        # Mock de la resposta de Wikipedia
        mock_events = [
            {'year': 1866, 'text': 'Test event 1', 'pages': []},
            {'year': 1923, 'text': 'Test event 2', 'pages': []}
        ]
        responses.add(
            responses.GET,
            'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
            json={'events': mock_events},
            status=200
        )

        events = wiki_client.get_events(2, 16, 'es')

        assert isinstance(events, list)
        assert len(events) == 2
        assert events[0]['year'] == 1866
        assert events[1]['year'] == 1923

    @responses.activate
    def test_get_random_event_returns_dict(self, wiki_client):
        """Test: get_random_event retorna un event aleatori"""
        mock_events = [
            {'year': 1492, 'text': 'Random event', 'pages': []}
        ]
        responses.add(
            responses.GET,
            'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
            json={'events': mock_events},
            status=200
        )

        event = wiki_client.get_random_event(2, 16, 'es')

        assert isinstance(event, dict)
        assert 'year' in event
        assert 'text' in event
        assert event['year'] == 1492

    @responses.activate
    def test_get_random_event_returns_none_when_no_events(self, wiki_client):
        """Test: get_random_event retorna None si no hi ha events"""
        responses.add(
            responses.GET,
            'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
            json={'events': []},
            status=200
        )

        event = wiki_client.get_random_event(2, 16, 'es')

        assert event is None

    def test_get_event_details_structure(self, wiki_client, sample_event):
        """Test: get_event_details retorna estructura correcta"""
        details = wiki_client.get_event_details(sample_event, 'es')

        assert isinstance(details, dict)
        assert 'year' in details
        assert 'text' in details
        assert 'links' in details
        assert isinstance(details['links'], list)

    def test_get_event_details_with_thumbnail(self, wiki_client):
        """Test: get_event_details extreu thumbnail correctament"""
        event_with_thumbnail = {
            'year': 2000,
            'text': 'Event with image',
            'pages': [{
                'title': 'Test',
                'extract': 'Description',
                'thumbnail': {'source': 'https://example.com/img.jpg'},
                'content_urls': {'desktop': {'page': 'https://example.com'}}
            }]
        }

        details = wiki_client.get_event_details(event_with_thumbnail, 'es')

        assert details['thumbnail'] == 'https://example.com/img.jpg'
        assert len(details['links']) == 1

    def test_get_event_details_without_pages(self, wiki_client):
        """Test: get_event_details funciona sense pàgines"""
        event_no_pages = {
            'year': 1999,
            'text': 'Event without pages',
            'pages': []
        }

        details = wiki_client.get_event_details(event_no_pages, 'es')

        assert details['year'] == 1999
        assert details['text'] == 'Event without pages'
        assert details['links'] == []

    @responses.activate
    def test_get_events_handles_http_error(self, wiki_client):
        """Test: get_events gestiona errors HTTP correctament"""
        responses.add(
            responses.GET,
            'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
            status=404
        )

        with pytest.raises(Exception) as exc_info:
            wiki_client.get_events(2, 16, 'es')

        assert 'Error fetching events from Wikipedia' in str(exc_info.value)

    @responses.activate
    def test_get_events_handles_timeout(self, wiki_client):
        """Test: get_events gestiona timeout correctament"""
        responses.add(
            responses.GET,
            'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
            body=Exception('Timeout')
        )

        with pytest.raises(Exception):
            wiki_client.get_events(2, 16, 'es')
