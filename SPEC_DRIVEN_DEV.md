# Spec-Driven Development - Guia Completa

## 🎯 Què és Spec-Driven Development?

Spec-Driven Development (SDD) és una metodologia de desenvolupament on:
1. **Primer** escrius especificacions que defineixen el comportament esperat
2. **Després** implementes el codi per complir aquestes especificacions
3. **Finalment** refactoritzes amb confiança sabent que els tests et protegeixen

## 📊 Estat Actual del Projecte

### ✅ Implementat

#### 1. Especificacions Gherkin (BDD)
- **29 escenaris** definits en llenguatge natural
- **3 fitxers `.feature`**:
  - `wikipedia_client.feature` - Client de Wikipedia (5 escenaris)
  - `api_endpoints.feature` - Endpoints Flask (12 escenaris)
  - `user_experience.feature` - Experiència d'usuari (12 escenaris)

#### 2. Tests Unitaris
- **9 tests** pel client de Wikipedia
- **Cobertura: 98%** del client Wikipedia
- Mocking d'API HTTP amb `responses`

#### 3. Tests d'Integració
- **16 tests** pels endpoints Flask
- **Cobertura: 85%** de app.py
- Verificació de tots els endpoints

#### 4. Tests E2E
- **15 tests** Selenium
- Simulació d'interacció real d'usuari
- Tests de responsive design
- Journey complet d'usuari

### 📈 Mètriques de Qualitat

```
Total Tests:      40 tests
Tests Passing:    39/40 (97.5%)
Code Coverage:    90%
  - Wikipedia Client: 98%
  - Flask App:        85%
  - Total:            90%
```

## 🚀 Workflow de Desenvolupament

### Cicle TDD/SDD

1. **Red** (Vermell) - Escriu el test que falla:
```python
def test_new_feature():
    result = new_feature()
    assert result == expected_value
```

2. **Green** (Verd) - Implementa el mínim necessari:
```python
def new_feature():
    return expected_value
```

3. **Refactor** - Millora el codi:
```python
def new_feature():
    # Implementació millor i més neta
    return calculate_expected_value()
```

### Exemple Pràctic

**Scenario**: Vols afegir un filtre per tipus d'event (naixements, morts, etc.)

#### Pas 1: Escriu especificació Gherkin

```gherkin
# tests/features/wikipedia_client.feature

Scenario: Filtrar events per tipus
  Given el client de Wikipedia està inicialitzat
  When sol·licito events de tipus "births" del dia 16 de febrer
  Then hauria de rebre només events de naixements
  And cada event hauria de tenir tipus "births"
```

#### Pas 2: Escriu step definition

```python
# tests/step_defs/test_wikipedia_client_steps.py

@when('sol·licito events de tipus "births" del dia 16 de febrer')
def request_events_by_type(wikipedia_client):
    return wikipedia_client.get_events_by_type(2, 16, 'births', 'es')

@then('hauria de rebre només events de naixements')
def verify_births_only(request_events_by_type):
    assert all(event['type'] == 'births' for event in request_events_by_type)
```

#### Pas 3: Executa test (hauria de fallar)

```bash
pytest tests/step_defs/test_wikipedia_client_steps.py::test_filtrar_events_per_tipus
# FAIL: AttributeError: 'WikipediaClient' object has no attribute 'get_events_by_type'
```

#### Pas 4: Implementa funcionalitat

```python
# api/wikipedia_client.py

def get_events_by_type(self, month: int, day: int, event_type: str, language: str = 'ca') -> List[Dict]:
    """Obté events filtrats per tipus"""
    url = self.base_url_template.format(
        lang=language,
        type=event_type,  # 'births', 'deaths', 'events', etc.
        month=month,
        day=day
    )
    # ... implementació
```

#### Pas 5: Executa test (hauria de passar)

```bash
pytest tests/step_defs/test_wikipedia_client_steps.py::test_filtrar_events_per_tipus
# PASS ✓
```

#### Pas 6: Refactoritza si cal

```python
# Ara pots refactoritzar amb confiança
def get_events_by_type(self, month: int, day: int, event_type: str, language: str = 'ca') -> List[Dict]:
    """Obté events filtrats per tipus amb validació"""
    valid_types = ['events', 'births', 'deaths', 'selected', 'holidays']
    if event_type not in valid_types:
        raise ValueError(f"Invalid event type: {event_type}")

    # ... implementació millorada
```

## 📚 Comandaments Principals

### Executar Tests

```bash
# Tots els tests (excepte E2E)
make test

# Només unitaris
make test-unit

# Només integració
make test-integration

# Tots (inclou E2E - requereix Chrome)
make test-all

# Amb cobertura
make coverage
```

