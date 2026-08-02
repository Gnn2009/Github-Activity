import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from collections import Counter

# ==========================================
# 1. CONSTANTS AND GLOBAL CONFIGURATION
# ==========================================
RED = "\033[1;31m"
CYAN = "\033[36m"
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
# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def get_last_date(event_type, target_url, data):
    date = max(
        event["date"] for event in data 
        if event["url"] == target_url and event["type"] == event_type
    )
    actual_time = datetime.now().astimezone()
    last_date = actual_time - datetime.fromisoformat(date).astimezone()
    total_seconds = int(last_date.total_seconds())
    total_hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if total_hours <= 48:
        return total_hours, minutes, "hours_format"
    else:
        days = total_hours // 24
        hours = total_hours % 24
        return days, hours, "days_format"
def process_dates_and_contributions(all_dates, combinations):
    counted_dates = Counter(all_dates)
    
    max_contributions = counted_dates.most_common(1)[0][1]
    most_days_contributions = [date for date, amount in counted_dates.most_common() if amount == max_contributions]
    formatted_dates = " & ".join(most_days_contributions)
    count = Counter(combinations)
    return max_contributions, most_days_contributions, formatted_dates, count
def event_setup_and_printing(event_type, repo_name, amount, first_time, second_time, format):
    noun, action = EVENT_TEMPLATES.get(event_type, ("Activities", "detected in"))
    left_text = f"{amount} {noun} {action}"
    time_str = f"{first_time}h {second_time}min" if format == "hours_format" else f"{first_time}d {second_time}h"
    print(f"│ <•> {CYAN}{left_text:<40}{RESET}│ {CYAN}{repo_name:<35}{RESET}│ last: {time_str:<20}│")
def most_contributions_day_print(args, most_days, max_contribs, formatted_dates):
    plural_text = "were" if len(most_days) > 1 else "was"
    lines = "─" * 110
    print(f"│{CYAN}{lines}{RESET}│")
    event_str = f"{args.type}'s" if args.type else "contributions"
    plain_text = f" <•> The day(s) with {CYAN}most {event_str}{RESET} {plural_text} {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contribs} contributions{RESET}"
    print(f"│{plain_text:<137}│")
    print(f"╰{lines}╯")
def get_combination_and_dates(filter, args, user, data, args_value):
    phrase, conector = ("There is no public repository named ", " by ") if args_value == "repo" else ("No events of type ", " found for ")
    filtered_events = [e for e in data if e[filter].split("/")[-1] == args]
    if not filtered_events:
        print(f"{phrase}'{args}'{conector}{user}.")
        sys.exit(0)
    combinations = [(e["url"], e["type"]) for e in filtered_events]
    all_dates = [e["date"].split("T")[0] for e in filtered_events]
    return combinations, all_dates
def filtered_by_argument(all_dates, combinations, events_data, args):
        max_contribs, most_days, formatted_dates, count = process_dates_and_contributions(all_dates, combinations)
        print(f"╭{('─' * 110)}╮")
        #  Desempaquetamos (repo_url, event_type) porque es una tupla
        for (repo_url, event_type), amount in count.items():
            repo_name = f"{repo_url.split('/')[-2]}/{repo_url.split('/')[-1]}"
            first_time, second_time, format = get_last_date(event_type, repo_url, events_data)
            event_setup_and_printing(event_type, repo_name, amount, first_time, second_time, format)
        most_contributions_day_print(args, most_days, max_contribs, formatted_dates)
# ==========================================
# 3. CORE LOGIC
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Fetch and display GitHub user activity.")
    parser.add_argument("user", help="Your GitHub username")
    parser.add_argument("-p", "--pages", help="Quantity of pages to show (100 max!)")
    parser.add_argument("-r", "--resumed", action="store_true", help="Show summarized information")
    parser.add_argument("-t", "--type", choices=EVENT_TEMPLATES, help="Select an event type to show")
    parser.add_argument("-re", "--repo", help="Enter the repository name to fetch activity")
    args = parser.parse_args()
    try:
        per_page = int(args.pages) if args.pages else 100
        per_page = min(max(1, per_page), 100)
    except ValueError:
        print(f"{RED}Error: --pages debe ser un número entero.{RESET}")
        sys.exit(1)
    # Fetch GitHub API
    url = f"https://api.github.com/users/{args.user}/events?per_page={args.pages}"
    req = urllib.request.Request(url, headers={"User-Agent": "Github-Activity-CLI"})
    events_data = []
    try:
        with urllib.request.urlopen(req) as response:
            raw_data = json.load(response)
            for event in raw_data:
                events_data.append({
                    "url": event.get("repo", {}).get("url", ""),
                    "type": event.get("type"),
                    "date": event.get("created_at"),
                })
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"{RED}Error: User '{args.user}' doesn't exist on GitHub.{RESET}")
        elif e.code == 403:
            print(f"{RED}Error: You have reached the GitHub API rate limit.{RESET}")
        else:
            print(f"{RED}HTTP Error: {e.code}{RESET}")
        sys.exit(1)
    if not events_data:
        print(f"No recent events found for user '{args.user}'.")
        sys.exit(0)
    print(f"Your activity, welcome {CYAN}{args.user}{RESET}")
    # Mode 1: Filter by event type
    if args.type:
        combinations, all_dates = get_combination_and_dates("type", args.type, args.user, events_data, "type")
        filtered_by_argument(all_dates,combinations,events_data, args)
    # Mode 2: Filter by repository
    elif args.repo:
        #  Cambiado args.type por args.repo
        combinations, all_dates = get_combination_and_dates("url", args.repo, args.user, events_data, "repo")
        filtered_by_argument(all_dates,combinations,events_data, args)
    # Mode 3: Resumed (-r) view
    elif args.resumed:
        combinations = [e["type"] for e in events_data]
        count = Counter(combinations)
        print(f"╭{('─' * 45)}╮")
        for event, amount in count.items():
            bar = (amount // 10 * "<•>")+((amount // 10)//5 * "<>") + ((amount % 10) % 5 * " ─")
            plain_text = f"{CYAN}{event}{RESET}: {bar} <({amount})"
            print(f"│{plain_text:<54}│")
        print(f"╰{("─"*45)}╯")
    # Mode 4: Standard View
    else:
        combinations = [(e["url"], e["type"]) for e in events_data]
        all_dates = [e["date"].split("T")[0] for e in events_data]
        filtered_by_argument(all_dates,combinations,events_data, args)
if __name__ == "__main__":
    main()