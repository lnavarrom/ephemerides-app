# Guia de Testing - Spec-Driven Development

Aquest document descriu l'estratègia de testing implementada per a l'aplicació d'Efemèrides Històriques utilitzant Spec-Driven Development (SDD) amb Behavior-Driven Development (BDD).

## 📋 Què s'ha Implementat

### 1. Infraestructura de Testing

✅ **Dependencies instal·lades** (`requirements-dev.txt`):
- `pytest==7.4.3` - Framework de testing principal
- `pytest-bdd==6.1.1` - Suport BDD amb Gherkin
- `pytest-cov==4.1.0` - Cobertura de codi
- `pytest-flask==1.3.0` - Testing per Flask
- `pytest-mock==3.12.0` - Mocking
- `selenium==4.16.0` - Tests E2E
- `responses==0.24.1` - Mocking d'API HTTP
- `faker==21.0.0` - Generació de dades de test

✅ **Estructura de directoris creada**:
```
tests/
├── features/              # Especificacions Gherkin (.feature)
├── step_defs/             # Step definitions (implementació)
├── unit/                  # Tests unitaris
├── integration/           # Tests d'integració
├── e2e/                   # Tests end-to-end
├── conftest.py            # Fixtures compartides
└── __init__.py
```

✅ **Configuració pytest** (`pytest.ini`):
- Configuració de cobertura
- Markers per tipus de tests (unit, integration, e2e, slow)
- Path de features per BDD

### 2. Especificacions Gherkin (Features)

S'han creat 3 fitxers `.feature` amb especificacions en llenguatge natural:

#### `wikipedia_client.feature`
- Obtenir tots els events d'un dia
- Obtenir un event aleatori
- Obtenir detalls d'un event
- Gestió d'errors amb idioma no suportat
- Gestió d'errors de xarxa

**Total**: 5 escenaris

#### `api_endpoints.feature`
- Pàgina principal accessible
- Health check endpoint
- Obtenir efemèride (CA, ES, EN)
- Idioma no suportat
- Obtenir detalls d'efemèride
- Detalls amb dades invàlides
- Obtenir traduccions (CA, ES, EN)
- Traduccions amb idioma no suportat

**Total**: 12 escenaris

#### `user_experience.feature`
- Càrrega inicial de l'aplicació
- Selector d'idioma visible
- Carregar una altra efemèride
- Expandir/col·lapsar més informació
- Canviar idioma (ES, EN, tornar a CA)
- Gestió d'errors de connexió
- Recuperació després d'error
- Responsive design en mòbil
- Links a Wikipedia funcionals

**Total**: 12 escenaris

**TOTAL ESPECIFICACIONS**: 29 escenaris definits

### 3. Fixtures Compartides

✅ Creat `tests/conftest.py` amb fixtures:
- `app` - Aplicació Flask en mode testing
- `client` - Client de test de Flask
- `wiki_client` - Client de Wikipedia
- `mock_date` - Data mockeada
- `sample_event` - Event de mostra
- `sample_events_list` - Llista d'events de mostra

### 4. Step Definitions

✅ Començat `test_wikipedia_client_steps.py`:
- Implementats steps GIVEN (precondicions)
- Implementats steps WHEN (accions)
- Implementats steps THEN (verificacions)

**Estat**: Necessita ajustaments en la integració amb pytest-bdd

## 🔧 Estat Actual i Pròxims Passos

### Què Funciona
- ✅ Infraestructura de testing instal·lada
- ✅ Especificacions Gherkin completes i documentades
- ✅ Fixtures compartides definides
- ✅ Configuració de pytest

### Què Necessita Ajustaments
- ⚠️ Step definitions necessiten correcció en la integració amb pytest-bdd
- ⚠️ Tests unitaris tradicionals encara no implementats
- ⚠️ Tests E2E amb Selenium encara no implementats

### Pròxims Passos Recomanats

#### 1. Solucionar Step Definitions (Prioritat Alta)

El problema actual és que les step definitions utilitzen decorators de manera que retornen funcions callable en lloc d'utilitzar les fixtures correctament.

**Solució recomanada**: Refactor step definitions per utilitzar context amb `pytest-bdd`:

```python
from pytest_bdd import scenarios, given, when, then
from pytest_bdd.parsers import parse

scenarios('../features/wikipedia_client.feature')

@given("el client de Wikipedia està inicialitzat", target_fixture="wiki_client")
def wikipedia_client_initialized(wiki_client):
    return wiki_client

@when("sol·licito els events del dia 16 de febrer en espanyol", target_fixture="events_result")
@responses.activate
def request_events_action(wiki_client, sample_events_list):
    responses.add(...)
    return wiki_client.get_events(2, 16, 'es')

@then("hauria de rebre una llista d'events")
def verify_events_list(events_result):
    assert isinstance(events_result, list)
    assert len(events_result) > 0
```

