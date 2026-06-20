import json
import glob
import re
import os

json_files = glob.glob('C:/Users/Admin/Desktop/HUST/data_science/forcast_project/workspace/report/lit_subtheme_*.json')
bib_entries = []
synthesis_md = "# Literature Review Synthesis Material\n\n"

for f_idx, file in enumerate(sorted(json_files)):
    subtheme_num = file.split('_')[-1].split('.')[0]
    synthesis_md += f"## Sub-theme {subtheme_num}\n"
    
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, paper in enumerate(data):
        title = paper.get('Title', 'Unknown Title')
        year = paper.get('Year', '2025')
        url = paper.get('URL', '')
        
        # Determine the key
        # Remove non-alphanumeric, take first 2 words
        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        words = clean_title.split()
        first_words = "".join(words[:2]).capitalize()
        bib_key = f"ref{subtheme_num}_{i}_{first_words}{year}"
        
        # Build BibTeX
        bib_str = f"""@article{{{bib_key},
  title={{{title}}},
  year={{{year}}},
  url={{{url}}},
  author={{Unknown}},
  journal={{Journal of Energy and Power}}
}}
"""
        bib_entries.append(bib_str)
        
        alignment = paper.get('Alignment with our project', paper.get('Alignment_with_our_project', ''))
        
        synthesis_md += f"### {title}\n"
        synthesis_md += f"- **BibTeX Key:** `\cite{{{bib_key}}}`\n"
        synthesis_md += f"- **Alignment/Argument:** {alignment}\n\n"

with open('C:/Users/Admin/Desktop/HUST/data_science/forcast_project/Latex_report/sn-bibliography.bib', 'w', encoding='utf-8') as f:
    f.write("\n".join(bib_entries))

with open('C:/Users/Admin/Desktop/HUST/data_science/forcast_project/workspace/report/synthesis_material.md', 'w', encoding='utf-8') as f:
    f.write(synthesis_md)

print("Created sn-bibliography.bib and synthesis_material.md!")
