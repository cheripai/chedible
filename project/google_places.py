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


import json
import project._config as c
from urllib.request import urlopen


class Places(object):

    data = ''

    def __init__(self, query, lat, lng, radius):
        places = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        types = 'bakery|bar|cafe|food|meal_delivery|meal_takeaway|restaurant'

        response = urlopen(
            places + 'location={},{}&radius={}&types={}&keyword={}&key={}'.format(
                lat, lng, radius, types, query, c.GOOGLE_API_KEY
            )
        )
        self.data = json.loads(response.read().decode('utf-8'))

    # Constructs list of coordinates and infoboxes from JSON data
    # returned from Google Places. Used to populate search map
    def get_places_data(self):
        places_coords = []
        places_info = []
        marker = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        for place in self.data['results']:
            info_box = '<h6>{}</h6><p>{}{}{}</p>'
            open_status = ''
            rating = ''
            places_coords.append(
                (place['geometry']['location']['lat'],
                 place['geometry']['location']['lng'])
            )
            if 'opening_hours' in place and 'open_now' in place['opening_hours']:
                if place['opening_hours']['open_now']:
                    open_status = '<br><span class=\'text-success\'>Open</span>'
                else:
                    open_status = '<br><span class=\'text-danger\'>Closed</span>'
            if 'rating' in place:
                rating = '<br>Rating: {}'.format(self.generate_stars(place['rating']))
            places_info.append(
                info_box.format(place['name'], place['vicinity'], rating, open_status)
            )
        places_coords = {marker: places_coords}
        return places_coords, places_info


    def get_names(self):
        return [place['name'] for place in self.data['results']]


    # Creates string of stars based on float input
    def generate_stars(self, rating):
        stars = ''
        if rating >= 0 and rating <= 5:
            for i in range(int(rating)):
                stars += '<i class=\'fa fa-star\'></i>'
            dec = rating - int(rating)
            if dec >= 0.33 and dec < 0.66:
                stars += '<i class=\'fa fa-star-half-o\'></i>'
            elif dec >= 0.66:
                stars += '<i class=\'fa fa-star\'></i>'
        return stars