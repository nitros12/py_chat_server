from asyncio import iscoroutinefunction


class pluginType:
    def __init__(self):
        self.plugins = {}

    def __call__(self, func):
        self.plugins[func.__name__] = func
        return func

    async def call_func(self, server, cmd, *args):
        plugin = self.plugins.get(cmd)
        if plugin is not None:
            if iscoroutinefunction(plugin):
                await plugin(*args, server=server)
            else:
                plugin(*args, server=server)


plugins = pluginType()

# plugins can be both coros or normal functions


@plugins
async def ping(server, *args):
    await server.send
