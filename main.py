import sys
from typing import ItemsView
import urllib.request
import json
from datetime import datetime
from collections import Counter

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

combinaciones = [(event["url"], event["type"], event["date"]) for event in DATA]
count = Counter(combinaciones)

for (url, eventype, date), amount in count.items():
    dateData = datetime.fromisoformat(date)
    finalDate = (f"{dateData.day}/{dateData.month}/{dateData.year} :: {dateData.hour}:{dateData.minute:02d}")
    split = url.split("/")[-1]
    if eventype == "PushEvent":
        print(f"- {amount} Commits {CYAN}pushed{RESET} to {CYAN}{split}{RESET}>---{finalDate}")
    elif eventype == "CreateEvent":
        print(f"- {amount} Files {CYAN}created{RESET} in {CYAN}{split}{GRIS} >--- {RESET}{finalDate}")   