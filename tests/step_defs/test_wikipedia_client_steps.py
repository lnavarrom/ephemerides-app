"""
Step definitions per a tests del client de Wikipedia
"""
import pytest
import responses
from pytest_bdd import scenarios, given, when, then, parsers
from datetime import datetime
from api.wikipedia_client import WikipediaClient
from config import Config

# Carregar tots els escenaris del feature
scenarios('../features/wikipedia_client.feature')


# ============== GIVEN (Precondicions) ==============

@given('el client de Wikipedia està inicialitzat', target_fixture='wikipedia_client')
def wikipedia_client_initialized(wiki_client):
    """El client de Wikipedia està inicialitzat"""
    return wiki_client


@given("la data actual és el 16 de febrer de 2026")
def mock_current_date(mock_date):
    """Mock de la data actual"""
    return mock_date


@given('tinc un event del dia 16 de febrer', target_fixture='sample_wikipedia_event')
def sample_wikipedia_event_fixture(sample_event):
    """Event de mostra"""
    return sample_event


@given("l'API de Wikipedia no està disponible")
@responses.activate
def mock_wikipedia_unavailable():
    """Mock de l'API de Wikipedia no disponible"""
    responses.add(
        responses.GET,
        'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
        status=503
    )


# ============== WHEN (Accions) ==============

@when("sol·licito els events del dia 16 de febrer en espanyol", target_fixture='request_events')
@responses.activate
def request_events_action(wikipedia_client, sample_events_list):
    """Sol·licitar events del dia"""
    responses.add(
        responses.GET,
        'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
        json={'events': sample_events_list},
        status=200
    )
    return wikipedia_client.get_events(2, 16, 'es')


@when("sol·licito un event aleatori del dia 16 de febrer en espanyol", target_fixture='request_random_event')
@responses.activate
def request_random_event_action(wikipedia_client, sample_events_list):
    """Sol·licitar event aleatori"""
    responses.add(
        responses.GET,
        'https://es.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
        json={'events': sample_events_list},
        status=200
    )
    return wikipedia_client.get_random_event(2, 16, 'es')


@when("sol·licito els detalls de l'event en espanyol", target_fixture='request_event_details')
def request_event_details_action(wikipedia_client, sample_wikipedia_event):
    """Sol·licitar detalls d'un event"""
    return wikipedia_client.get_event_details(sample_wikipedia_event, 'es')


@when("sol·licito events amb un idioma no suportat", target_fixture='request_unsupported_language')
@responses.activate
def request_unsupported_language_action(wikipedia_client):
    """Sol·licitar events amb idioma no suportat"""
    responses.add(
        responses.GET,
        'https://xx.wikipedia.org/api/rest_v1/feed/onthisday/events/02/16',
        json={'status': 404, 'title': 'Not found'},
        status=404
    )
    try:
        return wikipedia_client.get_events(2, 16, 'xx')
    except Exception as e:
        return {'error': str(e)}


@when("sol·licito events del dia 16 de febrer", target_fixture='request_events_network_error')
@responses.activate
def request_events_network_error_action(wikipedia_client):
    """Sol·licitar events amb error de xarxa"""
    try:
        return wikipedia_client.get_events(2, 16, 'es')
    except Exception as e:
        return {'error': str(e)}


# ============== THEN (Verificacions) ==============

@then("hauria de rebre una llista d'events")
def verify_events_list(request_events):
    """Verificar que es rep una llista d'events"""
    assert isinstance(request_events, list)
    assert len(request_events) > 0


@then("cada event hauria de tenir un any")
def verify_event_has_year(request_events):
    """Verificar que cada event té un any"""
    for event in request_events:
        assert 'year' in event
        assert isinstance(event['year'], int)


@then("cada event hauria de tenir un text descriptiu")
def verify_event_has_text(request_events):
    """Verificar que cada event té text"""
    for event in request_events:
        assert 'text' in event
        assert isinstance(event['text'], str)
        assert len(event['text']) > 0


@then("hauria de rebre un únic event")
def verify_single_event(request_random_event):
    """Verificar que es rep un únic event"""
    assert isinstance(request_random_event, dict)


@then("l'event hauria de tenir un any")
def verify_random_event_year(request_random_event):
    """Verificar any de l'event aleatori"""
    assert 'year' in request_random_event


@then("l'event hauria de tenir un text descriptiu")
def verify_random_event_text(request_random_event):
    """Verificar text de l'event aleatori"""
    assert 'text' in request_random_event
    assert len(request_random_event['text']) > 0


@then("l'event hauria de tenir pàgines relacionades")
def verify_random_event_pages(request_random_event):
    """Verificar pàgines relacionades"""
    assert 'pages' in request_random_event


@then("hauria de rebre detalls ampliats")
def verify_details(request_event_details):
    """Verificar detalls ampliats"""
    assert isinstance(request_event_details, dict)


@then("els detalls haurien d'incloure l'any")
def verify_details_year(request_event_details):
    """Verificar any als detalls"""
    assert 'year' in request_event_details


@then("els detalls haurien d'incloure el text")
def verify_details_text(request_event_details):
    """Verificar text als detalls"""
    assert 'text' in request_event_details


@then("els detalls podrien incloure una descripció")
def verify_details_description(request_event_details):
    """Verificar descripció opcional"""
    # És opcional, només verifiquem que si existeix és string
    if 'description' in request_event_details:
        assert isinstance(request_event_details['description'], str)


@then("els detalls podrien incloure una imatge thumbnail")
def verify_details_thumbnail(request_event_details):
    """Verificar thumbnail opcional"""
    # És opcional
    if 'thumbnail' in request_event_details:
        assert isinstance(request_event_details['thumbnail'], str)


@then("els detalls podrien incloure links a articles")
def verify_details_links(request_event_details):
    """Verificar links opcionals"""
    assert 'links' in request_event_details
    assert isinstance(request_event_details['links'], list)


@then("hauria de rebre un error")
def verify_error(request_unsupported_language):
    """Verificar que es rep un error"""
    assert 'error' in request_unsupported_language


@then("l'error hauria d'indicar que l'idioma no està disponible")
def verify_language_error(request_unsupported_language):
    """Verificar missatge d'error d'idioma"""
    assert 'error' in request_unsupported_language
    error_msg = request_unsupported_language['error'].lower()
    assert 'error' in error_msg or 'not found' in error_msg or '404' in error_msg


@then("hauria de rebre un error de connexió")
def verify_connection_error(request_events_network_error):
    """Verificar error de connexió"""
    assert 'error' in request_events_network_error


# Helper fixture per passar resultats entre steps
@pytest.fixture
def wikipedia_client_context():
    """Context per compartir dades entre steps"""
    return {}
