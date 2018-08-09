import json

Settings = None
Installed = None

with open('settings/config.json', 'r') as file:
    Settings = json.load(file)

with open('settings/client_secret.json', 'r') as file:
    Installed = json.load(file)['installed']
