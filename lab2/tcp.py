from bene.tcp import logger, sender_logger, receiver_logger
from bene.tcp import TCP as TCPStub
from bene.sim import Sim
import logging
import sys

sys.path.append('..')


class TCP(TCPStub):
    """ A TCP connection between two hosts."""

    def __init__(self, transport, source_address, source_port,
                 destination_address, destination_port, fast_retransmit, app=None, window=1000, drop=[]):

        self.fast_retransmit = fast_retransmit
        self.ack_count = 0
        self.prev_ack = 0
        self.window = window

        super(TCP, self).__init__(transport, source_address, source_port,
                                  destination_address, destination_port, app, window, drop)

    ''' Sender '''

    def send(self, data):

        self.send_buffer.put(data)

        while self.send_buffer.available() > 0 and self.send_buffer.outstanding() + self.mss <= self.cwnd:
            bufData, seqNumber = self.send_buffer.get(self.mss)
            self.send_packet(bufData, seqNumber)


    def handle_ack(self, packet):
        """ Handle an incoming ACK. """
        self.plot_sequence(packet.ack_number - packet.length, 'ack')
        sender_logger.debug("%s (%s) received ACK from %s for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.ack_number))
        
        # print("AckNumber: " + str(packet.ack_number))
        
        if self.sequence == packet.ack_number:
            self.ack_count += 1
            # print("ackcount: " + str(self.ack_count))

        if self.sequence < packet.ack_number:
            self.ack_count = 0

            self.sequence = packet.ack_number
            self.send_buffer.slide(self.sequence)
            self.cancel_timer()

            while self.send_buffer.available() > 0 and self.send_buffer.outstanding() + self.mss <= self.cwnd:
                bufData, seqNumber = self.send_buffer.get(self.mss)
                self.send_packet(bufData, seqNumber)
                
            if self.timer is None:
                self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)
            return

        if not self.fast_retransmit:
            return

        if self.ack_count == 3 and self.sequence == packet.ack_number:
            # print("triple ACK'd!!!")
            self.retransmit('retransmit')
                
            if self.timer is None:
                self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)


    def retransmit(self, event):
        """ Retransmit data. """
        sender_logger.warning("%s (%s) retransmission timer fired" % (
            self.node.hostname, self.source_address))

        dataToSend, seqNumber = self.send_buffer.resend(self.mss)
        self.timer = None
        if (len(dataToSend) > 0):
          self.send_packet(dataToSend, seqNumber)

    ''' Receiver '''

    def handle_data(self, packet):
        """ Handle incoming data."""
        sender_logger.debug("%s (%s) received TCP segment from %s for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.sequence))

        self.receive_buffer.put(packet.body, packet.sequence)
        cleanOrderlyData, startSequenceNum = self.receive_buffer.get()

        self.app.receive_data(cleanOrderlyData, self.window, packet.queueing_delay)

        if self.ack < startSequenceNum:
            self.ack = startSequenceNum

        self.send_ack()
