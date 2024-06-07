import json

import requests
from dotenv import dotenv_values

secrets = dotenv_values("../.env.secrets")

url = "https://simplicialsoftware.com/api/account/GetSkinIDs"

data = {
    "Game": "Nebulous",
    "Version": "1229",
    "Ticket": secrets.get("TICKET", ""),
    "Type": "ALL",
}

response = requests.post(url, data=data, timeout=10).json()
print(json.dumps(response, indent=2))
