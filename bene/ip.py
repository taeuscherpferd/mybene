import binascii
import socket

int_type_int = type(0xff)
int_type_long = type(0xffffffffffffffff)

class IPAddress(object):
    '''An IP address object.  The address instance var is an int.  If it is an
    IPv6 address, then its length is 128 bits; otherwise, it is an IPv4
    address, and its length is 32 bits.'''
    def __init__(self, address, family=None):
        if isinstance(address, (int_type_int, int_type_long)):
            assert family in (socket.AF_INET, socket.AF_INET), 'Address family must be specified'
            self.address_family = family
            if self.address_family == socket.AF_INET6:
                self.address_len = 128
            else:
                self.address_len = 32
            self.address = address
        else: # str
            if ':' in address:
                self.address_len = 128
                self.address_family = socket.AF_INET6
            else:
                self.address_len = 32
                self.address_family = socket.AF_INET
            self.address = self.__class__._str_to_int(address, self.address_family)

    @classmethod
    def _int_to_str(cls, address, family):
        if family == socket.AF_INET6:
            address_len = 128
        else:
            address_len = 32
        return socket.inet_ntop(family, binascii.unhexlify(('%x' % address).zfill(address_len >> 2)))

    @classmethod
    def _str_to_int(cls, address, family):
        return int_type_long(binascii.hexlify(socket.inet_pton(family, address)), 16)

    @classmethod
    def _all_ones(cls, n_bits):
        '''Return an int that is n_bits long and whose value is all ones.'''
        return int_type_long('ff' * (n_bits >> 3), 16)

    def __hash__(self):
        return hash(self.address)

    def __str__(self):
        return self.__class__._int_to_str(self.address, self.address_family)

    def __eq__(self, other):
        return self.address == other.address

    def __lt__(self, other):
        return self.address < other.address

    def __add__(self, other):
        assert isinstance(other, (int_type_int, int_type_long))
        return IPAddress(self.address + other, self.address_family)

    def __sub__(self, other):
        assert isinstance(other, (int_type_int, int_type_long))
        return IPAddress(self.address - other, self.address_family)

    def mask(self, prefix_len):
        '''Return the mask for the given prefix length, as an integer.'''
        #FIXME
        return 0

    def prefix(self, prefix_len):
        '''Return the prefix for the given prefix length, as an integer.  Note
        that address_len is also needed.'''
        #FIXME
        return 0

    def subnet(self, prefix_len):
        return Subnet(IPAddress(self.prefix(prefix_len), self.address_family), prefix_len)

class IPAddressFactory(object):
    def __init__(self, address='1.1.1.1', masklen=24):
        self.address = IPAddress(address)
        self.masklen = masklen
        self.max = self.address + 2**(32 - masklen) - 2
        self.advance()

    def next(self):
        return self.address

    def advance(self):
        self.address += 1
        if self.address > self.max:
            raise ValueError('Address outside of range!')

BROADCAST_IP_ADDRESS = IPAddress('255.255.255.255')

class Subnet(object):
    def __init__(self, prefix, prefix_len):
        self.prefix = prefix
        self.prefix_len = prefix_len
        self.mask = self.prefix.mask(self.prefix_len)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '%s/%d' % (self.prefix, self.prefix_len)

    def __contains__(self, ip):
        '''Return True if ip is in this subnet, False otherwise.'''
        #FIXME
        return ip == self.prefix

    def __hash__(self):
        return hash((self.prefix, self.prefix_len))

    def __eq__(self, other):
        return self.prefix == other.prefix and self.prefix_len == other.prefix_len
