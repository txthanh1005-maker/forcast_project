import json

with open(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\selected_papers.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

for p in papers:
    text = (p["Title"] + " " + p["Abstract"]).lower()
    if p["Year"] >= 2015 and ("asymmetric loss" in text or "custom loss" in text or "target transformation" in text or "extreme value" in text or "peak load" in text):
        print(f"[{p['Year']}] {p['Title']} - Cites: {p['Citations']}")
        print(f"URL: {p['URL']}")
        # print excerpt mentioning keywords
        import re
        match = re.search(r"(.{0,50}(asymmetric loss|custom loss|target transformation|extreme value|peak load).{0,50})", text)
        if match:
            print(f"...{match.group(1)}...")
        print()
