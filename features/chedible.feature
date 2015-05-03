Feature: Functioning of application skeleton

Scenario: page is visited
    Given chedible is set up
    When we visit the page
    Then we should see the text "chedible"
