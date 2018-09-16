class IPAddress(object):
    def __init__(self, address):
        self.address = address

    def __str__(self):
        return '%d.%d.%d.%d' % ((self.address >> 24) & 0xff, (self.address >> 16) & 0xff, (self.address >> 8) & 0xff, self.address & 0xff)

    def __eq__(self, other):
        return self.address == other.address

    def __lt__(self, other):
        return self.address < other.address

class IPAddressFactory(object):
    def __init__(self, address=0x01010100, mask=24):
        self.address = address
        self.mask = mask
        self.max = self.address + 2**(32 - mask) - 2
        self.advance()

    def next(self):
        return IPAddress(self.address)

    def advance(self):
        self.address += 1
        if self.address > self.max:
            raise ValueError('Address outside of range!')

BROADCAST_IP_ADDRESS = IPAddress(0xffffffff)
