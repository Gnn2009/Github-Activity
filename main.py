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

EVENT_TEMPLATES = {
    "PushEvent": ("Commits", "pushed to"),
    "CreateEvent": ("Branches/Tags/Repos", "created in"),
    "DeleteEvent": ("Branches/Tags", "deleted from"),
    "CommitCommentEvent": ("Comments", "added to commits in"),
    "PullRequestEvent": ("Pull Requests", "managed in"),
    "PullRequestReviewEvent": ("PR Reviews", "submitted in"),
    "PullRequestReviewCommentEvent": ("PR Review Comments", "written in"),
    "WatchEvent": ("Stars", "given to"),
    "ForkEvent": ("Forks", "created from"),
    "IssuesEvent": ("Issues", "updated in"),
    "IssueCommentEvent": ("Issue Comments", "posted in"),
    "ReleaseEvent": ("Releases", "published in"),
    "GollumEvent": ("Wiki Pages", "edited in"),
    "MemberEvent": ("Collaborators", "modified in"),
    "PublicEvent": ("Repository", "made open-source in")
}
DATA =[]

if len(sys.argv) <= 1:
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
    formatDate = setdate(eventype)
    noun, action = EVENT_TEMPLATES.get(eventype, ("Activities", "detected in"))
    print(f"- {amount} {noun} {CYAN}{action}{RESET} {CYAN}{split}{RESET} >--- {formatDate}")