# Stage 01 — Fetch (Layer 2)

## Job
Retrieve RSS articles from all configured sources published in the last 24 hours
(72 hours on thin days), skipping junk titles and articles already sent.
No AI involved — pure mechanical retrieval.

## Inputs
- Layer 3 (reference): `../../_config/sources.md` — list of RSS feeds

- Layer 4 (working): `../03_send/output/*.md` — the last 3 archived digests, for dedup

## Process
1. Parse `sources.md` to get the feed list
2. Fetch each RSS/Atom feed once via HTTP
3. Drop junk titles: empty, equal to the source name, a "Page N" segment
   (Google News indexes section/pagination pages such as "Actualités - Page 666 sur 1962"),
   or under 4 words. A "dropped N junk titles" count is printed per source.
4. Drop articles whose URL appears in the last 3 archived digests. URLs are compared
   without query string or trailing slash (Google News sometimes appends `?oc=5`).
5. Adaptive window: keep entries from the last 24 hours. If fewer than 40 remain,
   re-filter the same fetched entries with a 72-hour window (weekends: trade feeds go
   silent). The window used is printed. Google News searches request 3 days (`when:3d`)
   so the wide window has material.
6. Write results as a flat JSON array

## Outputs
- `output/articles.json` — array of objects:
  ```json
  [
    {
      "title": "Article title",
      "url": "https://...",
      "source": "Financial Post",
      "lang": "en",
      "date": "2026-06-27T10:00:00+00:00"
    }
  ]
  ```

## Script
```bash
python stages/01_fetch/fetch.py
```

## Notes
- Uses `xml.etree.ElementTree` (no feedparser dependency)
- Handles both RSS 2.0 and Atom feed formats
- Warns on failed sources but continues — partial results are acceptable
- Thresholds live at the top of `fetch.py`: `DEFAULT_WINDOW_H`, `WIDE_WINDOW_H`, `MIN_ARTICLES`
- Dedup is by URL only: the same story from another outlet can still reappear
