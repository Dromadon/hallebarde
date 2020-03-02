Feature: Upload token validation

  Scenario: Creating and validating an exchange
    Given I am authenticated to use the Hallebarde file transfer services
    And I create an exchange
    When I ask for a presigned upload url with this exchange upload token
    Then I can upload a file
