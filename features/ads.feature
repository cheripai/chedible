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


Feature: Display ads on pages

Scenario: user lands on main page
Given chedible is set up 
When we visit the page
Then we should not see the text "Ads n shit"

Scenario: user performs a search
Given chedible is set up
When we search "restaurants" for "test"
Then we should see the text "Ads n shit"

Scenario: user adds a restaurant
Given chedible is set up
When we log in with id "1"
And we add restaurant "restaurant_name" using the add restaurant page
Then we should see the text "Ads n shit"
