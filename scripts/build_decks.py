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

Two directives pull in files that sit next to content.md (see README.md,
"Review"):

    [[story: git-story.md | git-story]]   # alone in its own '---' block: expands into
                                          # a run of slides; the optional "| id" is
                                          # the first slide's anchor (#/git-story)
    [[flashcards: git.json]]              # inside a slide: a flashcard practice widget

Rerun after editing any content.md:

    python scripts/build_decks.py        # all sessions
    python scripts/build_decks.py 1      # just session-01
    python scripts/build_decks.py 1 3    # just session-01 and session-03
"""

import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
SESSIONS_DIR = os.path.join(ROOT, "sessions")

SESSION_BACKGROUNDS = {
    1: "wright-flyer.jpg",
    2: "spirit-of-st-louis.jpg",
    3: "pan-am-clipper.jpg",
    4: "x15-launch.jpg",
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
    3: "far-horizons",
    4: "higher-faster",
    5: "kfcv9ioc",
    6: "aan8y0rv",
    7: "jm9zuwep",
    8: "wwovt9ym",
}

# The actual folder name under sessions/ for each session. Finalized sessions
# get an "NN-" prefix so the folder listing (in an editor, or GitHub's file
# browser) sorts in session order instead of alphabetically. The public URL
# stays the clean slug from SESSION_SLUGS above: this script also writes a
# tiny redirect stub at sessions/<slug>/index.html pointing at the real
# sessions/NN-<slug>/ folder, so links like .../sessions/first-flight/ keep
# working. Placeholder (Topic TBD) sessions keep their bare random slug as
# the folder name -- no number -- so their order still isn't exposed.
SESSION_DIRS = {
    1: "01-first-flight",
    2: "02-age-of-exploration",
    3: "03-far-horizons",
    4: "04-higher-faster",
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
    1: "rgba(235, 205, 168, 0.85)",  # warm sepia, matches the old photograph -- lightened, slightly less transparent
    2: "rgba(210, 225, 240, 0.8)",  # slight blue tint, matches the sky
    3: "rgba(195, 220, 222, 0.76)",  # ocean teal, matches the Pacific crossing
    4: "rgba(205, 213, 224, 0.7)",  # cool steel-blue, matches the high-altitude drama
}

COURSE_TITLE = "Vibe Coding: Create Apps and Games with AI (8077)"
PRESENTER_NAME = "Vern McGeorge"
PRESENTER_EMAIL = "VernMcGeorge@gmail.com"
PRESENTER_PHONE = "408-256-1849"
CONTACT_NOTE = "Until you're in my contacts list, leave a text or voicemail."

# Published GitHub Pages site -- shown on each deck's title slide as the
# follow-along URL for that session (PUBLIC_BASE_URL + "/sessions/<slug>/").
PUBLIC_BASE_URL = "https://vemcg.github.io/cace-8077"


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
    text = re.sub(r"\\(?:\s+|$)", "<br>", text)  # trailing backslash = line break
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
DIAGRAM_RE = re.compile(r"^\[\[diagram-left:\s*([^|]+?)\s*\|\s*(.+?)\]\]$")
STORY_RE = re.compile(r"^\[\[story:\s*([^|\]]+?)\s*(?:\|\s*([a-zA-Z0-9_-]+)\s*)?\]\]$")
FLASHCARDS_RE = re.compile(r"^\[\[flashcards:\s*([^\]]+?)\s*\]\]$")

# Rough per-slide budget for [[story: ...]] pagination. Story slides use a
# smaller font (see .story-slide in style.css) because they're read on the
# student's own screen, not projected. The build can't measure rendered height,
# so this is only a guide; tune it by testing the longest slides in a browser.
STORY_CHAR_BUDGET = 1500
# A '###' heading starts a new slide only if the current slide is at least this
# fraction full.
TOPIC_BREAK_FRACTION = 0.4


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


NUMBERED_RE = re.compile(r"^\d+\.\s+(\S.*)$")


def split_table_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render_table(rows):
    """Markdown pipe table (header row, '|---|---|' separator, body rows)."""
    header = None
    if len(rows) > 1 and re.match(r"^\|?[\s:|-]+\|?$", rows[1]):
        header = split_table_row(rows[0])
        rows = rows[2:]
    parts = ['        <table>']
    if header:
        cells = "".join(f"<th>{inline_markdown(c)}</th>" for c in header)
        parts.append(f"          <thead><tr>{cells}</tr></thead>")
    parts.append("          <tbody>")
    for row in rows:
        cells = "".join(f"<td>{inline_markdown(c)}</td>" for c in split_table_row(row))
        parts.append(f"            <tr>{cells}</tr>")
    parts.extend(["          </tbody>", "        </table>"])
    return "\n".join(parts)


def render_body(raw_lines, ctx=None):
    html_parts = []
    bullet_run = []
    quote_run = []
    numbered_run = []
    table_run = []
    diagram_open = False

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

    def flush_numbered():
        if numbered_run:
            items = "\n".join(f"          <li>{t}</li>" for t in numbered_run)
            html_parts.append(f"        <ol>\n{items}\n        </ol>")
            numbered_run.clear()

    def flush_table():
        if table_run:
            html_parts.append(render_table(table_run))
            table_run.clear()

    def flush_all():
        flush_list()
        flush_quote()
        flush_numbered()
        flush_table()

    for raw_line in raw_lines:
        stripped = raw_line.strip()
        bullet = match_bullet(raw_line)
        diagram = DIAGRAM_RE.match(stripped)
        flashcards = FLASHCARDS_RE.match(stripped)
        numbered = NUMBERED_RE.match(stripped)
        if flashcards:
            flush_all()
            html_parts.extend(render_flashcards(flashcards.group(1), ctx))
        elif diagram:
            flush_all()
            image_url, image_alt = diagram.groups()
            html_parts.extend([
                '        <div class="diagram-layout">',
                '          <div class="diagram-visual">',
                f'            <img src="{escape_html(image_url)}" alt="{escape_html(image_alt)}">',
                '          </div>',
                '          <div class="diagram-text">',
            ])
            diagram_open = True
        elif stripped.startswith("### "):
            flush_all()
            heading, heading_id = extract_heading_id(stripped[4:].strip())
            id_attribute = f' id="{heading_id}"' if heading_id else ""
            html_parts.append(
                f"        <h3{id_attribute}>{inline_markdown(heading)}</h3>"
            )
        elif stripped.startswith("|"):
            flush_list()
            flush_quote()
            flush_numbered()
            table_run.append(stripped)
        elif numbered:
            flush_list()
            flush_quote()
            flush_table()
            numbered_run.append(inline_markdown(numbered.group(1)))
        elif bullet is not None:
            flush_quote()
            flush_numbered()
            flush_table()
            level, text = bullet
            bullet_run.append((level, inline_markdown(text)))
        elif stripped.startswith("> "):
            flush_list()
            flush_numbered()
            flush_table()
            quote_run.append(inline_markdown(stripped[2:].strip()))
        else:
            flush_all()
            html_parts.append(f"        <p>{inline_markdown(stripped)}</p>")
    flush_all()
    if diagram_open:
        html_parts.extend([
            '          </div>',
            '        </div>',
        ])

    return html_parts


def parse_content_block(raw_lines, ctx=None):
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
        html_parts.extend(render_body(body, ctx))

    return "\n".join(html_parts), slide_id


def read_session_file(filename, ctx, what):
    path = os.path.join(ctx["folder"], filename)
    if not os.path.isfile(path):
        raise ValueError(f"{what} file not found: {filename} (looked in {ctx['folder']})")
    with open(path, encoding="utf-8") as f:
        return f.read()


def render_flashcards(filename, ctx):
    """[[flashcards: deck.json]] -> a host <div> with the deck embedded as JSON
    (never fetched at runtime, so decks keep working from file://).
    assets/js/flashcards.js turns it into the practice widget."""
    if ctx is None:
        return []
    try:
        deck = json.loads(read_session_file(filename, ctx, "flashcards"))
    except json.JSONDecodeError as e:
        raise ValueError(f"flashcards file {filename} is not valid JSON: {e}")
    if not isinstance(deck, dict) or not isinstance(deck.get("deckId"), str) or not deck["deckId"]:
        raise ValueError(f"flashcards file {filename}: missing 'deckId'")
    cards = deck.get("cards")
    if not isinstance(cards, list) or not cards:
        raise ValueError(f"flashcards file {filename}: 'cards' must be a non-empty list")
    slim_cards = []
    for i, card in enumerate(cards):
        if not isinstance(card, dict) or not all(
            isinstance(card.get(k), str) and card.get(k) for k in ("id", "front", "back")
        ):
            raise ValueError(
                f"flashcards file {filename}: card {i + 1} needs string 'id', 'front' and 'back'"
            )
        slim = {"id": card["id"], "front": card["front"], "back": card["back"]}
        source = card.get("source")
        if isinstance(source, dict) and (source.get("title") or source.get("url")):
            slim["source"] = {"title": source.get("title") or "", "url": source.get("url") or ""}
        slim_cards.append(slim)
    title = deck.get("title")
    slim_deck = {
        "deckId": deck["deckId"],
        "title": title if isinstance(title, str) and title else deck["deckId"],
        "cards": slim_cards,
    }
    # '</' must not appear inside the <script> element.
    payload = json.dumps(slim_deck, ensure_ascii=False).replace("</", "<\\/")
    ctx["flashcards"] = True
    return [
        f'        <div class="flashcards" data-deck-id="{escape_html(deck["deckId"])}">',
        f'          <script type="application/json" class="flashcards-data">{payload}</script>',
        "          <noscript>Flash cards need JavaScript.</noscript>",
        "        </div>",
    ]


def table_units(rows):
    """Split a long pipe table into chunks that fit STORY_CHAR_BUDGET, each
    repeating the header row."""
    has_header = len(rows) > 1 and re.match(r"^\|?[\s:|-]+\|?$", rows[1])
    header = rows[:2] if has_header else []
    body = rows[2:] if has_header else rows
    units, chunk, size = [], [], 0
    for row in body:
        if chunk and size + len(row) > STORY_CHAR_BUDGET:
            units.append(header + chunk)
            chunk, size = [], 0
        chunk.append(row)
        size += len(row)
    if chunk:
        units.append(header + chunk)
    return units


def story_sections(md_text):
    """Story markdown -> [(heading_or_None, [unit, ...])], where each unit is a
    list of lines ready for render_body() and is never split across slides.
    '#'/'##' headings start a new section. A unit is a text paragraph, one
    quoted paragraph (bare '>' lines separate quoted paragraphs), a whole
    bullet / numbered list, a table, or a '###' heading. A '---' line is just
    a break."""
    sections = [(None, [])]
    kind = None
    buf = []

    def flush():
        nonlocal kind
        if buf:
            if kind == "text":
                unit = [" ".join(buf)]
            elif kind == "quote":
                unit = ["> " + " ".join(buf)]
            elif kind == "bullet":
                # One unit per item: consecutive items still share a slide, but
                # a long list can paginate.
                for line in buf:
                    sections[-1][1].append([line])
                unit = None
            elif kind == "table":
                sections[-1][1].extend(table_units(buf))
                unit = None
            else:
                unit = list(buf)
            if unit:
                sections[-1][1].append(unit)
        buf.clear()
        kind = None

    for raw in md_text.splitlines():
        stripped = raw.strip()
        heading = re.match(r"^#{1,2}\s+(.+)$", stripped)
        if heading:
            flush()
            sections.append((extract_heading_id(heading.group(1).strip())[0], []))
            continue
        if not stripped or re.match(r"^-{3,}$", stripped):
            flush()
            continue
        if stripped.startswith("### "):
            flush()
            sections[-1][1].append([stripped])
            continue
        if stripped.startswith(">"):
            content = stripped[1:].strip()
            if not content:
                flush()
                continue
            line_kind, line = "quote", content
        elif stripped.startswith("|"):
            line_kind, line = "table", stripped
        elif NUMBERED_RE.match(stripped):
            line_kind, line = "ol", raw
        elif match_bullet(raw):
            line_kind, line = "bullet", raw
        else:
            line_kind, line = "text", stripped
        if line_kind != kind:
            flush()
            kind = line_kind
        buf.append(line)
    flush()
    return [sec for sec in sections if sec[0] is not None or sec[1]]


def story_slides(filename, anchor, ctx):
    """[[story: file.md | anchor]] -> [(html, slide_id)], paginated by paragraph
    against STORY_CHAR_BUDGET. Never splits a paragraph; repeats the heading
    with ' (cont.)' on continuation slides."""
    if ctx is None:
        return []
    slides = []
    for heading, paras in story_sections(read_session_file(filename, ctx, "story")):
        # A '###' heading is glued to the unit after it, so it can't be left
        # stranded at the bottom of a slide.
        glued = []
        for para in paras:
            if glued and len(glued[-1]) == 1 and glued[-1][0].startswith("### "):
                glued[-1] = glued[-1] + para
            else:
                glued.append(para)
        paras = glued
        chunks, current, size = [], [], 0
        for para in paras:
            n = sum(len(line) for line in para)
            starts_topic = para[0].startswith("### ")
            # A '###' topic starts a fresh slide once the current one has a fair
            # amount on it; a nearly empty slide just keeps going.
            if current and (
                (starts_topic and size >= STORY_CHAR_BUDGET * TOPIC_BREAK_FRACTION)
                or size + n > STORY_CHAR_BUDGET
            ):
                chunks.append(current)
                current, size = [], 0
            current.append(para)
            size += n
        if current or not chunks:
            chunks.append(current)
        for i, chunk in enumerate(chunks):
            parts = []
            if heading:
                title = heading + (" (cont.)" if i else "")
                parts.append(f"        <h2>{inline_markdown(title)}</h2>")
            parts.extend(render_body([line for para in chunk for line in para], ctx))
            slides.append(["\n".join(parts), None])
    if not slides:
        print(f"  WARNING: story file {filename} is empty -- inserting a placeholder slide")
        slides.append(["        <h2>Story coming soon</h2>", None])
    if anchor:
        slides[0][1] = anchor
    return [tuple(s) for s in slides]


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


def parse_markdown(md_text, folder=None):
    """Returns (topic, content_slides, uses_flashcards). Directives that read
    files ([[story:]], [[flashcards:]]) are only expanded when `folder` (the
    session folder) is given -- the master index just needs the topic."""
    blocks = split_into_blocks(md_text.strip())
    title_block = blocks[0].strip()
    match = re.search(r"^#\s+(.+)$", title_block, re.MULTILINE)
    if not match:
        raise ValueError("content.md must start with a '# Session N: Topic' heading")
    topic = inline_markdown(match.group(1).strip())

    ctx = {"folder": folder, "flashcards": False} if folder else None
    content_slides = []
    for block in blocks[1:]:
        lines = block.splitlines()
        stories = [m for m in (STORY_RE.match(l.strip()) for l in lines) if m]
        if stories:
            others = [l for l in lines if l.strip() and not STORY_RE.match(l.strip())]
            if others or len(stories) > 1:
                raise ValueError(
                    "[[story: ...]] must be the only thing in its '---' block "
                    f"(found other content next to {stories[0].group(0)})"
                )
            # The whole story is one vertical stack: a single left/right
            # position in the deck, stepped through with up/down.
            stack = story_slides(stories[0].group(1), stories[0].group(2), ctx)
            if stack:
                content_slides.append({"stack": stack})
        else:
            content_slides.append(parse_content_block(lines, ctx))
    return topic, content_slides, bool(ctx and ctx["flashcards"])


def render_section(background, inner_html, extra_class="", section_id=None):
    cls = f' class="{extra_class}"' if extra_class else ""
    sid = f' id="{section_id}"' if section_id else ""
    return f'      <section{cls}{sid} data-background-image="../../assets/images/{background}">\n{inner_html}\n      </section>'


def build_deck_html(session_num, topic, content_slides, background, uses_flashcards=False):
    slide_url = f"{PUBLIC_BASE_URL}/sessions/{SESSION_SLUGS[session_num]}/"
    title_slide_inner = f"""        <div class="title-slide-top">
          <p class="course-title">{COURSE_TITLE}</p>
          <h1 class="session-title">{topic}</h1>
        </div>
        <div class="title-slide-contact">
          <p class="presenter-name">{PRESENTER_NAME}</p>
          <p class="contact-email">{PRESENTER_EMAIL}</p>
          <p class="contact-phone">{PRESENTER_PHONE}</p>
          <p class="contact-note">{CONTACT_NOTE}</p>
        </div>
        <div class="follow-along-block">
          <p class="follow-along-url">Follow along: {slide_url}</p>
          <p class="fullscreen-hint">Press F to toggle full screen</p>
        </div>"""

    sections = [render_section(background, title_slide_inner, extra_class="title-slide")]

    for entry in content_slides:
        if isinstance(entry, dict):
            # Vertical stack (a [[story:]]): outer <section> holding one inner
            # <section> per slide, so reveal.js navigates them with up/down.
            inner = []
            for slide_html, slide_id in entry["stack"]:
                wrapped = f'        <div class="slide-content">\n{slide_html}\n        </div>'
                inner.append(
                    render_section(background, wrapped, extra_class="story-slide", section_id=slide_id)
                )
            sections.append(
                '      <section class="story-stack">\n' + "\n".join(inner) + "\n      </section>"
            )
            continue
        slide_html, slide_id = entry
        wrapped = f'        <div class="slide-content">\n{slide_html}\n        </div>'
        sections.append(render_section(background, wrapped, section_id=slide_id))

    sections_html = "\n\n".join(sections)

    flashcards_script = (
        '  <script src="../../assets/js/flashcards.js"></script>\n' if uses_flashcards else ""
    )
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
{flashcards_script}  <script src="../../assets/js/deck.js"></script>
</body>
</html>
"""


REDIRECT_STUB_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=../{target}/">
  <link rel="canonical" href="../{target}/">
  <title>Redirecting&hellip;</title>
</head>
<body>
  <p>This session now lives at <a href="../{target}/">../{target}/</a>.</p>
</body>
</html>
"""


def write_redirect_stub(clean_slug, target_dir):
    """Write sessions/<clean_slug>/index.html as a meta-refresh redirect to
    sessions/<target_dir>/, so the clean URL keeps working after the real
    folder gained an 'NN-' sort prefix."""
    stub_dir = os.path.join(SESSIONS_DIR, clean_slug)
    os.makedirs(stub_dir, exist_ok=True)
    out_path = os.path.join(stub_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(REDIRECT_STUB_TEMPLATE.format(target=target_dir))
    print(f"  redirect stub: sessions/{clean_slug}/ -> sessions/{target_dir}/")


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
        folder = SESSION_DIRS[num]
        md_path = os.path.join(SESSIONS_DIR, folder, "content.md")
        topic = "Topic TBD"
        if os.path.exists(md_path):
            with open(md_path, encoding="utf-8") as f:
                md_text = f.read()
            try:
                topic, _, _ = parse_markdown(md_text)
                topic = leading_session_re.sub("", topic)
            except Exception:
                pass
        items.append(
            f'      <li><a href="sessions/{folder}/index.html">Session {num}: {topic}</a></li>'
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
        dir_name = SESSION_DIRS[num]
        folder = os.path.join(SESSIONS_DIR, dir_name)
        md_path = os.path.join(folder, "content.md")
        if not os.path.exists(md_path):
            print(f"{dir_name}: no content.md, skipping")
            continue

        with open(md_path, encoding="utf-8") as f:
            md_text = f.read()

        try:
            topic, content_slides, uses_flashcards = parse_markdown(md_text, folder)
            html = build_deck_html(
                num, topic, content_slides, SESSION_BACKGROUNDS[num], uses_flashcards
            )
        except Exception as e:
            print(f"{dir_name}: FAILED -- {e}")
            failures.append(num)
            continue

        out_path = os.path.join(folder, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"session {num} ({dir_name}): {topic!r} -> {out_path}")

        # Keep the clean URL (sessions/<slug>/) working when the real folder
        # carries an 'NN-' sort prefix.
        if slug != dir_name:
            write_redirect_stub(slug, dir_name)

    if failures:
        print(f"\n{len(failures)} session(s) failed to build: {failures}")
        print("Their index.html files were left untouched (not overwritten with broken output).")

    build_master_index()


if __name__ == "__main__":
    main()
