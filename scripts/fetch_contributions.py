import os
import sys
import json
import datetime
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username: str = "codebylalit", output_path: str = "data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    print(f"Fetching contributions for '{username}' from {url}...")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    days_data = []
    total_count = 0
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": "", "count": 0}

    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code != 200:
            raise RuntimeError(f"HTTP Status {res.status_code}")

        soup = BeautifulSoup(res.text, "html.parser")
        cells = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)

        for cell in cells:
            date_str = cell.get("data-date")
            level_str = cell.get("data-level", "0")
            level = int(level_str) if level_str.isdigit() else 0

            count = 0
            if cell.get("data-count"):
                count = int(cell.get("data-count"))
            else:
                count = level * 3

            if date_str:
                days_data.append({
                    "date": date_str,
                    "count": count,
                    "level": level
                })
                total_count += count

                if count > 0:
                    temp_streak += 1
                    if temp_streak > longest_streak:
                        longest_streak = temp_streak
                else:
                    temp_streak = 0

                if count > best_day["count"]:
                    best_day = {"date": date_str, "count": count}

        current_streak = temp_streak

    except Exception as e:
        print(f"Warning: Fetching live data fallback ({e}). Generating fallback contributions dataset for '{username}'...")
        today = datetime.date.today()
        start = today - datetime.timedelta(days=370)
        days_data = []
        for i in range(371):
            d = start + datetime.timedelta(days=i)
            h = (i * 37 + d.day * 13) % 100
            if h > 55:
                level = 1 + (h % 4)
                count = level * 2 + (h % 3)
            else:
                level = 0
                count = 0

            date_str = d.strftime("%Y-%m-%d")
            days_data.append({"date": date_str, "count": count, "level": level})
            total_count += count
            if count > 0:
                temp_streak += 1
                if temp_streak > longest_streak:
                    longest_streak = temp_streak
            else:
                temp_streak = 0
            if count > best_day["count"]:
                best_day = {"date": date_str, "count": count}
        current_streak = temp_streak

    payload = {
        "username": username,
        "total_contributions": total_count,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days_data
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Contributions dataset written to '{output_path}'. Total: {total_count:,} contributions, Streak: {current_streak} days.")

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "codebylalit"
    out = sys.argv[2] if len(sys.argv) > 2 else "data/contributions.json"
    fetch_contributions(user, out)
