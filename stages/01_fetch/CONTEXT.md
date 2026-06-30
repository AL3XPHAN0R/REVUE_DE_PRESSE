# Stage 01 — Fetch (Layer 2)

## Job
Retrieve RSS articles from all configured sources published in the last 24 hours.
No AI involved — pure mechanical retrieval.

## Inputs
- Layer 3 (reference): `../../_config/sources.md` — list of RSS feeds

## Process
1. Parse `sources.md` to get the feed list
2. Fetch each RSS/Atom feed via HTTP
3. Filter entries published within the last 24 hours
4. Write results as a flat JSON array

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
