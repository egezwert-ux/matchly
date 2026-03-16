import json

print("Updating results...")

with open("docs/predictions.json","r") as f:
    data = json.load(f)

for match in data["matches"]:
    if match["result"] == "pending":
        match["result"] = "pending"

with open("docs/predictions.json","w") as f:
    json.dump(data,f,indent=4)

print("Results checked")
