import json

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""
    word_index = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_index.append((pos, word))
    word_index.sort()
    return " ".join(word for pos, word in word_index)

with open("openalex_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

results = data.get("results", [])
filtered_papers = []

target_publishers = ['ieee', 'elsevier', 'science direct', 'sciencedirect', 'institute of electrical and electronics engineers']

for paper in results:
    loc = paper.get('primary_location') or {}
    source = loc.get('source') or {}
    publisher = (source.get('host_organization_name') or "").lower()
    
    is_target = any(tp in publisher for tp in target_publishers)
    source_name = (source.get('display_name') or "").lower()
    if 'ieee' in source_name or 'elsevier' in source_name:
        is_target = True
        
    # We also accept if not strictly matching because sometimes publisher is missing. 
    # But let's log them to see.
    abstract = reconstruct_abstract(paper.get('abstract_inverted_index'))
    title = paper.get('display_name', '')
    year = paper.get('publication_year', '')
    url = paper.get('doi') or (loc.get('landing_page_url') if loc else '')
    
    filtered_papers.append({
        "Title": title,
        "Year": year,
        "Abstract": abstract,
        "URL": url,
        "Publisher": publisher,
        "Source": source_name,
        "Is_Target": is_target
    })

with open("filtered_papers.json", "w", encoding="utf-8") as f:
    json.dump(filtered_papers, f, indent=2)

print(f"Total papers: {len(results)}")
print(f"Target publishers papers: {sum(1 for p in filtered_papers if p['Is_Target'])}")
