# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL


class AddRestaurantForm(Form):
    name = StringField(
        'Restaurant Name',
        validators=[
            DataRequired(message="A restaurant name is required"),
            Length(min=2,
                   max=32,
                   message="Must be between 2 and 32 characters")
        ])
    category = StringField(
        'Category',
        validators=[
            DataRequired(message="A category is required"),
            Length(min=2,
                   max=32,
                   message="Must be between 2 and 32 characters"),
            Regexp('(^([A-Za-z0-9_.\' ]*\,)*[A-Za-z0-9 ]*$)',
                   message="Must be a comma separated list")
        ])
    tags = StringField('Tags',
                       validators=[
                           Optional(), Length(
                               min=2,
                               max=64,
                               message="Must be between 2 and 64 characters"),
                           Regexp('(^([A-Za-z0-9_.\' ]*\,)*[A-Za-z0-9 ]*$)',
                                  message="Must be a comma separated list")
                       ])


class AddDishForm(Form):
    name = StringField('Dish Name',
                       validators=[
                           DataRequired(message="A name is required"), Length(
                               min=2,
                               max=32,
                               message="Must be between 2 and 32 characters")
                       ])
    price = StringField('Price',
                        validators=[
                            Optional(), Regexp('(^[0-9]*\.[0-9][0-9])$',
                                               message="Invalid price format. \
                        Must be a number followed by 2 decimal places. \
                        Example: 12.34")
                        ])
    beef = StringField('Beef')
    dairy = StringField('Dairy')
    egg = StringField('Egg')
    fish = StringField('Fish')
    gluten = StringField('Gluten')
    meat = StringField('Meat')
    nut = StringField('Nut')
    non_organic = StringField('Non-Organic')
    pork = StringField('Pork')
    poultry = StringField('Poultry')
    shellfish = StringField('Shellfish')
    soy = StringField('Soy')
    wheat = StringField('Wheat')


class SearchForm(Form):
    query = StringField('Query',
                        validators=[
                            DataRequired(), Length(
                                min=1,
                                max=64,
                                message="Must be between 1 and 64 characters")
                        ])
    location = StringField(
        'Location',
        validators=[
            Length(max=128, message="Must be less than 128 characters")
        ])
    radius = StringField('Radius')
    searchAll = BooleanField('SearchAll')


class EditUserForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="A username is required"),
            Length(min=2,
                   max=32,
                   message="Must be between 2 and 32 characters")
        ])
    about = TextAreaField(
        'About Me',
        validators=[
            Optional(), Length(min=2,
                               max=512,
                               message="Must be between 2 and 512 characters")
        ])
    beef = StringField('Beef')
    dairy = StringField('Dairy')
    egg = StringField('Egg')
    fish = StringField('Fish')
    gluten = StringField('Gluten')
    meat = StringField('Meat')
    nut = StringField('Nut')
    non_organic = StringField('Non-Organic')
    pork = StringField('Pork')
    poultry = StringField('Poultry')
    shellfish = StringField('Shellfish')
    soy = StringField('Soy')
    wheat = StringField('Wheat')


class AddLocationForm(Form):
    location = StringField(
        'Location',
        validators=[
            Length(max=64, message="Must be less than 64 characters")
        ])


class PhotoForm(Form):
    photo = FileField('Photo')
    photo_url = StringField('Photo URL',
                            validators=[
                                Optional(), URL(message="Invalid URL"), Regexp(
                                    '([^\s]+(\.(?i)(jpg|jpeg|png|gif|bmp))$)',
                                    message="Invalid image path")
                            ])
