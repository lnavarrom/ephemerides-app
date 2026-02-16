# Configuració de GitHub

Aquest document explica com pujar el projecte a GitHub i activar CI/CD.

## 📋 Prerequisits

- Compte de GitHub ([crear aquí](https://github.com/signup))
- Git instal·lat localment (✅ ja fet)

## 🚀 Passos per Pujar a GitHub

### 1. Crear Repositori a GitHub

1. Ves a [github.com](https://github.com) i inicia sessió
2. Clica el botó **"New"** (repositori nou)
3. Configura el repositori:
   - **Nom**: `ephemerides-app`
   - **Descripció**: `Aplicació web d'efemèrides històriques amb disseny vintage`
   - **Visibilitat**: Públic o Privat (a la teva elecció)
   - ⚠️ **NO** marquis "Add a README file"
   - ⚠️ **NO** marquis "Add .gitignore"
   - ⚠️ **NO** marquis "Choose a license"
4. Clica **"Create repository"**

### 2. Pujar el Codi Local a GitHub

Copia i executa aquestes comandes al terminal (substitueix `USERNAME` pel teu nom d'usuari de GitHub):

```bash
# Afegir remote de GitHub
git remote add origin https://github.com/USERNAME/ephemerides-app.git

# Pujar el codi
git push -u origin main
```

Si et demana autenticació, necessitaràs un **Personal Access Token**:
1. Ves a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Genera un nou token amb permisos de `repo`
3. Usa el token com a contrasenya quan facis `git push`

### 3. Verificar GitHub Actions

1. Ves al teu repositori a GitHub
2. Clica la pestanya **"Actions"**
3. Hauries de veure el workflow "Tests" executant-se automàticament
4. Espera que acabi (hauria de passar amb ✅)

### 4. Actualitzar Badges al README

Edita `README.md` i substitueix `USERNAME` amb el teu nom d'usuari de GitHub:

```markdown
[![Tests](https://github.com/USERNAME/ephemerides-app/workflows/Tests/badge.svg)](https://github.com/USERNAME/ephemerides-app/actions)
```

Després:
```bash
git add README.md
git commit -m "Update badges with GitHub username"
git push
```

### 5. (Opcional) Configurar Codecov

Per tenir cobertura de codi al badge:

1. Ves a [codecov.io](https://codecov.io/)
2. Inicia sessió amb GitHub
3. Afegeix el repositori `ephemerides-app`
4. Copia el token que et donen
5. Ves a GitHub → Settings del repositori → Secrets and variables → Actions
6. Afegeix un nou secret:
   - Name: `CODECOV_TOKEN`
   - Value: [el token de Codecov]

Actualitza `.github/workflows/tests.yml` afegint el token:
```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    file: ./coverage.xml
```

## 🎯 Què fa GitHub Actions?

El workflow configurat (`.github/workflows/tests.yml`) fa:

1. **S'executa automàticament** quan:
   - Fas `git push` a `main` o `develop`
   - Algú obre un Pull Request

2. **Executa els tests**:
   - Instal·la Python 3.12
   - Instal·la dependencies
   - Executa pytest amb cobertura
   - Puja resultats a Codecov

3. **Mostra resultats**:
   - Badge verd ✅ si tots els tests passen
   - Badge vermell ❌ si algun test falla
   - Report de cobertura al summary

## 📊 Avantatges de CI/CD

✅ **Detecció primerenca d'errors**: Els tests s'executen automàticament abans de merge
✅ **Confiança en el codi**: Codi revisat i testejat abans de producció
✅ **Documentació viva**: Badges mostren l'estat del projecte
✅ **Millor col·laboració**: Els PRs mostren si passen els tests
✅ **Qualitat consistent**: Mateix entorn de tests per a tothom

## 🔧 Comandes Git Útils

```bash
# Veure estat del repositori
git status

# Veure historial de commits
git log --oneline

# Crear nova branca
git checkout -b feature/nova-funcionalitat

# Pujar branca nova
git push -u origin feature/nova-funcionalitat

# Veure remotes configurats
git remote -v
```

## 📚 Recursos

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.com/)
