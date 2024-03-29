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
        super(TCP, self).__init__(transport, source_address, source_port,
                                  destination_address, destination_port, app, window, drop)

        self.fast_retransmit = fast_retransmit
        self.ack_count = 0
        self.prev_ack = 0
        self.ssthresh = 100000
        self.shouldSlowStart = True
        self.increment = 0

    ''' Sender '''

    def send(self, data):

        self.send_buffer.put(data)

        while self.send_buffer.available() > 0 and self.send_buffer.outstanding() < self.cwnd:
            bufData, seqNumber = self.send_buffer.get(self.mss)
            self.send_packet(bufData, seqNumber)

    def handle_ack(self, packet):
        """ Handle an incoming ACK. """
        self.plot_sequence(packet.ack_number - packet.length, 'ack')
        sender_logger.debug("%s (%s) received ACK from %s for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.ack_number))

        # ACKING
        # ----------------------------------------------------------------------------------------------------
        if self.sequence == packet.ack_number:
            self.ack_count += 1

        if self.sequence < packet.ack_number:
            self.ack_count = 0
            numBytesReceived = packet.ack_number - self.sequence
            self.sequence = packet.ack_number
            self.send_buffer.slide(self.sequence)
            self.cancel_timer()

            # SlowStart/CongestionAvoidance
            # ----------------------------------------------------------------------------------------------------
            if (self.shouldSlowStart):
                if (numBytesReceived <= 1000):
                    self.cwnd += numBytesReceived

                    if self.cwnd >= self.ssthresh:
                        self.shouldSlowStart = False
                else:
                    self.cwnd += 1000
                    if self.cwnd >= self.ssthresh:
                        self.shouldSlowStart = False
                self.plot_cwnd()
            else:
                self.increment += (1000 * numBytesReceived) / self.cwnd
                if self.increment >= 1000:
                    self.cwnd += 1000
                    self.plot_cwnd()
                    self.increment -= 1000

            while self.send_buffer.available() > 0 and self.send_buffer.outstanding() < self.cwnd:
                bufData, seqNumber = self.send_buffer.get(self.mss)
                self.send_packet(bufData, seqNumber)

            if self.timer is None and self.send_buffer.outstanding() > 0:
                self.timer = Sim.scheduler.add(
                    delay=self.timeout, event='retransmit', handler=self.retransmit)
            return

        # Triple ACK
        # ----------------------------------------------------------------------------------------------------
        if self.ack_count == 3 and self.sequence == packet.ack_number:
            print("triple ACK'd!!!")
            if self.send_buffer.outstanding() > 0:
                self.retransmit('fast-retransmit')

    def retransmit(self, event):
        """ Retransmit data. """
        sender_logger.warning("%s (%s) retransmission timer fired" % (
            self.node.hostname, self.source_address))

        dataToSend, seqNumber = self.send_buffer.resend(self.mss)

        if event == "retransmit":
            self.timer = None

        self.ssthresh = max(self.cwnd / 2, 1000)
        if self.ssthresh >= 1000:
            self.ssthresh -= self.ssthresh % 1000
        else:
            self.ssthresh += self.ssthresh % 1000

        self.increment = 0
        self.shouldSlowStart = True
        self.cwnd = 1000
        self.plot_cwnd()

        self.send_packet(dataToSend, seqNumber)

    ''' Receiver '''

    def handle_data(self, packet):
        """ Handle incoming data."""
        sender_logger.debug("%s (%s) received TCP segment from %s for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.sequence))

        self.receive_buffer.put(packet.body, packet.sequence)
        cleanOrderlyData, startSequenceNum = self.receive_buffer.get()

        self.app.receive_data(cleanOrderlyData, self.cwnd,
                              packet.queueing_delay)

        self.ack = startSequenceNum + len(cleanOrderlyData)

        self.send_ack()
