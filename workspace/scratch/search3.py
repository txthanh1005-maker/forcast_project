import urllib.request
import urllib.parse
import json

base_url = "https://api.openalex.org/works"
query_str = '("load forecasting" OR "demand forecasting") AND ("two-stage" OR "two stage" OR "rule-based" OR "rule based" OR "peak and valley")'
params = {
    "filter": f"title_and_abstract.search:{query_str}",
    "per-page": "100",
    "select": "id,display_name,publication_year,primary_location,abstract_inverted_index,doi"
}
url = base_url + "?" + urllib.parse.urlencode(params)
print("Requesting URL:", url)
req = urllib.request.Request(url, headers={"User-Agent": "mailto:antigravity@google.com"})
try:
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        with open("openalex_results.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("Success, results saved to openalex_results.json")
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
