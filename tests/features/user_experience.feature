Feature: Experiència d'usuari de l'aplicació
  Com a usuari de l'aplicació
  Vull poder veure i interactuar amb efemèrides històriques
  Per tal d'aprendre sobre esdeveniments del passat

  Background:
    Given obro l'aplicació al navegador
    And l'aplicació s'ha carregat completament

  Scenario: Càrrega inicial de l'aplicació
    Then hauria de veure el títol "Efemèrides Històriques"
    And hauria de veure la data actual formatada
    And hauria de veure una efemèride històrica
    And l'efemèride hauria de mostrar un any
    And l'efemèride hauria de mostrar un text descriptiu
    And els botons haurien d'estar habilitats

  Scenario: Selector d'idioma visible
    Then hauria de veure botons d'idioma CA, ES, EN
    And el botó CA hauria d'estar actiu per defecte

  Scenario: Carregar una altra efemèride
    Given veig una efemèride inicial
    When clico el botó "Següent efemèride"
    Then hauria de veure un indicador de càrrega
    And després hauria de veure una nova efemèride diferent
    And la nova efemèride hauria de tenir un any diferent o text diferent

  Scenario: Expandir més informació
    Given veig una efemèride amb detalls disponibles
    When clico el botó "Més informació"
    Then hauria de veure informació addicional expandida
    And podria veure una imatge relacionada
    And hauria de veure una descripció ampliada
    And hauria de veure links a articles de Wikipedia
    And el botó hauria de canviar a "Menys informació"

  Scenario: Col·lapsar més informació
    Given he expandit la informació d'una efemèride
    When clico el botó "Menys informació"
    Then la informació addicional s'hauria d'amagar
    And el botó hauria de tornar a "Més informació"

  Scenario: Canviar idioma a espanyol
    When clico el botó "ES"
    Then el botó ES hauria d'estar actiu
    And el botó CA no hauria d'estar actiu
    And tots els textos de la interfície haurien d'estar en espanyol
    And la data hauria d'estar formatada en espanyol
    And hauria de veure una nova efemèride en espanyol

  Scenario: Canviar idioma a anglès
    When clico el botó "EN"
    Then el botó EN hauria d'estar actiu
    And tots els textos de la interfície haurien d'estar en anglès
    And la data hauria d'estar formatada en anglès
    And hauria de veure una nova efemèride en anglès

  Scenario: Tornar al català des d'un altre idioma
    Given l'idioma actual és espanyol
    When clico el botó "CA"
    Then el botó CA hauria d'estar actiu
    And tots els textos de la interfície haurien de tornar al català
    And hauria de veure una nova efemèride

  Scenario: Gestió d'errors de connexió
    Given l'API no està disponible
    When intento carregar una efemèride
    Then hauria de veure un missatge d'error
    And hauria de veure un botó "Tornar a intentar"

  Scenario: Recuperació després d'error
    Given veig un missatge d'error
    And l'API torna a estar disponible
    When clico el botó "Tornar a intentar"
    Then l'error hauria de desaparèixer
    And hauria de veure una efemèride vàlida

  Scenario: Responsive design en mòbil
    Given obro l'aplicació en un dispositiu mòbil
    Then tots els elements haurien de ser visibles
    And els botons haurien d'estar apilats verticalment
    And el text hauria de ser llegible
    And els botons haurien de ser fàcils de prémer

  Scenario: Links a Wikipedia funcionals
    Given he expandit la informació d'una efemèride
    And veig links a articles de Wikipedia
    When clico un link de Wikipedia
    Then s'hauria d'obrir en una nova pestanya
    And hauria de portar-me a l'article correcte de Wikipedia
