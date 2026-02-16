"""
Fixtures compartits per tots els tests
"""
import pytest
from datetime import datetime
from api.wikipedia_client import WikipediaClient
from config import Config
from app import app as flask_app


@pytest.fixture
def app():
    """Flask application fixture"""
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    """Flask test client"""
    return app.test_client()


@pytest.fixture
def wiki_client():
    """Wikipedia client fixture"""
    return WikipediaClient(Config.WIKIPEDIA_API_BASE)


@pytest.fixture
def mock_date():
    """Mock date fixture"""
    return datetime(2026, 2, 16)


@pytest.fixture
def sample_event():
    """Sample Wikipedia event"""
    return {
        'year': 1492,
        'text': 'Cristóbal Colón descubre América',
        'pages': [
            {
                'title': 'Cristóbal Colón',
                'extract': 'Cristóbal Colón fue un navegante...',
                'thumbnail': {
                    'source': 'https://example.com/image.jpg'
                },
                'content_urls': {
                    'desktop': {
                        'page': 'https://es.wikipedia.org/wiki/Cristóbal_Colón'
                    }
                }
            }
        ]
    }


@pytest.fixture
def sample_events_list():
    """Sample list of Wikipedia events"""
    return [
        {
            'year': 1866,
            'text': 'Se adopta la bandera de Honduras',
            'pages': []
        },
        {
            'year': 1923,
            'text': 'Se abre la tumba de Tutankamón',
            'pages': [
                {
                    'title': 'Tutankamón',
                    'extract': 'Tutankamón fue un faraón...'
                }
            ]
        },
        {
            'year': 1959,
            'text': 'Fidel Castro asume el poder en Cuba',
            'pages': []
        }
    ]
