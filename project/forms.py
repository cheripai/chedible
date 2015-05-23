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


from flask_wtf import Form
from wtforms import BooleanField, FloatField, StringField
from wtforms.validators import DataRequired, Email, Length, URL, Optional


class AddRestaurantForm(Form):
    name = StringField('Restaurant Name', validators=[DataRequired(message="A restaurant name is required"), Length(min=2, max=32, message="Must be between 2 and 32 characters")])
    category = StringField('Category', validators=[DataRequired(message="A category is required"), Length(min=2, max=32, message="Must be between 2 and 32 characters")])
    image = StringField('Restaurant Image', validators=[Optional(), URL(message="Invalid URL")])


class AddDishForm(Form):
    name = StringField('Dish Name', validators=[DataRequired(message="A name is required"), Length(min=2, max=32, message="Must be between 2 and 32 characters")])
    price = FloatField('Price')
    image = StringField('Dish Image')
    beef = BooleanField('Beef')
    dairy = BooleanField('Dairy')
    egg = BooleanField('Egg')
    fish = BooleanField('Fish')
    gluten = BooleanField('Gluten')
    meat = BooleanField('Meat')
    nut = BooleanField('Nut')
    pork = BooleanField('Pork')
    poultry = BooleanField('Poultry')
    shellfish = BooleanField('Shellfish')
    soy = BooleanField('Soy')
    wheat = BooleanField('Wheat')
    notes = StringField('Additional Notes', validators=[Optional(), Length(min=2, max=512, message="Must be between 2 and 512 characters")])


class SearchForm(Form):
    query = StringField('Query', validators=[DataRequired(), Length(min=1, max=64, message="Must be between 1 and 64 characters")])
