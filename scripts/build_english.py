#!/usr/bin/env python3
"""Generate the static English mirror of the French Sumba website."""

from __future__ import annotations

import html
import json
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"
CACHE_PATH = Path("/tmp/sumba-en-translations.json")
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"

TEXT_RE = re.compile(r">([^<>]+)<")
SCRIPT_RE = re.compile(r"<script\b[\s\S]*?</script>", re.IGNORECASE)
LANG_SWITCH_RE = re.compile(r'<div class="lang-pill language-switcher"[\s\S]*?</div>', re.IGNORECASE)
ATTR_PATTERNS = (
    re.compile(r'\balt="([^"]*)"', re.IGNORECASE),
    re.compile(r'\bplaceholder="([^"]*)"', re.IGNORECASE),
    re.compile(r'(<meta\s+name="description"\s+content=")([^"]*)(")', re.IGNORECASE),
)


def should_translate(value: str) -> bool:
    return bool(re.search(r"[A-Za-zÀ-ÿ]", value)) and not value.startswith("http")


def extract_strings(source: str) -> set[str]:
    without_scripts = SCRIPT_RE.sub("", source)
    values: set[str] = set()
    for match in TEXT_RE.finditer(without_scripts):
        value = html.unescape(match.group(1).strip())
        if should_translate(value):
            values.add(value)
    for pattern in ATTR_PATTERNS:
        for match in pattern.finditer(without_scripts):
            value = html.unescape(match.group(match.lastindex - 1 if match.lastindex == 3 else 1).strip())
            if should_translate(value):
                values.add(value)
    return values


