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
    queries = [
        "asymmetric loss",
        "custom loss",
        "extreme value",
        "peak load",
        "target transformation"
    ]
    
    papers = {}
    
    for q in queries:
        f1 = 'title_and_abstract.search:"load forecasting"|"power system"'
        f2 = f'title_and_abstract.search:"{q}"'
        filter_param = f"{f1},{f2}"
        encoded_filter = urllib.parse.quote(filter_param)
        
        url = f"https://api.openalex.org/works?filter={encoded_filter}&per-page=30&sort=cited_by_count:desc"
        headers = {"User-Agent": "mailto:test@example.com"}
        req = urllib.request.Request(url, headers=headers)
        
        print(f"Fetching for: {q}")
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                for item in data.get("results", []):
                    # check publisher
                    publisher = ""
                    try:
                        publisher = item["primary_location"]["source"]["host_organization_name"]
                    except:
                        pass
                    
                    publisher_lower = (publisher or "").lower()
                    if "ieee" not in publisher_lower and "institute of electrical" not in publisher_lower and "elsevier" not in publisher_lower:
                        continue
                        
                    pid = item.get("id")
                    if pid not in papers:
                        papers[pid] = {
                            "Title": item.get("display_name"),
                            "Year": item.get("publication_year"),
                            "URL": item.get("doi") or pid,
                            "Abstract": reconstruct_abstract(item.get("abstract_inverted_index", {})),
                            "Citations": item.get("cited_by_count", 0),
                            "Alignment with our project": ""
                        }
        except Exception as e:
            print(f"Error for {q}: {e}")

    # sort by citations
    results = sorted(list(papers.values()), key=lambda x: x["Citations"], reverse=True)
    
    with open(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\selected_papers.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print(f"Found {len(results)} matching papers.")
    for i, p in enumerate(results[:10]):
        print(f"[{i}] {p['Title']} ({p['Year']}) - {p['Citations']} citations")

if __name__ == "__main__":
    main()
