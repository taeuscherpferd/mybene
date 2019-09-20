from __future__ import print_function

import os
import sys

sys.path.append('..')

from bene.sim import Sim

def hello_world(event):
    print('hello world', event, Sim.scheduler.current_time())

def main():
    Sim.scheduler.reset()
    Sim.scheduler.add(delay=1, event=4000, handler=hello_world)
    Sim.scheduler.run()

if __name__ == '__main__':
    main()
