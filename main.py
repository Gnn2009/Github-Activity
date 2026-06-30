import sys
from typing import ItemsView
import urllib.request
import json
import re
from collections import Counter

DATA =[]

if len(sys.argv) < 2:
    print("Please enter your user name")
    print("Use: python main.py <username>")
    sys.exit()

user = sys.argv[1]

url = f"https://api.github.com/users/{user}/events"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as file:
    data = json.load(file)

for event in data:
    urlRepo = event.get("repo",{}).get("url")
    typeRepo = event.get("type")
    date = re.sub(r'\D',"",event.get("created_at"))
    item ={
        "url": urlRepo,
        "type": typeRepo,
        "date": date,
    }
    DATA.append(item)

combinaciones = [(event["url"], event["type"]) for event in DATA]
count = Counter(combinaciones)

for (url, eventype), amount in count.items():
    split = url.split("/")[-1]
    if eventype == "PushEvent":
        print(f"- {amount} Commits pushed to {split}")
    elif eventype == "CreateEvent":
        print(f"- {amount} Files created in {split}")