from typing import Iterable
from django.core.management import os
import requests

class YelpHandler:
    @staticmethod
    def make_headers():
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {os.environ.get('YELP_API_KEY')}",
        }

    @staticmethod
    def search(params):
        url = "https://api.yelp.com/v3/businesses/search"
        headers = YelpHandler.make_headers()
        response = requests.get(url, headers=headers, params=params)
        print(response)
        return response.json()

    class QueryBuilder:
        def __init__(self):
            self.params = {
                "limit": 20,
            }

        def location(self, location):
            self.params["location"] = location
            return self

        def latitude(self, latitude):
            self.params["latitude"] = latitude
            return self

        def longitude(self, longitude):
            self.params["longitude"] = longitude
            return self

        def radius(self, radius):
            self.params["radius"] = radius
            return self

        def attributes(self, attributes: Iterable[str]):
            self.params["attributes"] = ",".join(attributes)
            return self

        def categories(self, categories: Iterable[str]):
            self.params["categories"] = ",".join(categories)
            return self

        def limit(self, limit):
            self.params["limit"] = limit
            return self

        def build(self):
            """Needs to have either loc or lat+lon"""
            hasLoc = "location" in self.params
            hasLatLon = "latitude" in self.params and "longitude" in self.params

            if not (hasLoc or hasLatLon):
                raise Exception("Needs to have either loc or lat+lon")
            
            return self.params

