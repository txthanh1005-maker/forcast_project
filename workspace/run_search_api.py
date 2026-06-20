import urllib.request
import urllib.parse
import json

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

def main():
    # Attempt proper filtering
    f1 = "title_and_abstract.search:load forecasting"
    f2 = "title_and_abstract.search:asymmetric loss|custom loss|extreme value"
    filter_param = f"{f1},{f2}"
    encoded_filter = urllib.parse.quote(filter_param)
    
    url = f"https://api.openalex.org/works?filter={encoded_filter}&per-page=50&sort=cited_by_count:desc"
    
    headers = {
        "User-Agent": "mailto:test@example.com"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching from OpenAlex API: {e}")
        return

    papers = []
    for item in data.get("results", []):
        abstract = reconstruct_abstract(item.get("abstract_inverted_index", {}))
        papers.append({
            "id": item.get("id"),
            "title": item.get("display_name"),
            "year": item.get("publication_year"),
            "doi": item.get("doi"),
            "citations": item.get("cited_by_count"),
            "abstract": abstract
        })
        
    for i, p in enumerate(papers):
        print(f"[{i}] {p['title']} ({p['year']}) - Citations: {p['citations']}")
        print(f"URL: {p['doi'] or p['id']}")
        
    with open(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\temp_papers.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(papers)} papers to temp_papers.json")

if __name__ == "__main__":
    main()
