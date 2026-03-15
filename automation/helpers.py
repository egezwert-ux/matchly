import requests
import datetime


def get_today_matches():

    today = datetime.date.today()

    url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{today}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    matches = []

    for event in data["events"]:

        match = {
            "id": event["id"],
            "league": event["tournament"]["name"],
            "home": event["homeTeam"]["name"],
            "away": event["awayTeam"]["name"],
            "time": event["startTimestamp"]
        }

        matches.append(match)

    return matches
