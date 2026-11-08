# RSS Sources (Layer 3 — Reference)

Add or remove sources here. Stage 01 reads this list at runtime.

| Name | URL | Lang |
|------|-----|------|
| Portail de l'assurance | Google News `site:portail-assurance.ca` | fr |
| Conseiller.ca | Google News `site:conseiller.ca` | fr |
| Finance et Investissement | Google News `site:finance-investissement.com` | fr |
| Avantages | https://www.avantages.ca/feed/ | fr |
| Insurance Business Canada | https://www.insurancebusinessmag.com/ca/rss/ | en |
| Wealth Professional | https://www.wealthprofessional.ca/rss/ | en |
| Benefits and Pensions Monitor | https://www.benefitsandpensionsmonitor.com/rss | en |
| C'est pas mon idée | https://blog.cestpasmonidee.fr/feeds/posts/default?alt=rss | fr |
| Chambre de la sécurité financière | https://www.chambresf.com/rss.xml | fr |
| La Presse — finances personnelles | https://www.lapresse.ca/affaires/finances-personnelles/rss | fr |
| Le Devoir — finances personnelles | https://www.ledevoir.com/rss/section/economie/finances-personnelles.xml | fr |
| ÉducÉpargne | https://educepargne.ca/feed/ | fr |
| Globe and Mail — personal finance | https://www.theglobeandmail.com/arc/outboundfeeds/rss/category/investing/personal-finance/ | en |
| MoneySense | https://www.moneysense.ca/feed/ | en |
| Canadian Mortgage Trends | https://www.canadianmortgagetrends.com/feed/ | en |
| La Presse — santé | https://www.lapresse.ca/actualites/sante/rss | fr |
| Radio-Canada — santé | https://ici.radio-canada.ca/rss/4171 | fr |

Note: this table is documentation only — `stages/01_fetch/fetch.py` hardcodes its own
`SOURCES` list, which currently matches the 17 rows above. Google News rows use the
`gnews()` helper: `https://news.google.com/rss/search?q=site:<domain>+when:2d&hl=fr-CA&gl=CA&ceid=CA:fr`.

## 2026-11-06 — ÉducÉpargne added

**ÉducÉpargne** (`educepargne.ca/feed/`, WordPress RSS) — 🇫🇷 Quebec financial-education site:
original studies on Quebecers' savings behaviour (e.g. 2026-11-04 study on economic uncertainty),
household debt, couple finances, retirement. Low volume: 11 items in the feed going back to
2026-06-12, 3 of them in the last 7 days, so it will be absent from most daily fetches. Mostly
general household finance, with no direct insurance coverage in the current items (Stage 02
filters); value is Quebec statistics and podcast angles for young households. Some items are
institutional ("Rapport d'activités", campaign launches).

## 2026-11-02 — re-targeting on the four porte A niches

Target groups now come from the "Niches de protection" / "Niches entrepreneurs" sheets:
Invalidité en pratique privée, Invalidité du propriétaire, Assurance prêt, Assurance prêt
des autonomes (see `persona.md`). Mix of groups, relevance first; overhead expense excluded.
Every feed below was validated 2026-11-02 (modern-browser UA, `feedparser`, 7-day item count,
keyword-relevance count on titles).

**Google News `site:` workaround.** Google News search RSS returns the latest indexed
articles of a single domain, which brings back sources with no RSS (Portail de l'assurance)
or that block direct feed requests with Cloudflare (Conseiller.ca, Finance et Investissement —
still `403` on `/feed/` today). Links are `news.google.com` redirects that open the article
in a browser; `fetch.py` strips the trailing ` - Source` from titles. Hub pages
("À l'agenda", "Dossier – …") show up too and are left to Stage 02. Plain keyword searches
("assurance invalidité", "travailleurs autonomes") were tested and rejected: too noisy
(horoscopes, Swiss *assurance-invalidité*, rate-comparison SEO pages).

Added:

| Source | Fit |
|--------|-----|
| **Portail de l'assurance** | 🇫🇷 Tier 1 Quebec insurance trade press — finally reachable. Individual and group insurance, claims data, insurer results. |
| **Conseiller.ca** | 🇫🇷 Advisor trade press, has a "Conseiller PME" section (owners, self-employed). |
| **Finance et Investissement** | 🇫🇷 Advisor trade press, insurance + regulation; heavier on investment (Stage 02 filters). |
| **Wealth Professional** | 🇬🇧 High volume (~54/7d) but strong hits: critical illness coverage gap, AMF warnings, young homebuyers, small-business sales. |
| **La Presse — finances personnelles** | 🇫🇷 Household finance columns (mortgage, budget). Low volume, cryptic headlines that keyword-counting undervalues. |
| **Le Devoir — finances personnelles** | 🇫🇷 Same profile, very low volume. |
| **Globe and Mail — personal finance** | 🇬🇧 Replaces Financial Post. Best EN household-finance hit rate (8/21 over 7 days: mortgage, tax, retirement). Paywalled, headlines still usable for prep. |
| **MoneySense** | 🇬🇧 Personal finance with regular self-employed / tradesperson stories. |

Fixed:
- **Radio-Canada — santé**: `rss/4159` was **not** the health feed (politics / US news). The
  health feed is `rss/4171` (37 items/7d, health network + private-surgery stories).

Dropped:
- **Financial Post** — `/feed/` now returns an HTML page (0 entries); category feeds too.
- **Retraite Québec** — 0 items in 7 days, entries are admin pages; RREGOP literacy is no longer a core theme.
- **Canadian HR Reporter** — employer/HR perspective, excluded by `persona.md` (3/20 relevant).

Kept: Avantages, Insurance Business Canada (31/51 relevant), Benefits and Pensions Monitor
(group-plan heavy, but supplies disability / mental-health / critical-illness claim statistics),
CSF, Canadian Mortgage Trends (6/10), La Presse santé, C'est pas mon idée (insurtech).

Considered and held back (2026-11-02):
- **Les Affaires** (`lesaffaires.com/feed/`) — works again but intermittently answers `202` (bot challenge); general business news, all section feeds return the same content.
- **Radio-Canada économie** (`rss/5717`), **Journal de Montréal / TVA argent** — high volume, 2–6 relevant out of 18–50.
- **Canadian Mortgage Professional** (`mpamag.com/ca/rss/`) — mortgage-broker industry news (awards, lender results); redundant with Canadian Mortgage Trends.
- **Benefits Canada** (`benefitscanada.com/feed/`) — works again, employer perspective.
- **Insurance Portal** (Google News `site:insurance-portal.ca`) — English twin of Portail de l'assurance, would duplicate it.
- **Advisor.ca**, **Investment Executive** (Google News `site:`) — reachable this way, but mostly markets; Conseiller.ca covers the same publisher in French.
- **nesto**, **Ratehub**, **Multi-Prêts** blogs — rate forecasts, thin.
- No feed: OPQ, OEQ, OOAQ, FMOQ, CPA Québec, FCEI, BDC, FCCQ, Planiprêt, Option consommateurs, Protégez-Vous (direct). Professional orders have no RSS — private-practice coverage relies on La Presse/Radio-Canada santé and the trade press.

## 2026-09-03 — market pivot (historical) from SME owners to French-Canadian healthcare workers

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
