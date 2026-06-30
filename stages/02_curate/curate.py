import json, os, sys
from pathlib import Path
from datetime import datetime
import anthropic

SCRIPT_DIR  = Path(__file__).parent
ROOT_DIR    = (SCRIPT_DIR / "../..").resolve()
ARTICLES    = ROOT_DIR / "stages/01_fetch/output/articles.json"
PERSONA     = ROOT_DIR / "_config/persona.md"
VOICE       = ROOT_DIR / "_config/voice.md"
OUTPUT_DIR  = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

if not ARTICLES.exists():
    print("ERROR: articles.json not found. Run Stage 01 first.")
    sys.exit(1)

articles = json.loads(ARTICLES.read_text(encoding="utf-8"))
if not articles:
    print("No articles from Stage 01. Nothing to curate.")
    sys.exit(0)

persona = PERSONA.read_text(encoding="utf-8")
voice   = VOICE.read_text(encoding="utf-8")

# Format article list for prompt
lines = [
    f"{i}. [{a['source']} | {a['lang']}] {a['title']}\n   {a['url']}"
    for i, a in enumerate(articles, 1)
]

MONTHS_FR = ["janvier","février","mars","avril","mai","juin",
             "juillet","août","septembre","octobre","novembre","décembre"]
DAYS_FR   = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
now       = datetime.now()
date_fr   = f"{DAYS_FR[now.weekday()]} {now.day} {MONTHS_FR[now.month - 1]} {now.year}"

prompt = f"""You are a content curator for Alexandre Phanor, a future insurance broker in Canada targeting SME owners.

## Persona & audience
{persona}

## Digest voice & format
{voice}

## Articles available today ({len(articles)} total)
{chr(10).join(lines)}

## Your task
1. Select 5 to 8 articles that best match the persona and relevance criteria above.
2. Format the complete Telegram digest using the exact format from the voice guide.
3. Use today's date: {date_fr}
4. Output ONLY the formatted digest — no preamble, no commentary.
"""

client  = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2048,
    messages=[{"role": "user", "content": prompt}],
)

digest      = message.content[0].text.strip()
output_file = OUTPUT_DIR / "curated.md"
output_file.write_text(digest, encoding="utf-8")

print(f"Stage 02 complete — digest → {output_file}")
print(f"Tokens: {message.usage.input_tokens} in / {message.usage.output_tokens} out")
print("\n--- PREVIEW (first 400 chars) ---")
print(digest[:400] + ("..." if len(digest) > 400 else ""))
