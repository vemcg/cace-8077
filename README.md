# AI: A Shortcut to Software Design (8077)

Course template repo for an 8-session class. Each session has its own [reveal.js](https://revealjs.com/) slide deck.

## Structure

```
sessions/
  session-01/
    index.html      # the deck for this session
    images/          # 8 background images for this deck: bg-1.jpg ... bg-8.jpg
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

Each deck expects 8 background images (one per slide), named `bg-1.jpg` through `bg-8.jpg`, placed in that session's `images/` folder. These aren't included yet — drop them in as they're provided. If you use a different file extension (`.png`, `.webp`, etc.), update the matching `data-background-image` attribute in that session's `index.html`.

## Viewing a deck

Open `sessions/session-01/index.html` (etc.) directly in a browser. reveal.js is loaded from a CDN, so no build step or local server is required.

## Adding a new session

Copy `sessions/_template/` to a new `sessions/session-NN/` folder, update the session number in the "Topic TBD" heading, and add its 8 background images.

## Setting up as a GitHub template

After pushing this repo to GitHub, enable **Settings > Template repository** so it can be used as a starting point for future course offerings.
