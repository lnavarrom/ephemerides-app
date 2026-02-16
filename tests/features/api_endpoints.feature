Feature: Endpoints de l'API Flask
  Com a interfície d'usuari
  Vull poder consultar efemèrides a través de l'API
  Per tal de mostrar contingut històric

  Background:
    Given l'aplicació Flask està executant-se
    And l'API de Wikipedia està disponible

  Scenario: Pàgina principal accessible
    When accedeixo a la ruta principal "/"
    Then hauria de rebre el codi d'estat 200
    And hauria de rebre contingut HTML
    And l'HTML hauria de contenir el títol "Efemèrides Històriques"

  Scenario: Health check endpoint
    When accedeixo a l'endpoint "/health"
    Then hauria de rebre el codi d'estat 200
    And hauria de rebre un JSON amb status "ok"
    And hauria de rebre un timestamp

  Scenario: Obtenir efemèride del dia en català
    When sol·licito GET "/api/ephemeris/today?lang=ca"
    Then hauria de rebre el codi d'estat 200
    And hauria de rebre un JSON amb clau "year"
    And hauria de rebre un JSON amb clau "text"
    And hauria de rebre un JSON amb clau "hasDetails"
    And el text hauria d'estar en espanyol (ja que CA usa ES)

  Scenario: Obtenir efemèride del dia en espanyol
    When sol·licito GET "/api/ephemeris/today?lang=es"
    Then hauria de rebre el codi d'estat 200
    And hauria de rebre un JSON amb un event vàlid

  Scenario: Obtenir efemèride del dia en anglès
    When sol·licito GET "/api/ephemeris/today?lang=en"
    Then hauria de rebre el codi d'estat 200
    And hauria de rebre un JSON amb un event vàlid
    And el text hauria d'estar en anglès

  Scenario: Idioma no suportat
    When sol·licito GET "/api/ephemeris/today?lang=fr"
    Then hauria de rebre el codi d'estat 400
    And hauria de rebre un error "Unsupported language"

  Scenario: Obtenir detalls d'una efemèride
    Given tinc una efemèride del dia actual
    When sol·licito POST "/api/ephemeris/details" amb les dades de l'efemèride
    Then hauria de rebre el codi d'estat 200
    And hauria de rebre detalls ampliats de l'efemèride
    And els detalls haurien de contenir "description"
    And els detalls haurien de contenir "links"

  Scenario: Detalls amb dades invàlides
    When sol·licito POST "/api/ephemeris/details" sense year o text
    Then hauria de rebre el codi d'estat 400
    And hauria de rebre un error "Missing required fields"

  Scenario: Obtenir traduccions en català
    When sol·licito GET "/api/translations/ca"
    Then hauria de rebre el codi d'estat 200
    And hauria de rebre un JSON amb traduccions
    And les traduccions haurien de contenir "app.title"
    And les traduccions haurien de contenir "actions.nextEvent"

  Scenario: Obtenir traduccions en espanyol
    When sol·licito GET "/api/translations/es"
    Then hauria de rebre el codi d'estat 200
    And les traduccions haurien d'estar en espanyol

  Scenario: Obtenir traduccions en anglès
    When sol·licito GET "/api/translations/en"
    Then hauria de rebre el codi d'estat 200
    And les traduccions haurien d'estar en anglès

  Scenario: Traduccions amb idioma no suportat
    When sol·licito GET "/api/translations/de"
    Then hauria de rebre el codi d'estat 400
