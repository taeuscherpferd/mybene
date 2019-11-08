from __future__ import print_function

import logging
import optparse
import os
import subprocess
import sys

sys.path.append('..')

from bene.network import Network
from bene.sim import Sim, TERM_COLOR_GREEN
from bene.transport import Transport

from tcp import TCP

logger = logging.getLogger('app')
# uncomment the lines below to make app output green
#from bene.sim import TERM_COLOR_GREEN
#Sim.add_console_logging('app', TERM_COLOR_GREEN)

class AppHandler(object):
    def __init__(self, filename):
        self.filename = filename
        self.directory = 'received'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.f = open(os.path.join(self.directory, os.path.basename(self.filename)), 'wb')

    def receive_data(self, data, window_size, qd):
        logger.info("application got %d bytes" % (len(data)))
        self.f.write(data)
        self.f.flush()

    def packet_stats(self, packet):
        pass

class Main(object):
    def __init__(self):
        self.directory = 'received'
        self.window = None
        self.filename = None
        self.drop = None
        self.loss = None
        self.parse_options()
        self.run()
        self.diff()

    def parse_options(self):
        parser = optparse.OptionParser(usage="%prog [options]",
                                       version="%prog 0.1")

        parser.add_option("-f", "--filename", type="str", dest="filename",
                          default='./internet-architecture.pdf',
                          help="filename to send")

        parser.add_option("-s", "--drop", type="str", dest="drop",
                          default='',
                          help="Comma delimited list of packet numbers to drop")

        parser.add_option("-w", "--window", type="int", dest="window",
                          default=1000,
                          help="window size")

        parser.add_option("-r", action="store_true", dest="fastRetransmit", default=False, help="Toggles Fast Retransmit")

        parser.add_option("-l", "--loss", type="float", dest="loss",
                          default=0.0,
                          help="random loss rate")

        parser.add_option("-d", "--debug", dest="debug",
                          action="store_true", default=False,
                          help="debug logging")

        (options, args) = parser.parse_args()
        self.filename = options.filename
        self.drop = [int(x) for x in options.drop.split(',') if x.strip().isdigit()]
        print(self.drop)
        self.loss = options.loss
        self.window = options.window
        self.debug = options.debug
        self.fastRetransmit = options.fastRetransmit

    def diff(self):
        args = ['diff', '-u', self.filename, os.path.join(self.directory, os.path.basename(self.filename))]
        try:
            result = subprocess.check_call(args)
        except OSError as e:
            print("There was a problem running diff: %s" % e)
        except subprocess.CalledProcessError as e:
            print("File transfer failed.  %s" % e)
        else:
            print("File transfer correct!")

    def run(self):
        # parameters
        Sim.scheduler.reset()
        logging.getLogger('app').setLevel(logging.INFO)
        logging.getLogger('bene.link.queue').setLevel(logging.DEBUG)
        logging.getLogger('bene.tcp.sequence').setLevel(logging.DEBUG)
        logging.getLogger('bene.tcp.cwnd').setLevel(logging.DEBUG)
        if self.debug:
            logging.getLogger('bene.tcp').setLevel(logging.DEBUG)
            logging.getLogger('bene.tcp.sender').setLevel(logging.DEBUG)
            logging.getLogger('bene.tcp.receiver').setLevel(logging.DEBUG)

        # setup network
        net = Network('./networks/one-hop.txt')
        net.loss(self.loss)

        # setup routes
        n1 = net.get_node('n1')
        n2 = net.get_node('n2')
        n1.add_forwarding_entry(n2.get_address('n1'), n1.links[0])
        n2.add_forwarding_entry(n1.get_address('n2'), n2.links[0])

        # setup transport
        t1 = Transport(n1)
        t2 = Transport(n2)

        # setup application
        a = AppHandler(self.filename)

        # setup connection
        c1 = TCP(t1, n1.get_address('n2'), 1, n2.get_address('n1'), 1, self.fastRetransmit, a, window=self.window, drop=self.drop)
        c2 = TCP(t2, n2.get_address('n1'), 1, n1.get_address('n2'), 1, self.fastRetransmit, a, window=self.window)

        # send a file
        with open(self.filename, 'rb') as f:
            while True:
                data = f.read(1000)
                if not data:
                    break
                Sim.scheduler.add(delay=0, event=data, handler=c1.send)

        # run the simulation
        Sim.scheduler.run()


if __name__ == '__main__':
    m = Main()
