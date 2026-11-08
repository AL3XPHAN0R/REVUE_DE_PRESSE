import requests, json, re, sys, time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/atom+xml, application/xml;q=0.9, */*;q=0.8",
}
# Google News "site:" search feeds — the only way to reach trade sources that have no RSS
# (Portail de l'assurance) or block direct feed requests with Cloudflare (Conseiller.ca,
# Finance et Investissement). Links are news.google.com redirects that open the article.
def gnews(site, lang="fr"):
    return (f"https://news.google.com/rss/search?q=site:{site}+when:3d"
            f"&hl={lang}-CA&gl=CA&ceid=CA:{lang}")


SOURCES = [
    # Personal-insurance trade press
    ("Portail de l'assurance",    gnews("portail-assurance.ca"),                                "fr"),
    ("Conseiller.ca",             gnews("conseiller.ca"),                                       "fr"),
    ("Finance et Investissement", gnews("finance-investissement.com"),                          "fr"),
    ("Avantages",                 "https://www.avantages.ca/feed/",                             "fr"),
    ("Insurance Business Canada", "https://www.insurancebusinessmag.com/ca/rss/",               "en"),
    ("Wealth Professional",       "https://www.wealthprofessional.ca/rss/",                     "en"),
    ("Benefits and Pensions Monitor", "https://www.benefitsandpensionsmonitor.com/rss",         "en"),
    ("C'est pas mon idée",        "https://blog.cestpasmonidee.fr/feeds/posts/default?alt=rss", "fr"),
    # Regulator
    ("Chambre de la sécurité financière", "https://www.chambresf.com/rss.xml",                  "fr"),
    # Household finance, mortgage, self-employed
    ("La Presse — finances personnelles", "https://www.lapresse.ca/affaires/finances-personnelles/rss", "fr"),
    ("Le Devoir — finances personnelles", "https://www.ledevoir.com/rss/section/economie/finances-personnelles.xml", "fr"),
    ("Globe and Mail — personal finance", "https://www.theglobeandmail.com/arc/outboundfeeds/rss/category/investing/personal-finance/", "en"),
    ("MoneySense",                "https://www.moneysense.ca/feed/",                            "en"),
    ("Canadian Mortgage Trends",  "https://www.canadianmortgagetrends.com/feed/",               "en"),
    # Health network (public -> private practice shift, workforce)
    ("La Presse — santé",         "https://www.lapresse.ca/actualites/sante/rss",               "fr"),
    ("Radio-Canada — santé",      "https://ici.radio-canada.ca/rss/4171",                       "fr"),
]
DEFAULT_WINDOW_H = 24
WIDE_WINDOW_H    = 72   # used when the 24h pool is thin (weekends: trade feeds go quiet)
MIN_ARTICLES     = 40

# Google News "site:" searches also index section and pagination pages
# ("Actualités", "Actualités - Page 666 sur 1962", "Frédéric Roy - Page 21").
# On a quiet weekend these were 10 of 15 items and starved the curator.
PAGINATION = re.compile(r"^page \d+( sur \d+)?$", re.IGNORECASE)


def is_junk_title(title, source):
    t = title.strip()
    if not t or t.casefold() == source.casefold():
        return True
    if any(PAGINATION.match(seg.strip()) for seg in t.split(" - ")):
        return True
    words = [w for w in t.split() if any(c.isalnum() for c in w)]
    return len(words) < 4


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
        channel = root.find("channel")
        if channel is None:
            channel = root
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


# Fetch every feed once; the date window is applied afterwards so a thin
# day can widen it without re-downloading anything.
raw = []  # (source, lang, title, url, pub)
junk_by_source = {}
for name, url, lang in SOURCES:
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        junk = 0
        for title, link, pub in parse_feed(r.content):
            if "news.google.com" in url and " - " in title:
                title = title.rsplit(" - ", 1)[0]  # drop Google News' " - Source" suffix
            if is_junk_title(title, name):
                junk += 1
                continue
            raw.append((name, lang, title, link, pub))
        junk_by_source[name] = junk
        time.sleep(1)
    except Exception as ex:
        print(f"WARN {name}: {ex}", file=sys.stderr)


def normalize_url(u):
    return u.split("?", 1)[0].split("#", 1)[0].rstrip("/")


# URLs already sent in the last 3 archived digests (committed, so present in
# the Actions checkout). A widened window would otherwise resend them.
ARCHIVE_DIR = SCRIPT_DIR.parent / "03_send" / "output"
recent_archives = sorted(ARCHIVE_DIR.glob("*.md"))[-3:]
already_sent = {
    normalize_url(u)
    for f in recent_archives
    for u in re.findall(r"https?://\S+", f.read_text(encoding="utf-8"))
}


def select(hours):
    cutoff = now - timedelta(hours=hours)
    kept, dup = [], 0
    for name, lang, title, link, pub in raw:
        if pub and pub < cutoff:
            continue
        if normalize_url(link) in already_sent:
            dup += 1
            continue
        kept.append({
            "title": title,
            "url": link,
            "source": name,
            "lang": lang,
            "date": pub.isoformat() if pub else "?",
        })
    return kept, dup


now = datetime.now(timezone.utc)
window = DEFAULT_WINDOW_H
items, dup = select(window)
if len(items) < MIN_ARTICLES:
    print(f"Only {len(items)} articles in {window}h (< {MIN_ARTICLES}) -- widening window")
    window = WIDE_WINDOW_H
    items, dup = select(window)

for name, _, _ in SOURCES:
    if name not in junk_by_source:
        continue  # fetch failed, already warned
    count = sum(1 for a in items if a["source"] == name)
    junk = junk_by_source[name]
    print(f"  {name}: {count} articles" + (f" (dropped {junk} junk titles)" if junk else ""))
print(f"Window used: {window}h | dropped {dup} already sent in "
      f"{', '.join(f.stem for f in recent_archives) or 'no archives'}")

output_file = OUTPUT_DIR / "articles.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
print(f"Stage 01 complete -- {len(items)} articles -> {output_file}")
