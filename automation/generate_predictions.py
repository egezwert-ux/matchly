import json
import os
import requests
from datetime import datetime
from helpers import fetch_today_fixtures

JSON_PATH = "docs/predictions.json"
AI_KEY = os.getenv("GEMINI_KEY")  # GitHub secret

AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def ai_predict(home, away):
    if not AI_KEY:
        print("GEMINI_KEY missing, returning dummy prediction")
        return {
            "mainPick": "MS X",
            "odds": "2.5",
            "confidence": 50,
            "predictedScore": "1-1",
            "btts": "KG VAR",
            "corners": "8.5 ALT",
            "cards": "2+",
            "htFt": "0-0",
            "analysis": "Dummy prediction since AI key is missing"
        }
    prompt = f"Predict for {home} vs {away} in JSON with mainPick, odds, confidence, predictedScore, btts, corners, cards, htFt, analysis"
    payload = {"contents":[{"parts":[{"text": prompt}]}]}
    headers = {"Authorization": f"Bearer {AI_KEY}"}
    try:
        r = requests.post(AI_URL, json=payload, headers=headers)
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except Exception as ex:
        print("AI prediction error:", ex)
        return {
            "mainPick": "MS X",
            "odds": "2.5",
            "confidence": 50,
            "predictedScore": "1-1",
            "btts": "KG VAR",
            "corners": "8.5 ALT",
            "cards": "2+",
            "htFt": "0-0",
            "analysis": "AI error, dummy prediction"
        }

def generate_predictions():
    fixtures = fetch_today_fixtures()
    predictions = []
    for match in fixtures:
        pred = ai_predict(match["homeTeam"], match["awayTeam"])
        predictions.append({
            "id": match["id"],
            "date": match["date"],
            "league": match["league"],
            "homeTeam": match["homeTeam"],
            "awayTeam": match["awayTeam"],
            "prediction": pred,
            "analysis": pred.get("analysis", ""),
            "result": "pending",
            "vip": False,
            "adUnlock": True
        })
    os.makedirs("docs", exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"lastUpdated": str(datetime.utcnow()), "matches": predictions}, f, indent=4)

if __name__ == "__main__":
    generate_predictions()
