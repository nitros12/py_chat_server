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

    def formatMsg(self, msg):
        return msg.format(peer=self.peer, numclients=len(self.factory.clients), server_name=self.factory.name)

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
        await self.factory.sendAll(json.dumps(self.formatMsg(config["welcome_message"])).encode("utf-8"))

    async def onClose(self, wasClean, code, reason):
        self.factory.clients.remove(self.client)
        await self.factory.sendAll(json.dumps().encode("utf-8"))

    async def onMessage(self, payload, isBinary):

        # TODO: message -> decode -> plugins

        await self.factory.sendAll(payload, isBinary)
