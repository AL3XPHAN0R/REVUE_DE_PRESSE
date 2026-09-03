# RSS Sources (Layer 3 — Reference)

Add or remove sources here. Stage 01 reads this list at runtime.

| Name | URL | Lang |
|------|-----|------|
| C'est pas mon idée | https://blog.cestpasmonidee.fr/feeds/posts/default?alt=rss | fr |
| Financial Post | https://financialpost.com/feed/ | en |
| Insurance Business Canada | https://www.insurancebusinessmag.com/ca/rss/ | en |
| Avantages | https://www.avantages.ca/feed/ | fr |
| Benefits and Pensions Monitor | https://www.benefitsandpensionsmonitor.com/rss | en |
| Retraite Québec | https://www.retraitequebec.gouv.qc.ca/rss.xml | fr |
| Chambre de la sécurité financière | https://www.chambresf.com/rss.xml | fr |
| Canadian Mortgage Trends | https://www.canadianmortgagetrends.com/feed/ | en |
| Canadian HR Reporter | https://www.hrreporter.com/rss | en |
| La Presse — santé | https://www.lapresse.ca/actualites/sante/rss | fr |
| Radio-Canada — santé | https://ici.radio-canada.ca/rss/4159 | fr |

Note: this table is documentation only — `stages/01_fetch/fetch.py` hardcodes its own
`SOURCES` list, which currently matches the 11 rows above.

## 2026-09-03 — market pivot from SME owners to French-Canadian healthcare workers

Dropped (see `_config/persona.md`, retired 2026-09-03):
- **Repreneuriat Québec** — 0 articles on last fetch and off-niche after the pivot (SME succession).
- **Conseiller.ca**, **Investment Executive**, **Advisor.ca** — all three began returning
  `403 Forbidden` on their `/feed/` URLs sometime after 2026-07-11 (verified with both the
  bare `Mozilla/5.0` UA already in `fetch.py` and a full modern browser UA — same 403 with a
  challenge page body, so it's Cloudflare-level bot protection, not a header problem).
  `avantages.ca` is the same publisher (Newcom Media) as Investment Executive/Advisor.ca and
  is unaffected, so the block isn't publisher-wide — worth re-testing these three periodically
  in case the block lifts.

Added, validated 2026-09-03 (full modern-browser UA, `feedparser` parse + entry count):

| Source | Fit |
|--------|-----|
| **Avantages** | 🇫🇷 Quebec, régimes collectifs + retraite trade press. Best single fit — same-day coverage of stories that also hit Insurance Business Canada in English, but native French. |
| **Benefits and Pensions Monitor** | 🇬🇧 Group benefits + DB pensions, high volume (~34 items/fetch). Volume backbone alongside Insurance Business Canada. |
| **Retraite Québec** | 🇫🇷 The RREGOP/RRQ administrator itself — authoritative for the DB-pension-literacy gap. Low volume (~10 items), infrequent. |
| **Chambre de la sécurité financière** | 🇫🇷 Alexandre's own regulator under LLQP/PQAP. |
| **Canadian Mortgage Trends** | 🇬🇧 Only real feeder for the mortgage-protection gap; mostly rate/market news, expect heavy Stage 02 filtering. |
| **Canadian HR Reporter** | 🇬🇧 Workplace benefits and disability, overlaps Benefits and Pensions Monitor somewhat. |
| **La Presse — santé** | 🇫🇷 Quebec healthcare-workforce and health-system news. High noise — most items are clinical/system news that `persona.md`'s exclusions reject; kept for the workforce-conditions angle. |
| **Radio-Canada — santé** | 🇫🇷 Same profile and purpose as La Presse santé. |

Considered and held back:
- **FSSS-CSN** (`fsss.qc.ca/feed/`) — the actual union for many health-network workers, feed
  works, but publishes bargaining/negotiation news, which is exactly where `persona.md`'s
  NON-NEGOTIABLE tone rule (never frame the group plan as inadequate) is riskiest to apply
  automatically. Revisit once Stage 02's tone handling is confirmed reliable on a few weeks
  of real output.
- **SCFP Québec** (`scfp.qc.ca/feed/`) — feed works but is largely non-health public-sector
  union news (e.g. municipal blue-collar disputes).
- **ChAD** (`chad.ca/feed/`) — feed works but is damages/P&C insurance, off-niche.
- **Ratehub blog** (`ratehub.ca/blog/feed/`) — works but thin, redundant with Canadian
  Mortgage Trends.

Notes on the sources kept from before the pivot (validated 2026-07-07/2026-07-11):
- **Insurance Business Canada** — Atom feed, high volume (~70 items, not all Canada-specific);
  Stage 02 curation is expected to filter.
- **Financial Post** — general Canadian business/markets; mostly filtered out post-pivot except
  for household-finance/mortgage-rate stories.

## Sources with no usable feed (tried 2026-09-03, full modern-browser UA + HTML `<link rel=alternate>` discovery)

| Source | URL | Result |
|--------|-----|--------|
| Finance et Investissement | finance-investissement.com | HTTP 403 (same publisher/protection pattern as Conseiller.ca) |
| Portail de l'assurance | portail-assurance.ca | HTTP 404 — no feed (see Tier 1 table below) |
| Protégez-Vous | protegez-vous.ca | HTTP 404 |
| Benefits Canada | benefitscanada.ca | Connection timeout |
| AMF (Autorité des marchés financiers) | lautorite.qc.ca | HTTP 403 |
| FIQ (syndicat infirmières) | fiq.qc.ca | Connection error |
| APTS | aptsq.com | HTTP 404 |
| OIIQ (ordre des infirmières) | oiiq.org | No feed link, HTML only |
| Profession Santé | professionsante.ca | HTTP 404 |
| Le Devoir — santé | ledevoir.com | HTTP 403 |

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
