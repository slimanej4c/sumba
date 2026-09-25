#!/usr/bin/env python3
"""Script pour remplacer automatiquement les 240 liens Unsplash
par les chemins locaux 'images/nom-le_code.webp' dans toutes les pages HTML.
"""

import glob
import re
from pathlib import Path

# Table de correspondance exacte (Code Unsplash -> Fichier local nom-code.webp)
MAPPING = {
    "1683610959831-aa4190402a2b": "images/rizieres-waikabubak-1683610959831-aa4190402a2b.webp",
    "1601696411367-ee6556fe1251": "images/savane-collines-1601696411367-ee6556fe1251.webp",
    "1506047453301-d4df41ee32c3": "images/plage-weekuri-1506047453301-d4df41ee32c3.webp",
    "1642510099706-df489bd6bd26": "images/mangrove-walakiri-1642510099706-df489bd6bd26.webp",
    "1618479357286-1288df6ec815": "images/falaises-marosi-1618479357286-1288df6ec815.webp",
    "1648873581098-3b37f8e10652": "images/canyon-tanggedu-1648873581098-3b37f8e10652.webp",
    "1602089413010-2f5c15d23aa8": "images/cascade-waimarang-1602089413010-2f5c15d23aa8.webp",
    "1581090829934-64c631cefed5": "images/piste-purukambera-1581090829934-64c631cefed5.webp",
    "1561354543-64e3bf714587": "images/cascade-lapopu-1561354543-64e3bf714587.webp",
    "1642510099705-206661e94bfd": "images/cascade-matayangu-1642510099705-206661e94bfd.webp",
    "1564986390370-0274b986df4a": "images/village-praiyawang-1564986390370-0274b986df4a.webp",
    "1683610960572-82722107237f": "images/bateaux-pero-1683610960572-82722107237f.webp",
    "1618479357329-14dd10e76f5e": "images/village-ratenggaro-1618479357329-14dd10e76f5e.webp",
    "1683610959796-b5eda734af7d": "images/littoral-aerien-1683610959796-b5eda734af7d.webp",
    "1678150913309-cbebdf17d804": "images/chevaux-plage-1678150913309-cbebdf17d804.webp",
    "1581090824720-3c9f822192dd": "images/mangrove-riviere-1581090824720-3c9f822192dd.webp",
}

# Regex pour capturer l'URL Unsplash et extraire le code photo
PATTERN = re.compile(r'https://images\.unsplash\.com/photo-([a-zA-Z0-9_-]+)[^\"\'\s>]*')

html_files = sorted(Path(".").glob("*.html"))
total_replaced = 0
files_modified = 0

print(f"=== Début du remplacement des liens dans {len(html_files)} fichiers HTML ===")

for filepath in html_files:
    content = filepath.read_text(encoding="utf-8")
    
    def replacer(match):
        code = match.group(1)
        return MAPPING.get(code, match.group(0))

    new_content, count = PATTERN.subn(replacer, content)
    
    if count > 0:
        filepath.write_text(new_content, encoding="utf-8")
        total_replaced += count
        files_modified += 1
        print(f"  {filepath.name} : {count} lien(s) remplacé(s)")

print(f"\n🎉 Succès ! {total_replaced} liens d'images ont été remplacés par les fichiers .webp dans {files_modified} fichiers HTML.")
print("Vous pouvez vérifier les changements avec : git diff")
