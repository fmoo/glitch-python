import time


MONTHS = [
    'Primuary',
    'Spork',
    'Bruise',
    'Candy',
    'Fever',
    'Junuary',
    'Septa',
    'Remember',
    'Doom',
    'Widdershins',
    'Eleventy',
    'Recurse',
]


DAYS_OF_WEEK = [
    'Hairday',
    'Moonday',
    'Twiday',
    'Weddingday',
    'Theday',
    'Fryday',
    'Standday',
    'Fabday',
]


MONTH_LENGTHS = [
  29, 3, 53, 17, 79, 19, 13, 37, 5, 47, 11, 1,
]


def dy_to_md(dy):
    for month, length in enumerate(MONTH_LENGTHS):
        if dy < length:
            return month, dy
        dy -= length
    return month, dy


EPOCH = 1238562000
SECONDS_PER_YEAR = 4435200
NON_RECURSE_DAYS_PER_YEAR = 307
SECONDS_PER_DAY = 14400
SECONDS_PER_HOUR = 600
SECONDS_PER_MINUTE = 10


def glitch_epoch(unixtime):
    return unixtime - EPOCH


class GlitchDateTime(object):
    def __init__(self, unixtime = None):
        unixtime = None or time.time()
        seconds = glitch_epoch(unixtime)

        self.year, seconds = divmod(seconds, SECONDS_PER_YEAR)
        day, seconds = divmod(seconds, SECONDS_PER_DAY)
        self.hour, seconds = divmod(seconds, SECONDS_PER_HOUR)

        self.minute, self.second = divmod(seconds, SECONDS_PER_MINUTE)

        self.weekday = \
          DAYS_OF_WEEK[int((day + (NON_RECURSE_DAYS_PER_YEAR * self.year)) % 8)]

        self.month, day = dy_to_md(day)
        self.day = day + 1

        self.hour = int(self.hour)
        self.minute = int(self.minute)
        self.second = int(self.second)
        self.year = int(self.year)

    @property
    def monthname(self):
        return MONTHS[self.month]

    def __repr__(self):
        return '<Year=%d,Month=%s,Day=%d,Hour=%d,Minute=%d,Second=%d>' % \
               (self.year, self.monthname, self.day, self.hour,
                self.minute, self.second)
