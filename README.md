# Efemèrides Històriques

[![Tests](https://github.com/USERNAME/ephemerides-app/workflows/Tests/badge.svg)](https://github.com/USERNAME/ephemerides-app/actions)
[![codecov](https://codecov.io/gh/USERNAME/ephemerides-app/branch/main/graph/badge.svg)](https://codecov.io/gh/USERNAME/ephemerides-app)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplicació web que mostra efemèrides històriques del dia actual amb un disseny vintage elegant.

## Característiques

- 📅 Mostra una efemèride històrica del dia actual
- 🔄 Botó per carregar una altra efemèride diferent
- 📖 Botó per expandir i veure més informació amb detalls ampliats
- 🌍 Suport multiidioma (Català, Castellà, Anglès)
- 🎨 Disseny històric/vintage amb colors càlids i tipografia clàssica
- 📱 Responsive design (funciona en desktop, tablet i mòbil)
- 📚 Font de dades: Wikipedia REST API

## Stack Tecnològic

- **Backend**: Flask (Python 3.12)
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **API externa**: Wikipedia REST API (gratuïta, sense clau d'API necessària)
- **Fonts**: Google Fonts (Playfair Display, Crimson Text)

## Instal·lació

### Prerequisits

- Python 3.12 o superior
- pip (gestor de paquets de Python)

### Passos

1. **Clonar o descarregar el projecte**

```bash
cd /home/laianavarro/ephemerides-app
```

2. **Crear entorn virtual**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instal·lar dependències**

```bash
pip install -r requirements.txt
```

## Ús

### Executar el servidor de desenvolupament

```bash
source venv/bin/activate
python app.py
```

El servidor s'iniciarà a http://localhost:5000

### Aturar el servidor

Prem `Ctrl+C` al terminal on s'executa el servidor.

## Estructura del Projecte

```
ephemerides-app/
├── app.py                      # Aplicació Flask principal
├── config.py                   # Configuració
├── requirements.txt            # Dependències Python
├── README.md                   # Aquesta documentació
│
├── api/
│   ├── __init__.py
│   └── wikipedia_client.py     # Client per Wikipedia API
│
├── static/
│   ├── css/
│   │   ├── vintage.css         # Estils principals vintage
│   │   └── responsive.css      # Estils responsive
│   │
│   └── js/
│       ├── api-client.js       # Client per backend
│       ├── i18n.js             # Sistema d'internacionalització
│       ├── animations.js       # Animacions
│       └── app.js              # Lògica principal
│
├── templates/
│   └── index.html              # Pàgina HTML principal
│
└── translations/
    ├── ca.json                 # Traduccions català
    ├── es.json                 # Traduccions castellà
    └── en.json                 # Traduccions anglès
```

## API Endpoints

### GET /
Servir la pàgina principal HTML

### GET /api/ephemeris/today?lang={ca|es|en}
Retorna una efemèride aleatòria del dia actual

**Response:**
```json
{
  "year": 1492,
  "text": "Cristóbal Colón descubre...",
  "hasDetails": true
}
```

### POST /api/ephemeris/details
Retorna detalls ampliats d'una efemèride

**Request body:**
```json
{
  "year": 1492,
  "text": "Cristóbal Colón descubre...",
  "lang": "es"
}
```

**Response:**
```json
{
  "year": 1492,
  "text": "Cristóbal Colón descubre...",
  "description": "Descripció detallada...",
  "thumbnail": "https://...",
  "links": [
    {"title": "Cristóbal Colón", "url": "https://..."}
  ]
}
```

### GET /api/translations/{lang}
Retorna traduccions per l'idioma especificat

### GET /health
Health check endpoint

## Funcionalitats

### 1. Càrrega Inicial
- L'aplicació carrega automàticament una efemèride en català
- Mostra la data actual formatada
- Els botons queden habilitats quan l'efemèride s'ha carregat

### 2. Següent Efemèride
- Clicar el botó "Següent efemèride" carrega una nova efemèride aleatòria
- Cada vegada es mostra contingut diferent del mateix dia
- Els detalls expandits es col·lapsen automàticament

### 3. Més Informació
- Clicar "Més informació" expandeix els detalls de l'efemèride
- Mostra descripció ampliada, imatge (si disponible) i links a Wikipedia
- Clicar "Menys informació" col·lapsa els detalls

### 4. Canvi d'Idioma
- Clicar els botons CA/ES/EN canvia l'idioma de tota la interfície
- Les traduccions es carreguen dinàmicament
- L'efemèride es recarrega en el nou idioma
- La data es reformata segons l'idioma seleccionat

## Notes Importants

### Idiomes i Wikipedia API
- **Important**: L'API "onthisday" de Wikipedia no suporta català actualment
- Quan se selecciona català, l'aplicació utilitza les dades en espanyol de Wikipedia
- La interfície d'usuari (botons, missatges) sí que es mostra en català
- Espanyol i anglès utilitzen les seves respectives versions de Wikipedia

### Limitacions Conegudes
- L'API de Wikipedia pot tenir límits de rate (no documentats oficialment)
- No totes les efemèrides tenen imatges o detalls ampliats
- Les dades depenen de la disponibilitat de Wikipedia

## Personalització

### Canviar Colors
Edita [static/css/vintage.css](static/css/vintage.css) i modifica les variables CSS a `:root`:

```css
:root {
    --color-primary: #8B4513;    /* Color principal */
    --color-secondary: #D4AF37;  /* Color secundari */
    --color-accent: #B8860B;     /* Color d'accent */
    /* ... */
}
```

### Afegir Més Idiomes
1. Afegir l'idioma a `SUPPORTED_LANGUAGES` a [config.py](config.py)
2. Afegir el mapatge a `WIKIPEDIA_LANGUAGE_MAP` (si Wikipedia no el suporta)
3. Crear fitxer `translations/{lang}.json`
4. Afegir botó d'idioma a [templates/index.html](templates/index.html)

## CI/CD

Aquest projecte utilitza GitHub Actions per executar tests automàticament:

- **Tests automàtics**: S'executen en cada push i pull request
- **Cobertura de codi**: 91% cobertura amb pytest-cov
- **Python 3.12**: Tests executats amb l'última versió de Python

Per veure l'estat dels tests, consulta la pestanya [Actions](https://github.com/USERNAME/ephemerides-app/actions) del repositori.

## Troubleshooting

### Error: Port 5000 ja en ús
```bash
# Trobar el procés que utilitza el port
lsof -ti:5000

# Aturar el procés
kill -9 $(lsof -ti:5000)
```

### Error: No module named 'flask'
```bash
# Assegura't que l'entorn virtual està activat
source venv/bin/activate

# Reinstal·la les dependències
pip install -r requirements.txt
```

### Error: Wikipedia API no respon
- Verifica la connexió a Internet
- Comprova que Wikipedia està accessible
- Intenta amb un idioma diferent

## Llicència

Projecte educatiu · 2026

Les dades provenen de Wikipedia i estan subjectes a les seves llicències respectives.

## Crèdits

- Dades: [Wikipedia](https://www.wikipedia.org/)
- Fonts: [Google Fonts](https://fonts.google.com/)
- Framework: [Flask](https://flask.palletsprojects.com/)
