import sys
import urllib.request
import json
from datetime import datetime
from collections import Counter

def setdate(eventype):
    date = max(event["date"] for event in DATA if event["url"] == url and event["type"] == eventype)
    lastDate= datetime.fromisoformat(date).astimezone()
    formatDate = lastDate.strftime("%Y-%m-%d %H:%M")
    return formatDate

lightBlue = "\033[94m"
CYAN = "\033[36m"
GRIS = "\033[90m"
RESET = "\033[0m"

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
    date = event.get("created_at")
    item ={
        "url": urlRepo,
        "type": typeRepo,
        "date": date,
    }
    DATA.append(item)

combinaciones = [(event["url"], event["type"]) for event in DATA]
count = Counter(combinaciones)

for (url, eventype,), amount in count.items():
    split = url.split("/")[-1]
    if eventype == "PushEvent":
        formatDate = setdate(eventype)
        print(f"- {amount} Commits {CYAN}pushed{RESET} to {CYAN}{split}{RESET} >--- {formatDate}")
    elif eventype == "CreateEvent":
        formatDate = setdate(eventype)
        print(f"- {amount} Files {CYAN}created{RESET} in {CYAN}{split}{RESET} >--- {formatDate}")   