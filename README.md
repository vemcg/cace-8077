# AI: A Shortcut to Software Design (8077)

Course template repo for an 8-session class. Each session has its own [reveal.js](https://revealjs.com/) slide deck, and a master `index.html` links out to all of them.

## Structure

```
index.html           # master index: links to all 8 session decks
assets/
  css/
    style.css         # shared deck styling (title slide, light-image overlay)
    index.css          # styling for the master index page
  images/               # shared background image set, used by every deck
    wright-flyer.svg
    curtiss-jenny.svg
    p51-mustang.svg
    f86-sabre.svg
    f100-super-sabre.svg
    apollo-capsule.svg
    gemini-capsule.svg
    moon-landing.svg
sessions/
  session-01/
    index.html      # the deck for this session
  session-02/
  ...
  session-08/
  _template/         # source template used to generate each session-NN deck
```

Every deck's first slide has the same title/contact info:

1. AI: A Shortcut to Software Design (8077)
2. Vern McGeorge
3. vernmcgeorge@gmail.com
4. 408-256-1849
5. Until you're in my contacts list, leave a message.

Slides 2-8 in each deck are placeholders ("Topic TBD") to be filled in with that session's content.

## Background images

There's one shared set of 8 images in `assets/images/`, reused identically by every session deck — each slide *position* (1st, 2nd, 3rd, ...) always shows the same image across all 8 sessions. The theme is the progression of flight, aviation to spaceflight:

| Slide | Image | Subject |
|---|---|---|
| 1 | `wright-flyer.svg` | Wright Flyer (1903) |
| 2 | `curtiss-jenny.svg` | Curtiss JN-4 "Jenny" |
| 3 | `p51-mustang.svg` | P-51 Mustang |
| 4 | `f86-sabre.svg` | F-86 Sabre |
| 5 | `f100-super-sabre.svg` | F-100 Super Sabre |
| 6 | `apollo-capsule.svg` | Apollo command/service module |
| 7 | `gemini-capsule.svg` | Gemini capsule |
| 8 | `moon-landing.svg` | Astronaut on the Moon |

These are original, simple line-art SVGs (not photos — real photos would carry their own licensing/sourcing concerns), drawn deliberately light so text and printouts stay legible over them. `assets/css/style.css` also lays a translucent white scrim under every slide's text for extra contrast.

Note: slides 6 and 7 are ordered Apollo-then-Gemini to match how they were requested, even though Gemini (1965-66) historically flew before Apollo (1968-72). Swap `data-background-image` on those two `<section>` elements in each deck (and in `sessions/_template/index.html`) if you'd rather have them in chronological order.

To swap in real photos later, replace the files in `assets/images/` (any raster/vector format works) and update the matching `data-background-image` path in each deck if the filename changes.

## Running the slide set

No build step or install is required — reveal.js loads from a CDN — but the decks use `<script type="module">`, and some browsers block ES module imports on pages opened directly via `file://`. So serve the folder locally instead:

```bash
# from the repo root, pick one:
python -m http.server 8000      # Python
npx serve .                     # Node
```

Then open `http://localhost:8000/` for the master index, or jump straight to a deck at `http://localhost:8000/sessions/session-01/index.html`.

Inside a deck: arrow keys / space to advance, `Esc` for slide overview, `S` for speaker notes view.

## Adding a new session

Copy `sessions/_template/` to a new `sessions/session-NN/` folder and update the "Session N" text in the placeholder headings.

## Setting up as a GitHub template

After pushing this repo to GitHub, enable **Settings > Template repository** so it can be used as a starting point for future course offerings.
