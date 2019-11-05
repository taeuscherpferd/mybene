from __future__ import print_function

import sys

sys.path.append('..')

from bene.network import Network
from bene.sim import Sim
from bene.packet import Packet

import random

rho = 0.1

class Generator(object):
    def __init__(self, node, destination, lambd, duration):
        self.node = node
        self.lambd = lambd
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
        p = Packet(destination_address=self.destination, ident=self.ident, protocol='delay', length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)
        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=random.expovariate(self.lambd), event='generate', handler=self.handle)


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet, **kwargs):
        global rho

        timeReceived = Sim.scheduler.current_time()
        print(rho)

        csv = open("data/queue-" + str(rho) + ".csv", "a")
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

    # setup packet generator
    destination = n3.get_address('n2')
    mew = 1000000 // (1000*8)
    global rho

#--------------------------------------------------------------------------------

    rho=0.1
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.2
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.3
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.4
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.5
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.6
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.7
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.8
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.9
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.95
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("TimeReceived,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

    rho=0.98
    load = rho * mew

    csv = open("data/queue-" + str(rho) + ".csv", "a")
    csv.write("Utilization,QD\n")
    csv.close()

    g = Generator(node=n1, destination=destination, lambd=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

    Sim.scheduler.reset()

#--------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

