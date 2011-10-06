import re


class Feature(object):
    """ Base class for other Models """
    pass


class Vendor(Feature):
    """ A vendor.  Has a `shop_type` attribute """
    def __init__(self, shop_type):
        self.shop_type = shop_type

    def __repr__(self):
        return "<vendor:%s>" % self.shop_type


class Shrine(Feature):
    """ A shrine.  Has a `giant` attribute. """
    def __init__(self, giant):
        self.giant = giant

    def __repr__(self):
        return "<shrine:%s>" % self.giant


class Resource(Feature):
    REPL = {
      "Trees": "Tree",
      "Rocks": "Rock",
      "Butterflies": "Butterfly",
      "Piggies": "Pig",
      "Plants": "Plant",
      "Chickens": "Chicken",
      "Growths": "Growth",
      "Barnacles": "Barnacle",
      "Batterflies": "Batterfly",
      "Piles": "Pile",
      "Bogs": "Bog",
    }

    """ A Resource.  Has an `amount` and a `name` attribute """
    def __init__(self, qty, name):
        self.amount = int(qty)

        # Clowncar alert!  Let's remove plurals from the names... by doing
        # dictionary lookups!  Hopefully at some point I can remove this
        # since the API has since improved.
        name = " ".join([self.REPL.get(t, t) for t in name.split(" ")])
        self.name = name

    def __repr__(self):
        return "<resource:%dx%s>" % (self.amount, self.name)


class FeaturesParser(object):
    """
    A helper class for parsing the "features" attribute of streetInfo
    calls.  Hopefully this will be unnecessary in the future
    """
    MATCHERS = [
      (re.compile('^An? <b>(.*?) Vendor</b>\.$'), Vendor),
      (re.compile('^A shrine dedicated to <b>(.+)</b>\.$'), Shrine),
    ]
    RESOURCE_MATCH = re.compile('<b>(\d+) (.*?)(?: for mining| plots)?</b>')

    def parse(self, s):
        """
        Parse a string, `s`, returning an array of Feature
        subclasses.
        """
        # Match the static jonx, like shrines, vendor
        for cre, cls in self.MATCHERS:
            m = cre.match(s)
            if m is not None:
                return [cls(*m.groups())]

        # Now try matching resources:
        res = []
        for item in self.RESOURCE_MATCH.findall(s):
            res.append(Resource(*item))
        return res

    def parse_all(self, arr):
        """
        Parse an `arr` of strings, returning an array of Feature
        subclasses.  Meant to be used with the "features" attribute of the
        street_info call
        """
        res = []
        for i in arr:
            res.extend(self.parse(i))
        return res
