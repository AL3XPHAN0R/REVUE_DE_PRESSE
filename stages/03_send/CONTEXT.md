# Stage 03 — Send (Layer 2)

## Job
Send the curated digest to Telegram and archive a timestamped copy.
No AI involved — pure mechanical dispatch.

## Inputs
- Layer 4 (working): `../02_curate/output/curated.md` — the reviewed digest

## Process
1. Read `curated.md`
2. Split into ≤4000-character chunks (Telegram limit)
3. POST each chunk to the Telegram Bot API
4. Archive a copy to `output/YYYY-MM-DD.md`

## Outputs
- Telegram message sent to configured chat
- `output/YYYY-MM-DD.md` — archived digest (versioned history)

## Script
```bash
python stages/03_send/send.py
```

## Environment variables required
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
