"""Generate sessions/session-NN/index.html from sessions/session-NN/content.md.

content.md format:

    # Session 1: Topic TBD

    ---

    ## Slide heading

    - Bullet, supports **bold**, *italic*, `code`, and [links](https://example.com)
    - Another bullet
      - Sub-bullet: indent by 2 spaces per level

    ---

    ## Another slide

    A plain paragraph works too, not just bullets.

To link to a specific slide from anywhere in the deck, tag its heading with
an id and link to it as '#/that-id':

    ## Pick a Game {#pick-a-game}

    ...

    ---

    ## Later slide

    - [Back to Pick a Game](#/pick-a-game)

Rerun after editing any content.md:

    python scripts/build_decks.py        # all sessions
    python scripts/build_decks.py 1      # just session-01
    python scripts/build_decks.py 1 3    # just session-01 and session-03
"""

import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
SESSIONS_DIR = os.path.join(ROOT, "sessions")

SESSION_BACKGROUNDS = {
    1: "wright-flyer.jpg",
    2: "spirit-of-st-louis.jpg",
    3: "p51-mustang.jpg",
    4: "f86-sabre.jpg",
    5: "f100-super-sabre.jpg",
    6: "apollo-capsule.jpg",
    7: "gemini-capsule.jpg",
    8: "moon-landing.jpg",
}

# Each session lives at sessions/<slug>/ instead of sessions/session-NN/, so a
# student can't reach one just by guessing/incrementing a URL -- they need to
# already know its title. A slug should normally just be the kebab-case of
# the session's real topic (see First Flight / Age of Exploration below).
# Sessions without a finalized topic yet get a random placeholder slug so
# even the *order* of untitled sessions isn't exposed -- once a real title
# is set, `git mv sessions/<old-slug> sessions/<new-slug>`, update the entry
# here, and rerun this script.
SESSION_SLUGS = {
    1: "first-flight",
    2: "age-of-exploration",
    3: "edwpygz7",
    4: "dnle66y4",
    5: "kfcv9ioc",
    6: "aan8y0rv",
    7: "jm9zuwep",
    8: "wwovt9ym",
}

