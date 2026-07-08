import requests, os, sys, shutil
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

SCRIPT_DIR   = Path(__file__).parent
ROOT_DIR     = (SCRIPT_DIR / "../..").resolve()
CURATED_FILE = ROOT_DIR / "stages/02_curate/output/curated.md"
OUTPUT_DIR   = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

TOKEN   = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

if not CURATED_FILE.exists():
    print(f"ERROR: {CURATED_FILE} not found. Run Stage 02 first.")
    sys.exit(1)

message = CURATED_FILE.read_text(encoding="utf-8").strip()

# Backticks aren't part of the digest format (voice.md) and never appear
# intentionally — a stray one leaking in from a source's article title turns
# the rest of the message into a single Telegram "code" entity, which kills
# link auto-detection and renders everything in monospace.
message = message.replace("`", "")

chunks = [message[i:i + 4000] for i in range(0, len(message), 4000)]

for i, chunk in enumerate(chunks, 1):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        },
        timeout=15,
    )
    if not r.ok:
        # Fall back to plain text so an unforeseen formatting character
        # (mismatched * or _ from a source title) doesn't silently drop
        # the whole day's digest — links still auto-link without parse_mode.
        print(f"WARN Telegram Markdown parse failed (chunk {i}): {r.status_code} — {r.text}")
        r = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": chunk,
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
        if not r.ok:
            print(f"ERROR Telegram (chunk {i}): {r.status_code} — {r.text}")
            sys.exit(1)

archive = OUTPUT_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"
shutil.copy(CURATED_FILE, archive)

print(f"Stage 03 complete — sent {len(chunks)} chunk(s) to Telegram")
print(f"Archived -> {archive}")