#### 2. Crear Tests Unitaris Tradicionals

Mentre es solucionen les step definitions de BDD, pots començar amb tests unitaris tradicionals:

```python
# tests/unit/test_wikipedia_client_unit.py
import pytest
from api.wikipedia_client import WikipediaClient

class TestWikipediaClient:
    def test_get_events_returns_list(self, wiki_client):
        # Test implementation
        pass

    def test_get_random_event_returns_dict(self, wiki_client):
        # Test implementation
        pass
```

#### 3. Tests d'Integració per Flask

```python
# tests/integration/test_api_integration.py
def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_ephemeris_today_endpoint(client):
    response = client.get('/api/ephemeris/today?lang=ca')
    assert response.status_code == 200
    data = response.get_json()
    assert 'year' in data
    assert 'text' in data
```

#### 4. Tests E2E amb Selenium

```python
# tests/e2e/test_user_flow.py
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_load_and_interact():
    driver = webdriver.Chrome()
    driver.get('http://localhost:5000')

    # Verificar càrrega inicial
    title = driver.find_element(By.CLASS_NAME, 'app-title')
    assert 'Efemèrides' in title.text

    # Clicar "Següent efemèride"
    next_btn = driver.find_element(By.ID, 'next-btn')
    next_btn.click()

    driver.quit()
```

## 📊 Executar Tests

### Tests BDD (quan estiguin funcionant)
```bash
pytest tests/step_defs/ -v
```

### Tests Unitaris
```bash
pytest tests/unit/ -v -m unit
```

### Tests d'Integració
```bash
pytest tests/integration/ -v -m integration
```

### Tests E2E
```bash
pytest tests/e2e/ -v -m e2e
```

### Tots els Tests amb Cobertura
```bash
pytest --cov=api --cov=app --cov-report=html --cov-report=term-missing
```

### Només Tests Ràpids (excloent E2E)
```bash
pytest -v -m "not slow"
```

## 📈 Objectius de Cobertura

- **Backend (api/, app.py)**: 80%+ cobertura
- **Tests crítics**: 100% cobertura per funcions crítiques
  - `WikipediaClient.get_events()`
  - `WikipediaClient.get_random_event()`
  - Endpoints Flask principals

## 🔍 Debugging Tests

### Veure fixtures disponibles
```bash
pytest --fixtures
```

### Executar un test específic amb verbose
```bash
pytest tests/step_defs/test_wikipedia_client_steps.py::test_obtenir_tots_els_events_dun_dia -vv
```

### Executar amb pdb (debugger)
```bash
pytest --pdb
```

## 📚 Recursos

- [pytest documentation](https://docs.pytest.org/)
- [pytest-bdd documentation](https://pytest-bdd.readthedocs.io/)
- [Gherkin syntax](https://cucumber.io/docs/gherkin/reference/)
- [responses library](https://github.com/getsentry/responses)

## 🎯 Beneficis del Spec-Driven Development

1. **Documentació viva**: Les especificacions Gherkin són documentació que sempre està actualitzada
2. **Comunicació clara**: Format Given-When-Then entenible per tots els stakeholders
3. **Tests com a contracte**: Els tests defineixen el comportament esperat
4. **Desenvolupament guiat**: Escrius tests primer, després implementes
5. **Refactoring segur**: Tests asseguren que no trenques funcionalitat existent

## ⚡ Quick Start

1. Instal·lar dependencies:
```bash
source venv/bin/activate
pip install -r requirements-dev.txt
```

2. Executar tests existents:
```bash
pytest -v
```

3. Veure cobertura:
```bash
pytest --cov=api --cov=app --cov-report=html
open htmlcov/index.html  # Veure report HTML
```

## 🐛 Problemes Coneguts

1. **Step definitions necessiten refactor**: Les funcions callable no s'integren bé amb pytest-bdd fixtures
2. **Tests E2E necessiten servidor executant**: Cal tenir Flask executant-se per tests Selenium
3. **Wikipedia API real**: Alguns tests poden fallar si Wikipedia no està disponible

## 💡 Recomanacions

1. **Començar amb tests unitaris tradicionals** mentre es solucionen les step definitions BDD
2. **Utilitzar mocking extensiu** per no dependre de l'API real de Wikipedia
3. **Executar tests freqüentment** durant el desenvolupament
4. **Mantenir especificacions Gherkin actualitzades** quan canviï funcionalitat
5. **CI/CD**: Configurar GitHub Actions o similar per executar tests automàticament
