# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


Feature: General function of application


Scenario: page is visited
    Given chedible is set up
    When we visit the page
    Then we should see the text "chedible"


Scenario: search for non-existing restaurant
    Given chedible is set up
    When we search "restaurants" for "test"
    Then we should see the text "No entries found"


Scenario: search for existing restaurant
    Given chedible is set up
    When we add "test_unique_string" to "restaurants" 
    And we search "restaurants" for "test_unique_string"
    Then we should see the text "test_unique_string"


Scenario: search non-existing table
    Given chedible is set up
    When we search "test" for "test"
    Then we should see the text "404"


Scenario: fuzzy search
    Given chedible is set up
    When we add "testing" to "restaurants" 
    And we add "test" to "restaurants" 
    And we search "restaurants" for "TEST"
    Then we should see the text "testing"
    AND we should see the text "test"


Scenario: we access the add restaurant page
    Given chedible is set up
    When we log in
    And we visit "/add"
    Then we should see the text "Restaurant Name"


Scenario: access the add restaurant page while not logged in
    Given chedible is set up
    When we log out
    And we visit "/add"
    Then we should see the text "You need to be logged in to do that!"


Scenario: we add a restaurant using the add restaurant page
    Given chedible is set up
    When we log in
    And we add restaurant "restaurant_name" using the add restaurant page with tag "restaurant"
    Then we should see "restaurant_name" in "restaurants"


Scenario: we can view a restaurant profile
    Given chedible is set up
    When we log in
    And we add restaurant "name_of_restaurant" using the add restaurant page with tag "name"
    Then we should see the text "name_of_restaurant"


Scenario: we can find a restaurant using its tags
    Given chedible is set up
    When we log in
    And we add restaurant "the_name" using the add restaurant page with tag "obscure"
    And we search "restaurants" for "obscure"
    Then we should see the text "the_name"


Scenario: we can add a dish to a restaurant
    Given chedible is set up
    When we log in
    And we add restaurant "test_restaurant" using the add restaurant page with tag "test"
    And we add dish "test_dish" to restaurant "test_restaurant"
    Then we should see the text "test_dish"
    And we should see the text "test_restaurant"


Scenario: we can edit a restaurant
    Given chedible is set up
    When we log in
    And we add restaurant "test1" using the add restaurant page with tag "test"
    And we edit restaurant "test1" to "test2"
    Then we should see "test2" in "restaurants"
    And we should not see "test1" in "restaurants"


Scenario: we can not edit a restaurant when not logged in
    Given chedible is set up
    When we log in
    And we add restaurant "test3" using the add restaurant page with tag "test"
    And we log out
    And we edit restaurant "test3" to "test4"
    Then we should see the text "You need to be logged in to do that!"


Scenario: we can edit a dish
    Given chedible is set up
    When we log in
    And we add restaurant "test5" using the add restaurant page with tag "test"
    And we add dish "test_dish1" to restaurant "test5"
    And we edit dish "test_dish1" of restaurant "test5" to "test_dish2"
    Then we should see "test_dish2" in "dishes"
    And we should not see "test_dish1" in "dishes"


Scenario: we can view a user's profile
    Given chedible is set up
    When we log in
    And we visit "/user/1"
    Then we should see the text "Joined on"


Scenario: we can edit a user's profile
    Given chedible is set up
    When we log in
    And we visit "/user/1/edit"
    And we update the username "1337user" to user "test user"
    And we visit "/user/1"
    Then we should see "1337user" as the "username" of "users" "1"
    And we should see the text "1337user"


Scenario: we can upvote a dish
    Given chedible is set up
    When we log in
    And we visit "/vote?vote=upvote&id=1"
    Then we should see "1" as the "score" of "dishes" "1"


Scenario: we can remove an upvote on a dish
    Given chedible is set up
    When we log in
    And we visit "/vote?vote=upvote&id=2"
    And we visit "/vote?vote=upvote&id=2"
    Then we should see "0" as the "score" of "dishes" "2"


