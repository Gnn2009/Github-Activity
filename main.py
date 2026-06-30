import sys
import urllib.request
import urllib.error
import json
import os, re
from collections import Counter

DATA =[]

if len(sys.argv) < 2:
    print("Please enter your user name")
    print("Use: python main.py <username>")
    sys.exit()

user = sys.argv[1]

url = f"https://api.github.com/users/{user}/events"
if not os.path.exists("events.json"):
    with open("events.json", "w", encoding="UTF-8") as file:
        json.dump({}, file, indent=4)
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as file:
    data = json.load(file)

for event in data:
    urlRepo = event.get("repo",{}).get("url")
    typeRepo = event.get("type")
    date = re.sub(r'\D',"",event.get("created_at"))
    DATA.append({"URL":[urlRepo, typeRepo, date]})