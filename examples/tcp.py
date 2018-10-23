import logging

from bene.sim import Sim
from bene.tcp import TCP as TCPStub
from bene.tcp import logger, sender_logger, receiver_logger


class TCP(TCPStub):
    """ A TCP connection between two hosts."""

    def __init__(self, transport, source_address, source_port,
                 destination_address, destination_port, app=None, window=1000,drop=[]):
        super(TCP, self).__init__(transport, source_address, source_port,
                            destination_address, destination_port, app, window, drop)

    ''' Sender '''

    def send(self, data):
        #FIXME
        self.send_packet(data, self.sequence)
        self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)

    def handle_ack(self, packet):
        """ Handle an incoming ACK. """
        self.plot_sequence(packet.ack_number - packet.length,'ack')
        sender_logger.debug("%s (%s) received ACK from %s for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.ack_number))
        #FIXME
        self.cancel_timer()

    def retransmit(self, event):
        """ Retransmit data. """
        sender_logger.warning("%s (%s) retransmission timer fired" % (self.node.hostname, self.source_address))
        #FIXME

    ''' Receiver '''

    def handle_data(self, packet):
        """ Handle incoming data."""
        sender_logger.debug("%s (%s) received TCP segment from %s for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.sequence))
        #FIXME
        self.app.receive_data(packet.body)
        self.send_ack()
