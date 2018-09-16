import copy
import logging

from .ip import BROADCAST_IP_ADDRESS
from .sim import Sim

logger = logging.getLogger(__name__)


class Node(object):
    _allow_forward = True

    def __init__(self, hostname, default_gateway=None):
        self.hostname = hostname
        self.default_gateway = default_gateway
        self.links = []
        self.protocols = {}
        self.forwarding_table = {}

    # -- Links --

    def add_link(self, link):
        self.links.append(link)

    def delete_link(self, link):
        if link not in self.links:
            return
        self.links.remove(link)

    def get_link(self, name):
        for link in self.links:
            if link.endpoint.hostname == name:
                return link
        return None

    def get_address(self, name):
        for link in self.links:
            if link.endpoint.hostname == name:
                return link.address
        return 0

    # -- Protocols --

    def add_protocol(self, protocol, handler):
        self.protocols[protocol] = handler

    def delete_protocol(self, protocol):
        if protocol not in self.protocols:
            return
        del self.protocols[protocol]

    # -- Forwarding table --

    def add_forwarding_entry(self, address, link):
        self.forwarding_table[address] = link

    def delete_forwarding_entry(self, address):
        if address not in self.forwarding_table:
            return
        del self.forwarding_table[address]

    # -- Handling packets --

    def send_packet(self, packet):
        # if this is the first time we have seen this packet, set its
        # creation timestamp
        if packet.created is None:
            packet.created = Sim.scheduler.current_time()

        # forward the packet
        self.forward_packet(packet)

    def receive_packet(self, (packet, link)):
        # handle broadcast packets
        if packet.destination_address == BROADCAST_IP_ADDRESS:
            logger.debug("%s received packet" % self.hostname)
            self.deliver_packet(packet, link)
        else:
            # check if unicast packet is for me
            for link in self.links:
                if link.address == packet.destination_address:
                    logger.debug("%s received packet" % self.hostname)
                    self.deliver_packet(packet, link)
                    return

        if self._allow_forward:
            # decrement the TTL and drop if it has reached the last hop
            packet.ttl -= 1
            if packet.ttl <= 0:
                logger.debug("%s dropping packet due to TTL expired" % self.hostname)
                return

            # forward the packet
            self.forward_packet(packet)

    def deliver_packet(self, packet, link):
        if packet.protocol not in self.protocols:
            return
        self.protocols[packet.protocol].receive_packet(packet, link=link)

    def forward_packet(self, packet):
        if packet.destination_address == BROADCAST_IP_ADDRESS:
            # broadcast the packet
            self.forward_broadcast_packet(packet)
        else:
            # forward the packet
            self.forward_unicast_packet(packet)

    def get_link_for_address(self, address):
        if address in self.forwarding_table:
            return self.forwarding_table[address]
        return None

    def send_packet_on_link(self, packet, link, next_hop_address):
        link.send_packet(packet)

    def forward_unicast_packet(self, packet):
        link = self.get_link_for_address(packet.destination_address)
        if link is None:
            logger.debug("%s no routing entry for %s" % (self.hostname, packet.destination_address))
            return
        logger.debug("%s forwarding packet to %s" % (self.hostname, packet.destination_address))
        next_hop_address = link.endpoint.get_address(self.hostname)
        self.send_packet_on_link(packet, link, next_hop_address)

    def forward_broadcast_packet(self, packet):
        for link in self.links:
            logger.debug("%s forwarding broadcast packet to %s" % (self.hostname, link.endpoint.hostname))
            packet_copy = copy.deepcopy(packet)
            link.send_packet(packet_copy)

class Host(Node):
    _allow_forward = False
