"""Output guard for Stage 02: decide whether Haiku's answer is a sendable digest.

Kept apart from curate.py so it can be tested without calling the API.
"""

MIN_LINKS = 3


def unwrap_fence(text):
    """Haiku sometimes wraps its whole answer in a markdown code fence, echoing
    the fenced example in voice.md. Telegram's Markdown parser would then treat
    the entire digest as one code block, breaking bold/italic and turning off
    link auto-detection — so unwrap a leading/trailing ``` fence if present."""
    text = text.strip()
    if text.startswith("```"):
        first_line_end = text.find("\n")
        text = text[first_line_end + 1:] if first_line_end != -1 else ""
        text = text.strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    return text


def trim_preamble(text):
    """Cut anything before the first 📰 (e.g. Nov 7's analysis block)."""
    i = text.find("📰")
    return text[i:] if i > 0 else text


def clean(text):
    return trim_preamble(unwrap_fence(text))


def is_valid(digest):
    links = sum(1 for line in digest.splitlines() if line.strip().startswith("🔗"))
    return digest.startswith("📰") and links >= MIN_LINKS
