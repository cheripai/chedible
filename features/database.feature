# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


Feature: Functioning of database


Scenario: entry is added to Restaurants table
    Given chedible is set up
    When we add "test" to "restaurants" 
    Then we should see "test" in "restaurants"


Scenario: entry is added to Dishes table
    Given chedible is set up
    When we add "test" to "dishes"
    Then we should see "test" in "dishes"


Scenario: entry is added to Users table
    Given chedible is set up
    When we add "test" to "users"
    Then we should see "test" in "users"


Scenario: entry is updated in Restaurants table
    Given chedible is set up
    When we update "test" in "restaurants" with "test_update"
    Then we should see "test_update" in "restaurants"
    And we should not see "test" in "restaurants"


Scenario: entry is updated in Dishes table
    Given chedible is set up
    When we update "test" in "dishes" with "test_update"
    Then we should see "test_update" in "dishes"
    And we should not see "test" in "dishes"


Scenario: entry is updated in Users table
    Given chedible is set up
    When we update "test" in "users" with "test_update"
    Then we should see "test_update" in "users"
    And we should not see "test" in "users"


Scenario: entry is deleted from Restaurants table
    Given chedible is set up
    When we delete "test_update" from "restaurants"
    Then we should not see "test" in "restaurants"


Scenario: entry is deleted from Dishes table
    Given chedible is set up
    When we delete "test_update" from "dishes"
    Then we should not see "test" in "dishes"


Scenario: entry is deleted from Users table
    Given chedible is set up
    When we delete "test_update" from "users"
    Then we should not see "test" in "users"


 Scenario: entry is added to Comments table
     Given chedible is set up
     When we add "test" to "comments"
     Then we should see "test" in "comments"


Scenario: entry is updated in Comments table
    Given chedible is set up
    When we update "test" in "comments" with "test_update"
    Then we should see "test_update" in "comments"
    And we should not see "test" in "comments"


Scenario: entry is deleted from Comments table
    Given chedible is set up
    When we delete "test_update" from "comments"
    Then we should not see "test_update" in "comments"
