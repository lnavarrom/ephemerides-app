Feature: Client de Wikipedia per obtenir efemèrides
  Com a aplicació d'efemèrides històriques
  Vull poder obtenir events històrics de Wikipedia
  Per tal de mostrar-los als usuaris

  Background:
    Given el client de Wikipedia està inicialitzat
    And la data actual és el 16 de febrer de 2026

  Scenario: Obtenir tots els events d'un dia
    When sol·licito els events del dia 16 de febrer en espanyol
    Then hauria de rebre una llista d'events
    And cada event hauria de tenir un any
    And cada event hauria de tenir un text descriptiu

  Scenario: Obtenir un event aleatori
    When sol·licito un event aleatori del dia 16 de febrer en espanyol
    Then hauria de rebre un únic event
    And l'event hauria de tenir un any
    And l'event hauria de tenir un text descriptiu
    And l'event hauria de tenir pàgines relacionades

  Scenario: Obtenir detalls d'un event
    Given tinc un event del dia 16 de febrer
    When sol·licito els detalls de l'event en espanyol
    Then hauria de rebre detalls ampliats
    And els detalls haurien d'incloure l'any
    And els detalls haurien d'incloure el text
    And els detalls podrien incloure una descripció
    And els detalls podrien incloure una imatge thumbnail
    And els detalls podrien incloure links a articles

  Scenario: Gestió d'errors amb idioma no suportat
    When sol·licito events amb un idioma no suportat
    Then hauria de rebre un error
    And l'error hauria d'indicar que l'idioma no està disponible

  Scenario: Gestió d'errors de xarxa
    Given l'API de Wikipedia no està disponible
    When sol·licito events del dia 16 de febrer
    Then hauria de rebre un error de connexió
