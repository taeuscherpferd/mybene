from .ip import Subnet

class ForwardingTable(object):
    def __init__(self):
        self.entries = {}

    def add_entry(self, subnet, link, next_hop):
        self.entries[subnet] = (link, next_hop)

    def remove_entry(self, subnet):
        if subnet in self.entries:
            del self.entries[subnet]

    def get_forwarding_entry(self, ip_address):
        #FIXME
        subnet = Subnet(ip_address, ip_address.address_len)
        if subnet in self.entries:
            return self.entries[subnet]
        else:
            return None, None
