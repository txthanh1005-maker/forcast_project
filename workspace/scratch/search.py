import subprocess
import sys

cmd = [
    "uv", "run", 
    r"C:\Users\Admin\.gemini\config\plugins\science\skills\literature_search_openalex\scripts\openalex_cli.py",
    "filter", "works",
    "--search", '("load forecasting" OR "demand forecasting") AND ("two-stage" OR "rule-based" OR "peak and valley")',
    "--sort", "cited_by_count:desc",
    "--per-page", "25"
]

with open("openalex_results.json", "w", encoding="utf-8") as f:
    subprocess.run(cmd, stdout=f, check=True)
