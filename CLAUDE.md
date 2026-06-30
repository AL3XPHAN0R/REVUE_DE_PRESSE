# RevueDePresse — Workspace Identity (Layer 0)

This is an ICM workspace that generates a daily Telegram press digest for Alexandre Phanor,
a future personal insurance broker in Canada targeting SME owners.

## Purpose
Curate 5–8 articles per day on personal insurance, disability, SME financial protection,
insurtech, and Quebec/Canada regulation — formatted as a Telegram digest for podcast prep.

## Folder map
```
RevueDePresse/
├── CLAUDE.md                  ← you are here (Layer 0)
├── CONTEXT.md                 ← task routing (Layer 1)
├── stages/
│   ├── 01_fetch/              ← fetch RSS → articles.json (no AI)
│   ├── 02_curate/             ← Claude Haiku selects + formats (AI)
│   └── 03_send/               ← send to Telegram + archive (no AI)
└── _config/                   ← stable reference material (Layer 3)
    ├── persona.md             ← Alexandre's profile + target audience
    ├── voice.md               ← digest tone and Telegram format
    └── sources.md             ← RSS feed list
```

## Run order
`01_fetch` → `02_curate` → [optional human review] → `03_send`

## Environment variables required
- `ANTHROPIC_API_KEY` — for Stage 02 (Claude Haiku)
- `TELEGRAM_BOT_TOKEN` — for Stage 03
- `TELEGRAM_CHAT_ID` — for Stage 03
