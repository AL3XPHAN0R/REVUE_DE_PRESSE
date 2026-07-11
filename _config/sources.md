# RSS Sources (Layer 3 — Reference)

Add or remove sources here. Stage 01 reads this list at runtime.

| Name | URL | Lang |
|------|-----|------|
| C'est pas mon idée | https://blog.cestpasmonidee.fr/feeds/posts/default?alt=rss | fr |
| Repreneuriat Québec | https://repreneuriat.quebec/feed | fr |
| Financial Post | https://financialpost.com/feed/ | en |
| Conseiller.ca | https://www.conseiller.ca/feed/ | fr |
| Insurance Business Canada | https://www.insurancebusinessmag.com/ca/rss/ | en |
| Investment Executive | https://www.investmentexecutive.com/feed/ | en |
| Advisor.ca | https://www.advisor.ca/feed/ | en |

Note: this table is documentation only — `stages/01_fetch/fetch.py` hardcodes its own
`SOURCES` list, which currently matches the 7 rows above.

Notes on the two new sources (validated 2026-07-07):
- **Conseiller.ca** — the global feed includes the "Conseiller PME" section plus AMF/OCRI
  regulation news. The section-only feed (`/conseiller-pme/feed/`) also exists but publishes
  too rarely (sometimes 10+ days between posts) to be worth a separate entry.
- **Insurance Business Canada** — Atom feed, high volume (~70 items, not all Canada-specific);
  Stage 02 curation is expected to filter.

Notes on the two Tier 3 additions (validated 2026-07-11):
- **Investment Executive** and **Advisor.ca** — both standard WordPress RSS 2.0 feeds
  (same publisher, Newcom Media), parse natively with `fetch.py`. Broad financial-industry
  coverage (markets, tax, investments for advisors), so most items will fall under
  `persona.md`'s "pure investment/portfolio/markets" exclusion — Stage 02 curation is
  expected to filter heavily, same pattern as Insurance Business Canada.

## Tier 3 sources without RSS (not addable to Stage 01)

Verified 2026-07-11 — no RSS/Atom feed exists (404 on standard paths, no feed link declared
in HTML even after following redirects):

| Source | URL | Note |
|--------|-----|------|
| FCEI / CFIB | cfib-fcei.ca/research-economic-analysis | No feed; reports/surveys published as static pages |
| BDC | bdc.ca | No feed detected on homepage or blog |
| Les Affaires | lesaffaires.com | Blocks automated requests (HTTP 202 empty response — bot challenge) |

## Tier 1 sources without RSS (not addable to Stage 01)

Verified 2026-07-07 — no RSS/Atom feed exists (404 on standard paths, none declared in HTML):

| Source | URL | Access alternative |
|--------|-----|--------------------|
| Portail de l'assurance | portail-assurance.ca | Free daily email newsletter |
| Journal de l'assurance | portail-assurance.ca/journal-assurance | Paywalled magazine |
| Insurance Portal | insurance-portal.ca | Free email newsletter (base tier); `/prfeed/` is an HTML page, not a feed |

To include these, the pipeline would need email-newsletter parsing or a third-party
RSS generator (Feedly/Inoreader/RSSHub) — see `sources_temp.md` implementation notes.