Scenario: we can downvote a dish
    Given chedible is set up
    When we log in
    And we add dish "test_dish3" to restaurant "test2"
    And we visit "/vote?vote=downvote&id=3"
    Then we should see "-1" as the "score" of "dishes" "3"


Scenario: we can remove a downvote on a dish
    Given chedible is set up
    When we log in
    And we add dish "test_dish4" to restaurant "test2"
    And we visit "/vote?vote=downvote&id=4"
    And we visit "/vote?vote=downvote&id=4"
    Then we should see "0" as the "score" of "dishes" "4"


Scenario: vote must contain id
    Given chedible is set up
    When we log in
    And we visit "/vote?vote=upvote&id="
    Then we should see the text "404"


Scenario: vote must contain type of vote
    Given chedible is set up
    When we log in
    And we visit "/vote?vote=&id=4"
    Then we should see the text "error"


Scenario: we cannot vote when not logged in
    Given chedible is set up
    When we log out
    And we visit "/vote?vote=downvote&id=4"
    Then we should see the text "You need to be logged in to do that!"


Scenario: type of vote must be correct
    Given chedible is set up
    When we log in
    And we visit "/vote?vote=test&id=4"
    Then we should see the text "error"


Scenario: dish id must exist
    Given chedible is set up
    When we log in
    And we visit "/vote?vote=upvote&id=1234"
    Then we should see the text "error"


Scenario: we can comment on a dish
    Given chedible is set up
    When we log in
    And we visit "/comment?content=Test&id=1"
    Then we should see "Test" as the "content" of "comments" "1"


Scenario: vote id must be of type int
    Given chedible is set up
    When we log in
    And we visit "/comment?content=test&id=test"
    Then we should see the text "error"


Scenario: we can comment using escaped reserved characters on a dish
    Given chedible is set up
    When we log in
    And we visit "/comment?content=Test %26 stuff'%3B&id=1"
    Then we should see "Test & stuff';" as the "content" of "comments" "2"


Scenario: we cannot comment when not logged in
    Given chedible is set up
    When we log out
    And we visit "/comment?content=Test&id=1"
    Then we should see the text "You must be logged in to do that!"


Scenario: comment must contain text
    Given chedible is set up
    When we log in
    And we visit "/comment?content=&id=1"
    Then we should see the text "error"


Scenario: comment must contain id
    Given chedible is set up
    When we log in
    And we visit "/comment?content=test&id="
    Then we should see the text "error"


Scenario: comment cannot exceed 512 characters
    Given chedible is set up
    When we log in
    And we visit "/comment?content=Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero egestas mattis sit amet vitae augue. Nam tincidunt congue enim, ut porta lorem lacinia consectetur. Donec ut libero sed arcu vehicula ultricies a non tortor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ut gravida lorem. Ut turpis felis, pulvinar a semper sed, adipiscing id dolor. Pellentesque auctor nisi id magna consequat sagittis. Curabitur dapibus enim sit amet elit pharetra tincidunt feugiat nisl imperdiet. Ut convallis libero in urna ultrices accumsan. Donec sed odio eros. Donec viverra mi quis quam pulvinar at malesuada arcu rhoncus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In rutrum accumsan ultricies. Mauris vitae nisi at sem facilisis semper ac in est.&id=1"
    Then we should see the text "error"
    Then we should see the text "Comment exceeds 512 characters"


Scenario: Comment route returns error when posting twice within post interval
    Given chedible is set up
    When we log in
    When we disable testing
    And we visit "/comment?content=test&id=1"
    And we visit "/comment?content=test&id=1"
    Then we should see the text "error"


Scenario: Comment route returns error when not sending any data
    Given chedible is set up
    When we log in
    When we visit "/comment"
    Then we should see the text "error"


Scenario: Comment route returns error when id is not an integer
    Given chedible is set up
    When we log in
    When we visit "/comment?content=test&id=test"
    Then we should see the text "error"


