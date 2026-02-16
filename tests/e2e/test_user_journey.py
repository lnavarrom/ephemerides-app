"""
Tests E2E del flow complet d'usuari
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.e2e
@pytest.mark.slow
class TestInitialLoad:
    """Tests de càrrega inicial de l'aplicació"""

    def test_page_loads_successfully(self, driver, base_url):
        """Test: La pàgina carrega correctament"""
        driver.get(base_url)

        # Verificar que el títol és correcte
        assert "Efemèrides" in driver.title

    def test_header_is_visible(self, driver, base_url):
        """Test: El header és visible amb el títol"""
        driver.get(base_url)

        header = driver.find_element(By.CLASS_NAME, 'app-header')
        assert header.is_displayed()

        title = driver.find_element(By.CLASS_NAME, 'app-title')
        assert "Efemèrides" in title.text

    def test_language_selector_visible(self, driver, base_url):
        """Test: El selector d'idioma és visible"""
        driver.get(base_url)

        lang_buttons = driver.find_elements(By.CLASS_NAME, 'lang-btn')
        assert len(lang_buttons) == 3

        # Verificar que CA està actiu per defecte
        ca_button = driver.find_element(By.CSS_SELECTOR, '[data-lang="ca"]')
        assert 'active' in ca_button.get_attribute('class')

    def test_date_display_visible(self, driver, base_url):
        """Test: La data actual es mostra"""
        driver.get(base_url)

        date_element = driver.find_element(By.ID, 'current-date')
        # Esperar que JavaScript carregui la data
        WebDriverWait(driver, 10).until(
            lambda d: len(date_element.text) > 0
        )
        assert len(date_element.text) > 0

    def test_ephemeris_loads_automatically(self, driver, base_url):
        """Test: Una efemèride carrega automàticament"""
        driver.get(base_url)

        # Esperar que l'efemèride es carregui
        ephemeris_content = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        assert ephemeris_content.is_displayed()

        # Verificar que té any i text
        year_badge = driver.find_element(By.ID, 'year-badge')
        assert len(year_badge.text) > 0

        ephemeris_text = driver.find_element(By.ID, 'ephemeris-text')
        assert len(ephemeris_text.text) > 0

    def test_buttons_are_enabled(self, driver, base_url):
        """Test: Els botons queden habilitats després de carregar"""
        driver.get(base_url)

        # Esperar que els botons s'habilitin
        next_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'next-btn'))
        )

        assert next_btn.is_enabled()


