Feature: Exchange management

  Scenario: Creating and listing exchanges
    Given I am authenticated to use the Hallebarde file transfer services
    And I create an exchange
    When I ask for all my exchanges
    Then the exchange I created is included in the list

  Scenario: Creating and revoking exchanges
    Given I am authenticated to use the Hallebarde file transfer services
    And I create an exchange
    When I revoke this exchange
    And I ask for all my exchanges
    Then the exchange I created is not included in the list
