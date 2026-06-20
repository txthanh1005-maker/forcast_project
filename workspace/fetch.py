import urllib.request
import urllib.parse
import json

url = 'https://api.openalex.org/works?search=' + urllib.parse.quote('("time series" OR "load forecasting") AND ("residual learning" OR "error correction" OR "residual boosting")') + '&select=id,title,publication_year,abstract_inverted_index,doi,primary_location&per-page=50'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        with open('raw_lit_4.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Success")
except Exception as e:
    print("Error:", e)
