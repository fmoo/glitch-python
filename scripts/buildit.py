import shelve
import time

from config import ACCESS_TOKEN
from glitch import GlitchAPI


# In this example, we pickle all the street metadata to a shelve

class DBBuilder(object):
    def __init__(self, db):
        """
        Constructor takes a `db` that has __setattr__ assigned
        for eventual flushing of the data.
        """
        self.db = db
        super(DBBuilder, self).__init__()

    def set_api(self, api):
        """
        You must set an API in order to load data from the shelf
        """
        self.api = api
        return self

    @classmethod
    def for_shelve_filename(cls, filename):
        """
        Factory function to open `filename` as a shelve db.

        shelve is a python standard module for storing arbitrary
        python data structures on disk.
        """
        db = shelve.open(filename, writeback=True)
        return cls(db)

    def refresh_skills(self):
        api = self.api
        db = self.db

        print "Fetching one skill..."
        num_skills = api.skills_listAll(per_page=1)['total']
        while True:
            print "Fetching %d skills" % num_skills
            skills = api.skills_listAll(per_page=num_skills)
            # Uh, we *just* got more skills
            if skills['total'] != num_skills:
                num_skills = skills['total']
                continue

            k = 'skills.all'
            if k not in db:
                print "Adding skill cache to db"
                db[k] = skills
            elif db[k] != skills:
                print "Skills changed!"
                db[k] = skills
                # TODO- diff them
            else:
                print "No skill updates"
            break
        return self

    def refresh_achievements(self):
        api = self.api
        db = self.db

        print "Fetching one achievement..."
        num_achievements = api.achievements_listAll(per_page=1)['total']
        while True:
            print "Fetching %d achievements" % num_achievements
            achievements = api.achievements_listAll(per_page=num_achievements)
            # Uh, we *just* got more skills
            if achievements['total'] != num_achievements:
                num_achievements = achievements['total']
                continue

            k = 'achievements.all'
            if k not in db:
                print "Adding achievement cache to db"
                db[k] = achievements
            elif db[k] != achievements:
                print "Achievements changed!"
                db[k] = achievements
                # TODO- diff them
            else:
                print "No achievement updates"
            break
        return self

    def refresh_locations(self):
        """
        Walk the API, refreshing all the contents of the db.
        """
        api = self.api
        db = self.db

        print "Fetching hubs..."
        hubs = api.locations_getHubs()['hubs']
        if 'hubs' not in db:
            print "Adding hubs to db cache"
            db['hubs'] = hubs
        elif db['hubs'] != hubs:
            print "New hubs!"
            # XXX- Show the new hubs.  For now, idc
            db['hubs'] = hubs

        for hub_id, hub_details in hubs.iteritems():
            print "Fetching streets for", hub_details['name']

            k = str("hub_streets:%s" % (hub_id))
            streets = api.locations_getStreets(hub_id=hub_id)['streets']
            if k not in db:
                print "Adding hub_streets to db cache"
                db[k] = streets
            elif db[k] != streets:
                print "New streets for", hub_details['name'], "!!"
                db[k] = streets


            for street_tsid, street_short in streets.iteritems():
                street_tsid = str(street_tsid)

                street_data = api.locations_streetInfo(street_tsid=street_tsid)
                k = "street:%s" % (street_tsid)
                if k in db:
                    if db[k] != street_data:
                        db[k] = street_data
                        print "updated data for", street_data['name'].encode('latin-1')
                    else:
                        print "No updates for", street_tsid, street_data['name'].encode('latin-1')
                else:
                    db[k] = street_data
                    print "Added new data for", street_data['name'].encode('latin-1')

                # sleep in-between data fetches... we want to be nice API users
                time.sleep(1.0)
        return self


if __name__ == '__main__':
    api = GlitchAPI(ACCESS_TOKEN)
    DBBuilder.for_shelve_filename('foo.db') \
             .set_api(GlitchAPI(ACCESS_TOKEN)) \
             .refresh_skills() \
             .refresh_achievements() \
             .refresh_locations()

