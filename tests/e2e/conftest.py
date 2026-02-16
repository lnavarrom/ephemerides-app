"""
Fixtures específiques per tests E2E
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import time
import requests
import shutil


def is_chrome_available():
    """Verifica si Chrome està instal·lat"""
    chrome_commands = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']
    for cmd in chrome_commands:
        if shutil.which(cmd):
            return True
    return False


@pytest.fixture(scope="session")
def flask_server():
    """
    Inicia el servidor Flask per als tests E2E
    """
    # Iniciar servidor Flask en background
    process = subprocess.Popen(
        ['python', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd='/home/laianavarro/ephemerides-app'
    )

    # Esperar que el servidor estigui llest
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get('http://localhost:5000/health', timeout=1)
            if response.status_code == 200:
                break
        except:
            time.sleep(0.5)
    else:
        process.kill()
        raise Exception("Flask server failed to start")

    yield process

    # Aturar servidor després dels tests
    process.terminate()
    process.wait(timeout=5)


@pytest.fixture
def driver(flask_server):
    """
    WebDriver de Selenium configurat
    """
    # Skip si Chrome no està disponible
    if not is_chrome_available():
        pytest.skip("Chrome/Chromium no està instal·lat. Instal·la Chrome per executar tests E2E.")

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Executar sense GUI
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture
def base_url():
    """URL base de l'aplicació"""
    return 'http://localhost:5000'