### Desenvolupament

```bash
# Formatar codi
make format

# Linting
make lint

# Netejar temporals
make clean

# Executar servidor
make run
```

## 🎨 Patrons i Best Practices

### 1. Escriu Tests Descriptius

❌ **Malament**:
```python
def test_1():
    assert func() == 5
```

✅ **Bé**:
```python
def test_get_events_returns_list_when_api_responds_successfully():
    """Test: get_events retorna una llista quan l'API respon correctament"""
    # Given
    mock_api_response()

    # When
    result = client.get_events(2, 16, 'es')

    # Then
    assert isinstance(result, list)
    assert len(result) > 0
```

### 2. Utilitza Fixtures

```python
@pytest.fixture
def authenticated_client():
    """Client autenticat per tests"""
    client = create_client()
    client.authenticate('test_user', 'password')
    return client

def test_protected_endpoint(authenticated_client):
    response = authenticated_client.get('/protected')
    assert response.status_code == 200
```

### 3. Mock Dependencies Externes

```python
@responses.activate
def test_api_call():
    responses.add(
        responses.GET,
        'https://external-api.com/endpoint',
        json={'data': 'value'},
        status=200
    )

    result = make_api_call()
    assert result['data'] == 'value'
```

### 4. Testa Edge Cases

```python
def test_empty_input():
    assert process_data([]) == []

def test_null_input():
    with pytest.raises(ValueError):
        process_data(None)

def test_large_input():
    large_data = [i for i in range(10000)]
    result = process_data(large_data)
    assert len(result) == 10000
```

## 🔄 Integració Contínua

### GitHub Actions Example

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.12

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: |
        pytest tests/unit tests/integration --cov --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## 📖 Recursos Addicionals

### Documentació
- **[TESTING.md](TESTING.md)** - Guia completa de testing
- **[README.md](README.md)** - Documentació de l'aplicació
- **[Especificacions Gherkin](tests/features/)** - Tots els escenaris

### Eines Utilitzades
- **pytest** - Framework de testing
- **pytest-bdd** - BDD amb Gherkin
- **pytest-cov** - Cobertura de codi
- **Selenium** - Tests E2E
- **responses** - Mocking HTTP
- **black** - Formatació de codi
- **flake8** - Linting

### Tutorials Recomanats
- [pytest Documentation](https://docs.pytest.org/)
- [BDD with pytest-bdd](https://pytest-bdd.readthedocs.io/)
- [Selenium Python](https://selenium-python.readthedocs.io/)

## 🎓 Exemples d'Ús

### Afegir Nova Funcionalitat

```bash
# 1. Escriu especificació Gherkin
vim tests/features/new_feature.feature

# 2. Executa test (hauria de fallar)
pytest tests/step_defs/test_new_feature_steps.py

# 3. Implementa step definitions
vim tests/step_defs/test_new_feature_steps.py

# 4. Implementa funcionalitat
vim api/new_feature.py

# 5. Executa tests fins que passin
pytest tests/step_defs/test_new_feature_steps.py

# 6. Verifica cobertura
make coverage

# 7. Commit canvis
git add .
git commit -m "Add new feature with specs"
```

### Debugging Tests

```bash
# Executar un test específic amb verbose
pytest tests/unit/test_wikipedia_client_unit.py::test_get_events_returns_list -vv

# Executar amb debugger
pytest --pdb

# Veure output de print statements
pytest -s

# Executar només tests fallits
pytest --lf
```

## 🏆 Beneficis Aconseguits

✅ **Confiança en canvis**: 90% cobertura permet refactoring segur
✅ **Documentació viva**: Gherkin documenta comportament esperat
✅ **Regression prevention**: Tests detecten bugs abans de production
✅ **Millor disseny**: TDD/SDD força millor arquitectura
✅ **Comunicació**: Format Given-When-Then és entenible per tots
✅ **Mantenibilitat**: Codi més net i testejable

## 📝 Checklist per Noves Features

- [ ] Escriu especificació Gherkin (Given-When-Then)
- [ ] Escriu step definitions
- [ ] Escriu tests unitaris
- [ ] Executa tests (haurien de fallar - RED)
- [ ] Implementa funcionalitat mínim viable
- [ ] Executa tests (haurien de passar - GREEN)
- [ ] Refactoritza codi
- [ ] Afegeix tests d'integració si cal
- [ ] Verifica cobertura >= 80%
- [ ] Executa linters i formata codi
- [ ] Commit amb missatge descriptiu

---

**Recorda**: El temps invertit en testing és temps estalviat en debugging! 🚀
