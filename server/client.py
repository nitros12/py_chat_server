import enum


class clientPerms(enum.IntFlag):
    send = 1 << 0
    recv = 1 << 1
    kick = 1 << 2
    ban = 1 << 3
    servmod = 1 << 4


DEFAULT_PERMS = clientPerms.send | clientPerms.recv


class client:

    def __init__(self, handle):
        self.handle = handle
        self.name = ""
        self.perms = clientPerms.send | clientPerms.recv  # default perms
        self.channel = None

    def setName(self, name):
        self.name = name

    def addPerm(self, perm):
        self.perms |= perm

    def removePerm(self, perm):
        self.perms &= ~perm

    def hasPerm(self, perm) -> bool:
        return perm in self.perms

    def rankHigher(self, other) -> bool:
        """Compares perms with another clients perms

        returns
        -------
            True  -> if own perms > other perms
            False -> otherwise
        """
        print(f"{self.perms} | {other}")

        if isinstance(other, client):
            return self.perms > other.perms

        elif isinstance(other, clientPerms):
            return self.perms > other

    def send(self, payload, isBinary):
        self.handle.sendMessage(payload, isBinary)

    def sendSimple(self, message):
        self.handle.simpleMessage(message)

    def setChannel(self, channel):
        self.channel = channel
