---
name: write-story
description: Write a teaching story for the Vibe Coding class on a given topic, as a Markdown file in a session folder, ready for the [[story: ...]] directive. Use when the user asks for a story about a topic (e.g. "/write-story Branching and merging").
---

# Write a story

Write a story about the topic the user gave (the arguments to this skill). If the topic or the target session is unclear, ask one short question first.

## Audience and purpose

The audience is non-programmers and non-technical people who are not comfortable with the command line or running tools on their laptop. They are students in a class on creating software by vibe coding: they never edit code or run the tools that build, deploy and test it. The AI does that.

## What the story is

- The story is a conversation between a student and their AI coding partner. In the Git story ([sessions/02-age-of-exploration/git-basics.md](../../../sessions/02-age-of-exploration/git-basics.md)) the student is Maya and the AI is simply "AI". Read it for tone and structure before writing, and keep the same cast unless the user says otherwise.
- Wherever possible, the AI handles all the technical details.
- Where the AI can't (for example, setting up accounts the AI will use), give the student detailed, step-by-step instructions for what *they* must do. Don't skip clicks or assume they know where things are.
- Avoid jargon. When some jargon must be introduced, define it in detail the first time it appears.
- Explain everything as you would to a child: simple words, concrete everyday analogies, short sentences.

## Explain in both directions

Throughout the story, and again in the cheat sheet, explain each idea both ways:

- "If I want to do X to my software, I should ask the AI to do Y."
- "If I ask the AI to do Y, what effect will that have on my software?"

## Required ending

1. **A cheat sheet chapter** summarizing both directions, as two tables (see the Git story's "The Cheat Sheet"): "I want to... so I ask the AI to..." and "I asked the AI to... so what will happen?" Add a short list of golden rules if it helps.
2. **A glossary** as the last section: a bullet list where each term is bold and its explanation is normal text, e.g. `- **Clone:** making a full copy of a project on your computer.` Cover every technical term the story introduces.

## Format (the deck builder only understands this)

The file is rendered by `scripts/build_decks.py` into a vertical stack of slides. Use only:

- `# Title` once, then one `## Chapter N: Title` per chapter (plus `## Epilogue` and `## Glossary ...`). Optionally an italic one-line subtitle under the title.
- `### Sub-topic` headings inside a chapter. **Each `###` starts a new slide**, so use them to break a chapter into slide-sized topics.
- Plain paragraphs, kept short (a slide holds roughly 700 characters).
- Dialogue and the AI's explanations as `>` quoted paragraphs, one speaker per paragraph, with a bare `>` line between paragraphs, e.g. `> **Maya:** ...` then `>` then `> **AI:** ...`.
- `-` bullet lists, `1.` numbered lists, and `| pipe | tables |` with a `|:---|:---|` separator row.
- Inline `**bold**`, `*italic*` and `` `code` `` (use code only for short names like file names, never for long commands). A trailing `\` at the end of a line forces a line break.

Do **not** use: code fences, images, HTML, nested bullets, horizontal rules, or `####` headings. Never show the student a command to type. Show what to *say to the AI* in quotes instead.

## Where to put it

Save it in the session folder the user names (for example `sessions/02-age-of-exploration/`), named after the topic in kebab-case, such as `branching-and-merging.md`. Don't overwrite an existing story without asking.

## After writing

Tell the user the file path and the chapter list, and show how to wire it into that session's `content.md`:

```
---

## Review: <Topic>

- [Read the story](#/<anchor>)
- [Practice the flash cards](#/<anchor>-flashcards)

---

[[story: <file>.md | <anchor>]]

---

## Flash cards: <Topic> {#<anchor>-flashcards}

[[flashcards: <deck>.json]]
```

The flash-card deck comes from the Learn2X extension, so the user exports that JSON separately. Don't edit `content.md` or run the build unless the user asks.
