# RevueDePresse — Task Routing (Layer 1)

## Workflow overview

| Stage | Folder | Job | AI? | Output |
|-------|--------|-----|-----|--------|
| 01 | `stages/01_fetch/` | Fetch RSS feeds from all sources | No | `articles.json` |
| 02 | `stages/02_curate/` | Select 5–8 articles, format digest | Yes (Haiku) | `curated.md` |
| 03 | `stages/03_send/` | Send to Telegram, archive | No | `YYYY-MM-DD.md` |

## Human review gate
After Stage 02 completes, open `stages/02_curate/output/curated.md`.
You can swap articles, edit copy, adjust tone — then run Stage 03.
Stage 03 reads whatever is in that file.

## Shared configuration (Layer 3)
All stages share the `_config/` folder:
- `persona.md` — who Alexandre is and who he's writing for
- `voice.md` — digest format, tone, emoji guide
- `sources.md` — RSS feed list (add or remove sources here)

## Running manually (local)
```bash
python stages/01_fetch/fetch.py
python stages/02_curate/curate.py
# review stages/02_curate/output/curated.md
python stages/03_send/send.py
```

## Running automatically (GitHub Actions)
Push to `main` → Actions runs on cron at 11:00 UTC (7:00 AM EDT) daily.
Manual trigger available via `workflow_dispatch`.

---

## Next steps (pick up here in a new session)

This workspace was built in a parent-directory session and is ready to go.
Open a new Claude Code session with `RevueDePresse/` as the working directory, then:

1. **Save project memories** — ask Claude to save ICM structure, pipeline design, and config decisions scoped to this folder
2. **Initialize git** — `git init` from this folder root (not the parent)
3. **Push to GitHub** — create a new GitHub repo and push
4. **Add GitHub Secrets** — in the repo: Settings → Secrets and variables → Actions → add:
   - `ANTHROPIC_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. **Create a local `.env`** — copy `.env.example` to `.env` and fill in real values (never commit this file)
6. **Test locally** — run the three stages in sequence to confirm end-to-end:
   ```bash
   python stages/01_fetch/fetch.py
   python stages/02_curate/curate.py
   # review stages/02_curate/output/curated.md
   python stages/03_send/send.py
   ```
7. **Trigger GitHub Actions manually** — use `workflow_dispatch` to confirm the cloud run works
