import copy
import logging

from .node import Node

logger = logging.getLogger(__name__)

class Switch(Node):
    def __init__(self, hostname):
        self.hostname = hostname
        self.links = []
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

    def receive_packet(self, (packet, link)):
        pass