def request_translation(payload: str) -> str:
    command = [
        "curl", "-fsSL", "--retry", "4", "--retry-delay", "1", "--get", TRANSLATE_URL,
        "--data-urlencode", "client=gtx", "--data-urlencode", "sl=fr",
        "--data-urlencode", "tl=en", "--data-urlencode", "dt=t",
        "--data-urlencode", f"q={payload}",
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return "".join(part[0] for part in data[0] if part and part[0])


def translate_batch(items: list[tuple[int, str]]) -> dict[str, str]:
    payload = "\n".join(f"[[[S{index:05d}]]] {value}" for index, value in items)
    output = request_translation(payload)
    marker = re.compile(r"\[\[\[S(\d{5})\]\]\]\s*")
    matches = list(marker.finditer(output))
    translated: dict[str, str] = {}
    source_by_id = dict(items)
    for position, match in enumerate(matches):
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(output)
        target = output[start:end].strip()
        source = source_by_id.get(int(match.group(1)))
        if source and target:
            translated[source] = target
    return translated


def translate_all(values: set[str]) -> dict[str, str]:
    cached: dict[str, str] = {}
    if CACHE_PATH.exists():
        cached = json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    missing = sorted((value for value in values if value not in cached), key=lambda value: (len(value), value))
    indexed = list(enumerate(missing))
    batches: list[list[tuple[int, str]]] = []
    batch: list[tuple[int, str]] = []
    length = 0
    for item in indexed:
        item_length = len(item[1]) + 20
        if batch and length + item_length > 3200:
            batches.append(batch)
            batch, length = [], 0
        batch.append(item)
        length += item_length
    if batch:
        batches.append(batch)

    for number, current in enumerate(batches, 1):
        translated = translate_batch(current)
        unresolved = [(index, value) for index, value in current if value not in translated]
        for index, value in unresolved:
            translated[value] = request_translation(value).strip()
        cached.update(translated)
        CACHE_PATH.write_text(json.dumps(cached, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Translated batch {number}/{len(batches)} ({len(cached)}/{len(values)} strings)")
        time.sleep(0.08)
    return cached


def replace_text_nodes(source: str, translations: dict[str, str]) -> str:
    scripts: list[str] = []

    def protect_script(match: re.Match[str]) -> str:
        scripts.append(match.group(0))
        return f"<script data-translation-placeholder=\"{len(scripts) - 1}\"></script>"

    source = SCRIPT_RE.sub(protect_script, source)

    def replace_text(match: re.Match[str]) -> str:
        raw = match.group(1)
        leading = raw[: len(raw) - len(raw.lstrip())]
        trailing = raw[len(raw.rstrip()) :]
        value = html.unescape(raw.strip())
        target = translations.get(value)
        if not target:
            return match.group(0)
        return f">{leading}{html.escape(target, quote=False)}{trailing}<"

    source = TEXT_RE.sub(replace_text, source)

    def replace_simple_attr(match: re.Match[str]) -> str:
        raw = match.group(1)
        value = html.unescape(raw.strip())
        target = translations.get(value, value)
        return match.group(0).replace(raw, html.escape(target, quote=True), 1)

    source = ATTR_PATTERNS[0].sub(replace_simple_attr, source)
    source = ATTR_PATTERNS[1].sub(replace_simple_attr, source)

    def replace_meta(match: re.Match[str]) -> str:
        value = html.unescape(match.group(2).strip())
        target = translations.get(value, value)
        return match.group(1) + html.escape(target, quote=True) + match.group(3)

    source = ATTR_PATTERNS[2].sub(replace_meta, source)

    for index, script in enumerate(scripts):
        source = source.replace(f'<script data-translation-placeholder="{index}"></script>', script, 1)
    return source


def french_switch(filename: str) -> str:
    return (
        '<div class="lang-pill language-switcher" aria-label="Sélecteur de langue">'
        '<span class="lang-option is-current" aria-current="true">FR</span>'
        f'<a class="lang-option" href="en/{filename}" hreflang="en" lang="en">EN</a>'
        '</div>'
    )


def english_switch(filename: str) -> str:
    return (
        '<div class="lang-pill language-switcher" aria-label="Language selector">'
        f'<a class="lang-option" href="../{filename}" hreflang="fr" lang="fr">FR</a>'
        '<span class="lang-option is-current" aria-current="true">EN</span>'
        '</div>'
    )


def polish_english(source: str) -> str:
    replacements = {
        "An island again<br><em>to herself.</em>": "An island still<br><em>true to itself.</em>",
        "Sumba cannot be visited <em>running</em>. It crosses itself — one village, one waterfall, one dirt road at a time.":
            "Sumba isn't a place to <em>rush through</em>. It unfolds one village, one waterfall and one dirt road at a time.",
        "See the circuits": "View the tours",
        "Withdrawal cities": "Pickup locations",
        "Three withdrawal cities": "Three pickup locations",
        "confidential waterfalls": "hidden waterfalls",
        "still confidential waterfalls": "still-hidden waterfalls",
        "Circuits &amp; <em>stays</em> in Sumba": "Tours &amp; <em>stays</em> in Sumba",
        "the page of each circuit": "each tour page",
        "This circuit also exists without a guide": "This tour is also available without a guide",
        "This circuit includes": "This tour includes",
        "complete circuit": "complete tour",
        "shorter circuit": "shorter tour",
        "classic circuits": "classic routes",
        "so few circuits include it": "so few tours include it",
        "Circuit · West": "Tour · West",
        "Circuit · East": "Tour · East",
        "Circuit · South": "Tour · South",
        "West Sumba Circuit": "West Sumba Tour",
        "A <em>project</em> in mind?": "A <em>trip</em> in mind?",
        "Your project": "Your trip",
        "we will come back to you with a suitable proposal": "we'll get back to you with a tailored proposal",
        "Number of people": "Number of guests",
        "Before leaving": "Before you travel",
        "+62 xxx xxxx xxxx — fastest for response.": "+62 xxx xxxx xxxx — the fastest way to reach us.",
        "Response within 24 hours generally.": "We usually reply within 24 hours.",
        "By sending, your message opens pre-filled in WhatsApp — all you have to do is confirm sending.":
            "Your message will open pre-filled in WhatsApp; simply confirm to send it.",
        "A la carte services": "À la carte services",
        "Flagship Service": "Featured service",
        "View scooters by city": "View scooters by location",
        "9 places referenced": "9 featured places",
        "8 places referenced": "8 featured places",
        "7 places referenced": "7 featured places",
        "5 places referenced": "5 featured places",
        "Formulas": "Rental options",
        ">Formula<": ">Option<",
        "On quote": "Price on request",
        ">Is<": ">East<",
        "Is — available": "East — available",
        "Is — confidential": "East — secluded",
        "The<em>Is</em> of Sumba": "The <em>East</em> of Sumba",
        "The<em>": "The <em>",
        "Eastern Sumba — Savanes &amp; Soleil": "East Sumba — Savannas &amp; Sunshine",
        "East Sumba Circuit 4 days — Savanes": "East Sumba Tour — 4 Days of Savannas",
        "South-East Sumba Circuit — 7 Days": "Southeast Sumba Tour — 7 Days",
        "Pasola de Kodi": "Kodi Pasola",
        "the still confidential cascade of ": "the still-hidden waterfall at ",
        "cascade of ": "waterfall at ",
        "megaliths of<a": "megaliths at <a",
        "complete Sumba circuit": "complete Sumba tour",
        "multi-day circuit dedicated to birdwatching": "multi-day birdwatching tour",
        "circuits combining several areas": "itineraries combining several areas",
        "12 à la carte services": "12 bookable services",
    }
    for old, new in replacements.items():
        source = source.replace(old, new)
    return source


def build_page(path: Path, translations: dict[str, str]) -> tuple[str, str]:
    original = path.read_text(encoding="utf-8")
    english = replace_text_nodes(original, translations)
    english = english.replace('<html lang="fr">', '<html lang="en">', 1)
    english = english.replace('href="css/style.css"', 'href="../css/style.css"')
    english = english.replace('src="js/main.js"', 'src="../js/main.js"')
    english = LANG_SWITCH_RE.sub(english_switch(path.name), english, count=1)
    english = english.replace('<span class="lang-pill">EN</span>', english_switch(path.name), 1)
    english = english.replace('<span class="lang-pill">FR</span>', english_switch(path.name), 1)

    if path.name == "contact.html":
        english = english.replace('"Bonjour Sumba Nusantara,%0A%0ANom : "', '"Hello Sumba Nusantara,%0A%0AName: "')
        english = english.replace('"%0AEmail : "', '"%0AEmail: "')
        english = english.replace('"%0ADates approximatives : "', '"%0AApproximate dates: "')
        english = english.replace('"%0ANombre de personnes : "', '"%0ANumber of guests: "')
        english = english.replace('"%0A%0AProjet : "', '"%0A%0ATrip request: "')

    english = polish_english(english)

    french = LANG_SWITCH_RE.sub(french_switch(path.name), original, count=1)
    french = french.replace('<span class="lang-pill">FR</span>', french_switch(path.name), 1)
    return french, english


def main() -> None:
    pages = sorted(ROOT.glob("*.html"))
    values: set[str] = set()
    for page in pages:
        values.update(extract_strings(page.read_text(encoding="utf-8")))

    print(f"Found {len(values)} unique strings across {len(pages)} pages")
    translations = translate_all(values)
    EN_DIR.mkdir(exist_ok=True)

    for page in pages:
        french, english = build_page(page, translations)
        page.write_text(french, encoding="utf-8")
        (EN_DIR / page.name).write_text(english, encoding="utf-8")
    print(f"Generated {len(pages)} English pages in {EN_DIR}")


if __name__ == "__main__":
    main()
