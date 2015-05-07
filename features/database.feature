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


Scenario: entry is deleted from Restaurants table
    Given chedible is set up
    When we delete "test" from "restaurants"
    Then we should not see "test" in "restaurants"


Scenario: entry is deleted from Dishes table
    Given chedible is set up
    When we delete "test" from "dishes"
    Then we should not see "test" in "dishes"


Scenario: entry is deleted from Users table
    Given chedible is set up
    When we delete "test" from "users"
    Then we should not see "test" in "users"
