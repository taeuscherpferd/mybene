from __future__ import print_function

import logging
import sys

sys.path.append('..')

from bene.ip import IPAddress, Subnet
from bene.link import Link
from bene.node import Node, Host
from bene.packet import Packet
from bene.sim import Sim
from bene.switch import Switch

class ARPApp(object):
    def __init__(self, node):
        self.node = node

    def receive_packet(self, packet, link=None):
        self.node.handle_arp(link, packet)

def lan():
    # parameters
    Sim.scheduler.reset()

    h1 = Host('h1')
    h1.add_protocol('arp', ARPApp(h1))
    h2 = Host('h2')
    h2.add_protocol('arp', ARPApp(h2))

    h1.add_link(Link(mac_address='AA-AA-AA-AA', address=IPAddress('1.1.1.2'), prefix_len=28, startpoint=h1, endpoint=h2))
    h2.add_link(Link(mac_address='BB-BB-BB-BB', address=IPAddress('1.1.1.5'), prefix_len=28, startpoint=h2, endpoint=h1))

    # send packet from h1 to h2
    p = Packet(destination_address=h2.get_address('h1'), length=100)
    Sim.scheduler.add(1.1, event=p, handler=h1.send_packet)
    p = Packet(destination_address=h1.get_address('h2'), length=100)
    Sim.scheduler.add(1.2, event=p, handler=h2.send_packet)

    # run the simulation
    Sim.scheduler.run()

def lan_switch():
    # parameters
    Sim.scheduler.reset()

    h1 = Host('h1')
    h1.add_protocol('arp', ARPApp(h1))
    h2 = Host('h2')
    h2.add_protocol('arp', ARPApp(h2))

    s1 = Switch('s1')

    h1.add_link(Link(mac_address='AA-AA-AA-AA', address=IPAddress('1.1.1.2'), prefix_len=28, startpoint=h1, endpoint=s1))
    s1.add_link(Link(startpoint=s1, endpoint=h1))
    h2.add_link(Link(mac_address='BB-BB-BB-BB', address=IPAddress('1.1.1.5'), prefix_len=28, startpoint=h2, endpoint=s1))
    s1.add_link(Link(startpoint=s1, endpoint=h2))

    p = Packet(destination_address=h2.get_address('s1'), length=100)
    Sim.scheduler.add(1.1, event=p, handler=h1.send_packet)
    p = Packet(destination_address=h2.get_address('s1'), length=100)
    Sim.scheduler.add(1.2, event=p, handler=h1.send_packet)
    p = Packet(destination_address=h1.get_address('s1'), length=100)
    Sim.scheduler.add(2.1, event=p, handler=h2.send_packet)
    p = Packet(destination_address=h1.get_address('s1'), length=100)
    Sim.scheduler.add(2.2, event=p, handler=h2.send_packet)

    # run the simulation
    Sim.scheduler.run()

def router():
    # parameters
    Sim.scheduler.reset()

    h1 = Host('h1', default_gateway=IPAddress('1.1.1.1'))
    h1.add_protocol('arp', ARPApp(h1))
    h2 = Host('h2', default_gateway=IPAddress('1.1.1.1'))
    h2.add_protocol('arp', ARPApp(h2))
    h3 = Host('h3', default_gateway=IPAddress('2.2.2.1'))
    h3.add_protocol('arp', ARPApp(h3))
    h4 = Host('h4', default_gateway=IPAddress('2.2.2.1'))
    h4.add_protocol('arp', ARPApp(h4))

    s1 = Switch('s1')
    s2 = Switch('s2')

    n1 = Node('n1')
    n1.add_protocol('arp', ARPApp(n1))
    n2 = Node('n2')
    n2.add_protocol('arp', ARPApp(n2))

    h1.add_link(Link(mac_address='AA-AA-AA-AA', address=IPAddress('1.1.1.2'), prefix_len=28, startpoint=h1, endpoint=s1))
    s1.add_link(Link(startpoint=s1, endpoint=h1))
    h2.add_link(Link(mac_address='BB-BB-BB-BB', address=IPAddress('1.1.1.5'), prefix_len=28, startpoint=h2, endpoint=s1))
    s1.add_link(Link(startpoint=s1, endpoint=h2))
    n1.add_link(Link(mac_address='CC-CC-CC-CC', address=IPAddress('1.1.1.1'), prefix_len=28, startpoint=n1, endpoint=s1))
    s1.add_link(Link(startpoint=s1, endpoint=n1))

    h3.add_link(Link(mac_address='DD-DD-DD-DD', address=IPAddress('2.2.2.2'), prefix_len=28, startpoint=h3, endpoint=s2))
    s2.add_link(Link(startpoint=s2, endpoint=h3))
    h4.add_link(Link(mac_address='EE-EE-EE-EE', address=IPAddress('2.2.2.5'), prefix_len=28, startpoint=h4, endpoint=s2))
    s2.add_link(Link(startpoint=s2, endpoint=h4))
    n2.add_link(Link(mac_address='00-00-00-00', address=IPAddress('2.2.2.1'), prefix_len=28, startpoint=n2, endpoint=s2))
    s2.add_link(Link(startpoint=s2, endpoint=n2))

    n1.add_link(Link(mac_address='11-11-11-11', address=IPAddress('3.3.3.1'), prefix_len=30, startpoint=n1, endpoint=n2))
    n2.add_link(Link(mac_address='22-22-22-22', address=IPAddress('3.3.3.2'), prefix_len=30, startpoint=n2, endpoint=n1))

    n1.add_forwarding_entry(Subnet(IPAddress('2.2.2.0'), 28), n1.get_link('n2'), IPAddress('3.3.3.2'))
    n2.add_forwarding_entry(Subnet(IPAddress('1.1.1.0'), 28), n2.get_link('n1'), IPAddress('3.3.3.1'))

    p = Packet(destination_address=h2.get_address('s1'), length=100)
    Sim.scheduler.add(1.1, event=p, handler=h1.send_packet)
    p = Packet(destination_address=h3.get_address('s2'), length=100)
    Sim.scheduler.add(1.2, event=p, handler=h1.send_packet)

    # run the simulation
    Sim.scheduler.run()

def usage():
    sys.stderr.write('''Usage: %s [ -d ] <topology>
            
Available experiments:
  lan - send packets between nodes in a lan
  switch - send packets across a switch
  router - send packets through a router
''' % sys.argv[0])

def main():
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd')
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    opts = dict(opts)
    if '-d' in opts:
        logging.getLogger('bene.node').setLevel(logging.DEBUG)
        logging.getLogger('bene.host').setLevel(logging.DEBUG)
        logging.getLogger('bene.switch').setLevel(logging.DEBUG)
    else:
        logging.getLogger('bene.node').setLevel(logging.INFO)
        logging.getLogger('bene.host').setLevel(logging.INFO)
        logging.getLogger('bene.switch').setLevel(logging.INFO)

    if len(args) < 1 or args[0] not in ('lan', 'switch', 'router'):
        usage()
        sys.exit(1)

    if args[0] == 'lan':
        lan()
    elif args[0] == 'switch':
        lan_switch()
    elif args[0] == 'router':
        router()
    else:
        sys.stderr.write('No such experiment!')

if __name__ == '__main__':
    main()
