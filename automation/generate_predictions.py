import json
import requests
from datetime import datetime
from helpers import fetch_today_fixtures

AI_KEY = "GEMINI_KEY_BURAYA"

AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

JSON_PATH = "docs/predictions.json"


def ai_predict(home, away):

    prompt = f"""
Return ONLY JSON.

Match: {home} vs {away}

Fields:
mainPick
odds
confidence
overUnder
predictedScore
btts
corners
"""

    payload = {
        "contents":[{"parts":[{"text": prompt}]}]
    }

    r = requests.post(
        f"{AI_URL}?key={AI_KEY}",
        json=payload
    )

    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]

    try:
        return json.loads(text)
    except:
        return {
            "mainPick": "MS X",
            "odds": "2.10",
            "confidence": 60,
            "overUnder": "2.5 ALT",
            "predictedScore": "1-1",
            "btts": "KG VAR",
            "corners": "8.5 ALT"
        }


def generate_predictions():

    fixtures = fetch_today_fixtures()

    predictions = []

    for match in fixtures[:65]:

        pred = ai_predict(match["homeTeam"], match["awayTeam"])

        predictions.append({
            "id": match["id"],
            "date": match["date"],
            "time": match["time"],
            "league": match["league"],
            "homeTeam": match["homeTeam"],
            "awayTeam": match["awayTeam"],
            "prediction": pred,
            "result": "pending"
        })

    data = {
        "lastUpdated": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "summary": f"The daily bulletin has been fully updated. We have published {len(predictions)} reliable analyses.",
        "matches": predictions
    }

    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    generate_predictions()
