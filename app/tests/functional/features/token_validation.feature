Feature: Upload token validation

  Scenario: Creating and validating an exchange
    Given I am authenticated to use the Hallebarde file transfer services
    And I create an exchange
    When I ask for a presigned upload url with this exchange upload token
    And I can upload a file
    Then I ask for a presigned download url with this exchange download token
    And I can download a file
