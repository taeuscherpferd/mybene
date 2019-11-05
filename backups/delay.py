#The transmission experiment is the following: Node A transmits a 10 MB (1 MB = 106 bytes) file, divided into 1 KB (1 KB = 1000 bytes) packets, to Node C. 

from __future__ import print_function

import sys
import random

sys.path.append('..')

from bene.network import Network
from bene.sim import Sim
from bene.packet import Packet

class CoolerPacket(Packet):
    def __init__(self, valOfRho, **kwds):
        self.valOfRho = valOfRho
        super().__init__(**kwds)

class Generator(object):
     def __init__(self, node, destination, load, duration, rho):
         self.node = node
         self.load = load
         self.rho = rho
         self.destination = destination
         self.duration = duration
         self.start = 0
         self.ident = 1

     def handle(self, event):
         # quit if done
         now = Sim.scheduler.current_time()
         if (now - self.start) > self.duration:
             return

         # generate a packet
         self.ident += 1
         p = CoolerPacket(destination_address=self.destination, ident=self.ident, protocol='delay', length=1000, valOfRho=self.rho)
         Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)
         # schedule the next time we should generate a packet
         Sim.scheduler.add(delay=random.expovariate(self.load), event='generate', handler=self.handle)


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet, **kwargs):
        timeReceived = Sim.scheduler.current_time()

        csv = open("data/queue-" + str(packet.valOfRho) + ".csv", "a")
        csv.write(str(timeReceived) + "," + str(packet.queueing_delay) + "\n")
        csv.close()

def main():
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('./networks/fast-fast.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(n3.get_address('n2'), n1.links[0])
    n2.add_forwarding_entry(n3.get_address('n2'), n2.links[1])

    # setup app
    d = DelayHandler()
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)
    
    destination = n3.get_address('n2')
    mew = 1000000 // (1000*8)

    rho=0.1

    while rho <= 0.90:
        Sim.scheduler.reset()
        lambd = rho * mew

        csv = open("data/queue-" + str(rho) + ".csv", "a")
        csv.write("Queueing Delay,Utilization")
        csv.close()

        g = Generator(node=n1, destination=destination, load=lambd, duration=60, rho=rho)
        Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

        Sim.scheduler.run()

        rho = rho + .10

    Sim.scheduler.reset()

    rho = 0.95
    lambd = rho * mew

    g = Generator(node=n1, destination=destination, load=lambd, duration=60, rho=rho)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    Sim.scheduler.run()

    Sim.scheduler.reset()
    rho = 0.98
    lambd = rho * mew

    g = Generator(node=n1, destination=destination, load=lambd, duration=60, rho=rho)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)
        
    # Run the simulation
    Sim.scheduler.run()

if __name__ == '__main__':
    main()

