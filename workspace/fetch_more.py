import urllib.request
import urllib.parse
import json

queries = [
    '"load forecasting" "residual learning"',
    '"time series" "residual boosting"'
]

results = []
for q in queries:
    url = 'https://api.openalex.org/works?search=' + urllib.parse.quote(q) + '&select=id,title,publication_year,abstract_inverted_index,doi,primary_location&per-page=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            for work in data.get('results', []):
                location = work.get('primary_location', {})
                source = location.get('source', {}) if location else {}
                publisher = source.get('host_organization_name', '') if source else ''
                if publisher and ('IEEE' in publisher or 'Elsevier' in publisher):
                    results.append(work)
    except Exception as e:
        print("Error:", e)

def reconstruct_abstract(inverted_index):
    if not inverted_index: return ""
    max_idx = max(max(positions) for positions in inverted_index.values())
    words = [""] * (max_idx + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words)

for r in results:
    r['abstract'] = reconstruct_abstract(r.get('abstract_inverted_index', {}))
    
with open('raw_lit_4_extra.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
