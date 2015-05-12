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
    When we add "test" to "restaurants" 
    When we search "restaurants" for "test"
    Then we should see the text "test"


Scenario: search non-existing table
    Given chedible is set up
    When we search "test" for "test"
    Then we should see the text "No entries found"


Scenario: fuzzy search
    Given chedible is set up
    When we add "testing" to "dishes" 
    When we search "dishes" for "TEST"
    Then we should see the text "testing"
