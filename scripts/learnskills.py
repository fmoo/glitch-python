import glitch

from config import *

class CharAPI(glitch.GlitchAPI):
    @property
    def learning_something(self):
        return len(self.skills_listLearning().content['learning'])

    @property
    def learning(self):
        return self.skills_listLearning().content['learning']

    @property
    def learn_time_left(self):
        pass

    def learn(self, skill_name):
        return self.skills_learn(skill_id=skill_name)


char = CharAPI(ACCESS_TOKEN)


import random
import time

while True:
    while char.learning_something:
        print "you are already learning something"
        remaining_time = 0xffffffff
        for name, skill in char.learning.iteritems():
            skill_time = skill['time_complete'] - time.time()
            print "will finish", name, "in", skill_time, "seconds"
            remaining_time = min(remaining_time, skill_time)

        time.sleep(remaining_time)

    print "you are not learning anything!"
    print "fetching learnable skills:"
    can_learn = char.skills_listAvailable().content['skills']

    if len(can_learn) > 0:
        picked = random.choice(can_learn.keys())
        print "learning", picked, "..."
        print char.learn(picked).content
    else:
        print "... no more skills to learn!  Play the game some more!"
        break

