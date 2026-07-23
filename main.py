import sys, json, argparse
import urllib.request, urllib.error
from datetime import datetime
from collections import Counter
from pathlib import Path

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
file_direction = Path(__file__).resolve()

parse = argparse.ArgumentParser()
parse.add_argument("user", help="Your Github username")
parse. add_argument("-r",action="store_true", help="Show resumed information")
parse. add_argument("--type", choices=EVENT_TEMPLATES, help="Select an event type to show")
args = parse.parse_args()
if not args.user:
    print("Please enter your user name")
    print(f"Use: python {file_direction} <username>")
    sys.exit()
url = f"https://api.github.com/users/{args.user}/events?per_page=50"
req = urllib.request.Request(url, headers={"User-Agent": "Github-Activity-CLI"})
try:
    with urllib.request.urlopen(req) as file:
        data = json.load(file)
    for event in data:
        url_repo = event.get("repo").get("url")
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
        print(f"{RED}Error: User: '{args.user}' does't exist on githib.{RESET}")
    elif e.code == 403:
        print(f"{RED}Error: You have reach igthib api litmi request.{RESET}")
    else:
        print(f"{RED}Error HTTP: {e.code}{RESET}")
    exit()
if not DATA:
    print(f"No se encontraron eventos recientes para el usuario '{args.user}'.")
    exit()
if args.user:
    if args.type:
        if args.type in EVENT_TEMPLATES:
            combinations = [event["url"] for event in DATA if event["type"] == args.type]
            all_dates = [event["date"].split("T")[0] for event in DATA if event["type"] == args.type]
            max_contributions, most_days_contributions, formatted_dates, count = proceing_dates_and_contributions(all_dates, combinations)
            for url, amount in count.items():
                split_url = url.split("/")[-1]
                formatted_date = set_date(args.type,url, DATA)
                noun, action = EVENT_TEMPLATES.get(args.type, ("Activities", "detected in"))
                print(f">─ {amount} {noun} {CYAN}{action}{RESET} {CYAN}{split_url}{RESET} >--- {formatted_date}")
            print(f"<─> The day with {CYAN}most {args.type}'s {RESET}was {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contributions} contributions{RESET}" if len(most_days_contributions) <= 1 else f"<─> The days with {CYAN}most {args.type}'s {RESET}were {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contributions} contributions{RESET}")
        else:
            print(f"{RED}ERROR (non-existent event){RESET}\n{CYAN}POSIBLE EVENTS:{RESET}")
            for event in EVENT_TEMPLATES.keys():
                print(event)
    elif args.r == True:
        combinations = [event["type"] for event in DATA]
        count = Counter(combinations)
        print(f"┌{('─' * 45)}┐")
        for event, amount in count.items():
            print(f"  {event}: " + (amount // 10 * "<•>") + (amount % 10 * " ─") + f" <({amount})")
        print(f"└{('─' * 45)}┘")
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
else:
    print("Please enter your user name")
    print("Use: python main.py <username>")
    sys.exit()