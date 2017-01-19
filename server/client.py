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
        return self.perms > other.perms

    def __eq__(self, other):
        if isinstance(other, client):
            return self.handle == other.handle
        elif isinstance(other, self.handle):  # comparing with a handler
            return self.handle == other

    def send(self, payload, isBinary):
        self.handle.sendMessage(payload, isBinary)
