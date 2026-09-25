#!/usr/bin/env python3
"""Script pour télécharger automatiquement les 16 photos du projet Sumba.
Chaque image est nommée selon le format : nom-le_code.jpg
"""

import time
import urllib.request
from pathlib import Path

# Dossier de destination : images/
OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

# Liste des 16 photos avec le format : nom-code.jpg
IMAGES = [
    {
        "filename": "rizieres-waikabubak-1683610959831-aa4190402a2b.jpg",
        "code": "1683610959831-aa4190402a2b",
        "url": "https://images.unsplash.com/photo-1683610959831-aa4190402a2b?w=1600&q=80&auto=format&fit=crop",
        "description": "Rizières et collines (Waikabubak, Praigoli)",
    },
    {
        "filename": "savane-collines-1601696411367-ee6556fe1251.jpg",
        "code": "1601696411367-ee6556fe1251",
        "url": "https://images.unsplash.com/photo-1601696411367-ee6556fe1251?w=1600&q=80&auto=format&fit=crop",
        "description": "Voyageur dans la savane (Tenau, Hiliwuku)",
    },
    {
        "filename": "plage-weekuri-1506047453301-d4df41ee32c3.jpg",
        "code": "1506047453301-d4df41ee32c3",
        "url": "https://images.unsplash.com/photo-1506047453301-d4df41ee32c3?w=1600&q=80&auto=format&fit=crop",
        "description": "Lagon et plage turquoise (Weekuri, Mandorak)",
    },
    {
        "filename": "mangrove-walakiri-1642510099706-df489bd6bd26.jpg",
        "code": "1642510099706-df489bd6bd26",
        "url": "https://images.unsplash.com/photo-1642510099706-df489bd6bd26?w=1600&q=80&auto=format&fit=crop",
        "description": "Mangrove et arbre sur la plage (Walakiri)",
    },
    {
        "filename": "falaises-marosi-1618479357286-1288df6ec815.jpg",
        "code": "1618479357286-1288df6ec815",
        "url": "https://images.unsplash.com/photo-1618479357286-1288df6ec815?w=1600&q=80&auto=format&fit=crop",
        "description": "Côtes sauvages et falaises (Marosi, Mbawana)",
    },
    {
        "filename": "canyon-tanggedu-1648873581098-3b37f8e10652.jpg",
        "code": "1648873581098-3b37f8e10652",
        "url": "https://images.unsplash.com/photo-1648873581098-3b37f8e10652?w=1600&q=80&auto=format&fit=crop",
        "description": "Canyon minéral et cascades (Tanggedu)",
    },
    {
        "filename": "cascade-waimarang-1602089413010-2f5c15d23aa8.jpg",
        "code": "1602089413010-2f5c15d23aa8",
        "url": "https://images.unsplash.com/photo-1602089413010-2f5c15d23aa8?w=1600&q=80&auto=format&fit=crop",
        "description": "Cascade et rivière encaissée (Waimarang, Koalat)",
    },
    {
        "filename": "piste-purukambera-1581090829934-64c631cefed5.jpg",
        "code": "1581090829934-64c631cefed5",
        "url": "https://images.unsplash.com/photo-1581090829934-64c631cefed5?w=1600&q=80&auto=format&fit=crop",
        "description": "Piste de terre dans la savane (Puru Kambera)",
    },
    {
        "filename": "cascade-lapopu-1561354543-64e3bf714587.jpg",
        "code": "1561354543-64e3bf714587",
        "url": "https://images.unsplash.com/photo-1561354543-64e3bf714587?w=1600&q=80&auto=format&fit=crop",
        "description": "Cascade en gradins dans la jungle (Lapopu)",
    },
    {
        "filename": "cascade-matayangu-1642510099705-206661e94bfd.jpg",
        "code": "1642510099705-206661e94bfd",
        "url": "https://images.unsplash.com/photo-1642510099705-206661e94bfd?w=1600&q=80&auto=format&fit=crop",
        "description": "Cascade haute (Matayangu, Lokomboro)",
    },
    {
        "filename": "village-praiyawang-1564986390370-0274b986df4a.jpg",
        "code": "1564986390370-0274b986df4a",
        "url": "https://images.unsplash.com/photo-1564986390370-0274b986df4a?w=1600&q=80&auto=format&fit=crop",
        "description": "Village traditionnel et toits hauts (Praiyawang)",
    },
    {
        "filename": "bateaux-pero-1683610960572-82722107237f.jpg",
        "code": "1683610960572-82722107237f",
        "url": "https://images.unsplash.com/photo-1683610960572-82722107237f?w=1600&q=80&auto=format&fit=crop",
        "description": "Bateaux de pêche côtiers et vagues (Pero)",
    },
    {
        "filename": "village-ratenggaro-1618479357329-14dd10e76f5e.jpg",
        "code": "1618479357329-14dd10e76f5e",
        "url": "https://images.unsplash.com/photo-1618479357329-14dd10e76f5e?w=1600&q=80&auto=format&fit=crop",
        "description": "Village mégalithique face à la mer (Ratenggaro)",
    },
    {
        "filename": "littoral-aerien-1683610959796-b5eda734af7d.jpg",
        "code": "1683610959796-b5eda734af7d",
        "url": "https://images.unsplash.com/photo-1683610959796-b5eda734af7d?w=1600&q=80&auto=format&fit=crop",
        "description": "Vue aérienne du littoral et de la savane",
    },
    {
        "filename": "chevaux-plage-1678150913309-cbebdf17d804.jpg",
        "code": "1678150913309-cbebdf17d804",
        "url": "https://images.unsplash.com/photo-1678150913309-cbebdf17d804?w=1600&q=80&auto=format&fit=crop",
        "description": "Chevaux sauvages galopant sur la plage",
    },
    {
        "filename": "mangrove-riviere-1581090824720-3c9f822192dd.jpg",
        "code": "1581090824720-3c9f822192dd",
        "url": "https://images.unsplash.com/photo-1581090824720-3c9f822192dd?w=1600&q=80&auto=format&fit=crop",
        "description": "Mangrove et embouchure de rivière (Sortie bateau)",
    },
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

print("=== Téléchargement des 16 images avec nom-code ===")
total = len(IMAGES)

for index, item in enumerate(IMAGES, 1):
    dest_path = OUTPUT_DIR / item["filename"]
    print(f"[{index:02d}/{total:02d}] {item['filename']}...", end=" ", flush=True)

    try:
        req = urllib.request.Request(item["url"], headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read()
            dest_path.write_bytes(content)
            size_kb = len(content) // 1024
            print(f"OK ({size_kb} Ko)")
    except Exception as e:
        print(f"ERREUR : {e}")

    time.sleep(0.3)

print(f"\n🎉 Terminé ! Les 16 fichiers sont dans '{OUTPUT_DIR.resolve()}'.")
