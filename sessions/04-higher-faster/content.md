# Higher, Faster

---

## Today's Agenda

- Best practices that make AI-assisted development smoother
- Spec before code
- Let the AI stress-test your own design
- Where things live: hosting, platforms, and frameworks

---

## Write the Spec First

- Before asking the AI to write code, ask it to help you write a short specification: what the app does, who it's for, the core features, and what's explicitly *out* of scope
- A spec turns a vague idea into something the AI — and you — can actually build against
- Keep it short: a page, not a novel

---

## Let the AI Poke Holes

- Once you have a draft spec, ask directly: "What questions do you have? What's underspecified? What could go wrong?"
- Ask it to challenge your assumptions and surface edge cases *before* a line of code exists
- Cheap to fix a design on paper; expensive to fix it after the code is written

---

## Where Will It Live? (Hosting)

- **Just files, no server** *(games, most Far Horizons ideas)*: GitHub Pages, Netlify, Vercel — free, and it's what this course site itself runs on
- **Needs to remember things across visits or devices**: a backend-as-a-service like Firebase or Supabase — no server for you to manage
- **Multiple people sharing the same live data** *(collaboration/community tools)*: the same backend-as-a-service options, or your own small always-on service
- **A long-running process**, something that keeps working when nobody's looking: Render, Railway, Fly.io — "always on" hosting, usually a small monthly cost

---

## Picking a Framework

- You don't need one — plain HTML/CSS/JavaScript (what you used in *First Flight*) works everywhere, forever, no build step
- A framework (React, Vue, Svelte, etc.) pays off once a project gets big enough that plain JS gets unwieldy — not before
- Let the AI recommend one *after* you know what you're building, not before

---

## Your *Higher, Faster* Activity

- Take the project idea from *Far Horizons*
- Ask your AI partner to draft a one-page spec with you
- Ask it what questions it has, and address the biggest ones
- Decide where you'd host it, and why
