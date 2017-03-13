import enum


class clientPerms(enum.IntFlag):
    recv = enum.auto()
    send = enum.auto()
    kick = enum.auto()
    ban = enum.auto()
    servmod = enum.auto()


DEFAULT_PERMS = clientPerms.send | clientPerms.recv


class client:

    def __init__(self, handle):
        self.handle = handle
        self.name = ""
        self.perms = clientPerms.send | clientPerms.recv  # default perms
        self.channel = None

    @property
    def prefix(self):
        """
        Get prefix for client
        """
        highest_perm = self.highest_perm

        return {
            clientPerms.servmod: "+++",
            clientPerms.ban: "++",
            clientPerms.kick: "-",
            clientPerms.send: "@"
        }[highest_perm]

    @property
    def highest_perm(self):
        """
        Extract highest permission from the group of permissions
        """
        for i in reversed(self.perms.__class__):
            if i in self.perms:
                return i

    def __str__(self):
        return f"{self.prefix}{self.name}"

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