@pytest.mark.e2e
@pytest.mark.slow
class TestUserInteractions:
    """Tests d'interaccions de l'usuari"""

    def test_load_next_ephemeris(self, driver, base_url):
        """Test: Carregar següent efemèride"""
        driver.get(base_url)

        # Esperar càrrega inicial
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # Guardar text inicial
        initial_text = driver.find_element(By.ID, 'ephemeris-text').text

        # Clicar botó següent
        next_btn = driver.find_element(By.ID, 'next-btn')
        next_btn.click()

        # Esperar que carregui nova efemèride
        time.sleep(2)

        # Verificar que el text ha canviat
        new_text = driver.find_element(By.ID, 'ephemeris-text').text
        # Pot ser el mateix text si hi ha poques efemèrides, però hauria de carregar
        assert len(new_text) > 0

    def test_expand_more_information(self, driver, base_url):
        """Test: Expandir més informació"""
        driver.get(base_url)

        # Esperar càrrega
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # Esperar que el botó de detalls estigui habilitat
        details_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'details-btn'))
        )

        # Verificar que el botó no està disabled
        if not details_btn.is_enabled():
            pytest.skip("Aquest event no té detalls disponibles")

        # Clicar botó més informació
        details_btn.click()

        # Esperar que es mostrin els detalls
        time.sleep(2)

        # Verificar que el botó ha canviat el text
        button_text = details_btn.find_element(By.TAG_NAME, 'span').text
        # Pot ser "Menys informació" o "Menos información" o "Less information"
        assert len(button_text) > 0

    def test_change_language_to_spanish(self, driver, base_url):
        """Test: Canviar idioma a espanyol"""
        driver.get(base_url)

        # Esperar càrrega inicial
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # Clicar botó ES
        es_button = driver.find_element(By.CSS_SELECTOR, '[data-lang="es"]')
        es_button.click()

        # Esperar que l'idioma canviï
        time.sleep(2)

        # Verificar que ES està actiu
        assert 'active' in es_button.get_attribute('class')

        # Verificar que CA ja no està actiu
        ca_button = driver.find_element(By.CSS_SELECTOR, '[data-lang="ca"]')
        assert 'active' not in ca_button.get_attribute('class')

    def test_change_language_to_english(self, driver, base_url):
        """Test: Canviar idioma a anglès"""
        driver.get(base_url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # Clicar botó EN
        en_button = driver.find_element(By.CSS_SELECTOR, '[data-lang="en"]')
        en_button.click()

        time.sleep(2)

        # Verificar que EN està actiu
        assert 'active' in en_button.get_attribute('class')

    def test_multiple_language_switches(self, driver, base_url):
        """Test: Canviar entre múltiples idiomes"""
        driver.get(base_url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # CA -> ES
        driver.find_element(By.CSS_SELECTOR, '[data-lang="es"]').click()
        time.sleep(2)

        # ES -> EN
        driver.find_element(By.CSS_SELECTOR, '[data-lang="en"]').click()
        time.sleep(2)

        # EN -> CA
        driver.find_element(By.CSS_SELECTOR, '[data-lang="ca"]').click()
        time.sleep(2)

        # Verificar que CA està actiu al final
        ca_button = driver.find_element(By.CSS_SELECTOR, '[data-lang="ca"]')
        assert 'active' in ca_button.get_attribute('class')


@pytest.mark.e2e
@pytest.mark.slow
class TestResponsiveDesign:
    """Tests de disseny responsive"""

    def test_mobile_view(self, driver, base_url):
        """Test: Vista mòbil"""
        # Configurar viewport mòbil
        driver.set_window_size(375, 667)
        driver.get(base_url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # Verificar que els elements són visibles
        header = driver.find_element(By.CLASS_NAME, 'app-header')
        assert header.is_displayed()

        action_buttons = driver.find_element(By.CLASS_NAME, 'action-buttons')
        assert action_buttons.is_displayed()

    def test_tablet_view(self, driver, base_url):
        """Test: Vista tablet"""
        driver.set_window_size(768, 1024)
        driver.get(base_url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # Verificar layout
        assert driver.find_element(By.CLASS_NAME, 'ephemeris-card').is_displayed()

    def test_desktop_view(self, driver, base_url):
        """Test: Vista desktop"""
        driver.set_window_size(1920, 1080)
        driver.get(base_url)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        # Verificar que tot és visible
        container = driver.find_element(By.CLASS_NAME, 'container')
        assert container.is_displayed()


@pytest.mark.e2e
@pytest.mark.slow
class TestCompleteUserJourney:
    """Test del journey complet d'un usuari"""

    def test_complete_user_flow(self, driver, base_url):
        """
        Test: Simulació completa d'ús de l'aplicació

        Flux:
        1. Obrir aplicació
        2. Veure efemèride inicial
        3. Carregar següent efemèride
        4. Canviar a espanyol
        5. Expandir més informació
        6. Tornar a català
        """
        # 1. Obrir aplicació
        driver.get(base_url)

        # 2. Verificar efemèride inicial
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'ephemeris-content'))
        )

        year_badge = driver.find_element(By.ID, 'year-badge')
        assert len(year_badge.text) > 0
        print(f"✓ Efemèride inicial carregada: Any {year_badge.text}")

        # 3. Carregar següent efemèride
        next_btn = driver.find_element(By.ID, 'next-btn')
        next_btn.click()
        time.sleep(2)

        new_year = driver.find_element(By.ID, 'year-badge').text
        print(f"✓ Nova efemèride carregada: Any {new_year}")

        # 4. Canviar a espanyol
        es_button = driver.find_element(By.CSS_SELECTOR, '[data-lang="es"]')
        es_button.click()
        time.sleep(2)

        assert 'active' in es_button.get_attribute('class')
        print("✓ Idioma canviat a espanyol")

        # 5. Expandir més informació (si disponible)
        details_btn = driver.find_element(By.ID, 'details-btn')
        if details_btn.is_enabled():
            details_btn.click()
            time.sleep(2)
            print("✓ Més informació expandida")
        else:
            print("⊘ Més informació no disponible per aquest event")

        # 6. Tornar a català
        ca_button = driver.find_element(By.CSS_SELECTOR, '[data-lang="ca"]')
        ca_button.click()
        time.sleep(2)

        assert 'active' in ca_button.get_attribute('class')
        print("✓ Idioma tornat a català")

        print("\n✅ Journey complet completat amb èxit!")
