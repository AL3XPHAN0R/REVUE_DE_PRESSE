# Stage 02 — Curate (Layer 2)

## Job
Use Claude Haiku to select the 5–8 most relevant articles and format the Telegram digest.

## Inputs
- Layer 4 (working):   `../01_fetch/output/articles.json` — today's fetched articles
- Layer 3 (reference): `../../_config/persona.md` — author profile + audience criteria
- Layer 3 (reference): `../../_config/voice.md` — digest format + tone + emoji guide

## Process
1. Load articles from Stage 01 output
2. Load persona and voice from `_config/`
3. Send a single prompt to Claude Haiku with all three inputs
4. Haiku selects 5–8 articles and formats the complete Telegram digest. It only gets
   titles, sources and URLs; the prompt forbids asking for article text, asking questions
   or outputting analysis, and requires filling to 5 with indirect-theme articles.
5. Output guard (`guard.py`): unwrap a code fence, cut anything before the first 📰, then
   accept only if the text starts with 📰 and has at least 3 🔗 lines
6. If rejected, retry once (bad answer fed back as an assistant turn + a corrective user turn)
7. If still rejected, print the raw output and exit 1 without writing `curated.md`:
   the workflow fails, GitHub emails, and Stage 03 never runs
8. Write the digest to `output/curated.md`

Any old `output/curated.md` is deleted at startup, so a failed run can never resend
a previous digest.

## Outputs
- `output/curated.md` — formatted Telegram digest, ready to send

## REVIEW GATE
Open `output/curated.md` before running Stage 03.
You can edit, swap articles, adjust copy. Stage 03 sends whatever is in this file.

## Script
```bash
python stages/02_curate/curate.py
python -m unittest discover tests   # offline guard tests (Nov 7/8 archives must be rejected)
```

## Token budget (approximate)
- persona.md: ~300 tokens
- voice.md: ~250 tokens
- articles list (50 articles): ~1,500 tokens
- Total input: ~2,050 tokens → well within Haiku's optimal range
