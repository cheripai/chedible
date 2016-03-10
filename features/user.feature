# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


Feature: Ensure user related actions function correctly


Scenario: log in when not logged in
    Given chedible is set up
    When we log out
    And we add "test" to "users"
    And we log in
    Then we should see the text "test"
    And we should not see the text "Login"


Scenario: log out when logged in 
    Given chedible is set up
    When we log out
    Then we should see the text "Login"


Scenario: log out when not logged in
    Given chedible is set up
    When we log out
    Then we should see the text "You need to be logged in to do that!"
    And we should see the text "Login"


Scenario: User score is increased after user performs actions
    Given chedible is set up
    When we log in
    And we add "test1" to "restaurants" 
    And we add dish "test_dish1" to restaurant "test1"
    And we visit "/comment?content=Test&id=1"
    Then we should see "Test" as the "content" of "comments" "1"
    Then we should not see "0" as the "score" of "users" "3"


Scenario: User activity is updated after user posts
    Given chedible is set up
    When we log in
    And we visit "/comment?content=Test&id=1"
    Then we should see "time" as the "last_activity" of "users" "3"
