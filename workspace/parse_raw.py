import json

def reconstruct_abstract(inverted_index):
    if not inverted_index: return ""
    max_idx = max(max(positions) for positions in inverted_index.values())
    words = [""] * (max_idx + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words)

with open('raw_lit_4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = []
for work in data.get('results', []):
    title = work.get('title', '')
    year = work.get('publication_year', '')
    doi = work.get('doi', '')
    abstract = reconstruct_abstract(work.get('abstract_inverted_index', {}))
    location = work.get('primary_location', {})
    source = location.get('source', {}) if location else {}
    publisher = source.get('host_organization_name', '') if source else ''
    
    # Filter for IEEE or Elsevier/ScienceDirect
    if publisher and ('IEEE' in publisher or 'Elsevier' in publisher):
        results.append({
            'title': title,
            'year': year,
            'doi': doi,
            'publisher': publisher,
            'abstract': abstract[:1000] + '...' if len(abstract) > 1000 else abstract
        })

with open('parsed_lit_4.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print(f"Found {len(results)} matching papers.")
