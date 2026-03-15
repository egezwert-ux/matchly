import json
from datetime import datetime, timedelta
from helpers import fetch_today_results

JSON_PATH = "docs/predictions.json"


def update_results():

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    results = fetch_today_results()

    for match in data["matches"]:

        for r in results:

            if match["id"] == r["id"]:

                predicted = match["prediction"]["predictedScore"]
                actual = r["score"]

                if predicted == actual:
                    match["result"] = "won"
                else:
                    match["result"] = "lost"

    cleaned = []

    for m in data["matches"]:

        match_date = datetime.strptime(m["date"], "%Y-%m-%d")

        if datetime.utcnow() - match_date < timedelta(days=7):
            cleaned.append(m)

    data["matches"] = cleaned

    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    update_results()