Scenario: we check the chediblity of a dish that contains nothing for a user that will eat anything
    Given chedible is set up
    When we log in
    And we add "ched test" to "users"
    And we enable testing
    And we set all of user "ched test" preferences to "True" except for "none"
    And we add dish "test_dish5" to restaurant "test2"
    And we set dish "test_dish5" so contains is "False" for attribute/s "everything"
    Then is_chedible should evaluate to True given user "ched test" and "test_dish5"


Scenario: we check the chediblity of a dish that contains everything for a user that will eat nothing
    Given chedible is set up
    When we add "ched test2" to "users"
    And we set all of user "ched test2" preferences to "False" except for "none"
    And we add dish "test_dish6" to restaurant "test2"
    And we set dish "test_dish6" so contains is "True" for attribute/s "everything"
    Then is_chedible should evaluate to False given user "ched test2" and "test_dish6"


Scenario: we check the chediblity of a dish that contains everything for a user that can't eat shellfish
    Given chedible is set up
    When we add "ched test3" to "users"
    And we set all of user "ched test3" preferences to "True" except for "shellfish"
    And we add dish "test_dish7" to restaurant "test2"
    And we set dish "test_dish7" so contains is "True" for attribute/s "everything"
    Then is_chedible should evaluate to False given user "ched test3" and "test_dish7"


Scenario: we check the chediblity of a dish that might contain everything for a user that can't eat shellfish
    Given chedible is set up 
    When we add dish "test_dish8" to restaurant "test2"
    And we set dish "test_dish8" so contains is "None" for attribute/s "everything"
    Then is_chedible should evaluate to False given user "ched test3" and "test_dish8"


Scenario: We can add a location to a restaurant
    Given chedible is set up
    When we log in
    And we visit "/restaurant/1/add_location?api_id=test&lat=0&lng=0&address=test"
    Then we should see the text "success"


Scenario: Add location route returns error when not sending any data
    Given chedible is set up
    When we log in
    And we visit "/restaurant/1/add_location"
    Then we should see the text "error"


Scenario: Add location route returns error when not sending api_id
    Given chedible is set up
    When we log in
    And we visit "/restaurant/1/add_location?lat=0&lng=0&address=test"
    Then we should see the text "error"


Scenario: Add location route returns error when not sending latitude or longitude
    Given chedible is set up
    When we log in
    And we visit "/restaurant/1/add_location?api_id=test&address=test"
    Then we should see the text "error"


Scenario: Add location route returns error when latitude and longitude is not a double
    Given chedible is set up
    When we log in
    And we visit "/restaurant/1/add_location?api_id=test&lat=test&lng=test&address=test"
    Then we should see the text "error"


Scenario: Add location route returns error when not sending address
    Given chedible is set up
    When we log in
    And we visit "/restaurant/1/add_location?api_id=test&lat=0&lng=0&address="
    Then we should see the text "error"


Scenario: Coords to city function returns the correct value
    Given chedible is set up
    When we log in
    And we visit "/search_results/restaurants/test/37.7749295,-122.4194155/3220"
    Then we should see the text "SF"


Scenario: We can report an issue
    Given chedible is set up
    When we log in
    And we visit "/report?type=dish&id=1&reason=test"
    Then we should see "test" as the "content" of "issues" "1"


Scenario: Add issue route returns error when not sending id
    Given chedible is set up
    When we log in
    And we visit "/report?type=dish&id=&reason=test"
    Then we should see the text "error"


Scenario: Add issue route returns error when not sending type
    Given chedible is set up
    When we log in
    And we visit "/report?type=&id=1&reason=test"
    Then we should see the text "error"


Scenario: we cannot add an issue when not logged in
    Given chedible is set up
    When we log out
    And we visit "/report?type=test&id=1&reason=test"
    Then we should see the text "You must be logged in to do that!"
