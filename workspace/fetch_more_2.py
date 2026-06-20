import urllib.request
import urllib.parse
import json

dois = [
    "10.1016/j.apenergy.2019.114368",
    "10.1016/j.ins.2020.08.053",
    "10.1016/j.neucom.2018.12.084"
]

results = []
for doi in dois:
    url = f'https://api.openalex.org/works/doi:{doi}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            work = json.loads(response.read().decode('utf-8'))
            results.append(work)
    except Exception as e:
        print("Error fetching", doi, e)

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
    
with open('raw_lit_4_extra_2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
