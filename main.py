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
# ==========================================
# 3. CORE LOGIC
# ==========================================
def main():
    print()
    parser = argparse.ArgumentParser(description="Fetch and display GitHub user activity.")
    parser.add_argument("user", help="Your GitHub username")
    parser.add_argument("-r", action="store_true", help="Show summarized information")
    parser.add_argument("--type", "-type", choices=EVENT_TEMPLATES, help="Select an event type to show")
    args = parser.parse_args()
    # Fetch GitHub API
    url = f"https://api.github.com/users/{args.user}/events?per_page=100"
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
        filtered_events = [e for e in events_data if e["type"] == args.type]
        if not filtered_events:
            print(f"No events of type '{args.type}' found for {args.user}.")
            return
            
        combinations = [e["url"] for e in filtered_events]
        all_dates = [e["date"].split("T")[0] for e in filtered_events]
        max_contribs, most_days, formatted_dates, count = process_dates_and_contributions(all_dates, combinations)
        print(f"┌{('─' * 100)}┐")
        for repo_url, amount in count.items():
            repo_name = repo_url.split("/")[-1]
            hours, minutes, format = get_last_date(args.type, repo_url, events_data)
            noun, action = EVENT_TEMPLATES.get(args.type, ("Activities", "detected in"))
            left_text = f"{amount} {noun} {action}"
            time_str = f"{hours}h {minutes}min" if format == "hours_format" else f"{hours}d {minutes}h"
            print(f"│ <•> {CYAN}{left_text:<40}{RESET}│ {CYAN}{repo_name:<25}{RESET}│ last: {time_str:<20}│")
        plural_text = "were" if len(most_days) > 1 else "was"
        print(f"│{CYAN}{"─"*100}{RESET}│")
        plain_text = f" <•> The day(s) with {CYAN}most {args.type}'s{RESET} {plural_text}{CYAN} {formatted_dates}{RESET} with{CYAN} {max_contribs} contributions{RESET}"
        print(f"│{plain_text:<127}│")
        print(f"└{('─' * 100)}┘")
    # Mode 2: Resumed (-r) view
    elif args.r:
        combinations = [e["type"] for e in events_data]
        count = Counter(combinations)
        print(f"┌{('─' * 45)}┐")
        for event, amount in count.items():
            bar = (amount // 10 * "<•>") + (amount % 10 * " ─")
            plain_text = f"{CYAN}{event}{RESET}: {bar} <({amount})"
            print(f"│{plain_text:<54}│")
        print(f"└{('─' * 45)}┘")
    # Mode 3: Standard View
    else:
        combinations = [(e["url"], e["type"]) for e in events_data]
        all_dates = [e["date"].split("T")[0] for e in events_data]
        max_contribs, most_days, formatted_dates, count = process_dates_and_contributions(all_dates, combinations)
        print(f"┌{('─' * 100)}┐")
        for (repo_url, event_type), amount in count.items():
            repo_name = repo_url.split("/")[-1]
            hours, minutes, format = get_last_date(event_type, repo_url, events_data)
            noun, action = EVENT_TEMPLATES.get(event_type, ("Activities", "detected in"))
            left_text = f"{amount} {noun} {action}"
            time_str = f"{hours}h {minutes}min" if format == "hours_format" else f"{hours}d {minutes}h"
            print(f"│ <•> {CYAN}{left_text:<40}{RESET}│ {CYAN}{repo_name:<25}{RESET}│ last: {time_str:<20}│")
        plural_text = "were" if len(most_days) > 1 else "was"
        print(f"│{CYAN}{"─"*100}{RESET}│")
        plain_text = f" <•> The day(s) with {CYAN}most contributions{RESET} {plural_text} {CYAN}{formatted_dates}{RESET} with {CYAN}{max_contribs} contributions{RESET}"
        print(f"│{plain_text:<127}│")
        print(f"└{('─' * 100)}┘")
if __name__ == "__main__":
    main()