# Per-session overlay color, tinting the photo behind the text as well as
# fading it. Any rgba() works: white for a plain fade, a warm tone for a
# sepia-ish look, cool for blue, etc. Sessions not listed here fall back to
# assets/css/style.css's own default (currently plain white at 80%).
SESSION_OVERLAYS = {
    1: "rgba(225, 190, 148, 0.78)",  # warm sepia, matches the old photograph
    2: "rgba(210, 225, 240, 0.8)",  # slight blue tint, matches the sky
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


SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def normalize_url(url):
    """A bare domain like 'claude.ai' isn't a valid href on its own -- the
    browser treats it as a relative path. Add https:// unless it already has
    a scheme (https:, mailto:, etc.) or is an in-page/relative link (#, /)."""
    if SCHEME_RE.match(url) or url.startswith(("#", "/")):
        return url
    return f"https://{url}"


def render_link(m):
    url = normalize_url(m.group(2))
    text = m.group(1)
    if url.startswith(("#", "/")):
        # In-deck navigation (internal slide links) -- stays in the same tab.
        return f'<a href="{url}">{text}</a>'
    # External link -- open in a new tab so the presentation stays open.
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'


def inline_markdown(text):
    text = escape_html(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", render_link, text)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


BULLET_RE = re.compile(r"^(-{1,})\s*(\S.*)$")


def match_bullet(raw_line):
    """A bullet is a run of 1+ leading dashes (with or without a following
    space) followed by content: '- text', '-- text', or '--text' all count.
    Nesting level = (dash count - 1) + (indent spaces // 2), so both '--'
    and 2-space-indented '-' work as a sub-bullet marker."""
    expanded = raw_line.replace("\t", "  ")
    stripped = expanded.lstrip(" ")
    indent = len(expanded) - len(stripped)
    m = BULLET_RE.match(stripped)
    if not m:
        return None
    dashes, text = m.groups()
    level = (len(dashes) - 1) + (indent // 2)
    return level, text.strip()


def build_bullet_tree(items):
    """items: list of (level, html_text) -> nested [{"text":..., "children":[...]}]."""
    root = []
    stack = [(-1, root)]
    for level, text in items:
        node = {"text": text, "children": []}
        while stack[-1][0] >= level:
            stack.pop()
        stack[-1][1].append(node)
        stack.append((level, node["children"]))
    return root


def render_bullet_tree(nodes, indent="        "):
    lines = [f"{indent}<ul>"]
    for node in nodes:
        if node["children"]:
            lines.append(f"{indent}  <li>{node['text']}")
            lines.append(render_bullet_tree(node["children"], indent + "    "))
            lines.append(f"{indent}  </li>")
        else:
            lines.append(f"{indent}  <li>{node['text']}</li>")
    lines.append(f"{indent}</ul>")
    return "\n".join(lines)


HEADING_ID_RE = re.compile(r"\s*\{#([a-zA-Z0-9_-]+)\}\s*$")


def extract_heading_id(heading_text):
    """'Pick a Game {#pick-a-game}' -> ('Pick a Game', 'pick-a-game')."""
    m = HEADING_ID_RE.search(heading_text)
    if not m:
        return heading_text, None
    return heading_text[: m.start()].rstrip(), m.group(1)


def split_into_groups(raw_lines):
    """Split a slide's lines into (heading_or_None, body_lines, slide_id)
    groups, one per '## ' heading encountered. Content before the first
    heading (if any) becomes a headingless leading group."""
    groups = []
    current_heading = None
    current_id = None
    current_body = []
    started = False

    def flush():
        if started:
            groups.append((current_heading, current_body, current_id))

    for raw_line in raw_lines:
        content = raw_line.rstrip("\n")
        if not content.strip():
            continue
        if content.strip().startswith("## "):
            flush()
            current_heading, current_id = extract_heading_id(content.strip()[3:].strip())
            current_body = []
            started = True
        else:
            if not started:
                started = True
            current_body.append(content)
    flush()

    return groups


def render_body(raw_lines):
    html_parts = []
    bullet_run = []
    quote_run = []

    def flush_list():
        if bullet_run:
            tree = build_bullet_tree(bullet_run)
            html_parts.append(render_bullet_tree(tree))
            bullet_run.clear()

    def flush_quote():
        if quote_run:
            # Consecutive '> ' lines become one blockquote (one line per
            # paragraph inside it), not a separate box per line.
            paras = "\n".join(f"          <p>{line}</p>" for line in quote_run)
            html_parts.append(f"        <blockquote>\n{paras}\n        </blockquote>")
            quote_run.clear()

    for raw_line in raw_lines:
        stripped = raw_line.strip()
        bullet = match_bullet(raw_line)
        if bullet is not None:
            flush_quote()
            level, text = bullet
            bullet_run.append((level, inline_markdown(text)))
        elif stripped.startswith("> "):
            flush_list()
            quote_run.append(inline_markdown(stripped[2:].strip()))
        else:
            flush_list()
            flush_quote()
            html_parts.append(f"        <p>{inline_markdown(stripped)}</p>")
    flush_list()
    flush_quote()

    return html_parts


def parse_content_block(raw_lines):
    """Parse one '---'-separated block (after the title block) into HTML.
    Supports more than one '## ' heading per block, each becoming its own
    headed subsection stacked on the same slide. Returns (html, slide_id) --
    slide_id is the first {#id} found among the block's headings, if any."""
    html_parts = []
    slide_id = None
    for heading, body, heading_id in split_into_groups(raw_lines):
        if slide_id is None:
            slide_id = heading_id
        if heading:
            html_parts.append(f"        <h2>{inline_markdown(heading)}</h2>")
        html_parts.extend(render_body(body))

    return "\n".join(html_parts), slide_id


SEPARATOR_RE = re.compile(r"^-{3,}$")


def split_into_blocks(md_text):
    """Split on lines that are nothing but 3+ dashes, tolerating surrounding
    whitespace on that line (e.g. a trailing space after '---')."""
    blocks = []
    current = []
    for line in md_text.splitlines():
        if SEPARATOR_RE.match(line.strip()):
            blocks.append("\n".join(current))
            current = []
        else:
            current.append(line)
    blocks.append("\n".join(current))
    return blocks


def parse_markdown(md_text):
    blocks = split_into_blocks(md_text.strip())
    title_block = blocks[0].strip()
    match = re.search(r"^#\s+(.+)$", title_block, re.MULTILINE)
    if not match:
        raise ValueError("content.md must start with a '# Session N: Topic' heading")
    topic = inline_markdown(match.group(1).strip())

    content_slides = [parse_content_block(b.splitlines()) for b in blocks[1:]]
    return topic, content_slides


def render_section(background, inner_html, extra_class="", section_id=None):
    cls = f' class="{extra_class}"' if extra_class else ""
    sid = f' id="{section_id}"' if section_id else ""
    return f'      <section{cls}{sid} data-background-image="../../assets/images/{background}">\n{inner_html}\n      </section>'


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

    for slide_html, slide_id in content_slides:
        sections.append(render_section(background, slide_html, section_id=slide_id))

    sections_html = "\n\n".join(sections)

    overlay = SESSION_OVERLAYS.get(session_num)
    overlay_style = f'\n  <style>:root {{ --overlay: {overlay}; }}</style>' if overlay else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Session {session_num} &mdash; {COURSE_TITLE}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
  <link rel="stylesheet" href="../../assets/css/style.css">{overlay_style}
</head>
<body>
  <div class="reveal">
    <div class="slides">

{sections_html}

    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script>
    Reveal.initialize({{ hash: true }});
  </script>
</body>
</html>
"""


MASTER_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{course_title}</title>
  <link rel="stylesheet" href="assets/css/index.css">
</head>
<body>
  <main>
    <h1>{course_title}</h1>
    <p class="presenter">{presenter_name} &middot; {presenter_email} &middot; {presenter_phone}</p>
    <p class="presenter">Local-only master list &mdash; not part of the published site. See README.md.</p>

    <ol class="session-list">
{items}
    </ol>
  </main>
</body>
</html>
"""


def build_master_index():
    """Regenerate the root index.html that links every session by slug. This
    file is gitignored on purpose -- it's the one place session order/topic
    and slug are listed side by side, so it never gets committed or
    published. Keep it locally and open it directly when you need the full
    list."""
    leading_session_re = re.compile(r"^Session\s+\d+:\s*", re.IGNORECASE)
    items = []
    for num in sorted(SESSION_SLUGS):
        slug = SESSION_SLUGS[num]
        md_path = os.path.join(SESSIONS_DIR, slug, "content.md")
        topic = "Topic TBD"
        if os.path.exists(md_path):
            with open(md_path, encoding="utf-8") as f:
                md_text = f.read()
            try:
                topic, _ = parse_markdown(md_text)
                topic = leading_session_re.sub("", topic)
            except Exception:
                pass
        items.append(
            f'      <li><a href="sessions/{slug}/index.html">Session {num}: {topic}</a></li>'
        )

    html = MASTER_INDEX_TEMPLATE.format(
        course_title=COURSE_TITLE,
        presenter_name=PRESENTER_NAME,
        presenter_email=PRESENTER_EMAIL,
        presenter_phone=PRESENTER_PHONE,
        items="\n".join(items),
    )
    out_path = os.path.join(ROOT, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"master index (local-only, gitignored) -> {out_path}")


def main():
    if len(sys.argv) > 1:
        requested = [int(a) for a in sys.argv[1:]]
        unknown = [n for n in requested if n not in SESSION_BACKGROUNDS]
        if unknown:
            print(f"Unknown session number(s): {unknown}. Valid: {sorted(SESSION_BACKGROUNDS)}")
            sys.exit(1)
        targets = sorted(requested)
    else:
        targets = sorted(SESSION_BACKGROUNDS)

    failures = []
    for num in targets:
        slug = SESSION_SLUGS[num]
        folder = os.path.join(SESSIONS_DIR, slug)
        md_path = os.path.join(folder, "content.md")
        if not os.path.exists(md_path):
            print(f"{slug}: no content.md, skipping")
            continue

        with open(md_path, encoding="utf-8") as f:
            md_text = f.read()

        try:
            topic, content_slides = parse_markdown(md_text)
            html = build_deck_html(num, topic, content_slides, SESSION_BACKGROUNDS[num])
        except Exception as e:
            print(f"{slug}: FAILED -- {e}")
            failures.append(num)
            continue

        out_path = os.path.join(folder, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"session {num} ({slug}): {topic!r} -> {out_path}")

    if failures:
        print(f"\n{len(failures)} session(s) failed to build: {failures}")
        print("Their index.html files were left untouched (not overwritten with broken output).")

    build_master_index()


if __name__ == "__main__":
    main()
