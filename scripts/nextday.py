from glitch.datetime import GlitchDateTime
from glitch import datetime as gd
from datetime import timedelta


def main():
    d = GlitchDateTime()
    day_second = d.hour * gd.SECONDS_PER_HOUR + \
                 d.minute * gd.SECONDS_PER_MINUTE + \
                 d.second

    dt = timedelta(seconds=(gd.SECONDS_PER_DAY - day_second))
    print d.monthname, d.day, "will be over in", dt


if __name__ == '__main__':
    main()

