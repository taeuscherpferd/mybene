#The transmission experiment is the following: Node A transmits a 10 MB (1 MB = 106 bytes) file, divided into 1 KB (1 KB = 1000 bytes) packets, to Node C. 

from __future__ import print_function

import sys

sys.path.append('..')

from bene.network import Network
from bene.sim import Sim
from bene.packet import Packet

class DelayHandler(object):
    @staticmethod
    def receive_packet(packet, **kwargs):
        timeReceived = Sim.scheduler.current_time()
        print((packet.ident,
               packet.created,
               packet.ident,
               timeReceived,
               packet.ident,
               timeReceived - packet.created,
               packet.ident,
               packet.transmission_delay,
               packet.ident,
               packet.propagation_delay,
               packet.ident,
               packet.queueing_delay,
               packet.ident))

               #Sim.scheduler.current_time() - packet.created,
               #packet.transmission_delay,
               #packet.propagation_delay,
               #packet.queueing_delay))

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

    print("********Scenario 1********")
    # Send packets (Transmission Delay = 1?)
    # Ask Prof how to find (s) or propogation speed for this problem.
    i = 1
    while i <= 1000:
      p = Packet(destination_address=n3.get_address('n2'), ident=i, protocol='delay', length=1000)
      Sim.scheduler.add(delay=(108) * (i - 1), event=p, handler=n1.send_packet)
      i += 1

    Sim.scheduler.run()

    #TODO: Scenario2
    print("********Scenario 2********")

    # setup network
    net = Network('./networks/faster-faster.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(n3.get_address('n2'), n1.links[0])
    n2.add_forwarding_entry(n3.get_address('n2'), n2.links[1])

    # setup app
    d = DelayHandler()
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)

    Sim.scheduler.reset()

    i = 1
    while i <= 1000:
      p = Packet(destination_address=n3.get_address('n2'), ident=i, protocol='delay', length=1000)
      Sim.scheduler.add(delay=(108) * (i - 1), event=p, handler=n1.send_packet)
      i += 1

    Sim.scheduler.run()

    #TODO: Scenario3 -- use scheduler.add here (Usage: scheduler.add(delay,event,handler))
    print("********Scenario 3********")
    
    # setup network
    net = Network('./networks/fast-slow.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n1.add_forwarding_entry(n3.get_address('n2'), n1.links[0])
    n2.add_forwarding_entry(n3.get_address('n2'), n2.links[1])

    # setup app
    d = DelayHandler()
    net.nodes['n3'].add_protocol(protocol="delay", handler=d)
    Sim.scheduler.reset()

    i = 1
    while i <= 1000:
      p = Packet(destination_address=n3.get_address('n2'), ident=i, protocol='delay', length=1000)
      Sim.scheduler.add(delay=(108) * (i - 1), event=p, handler=n1.send_packet)
      i += 1

    Sim.scheduler.run()

if __name__ == '__main__':
    main()
