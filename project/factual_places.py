# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from factual import Factual
from factual.utils import circle
import project._config as c
from project.schema import Location


class Places(object):

    data = None


    def __init__(self, query, lat, lng, radius):
        factual = Factual(c.FACTUAL_KEY, c.FACTUAL_SECRET)
        places = factual.table('places')
        # Searches for all restaurants
        if query.lower() == 'restaurants':
            self.data = places.filters({'category_ids':{'$includes_any':[312,338]}}).geo(circle(lat, lng, radius)).limit(50).data()
        # Searches according to user's query
        else:
            self.data = places.search(query).geo(circle(lat, lng, radius)).limit(50).data()
            from pprint import pprint
            pprint(self.data)


    # Constructs list of coordinates from query
    def get_coords(self):
        coords = []
        marker = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        for place in self.data:
            coords.append(
                (place['latitude'], place['longitude'])
            )
        coords = {marker: coords}
        return coords


    # Constructs list of info boxes to be displayed above map markers
    def get_info_boxes(self):
        boxes = []
        for place in self.data:
            info_box = '<h6>{} {}</h6><p>{}{}</p>'
            address = ''
            open_status = ''
            if 'address' in place and 'postcode' in place and 'locality' in place:
                address = '<a target=\'_blank\' href=\'http://maps.google.com/?q={}, {}\'>{}, {}</a>'.\
                    format(place['address'], place['postcode'], place['address'], place['locality'])
            # rating = ''
            # if 'opening_hours' in place and 'open_now' in place['opening_hours']:
            #     if place['opening_hours']['open_now']:
            #         open_status = '<small class=\'text-success\'>Open</small>'
            #     else:
            #         open_status = '<small class=\'text-danger\'>Closed</small>'
            # if 'rating' in place:
            #     rating = '<br>Rating: {}'.format(self.generate_stars(place['rating']))
            open_status = ''
            rating = ''
            boxes.append(
                info_box.format(place['name'], open_status, address, rating)
            )
        return boxes


    def get_add_location_boxes(self):
        boxes = []
        for place in self.data:
            address = ''
            locality = ''
            if 'address' in place:
                address = place['address']
            if 'locality' in place:
                locality = place['locality']

            info_box = '<h6>{}</h6><p>{}, {}</p>'.format(place['name'], address, locality)
            if Location.query.filter_by(google_id=place['factual_id']).first():
                info_box += '<p><button class=\'btn btn-danger\'onclick=\
                \'flagLocation(&quot;{}&quot;)\'>Flag Inaccurate</button></p>'.format(
                    place['factual_id']
                )
            else:
                info_box += '<p><button class=\'btn btn-primary\'onclick=\
                    \'addLocation(this, &quot;{}&quot;, {}, {}, &quot;{}, {}&quot;)\'>\
                    Add</button></p>'.format(
                        place['factual_id'],
                        place['latitude'],
                        place['longitude'],
                        address,
                        locality
                    )
            boxes.append(info_box)
        return boxes
        


    # Constructs list of names from query
    def get_names(self):
        return [place['name'] for place in self.data]


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
