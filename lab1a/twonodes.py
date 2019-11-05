from __future__ import print_function

import sys

sys.path.append('..')

from bene.network import Network
from bene.sim import Sim
from bene.packet import Packet

class DelayHandler(object):
    @staticmethod
    def receive_packet(packet, **kwargs):
        print((packet.ident,packet.created,
               packet.ident,
               Sim.scheduler.current_time(),
               packet.ident))
               #Sim.scheduler.current_time() - packet.created,
               #packet.transmission_delay,
               #packet.propagation_delay,
               #packet.queueing_delay))

def main():
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('./networks/fast-long.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(n2.get_address('n1'), n1.links[0])
    n2.add_forwarding_entry(n1.get_address('n2'), n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    print("********Scenario 1********")

    # send one packet
    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    Sim.scheduler.run()


    #TODO: Scenario2
    print("********Scenario 2********")

    # setup network
    net = Network('./networks/slow-short.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(n2.get_address('n1'), n1.links[0])
    n2.add_forwarding_entry(n1.get_address('n2'), n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)

    Sim.scheduler.reset()

    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    Sim.scheduler.run()

    #TODO: Scenario 3 -- use scheduler.add here (Usage: scheduler.add(delay,event,handler))
    print("********Scenario 3********")

    
    # setup network
    net = Network('./networks/fast-short.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(n2.get_address('n1'), n1.links[0])
    n2.add_forwarding_entry(n1.get_address('n2'), n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)
    Sim.scheduler.reset()

    p = Packet(destination_address=n2.get_address('n1'), ident=1, protocol='delay', length=1000)
    p2 = Packet(destination_address=n2.get_address('n1'), ident=2, protocol='delay', length=1000)
    p3 = Packet(destination_address=n2.get_address('n1'), ident=3, protocol='delay', length=1000)
    p4 = Packet(destination_address=n2.get_address('n1'), ident=4, protocol='delay', length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)
    Sim.scheduler.add(delay=0, event=p2, handler=n1.send_packet)
    Sim.scheduler.add(delay=0, event=p3, handler=n1.send_packet)
    Sim.scheduler.add(delay=2000, event=p4, handler=n1.send_packet)

    Sim.scheduler.run()

if __name__ == '__main__':
    main()

