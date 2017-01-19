import asyncio

from autobahn.asyncio.websocket import WebSocketServerFactory
from config import config
from protocol import PyIrcProtocol

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    print("uvloop available, using uvloop event loop")
except ImportError:
    print("Uvloop unvailable, using default event loop")


class IrcFactory(WebSocketServerFactory):
    def __init__(self, name="server", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clients = []
        self.name = name

    async def sendAll(self, payload, isBinary=False):
        for i in self.clients:
            i.send(payload, isBinary)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    factory = IrcFactory(name=config["server_name"], loop=loop)
    factory.protocol = PyIrcProtocol

    coro = loop.create_server(factory, port=8081)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except:
        pass
    finally:
        server.close()
        loop.close()
