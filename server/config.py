"""Config manager

Available text format options:

peer: IP of client that generates message
numclients: count of clients online
server_name: name of server

"""

import json

config = json.load(open("config.json"))
