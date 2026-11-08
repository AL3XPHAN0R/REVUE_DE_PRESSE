import json, os, sys
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv
from guard import clean, is_valid

load_dotenv(Path(__file__).parent.parent.parent / ".env")

SCRIPT_DIR  = Path(__file__).parent
ROOT_DIR    = (SCRIPT_DIR / "../..").resolve()
ARTICLES    = ROOT_DIR / "stages/01_fetch/output/articles.json"
PERSONA     = ROOT_DIR / "_config/persona.md"
VOICE       = ROOT_DIR / "_config/voice.md"
OUTPUT_DIR  = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "curated.md"

# A failed run must never leave yesterday's digest behind for Stage 03 to resend.
OUTPUT_FILE.unlink(missing_ok=True)

if not ARTICLES.exists():
    print("ERROR: articles.json not found. Run Stage 01 first.")
    sys.exit(1)

articles = json.loads(ARTICLES.read_text(encoding="utf-8"))
if not articles:
    print("No articles from Stage 01. Nothing to curate.")
    sys.exit(0)

persona = PERSONA.read_text(encoding="utf-8")
voice   = VOICE.read_text(encoding="utf-8")

# Static content — identical across reruns, marked for caching.
# Caching activates once this block exceeds Haiku 4.5's 4096-token minimum;
# silently a no-op below that threshold (add more RSS sources to cross it).
system_text = f"""You are a content curator for Alexandre Phanor, a future insurance broker in Canada targeting French-Canadian healthcare professionals, self-employed workers and young homeowning households.

## Persona & audience
{persona}

## Digest voice & format
{voice}

## Task
Select 5 to 8 articles from the list provided that best match the persona and relevance criteria above.
If two or more articles cover the same underlying story or statistic (e.g. the same survey
picked up by multiple outlets), select only the single best version of it, not each copy.
Apply the NON-NEGOTIABLE tone rule to every insight line: frame each article as complementing
the coverage people already have (union-negotiated group plans, order/association plans,
lender creditor insurance), never as exposing a weakness in it.
Format the complete Telegram digest using the exact format from the voice guide.
Output ONLY the formatted digest — no preamble, no commentary.

Hard rules:
- You only ever get titles, sources and URLs, by design. You will never get article text
  and must not ask for it. Judge relevance from the title and source alone.
- This runs unattended and nobody will reply. Never ask questions, never explain your
  reasoning, never output analysis.
- Always produce a digest of 5 to 8 articles. If fewer than 5 are strongly relevant,
  complete it with the closest indirect-theme articles from the persona. Never output
  zero articles. Only go below 5 if the list itself has fewer than 5 usable articles.
- The response must start with "📰 *Revue de presse"."""

# Dynamic content — changes every day (articles + date go in the user turn)
lines = [
    f"{i}. [{a['source']} | {a['lang']}] {a['title']}\n   {a['url']}"
    for i, a in enumerate(articles, 1)
]

MONTHS_FR = ["janvier","février","mars","avril","mai","juin",
             "juillet","août","septembre","octobre","novembre","décembre"]
DAYS_FR   = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
now       = datetime.now()
date_fr   = f"{DAYS_FR[now.weekday()]} {now.day} {MONTHS_FR[now.month - 1]} {now.year}"

user_text = f"""## Articles disponibles aujourd'hui ({len(articles)} au total)
{chr(10).join(lines)}

Date du digest : {date_fr}"""

RETRY_TEXT = ("That output was not a digest. Reply with ONLY the formatted Telegram digest, "
              "starting with 📰, selecting 5–8 articles from the list based on titles alone.")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def ask(messages):
    return client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": system_text,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=messages,
    )


messages = [{"role": "user", "content": user_text}]
message  = ask(messages)
raw      = message.content[0].text
digest   = clean(raw)

if not is_valid(digest):
    print("WARN Haiku's answer is not a digest -- retrying once")
    messages += [
        {"role": "assistant", "content": raw.strip()},
        {"role": "user", "content": RETRY_TEXT},
    ]
    message = ask(messages)
    raw     = message.content[0].text
    digest  = clean(raw)

if not is_valid(digest):
    print("ERROR Haiku did not return a valid digest after one retry. Raw output:\n")
    print(raw)
    sys.exit(1)

OUTPUT_FILE.write_text(digest, encoding="utf-8")

u             = message.usage
cache_created = getattr(u, "cache_creation_input_tokens", 0) or 0
cache_read    = getattr(u, "cache_read_input_tokens", 0) or 0

print(f"Stage 02 complete -- digest -> {OUTPUT_FILE}")
print(f"Tokens: {u.input_tokens} in / {u.output_tokens} out"
      f" | cache write: {cache_created} / read: {cache_read}")
if cache_created == 0 and cache_read == 0:
    print("  (cache inactive -- Haiku 4.5 requires 4096+ tokens to cache; add more RSS sources)")
print("\n--- PREVIEW (first 400 chars) ---")
print((digest[:400] + ("..." if len(digest) > 400 else "")).encode("ascii", "replace").decode("ascii"))
