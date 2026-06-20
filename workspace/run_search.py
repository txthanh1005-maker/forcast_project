import subprocess
import json
import os
import sys

def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""
    words = []
    max_idx = max([max(positions) for positions in inverted_index.values()])
    words = [""] * (max_idx + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words)

def main():
    cli_path = r"C:\Users\Admin\.gemini\config\plugins\science\skills\literature_search_openalex\scripts\openalex_cli.py"
    
    cmd = [
        "uv", "run", cli_path, "filter", "works",
        "--search", "(\"load forecasting\" OR \"power system\") AND (\"extreme value\" OR \"peak load\" OR \"custom loss\" OR \"target transformation\" OR \"asymmetric loss\")",
        "--per-page", "30",
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=r"C:\Users\Admin\.gemini\config\plugins\science\skills\literature_search_openalex")
    
    if result.returncode != 0:
        print("Error running openalex cli:")
        print(result.stderr)
        return
        
    try:
        data = json.loads(result.stdout)
    except Exception as e:
        print("Failed to parse json output")
        print(result.stdout[:500])
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
        
    with open(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\temp_papers.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(papers)} papers to temp_papers.json")

if __name__ == "__main__":
    main()
