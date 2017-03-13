from asyncio import iscoroutinefunction
from functools import wraps

from client import clientPerms


class pluginType:

    PREFIX = "/"

    def __init__(self):
        self.plugins = {}

    def __call__(self, func):
        """Decorator, adds function to command list"""
        self.plugins[func.__name__] = func
        return func

    def formatted_commands(self):
        """
        Generate a list of commands
        """
        return (f"{k}: {j.__doc__}"for k, j in self.plugins.items())

    async def generate_func(self, client, funcstr):
        cmd, *args = funcstr.split()
        isafunc = await self.call_func(client, cmd, *args)
        if not isafunc:
            if client.channel is None:
                client.sendSimple(f"You are not connected to any channel, type '/join <channel>' to join a channel. A list of available channels is on /clist")
            else:
                # await client.handle.factory.sendAll_simple(funcstr)
                client.channel.sendAllSimple(funcstr)

    async def call_func(self, client, cmd, *args):
        if cmd.startswith(self.PREFIX):
            plugin = self.plugins.get(cmd.lstrip(self.PREFIX))
            if plugin is not None:
                if iscoroutinefunction(plugin):
                    await plugin(client, *args)
                else:
                    plugin(client, *args)
                return True
        return False


def perms_for(perms):
    """
    Decorator that verifies permissions for a command

    Client can run command if they have required permissions or higher

    example:
    @plugins
    @perms_for(clientPerms.kick)
    async def kick(client, userID, *_):
        await client.handle.factory.kick(userID)
    """
    def predicate(func):
        @wraps(func)
        def test(client, *args):
            if client.rankHigher(perms):
                func(client, *args)
            else:
                client.sendSimple(f"You do not have the permissions for: {func.__name__}. (your perms: {str(client.perms)}, required: {str(perms)})")
        return test
    return predicate

plugins = pluginType()

# plugins can be both coros or normal functions


@plugins
async def help(client, *_):
    """List commands"""
    for i in plugins.formatted_commands():
        client.sendSimple(i)


@plugins
async def login(client, *args):
    """Set user name TODO: AUTH"""
    client.name = args[0]
    # todo: password Auth?


@plugins
async def ping(client, *args):
    """pong"""
    await client.handle.factory.sendAll_simple("Pong")


@plugins
@perms_for(clientPerms.kick)
async def kick(client, userID, *_):
    """Kick a userid"""
    await client.handle.factory.kick(userID)


@plugins
async def addperms(client, *args):
    """Add perms to a self"""

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
    """Get a list of active users"""
    for c, i in enumerate(client.handle.factory.clients):
        client.sendSimple(f"Client #{c}, {i}, {id(i)}")


@plugins
async def join(client, *args):
    """Join a channel"""
    if args[0] in client.handle.factory.channels:
        client.handle.factory.setChannel(client, args[0])


@plugins
async def clist(client, *args):
    """List availiable channels"""
    client.sendSimple(", ".join(client.handle.factory.channels))
