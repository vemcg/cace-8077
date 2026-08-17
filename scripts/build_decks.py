"""Generate sessions/session-NN/index.html from sessions/session-NN/content.md.

content.md format:

    # Session 1: Topic TBD

    ---

    ## Slide heading

    - Bullet, supports **bold**, *italic*, `code`, and [links](https://example.com)
    - Another bullet

    ---

    ## Another slide

    A plain paragraph works too, not just bullets.

Rerun after editing any content.md:

    python scripts/build_decks.py
"""

import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
SESSIONS_DIR = os.path.join(ROOT, "sessions")

SESSION_BACKGROUNDS = {
    1: "wright-flyer.jpg",
    2: "curtiss-jenny.jpg",
    3: "p51-mustang.jpg",
    4: "f86-sabre.jpg",
    5: "f100-super-sabre.jpg",
    6: "apollo-capsule.jpg",
    7: "gemini-capsule.jpg",
    8: "moon-landing.jpg",
}

COURSE_TITLE = "AI: A Shortcut to Software Design (8077)"
PRESENTER_NAME = "Vern McGeorge"
PRESENTER_EMAIL = "VernMcGeorge@gmail.com"
PRESENTER_PHONE = "408-256-1849"
CONTACT_NOTE = "Until you're in my contacts list, leave a text or voicemail."


def escape_html(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_markdown(text):
    text = escape_html(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def parse_content_block(lines):
    """Parse one '---'-separated block (after the title block) into HTML."""
    heading = None
    body_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("## ") and heading is None:
            heading = inline_markdown(stripped[3:].strip())
        else:
            body_lines.append(stripped)

    html_parts = []
    if heading:
        html_parts.append(f"        <h2>{heading}</h2>")

    list_items = []

    def flush_list():
        if list_items:
            items_html = "\n".join(f"          <li>{item}</li>" for item in list_items)
            html_parts.append(f"        <ul>\n{items_html}\n        </ul>")
            list_items.clear()

    for line in body_lines:
        if line.startswith("- "):
            list_items.append(inline_markdown(line[2:].strip()))
        else:
            flush_list()
            html_parts.append(f"        <p>{inline_markdown(line)}</p>")
    flush_list()

    return "\n".join(html_parts)


def parse_markdown(md_text):
    blocks = re.split(r"\n-{3,}\n", md_text.strip())
    title_block = blocks[0].strip()
    match = re.search(r"^#\s+(.+)$", title_block, re.MULTILINE)
    if not match:
        raise ValueError("content.md must start with a '# Session N: Topic' heading")
    topic = inline_markdown(match.group(1).strip())

    content_slides = [parse_content_block(b.splitlines()) for b in blocks[1:]]
    return topic, content_slides


def render_section(background, inner_html, extra_class=""):
    cls = f' class="{extra_class}"' if extra_class else ""
    return f'      <section{cls} data-background-image="../../assets/images/{background}">\n{inner_html}\n      </section>'


def build_deck_html(session_num, topic, content_slides, background):
    title_slide_inner = f"""        <div class="title-slide-top">
          <p class="course-title">{COURSE_TITLE}</p>
          <h1 class="session-title">{topic}</h1>
        </div>
        <div class="title-slide-contact">
          <p class="presenter-name">{PRESENTER_NAME}</p>
          <p class="contact-email">{PRESENTER_EMAIL}</p>
          <p class="contact-phone">{PRESENTER_PHONE}</p>
          <p class="contact-note">{CONTACT_NOTE}</p>
        </div>"""

    sections = [render_section(background, title_slide_inner, extra_class="title-slide")]

    header_inner = f"        <h2>{topic}</h2>"
    sections.append(render_section(background, header_inner))

    for slide_html in content_slides:
        sections.append(render_section(background, slide_html))

    sections_html = "\n\n".join(sections)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Session {session_num} &mdash; {COURSE_TITLE}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">

{sections_html}

    </div>
  </div>

  <script type="module">
    import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.esm.js';
    Reveal.initialize({{ hash: true }});
  </script>
</body>
</html>
"""


def main():
    for num in sorted(SESSION_BACKGROUNDS):
        folder = os.path.join(SESSIONS_DIR, f"session-{num:02d}")
        md_path = os.path.join(folder, "content.md")
        if not os.path.exists(md_path):
            print(f"session-{num:02d}: no content.md, skipping")
            continue

        with open(md_path, encoding="utf-8") as f:
            md_text = f.read()

        topic, content_slides = parse_markdown(md_text)
        html = build_deck_html(num, topic, content_slides, SESSION_BACKGROUNDS[num])

        out_path = os.path.join(folder, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"session-{num:02d}: {topic!r} -> {out_path}")


if __name__ == "__main__":
    main()
