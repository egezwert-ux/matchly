import json
from helpers import fetch_today_results

JSON_PATH = "docs/predictions.json"

def update_results():
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    results = fetch_today_results()
    for m in data["matches"]:
        for r in results:
            if m["id"] == r["id"]:
                predicted_score = m["prediction"].get("predictedScore")
                m["result"] = "won" if r["score"] == predicted_score else "lost"

    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    update_results()
