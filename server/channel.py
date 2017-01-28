class Channel:

    def __init__(self, name):
        self.name = name
        self.members_ = set()

    def insert(self, client):
        if client.channel is not None:
            client.channel.remove(client)
        client.setChannel(self)
        self.members_.add(client)
        self.sendAllSimple(f"User <{client.name}> has joined {self.name}!")

    def remove(self, client):
        client.setChannel(None)
        self.members_.remove(client)
        self.sendAllSimple(f"User <{client.name}> has left {self.name}")

    @property
    def members(self):
        return list(self.members_)

    def sendAll(self, message, isBinary):
        for i in self.members_:
            i.send(message, isBinary)

    def sendAllSimple(self, message):
        for i in self.members_:
            i.sendSimple(message)
