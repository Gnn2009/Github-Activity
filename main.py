import sys, json
import urllib.request, urllib.error
from datetime import datetime
from collections import Counter

def separator(symbol):
    print(symbol * 50)

def set_date(event_type, targey_url, data):
    date = max(
        event["date"] for event in data 
        if event["url"] == targey_url and event["type"] == event_type
    )
    last_date = datetime.fromisoformat(date).astimezone()
    formatted_date = last_date.strftime("%Y-%m-%d %H:%M")
    return formatted_date

def print_dashboard(message):
    separator("=")
    print(message.upper())
    separator("=")

def proceing_dates_and_contributions(all_dates, combinations):
    counted_dates = Counter(all_dates)
    max_contributions = counted_dates.most_common(1)[0][1]
    most_days_contributions = [date for date, amount in counted_dates.most_common() if amount == max_contributions]
    formatted_dates = ", ".join(most_days_contributions)
    count = Counter(combinations)
    return max_contributions, most_days_contributions, formatted_dates, count


RED = "\033[1;31m"
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
DATA = []

if len(sys.argv) <= 1:
    print("Please enter your user name")
    print("Use: python main.py <username>")
    sys.exit()
user = sys.argv[1]
url = f"https://api.github.com/users/{user}/events"
req = urllib.request.Request(url, headers={"User-Agents": "Github-Activity-CLI"})
try:
    with urllib.request.urlopen(req) as file:
        data = json.load(file)
    for event in data:
        url_repo = event.get("repo", {}).get("url")
        type_repo = event.get("type")
        date = event.get("created_at")
        item = {
            "url": url_repo,
            "type": type_repo,
            "date": date,
        }
        DATA.append(item)
except urllib.error.HTTPError as e:
    if e.code == 404:
        print(f"{RED}Error: User: '{user}' does't exist on githib.{RESET}")
    elif e.code == 403:
        print(f"{RED}Error: You have reach igthib api litmi request.{RESET}")
    else:
        print(f"{RED}Error HTTP: {e.code}{RESET}")
    exit()
if len(sys.argv) == 4:
    if sys.argv[2] == "--type":
        if sys.argv[3] in EVENT_TEMPLATES:
            combinations = [event["url"] for event in DATA if event["type"] == sys.argv[3]]
            all_dates = [event["date"].split("T")[0] for event in DATA if event["type"] == sys.argv[3]]
            max_contributions, most_days_contributions, formatted_dates, count = proceing_dates_and_contributions(all_dates, combinations)
            for url, amount in count.items():
                split_url = url.split("/")[-1]
                formatted_date = set_date(sys.argv[3],url, DATA)
                noun, action = EVENT_TEMPLATES.get(sys.argv[3], ("Activities", "detected in"))
                print(f">─ {amount} {noun} {CYAN}{action}{RESET} {CYAN}{split_url}{RESET} >--- {formatted_date}")
            print(f"<─> The day with {CYAN}most {sys.argv[3]}'s {RESET}was {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contributions} contributions{RESET}" if len(most_days_contributions) <= 1 else f"<─> The days with {CYAN}most {sys.argv[3]}'s {RESET}were {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contributions} contributions{RESET}")
        else:
            print(f"{RED}ERROR (non-existent event){RESET}\n{CYAN}POSIBLE EVENTS:{RESET}")
            for event in EVENT_TEMPLATES.keys():
                print(event)
    elif sys.argv[2] == "-r":
        print_dashboard("RESUME DASHBOARD")
        combinations = [event["type"] for event in DATA]
        count = Counter(combinations)
        print(f"┌{('─' * 45)}┐")
        for event, amount in count.items():
            print(f"  {event}: " + (amount // 10 * "<•>") + (amount % 10 * " ─") + f" <({amount})")
        print(f"└{('─' * 45)}┘")
    else:
        print(f"{RED}ERROR (non-existent command){RESET}")
        exit()
else:
    combinations = [(event["url"], event["type"]) for event in DATA]
    all_dates = [event["date"].split("T")[0] for event in DATA]
    max_contributions, most_days_contributions, formatted_dates, count = proceing_dates_and_contributions(all_dates, combinations)
    for (url, event_type), amount in count.items():
        split_url = url.split("/")[-1]
        formatted_date = set_date(event_type,url, DATA)
        noun, action = EVENT_TEMPLATES.get(event_type, ("Activities", "detected in"))
        print(f">─ {amount} {noun} {CYAN}{action}{RESET} {CYAN}{split_url}{RESET} >--- {formatted_date}")
    print(f"<─> The day with {CYAN}most contributions {RESET}was {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contributions} contributions{RESET}" if len(most_days_contributions) <= 1 else f"<─> The days with {CYAN}most contributions {RESET}were {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contributions} contributions{RESET}")