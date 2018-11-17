import copy
import logging

from bene.node import Node

logger = logging.getLogger('bene.node')

class DVRouter(Node):
    def __init__(self, hostname, default_gateway=None):
        super(DVRouter, self).__init__(hostname, default_gateway)

        # add custom initialization here
