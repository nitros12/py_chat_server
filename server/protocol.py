"""
Web protocol for handling clients
"""
import asyncio
import json

import pluginmanager
from autobahn.asyncio.websocket import WebSocketServerProtocol
from client import client
from config import config


class PyIrcProtocol(WebSocketServerProtocol):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugins = pluginmanager.plugins
        self.client = client(self)

    def simpleMessage(self, message):
        print(message)
        self.sendMessage(json.dumps(message).encode("utf-8"), False)

    async def onConnect(self, request):
        print(f"opened connection from {request.peer}")
        self.factory.clients.append(self.client)  # yeyee

    async def onOpen(self):
        print(f"Client {self} opened")
        await self.factory.sendAllSimple("Client: {peer} connected to {server_name}! There are currently {numclients} users connected".format(peer=self.peer, numclients=len(self.factory.clients), server_name=self.factory.name))

    async def onClose(self, wasClean, code, reason):
        self.factory.clients.remove(self.client)
        await self.factory.sendAllSimple(f"<Client: {self.client.name} disconnected from server>")

    async def onMessage(self, payload, isBinary):
        await self.plugins.generate_func(self.client, payload.decode("utf-8"))
