import json
import re

file_path = r"C:\Users\Admin\.gemini\antigravity-cli\brain\15f9dad6-f9cb-4df6-ab3b-d9be3d0c58c0\.system_generated\steps\30\content.md"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.split("---", 1)[1].strip()
data = json.loads(json_str)

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""
    words = []
    try:
        max_idx = max([max(positions) for positions in inverted_index.values()])
    except:
        return ""
    words = [""] * (max_idx + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words)

selected = []
for item in data.get("results", []):
    abstract = reconstruct_abstract(item.get("abstract_inverted_index", {}))
    # basic filtering:
    text = (item.get("display_name") or "") + " " + abstract
    text = text.lower()
    
    if "loss" in text or "extreme" in text or "peak" in text or "transformation" in text or "asymmetric" in text:
        selected.append({
            "Title": item.get("display_name"),
            "Year": item.get("publication_year"),
            "URL": item.get("doi") or item.get("id"),
            "Abstract": abstract
        })

with open(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\temp_parsed.json", "w", encoding="utf-8") as f:
    json.dump(selected[:20], f, indent=2, ensure_ascii=False)

print(f"Extracted {len(selected)} papers.")
