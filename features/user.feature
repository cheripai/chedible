#    Copyright 2015 Dat Do
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#        http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


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
    Then we should not see the text "test"
    And we should see the text "Login"


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
