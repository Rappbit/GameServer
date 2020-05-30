class Client(object):

    value = "test"
    def __init__(self, address):
        self.address = address

    def getAddress(self):
        return self.address
