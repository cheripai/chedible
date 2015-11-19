# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import project._config as c
from project.schema import Location
from urllib.request import urlopen
from urllib.parse import quote_plus

class Places(object):

    data = ''


    def __init__(self, query, lat, lng, radius):
        places = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        types = 'bakery|bar|cafe|food|meal_delivery|meal_takeaway|restaurant'

        query = quote_plus(query)
        response = urlopen(
            places + 'location={},{}&radius={}&types={}&keyword={}&key={}'.format(
                lat, lng, radius, types, query, c.GOOGLE_API_KEY
            )
        )
        self.data = json.loads(response.read().decode('utf-8'))


    # Constructs list of coordinates from query
    def get_coords(self):
        coords = []
        marker = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        for place in self.data['results']:
            coords.append(
                (place['geometry']['location']['lat'],
                 place['geometry']['location']['lng'])
            )
        coords = {marker: coords}
        return coords


    # Constructs list of info boxes to be displayed above map markers
    def get_info_boxes(self):
        boxes = []
        for place in self.data['results']:
            info_box = '<h6>{} {}</h6><p>{}{}</p>'
            open_status = ''
            rating = ''
            if 'opening_hours' in place and 'open_now' in place['opening_hours']:
                if place['opening_hours']['open_now']:
                    open_status = '<small class=\'text-success\'>Open</small>'
                else:
                    open_status = '<small class=\'text-danger\'>Closed</small>'
            if 'rating' in place:
                rating = '<br>Rating: {}'.format(self.generate_stars(place['rating']))
            boxes.append(
                info_box.format(place['name'], open_status, place['vicinity'], rating)
            )
        return boxes


    def get_add_location_boxes(self):
        boxes = []
        for place in self.data['results']:
            info_box = '<h6>{}</h6><p>{}</p>'.format(place['name'], place['vicinity'])
            if Location.query.filter_by(google_id=place['id']).first():
                info_box += '<p><button class=\'btn btn-danger\'onclick=\
                \'flagLocation(&quot;{}&quot;)\'>Flag Inaccurate</button></p>'.format(
                    place['id']
                )
            else:
                info_box += '<p><button class=\'btn btn-primary\'onclick=\
                    \'addLocation(this, &quot;{}&quot;, {}, {}, &quot;{}&quot;)\'>\
                    Add</button></p>'.format(
                        place['id'],
                        place['geometry']['location']['lat'],
                        place['geometry']['location']['lng'],
                        place['vicinity']
                    )
            boxes.append(info_box)
        return boxes
        


    # Constructs list of names from query
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
