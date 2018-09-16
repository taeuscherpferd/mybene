BROADCAST_MAC_ADDRESS = 'FF-FF-FF-FF'

class MacAddressFactory(object):
    def __init__(self, seed=None):
        if seed is None:
            seed = 0
        self.val = seed

    def advance(self):
        self.val += 1

    def __str__(self):
        return '%02x-%02x-%02x-%02x' % ((self.val >> 24) & 0xff, (self.val >> 16) & 0xff, (self.val >> 8) & 0xff, self.val & 0xff)

class ByteSimilarMacAddressFactory(MacAddressFactory):
    def __init__(self, seed=None):
        super(ByteSimilarMacAddressFactory, self).__init__(seed)
        for i in range(4):
            b = '%02x' % ((self.val >> (i << 3)) & 0xff)
            if b[0] != b[1]:
                raise ValueError('Invalid seed value for %s: 0x%x' % (self.__class__.__name__, self.val))

    def advance(self):
        self.val += 1 # 2^0
        if self.val & 0xff:
            self.val += 0x10 # 2^4
        else:
            if (self.val >> 8) & 0xff:
                self.val += 0x1000 # 2^12
            else:
                if (self.val >> 16) & 0xff:
                    self.val += 0x100000 # 2^20
                else:
                    self.val += 0x10000000 # 2^28
