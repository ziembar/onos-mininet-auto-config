class connection_request:
    def __init__(self, id, source, destination, connection_type,bw,delay):
        self.id = id
        self.source = source
        self.destination = destination
        self.type = connection_type
        self.bw = bw
        self.delay = delay
    def __str__(self):
        return f"ConnectionRequest(id={self.id}, source={self.source}, destination={self.destination}, connection_type='{self.connection_type}')"
