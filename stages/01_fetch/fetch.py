import requests, json, sys, time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}
SOURCES = [
    ("C'est pas mon idée",    "https://blog.cestpasmonidee.fr/feeds/posts/default?alt=rss",    "fr"),
    ("Repreneuriat Québec",   "https://repreneuriat.quebec/feed",                              "fr"),
    ("Financial Post",        "https://financialpost.com/feed/",                              "en"),
]
cutoff = datetime.now(timezone.utc) - timedelta(hours=24)


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        return parsedate_to_datetime(s).astimezone(timezone.utc)
    except Exception:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f%z"):
        try:
            dt = datetime.strptime(s[:25], fmt[:len(s[:25])])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except Exception:
            pass
    return None


def parse_feed(content):
    results = []
    try:
        root = ET.fromstring(content)
    except Exception as e:
        print(f"  XML parse error: {e}", file=sys.stderr)
        return results

    if "atom" in root.tag.lower() or root.tag == "{http://www.w3.org/2005/Atom}feed":
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.findtext("{http://www.w3.org/2005/Atom}title", "").strip()
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            url = link_el.get("href", "") if link_el is not None else ""
            pub_str = (entry.findtext("{http://www.w3.org/2005/Atom}published") or
                       entry.findtext("{http://www.w3.org/2005/Atom}updated"))
            results.append((title, url, parse_date(pub_str)))
    else:
        channel = root.find("channel") or root
        items = channel.findall("item") or root.findall(".//item")
        for item in items:
            title = item.findtext("title", "").strip()
            url = item.findtext("link", "").strip()
            if not url:
                link_el = item.find("{http://www.w3.org/2005/Atom}link")
                if link_el is not None:
                    url = link_el.get("href", "")
            pub_str = (item.findtext("pubDate") or
                       item.findtext("{http://purl.org/dc/elements/1.1/}date"))
            results.append((title, url, parse_date(pub_str)))
    return results


items = []
for name, url, lang in SOURCES:
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        count = 0
        for title, link, pub in parse_feed(r.content):
            if pub and pub < cutoff:
                continue
            items.append({
                "title": title,
                "url": link,
                "source": name,
                "lang": lang,
                "date": pub.isoformat() if pub else "?",
            })
            count += 1
        print(f"  {name}: {count} articles")
        time.sleep(1)
    except Exception as ex:
        print(f"WARN {name}: {ex}", file=sys.stderr)

output_file = OUTPUT_DIR / "articles.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
print(f"Stage 01 complete -- {len(items)} articles -> {output_file}")
