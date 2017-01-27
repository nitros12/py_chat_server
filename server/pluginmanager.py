from asyncio import iscoroutinefunction
from client import clientPerms

class pluginType:
    def __init__(self):
        self.plugins = {}

    def __call__(self, func):
        self.plugins[func.__name__] = func
        return func

    async def generate_func(self, client, funcstr):
        cmd, *args = funcstr.split()
        isafunc = await self.call_func(client, cmd, *args)
        if not isafunc:
            if client.channel is None:
                client.handle.simpleMessage(f"You are not connected to any channel, type '/join <channel>' to join a channel. A list of available channels is on /clist")
            else:
                client.channel.sendAllSimple(funcstr) #await client.handle.factory.sendAll_simple(funcstr)

    async def call_func(self, client, cmd, *args):
        if cmd.startswith("/"):
            plugin = self.plugins.get(cmd[1:])
            if plugin is not None:
                if iscoroutinefunction(plugin):
                    await plugin(client, *args)
                else:
                    plugin(client, *args)

                return True
        return False


def perms_for(perms):
    def predicate(func):
        def test(client, *args):
            client.handle.simpleMessage(client.perms)
            client.handle.simpleMessaeg(perms)
            if client.rankHigher(perms):
                func(client, *args)
            else:
                client.handle.simpleMessage(f"You do not have access to {func.__name__}")
        return test
    return predicate

plugins = pluginType()

# plugins can be both coros or normal functions

@plugins
async def ping(client, *args):
    await client.handle.factory.sendAll_simple("Pong")

@perms_for(clientPerms.kick)
@plugins
async def kick(client, *args):
    await client.handle.factory.kick(args[0])

@plugins
async def addperms(client, *args):

    permDict = {
            "send": clientPerms.send,
            "recv": clientPerms.recv,
            "kick": clientPerms.kick,
            "ban": clientPerms.ban,
            "admin": clientPerms.servmod
            }

    for i in args:
        if i in permDict:
            client.addPerm(permDict[i])

@plugins
async def ulist(client, *args):
    for c, i in enumerate(client.handle.factory.clients):
        client.handle.simpleMessage(f"Client #{c}, {i.name}, {id(i)}")

@plugins
async def join(client, *args):
    if args[0] in client.handle.factory.channels:
        client.handle.factory.set_channel(client, args[0])

@plugins
async def clist(client, *args):
    client.sendSimple(", ".join(client.handle.factory.channels))
