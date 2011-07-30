import shelve
import time

from config import ACCESS_TOKEN
from glitch import GlitchAPI
from glitch import models


class Cache(object):
    def __init__(self, db):
        self.db = db

    @classmethod
    def for_shelve_filename(cls, filename):
        """
        Factory function to open `filename` as a shelve db.

        shelve is a python standard module for storing arbitrary
        python data structures on disk.
        """
        db = shelve.open(filename, writeback=True)
        return cls(db)

    @property
    def hubs(self):
        return self.db['hubs']

    def hub_streets(self, hub):
        return self.db[str('hub_streets:%s' % hub)]

    def street(self, street):
        return self.db[str('street:%s' % street)]


if __name__ == '__main__':
    cache = Cache.for_shelve_filename('foo.db')
    p = models.FeaturesParser()
    for h in cache.hubs:
        for street_id in cache.hub_streets(h):
            street = cache.street(street_id)
            features = street['features']
            print street_id, street['name'].encode('latin-1'), p.parse_all(features)
            #print street_id, street['name'].encode('latin-1'), features
