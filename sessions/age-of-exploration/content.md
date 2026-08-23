# Age of Exploration

---

## Anybody have any Problems?

- Troubles with Copy/Paste
- Inconvenience of Copy/Paste
- Getting things working and then breaking them
- Way too much interaction with confusing code
- Way too much interaction with processes you don't understand

---

## Tooling Up

- You can continue doing reasonable work the way you have been uh with no tools and no expenses
- It gets a lot easier if you can install tools on your laptop
- It gets even easier if you're willing to Incur some minor expenses (~20/month)

---

## Must Have Free Tools

The two immediate "must haves" are:
- **An Integrated Development Environment (IDE)** - This is Where you manage your projects, where you edit your code, and where you get and save your work. You can do this with an editor such as Notepad (or Mac/Linux equivalent) but it's incredibly painful.
- **A Version Control System** - This is where you keep track of versions of your work, save working results, and incrementally improve your project. You can do this with File Explorer (or Mac/Linux equivalent) by maintaining folders for different versions, but it's incredibly painful

I use **[Visual Studio Code](https://code.visualstudio.com/download?_exp_download=fb315fc982)** and **[git](https://git-scm.com/install/)**. I strongly recommend **git** especially if you are going to allow the AI to help you with it.

---

## Tools You Pay For

Adding an AI Coding partner to your IDE is how you offload most of technical details to AI by allowing the AI to edit your files directly and to interact with other tools such as **git**.

All four of the AI options listed in the last session (and no doubt many more) offer such integration. The following slides written by each of these AIs list feratures, costs, and links to get started.

- **[Claude](#/Claude)** — strong at coding, free tier available, requires login (email/Google/Apple).
- **[ChatGPT](#/OpenAI)** — the default most students already know, free tier available, requires login.
- **[Gemini](#/Google-Gemini)** — Google's model, free tier, and it's a natural fit for students who already have school Google accounts since login friction is near-zero for them.
- **[Microsoft Copilot](#/Microsoft-Copilot)** — runs on OpenAI's models; one of the few that's usable with no signup at all for basic chat, though signing in (Microsoft account) raises usage limits.

---

## Claude Code — AI That Edits Your Codebase Directly {#Claude}

**What it is:** A VS Code extension (built on the Claude Code CLI) that lets Claude read, edit, and create files across your whole project — not just answer questions in a chat window.

**IDE integration**
- Docks right into VS Code — sidebar, panel, or its own tab
- Side-by-side diff viewer for every change before you accept it
- @-mention files or your current text selection to give Claude context
- Reads VS Code's own error/warning diagnostics automatically

**Beyond the editor**
- Runs terminal commands, installs packages, and manages **git** (commits, branches, PRs) on your behalf
- Can trigger **deployments** and other project tooling
- Connects to third-party tools/services via **MCP** (Model Context Protocol) — e.g. issue trackers, docs, databases

**Cost**
- Requires **Claude Pro**: **$20/month** (or **$17/month billed annually**)
- Free Claude.ai accounts do **not** include this level of Claude Code access

**Get started:**
- [code.claude.com/docs/en/ide-integrations](https://code.claude.com/docs/en/ide-integrations)

---

## AI-Powered Development with OpenAI Codex {#OpenAI}

- **Codex + VS Code:** AI coding agent that works directly in your codebase
- **Edit & build:** Reads, creates, and modifies files; runs commands, tests, and debugging
- **Developer workflow:** Works with **Git**, terminals, extensions, and external tools
- **Cloud option:** Delegate larger coding tasks to Codex in the cloud while you continue working
- **Cost:** Included with ChatGPT plans; **ChatGPT Plus — $20/month** is a good starting point
- **Get started:** [developers.openai.com/codex/ide](https://developers.openai.com/codex/ide/)

---

## Gemini Code Assist for Development {#Google-Gemini}

- **IDE Integration:** Built-in extension for **VS Code**, JetBrains, and Android Studio supporting real-time code completion, multi-file agentic editing, and conversational debugging.
- **Ecosystem & Tooling:** Seamless connectivity with GitHub (automated pull request reviews), Model Context Protocol (MCP) ecosystems, and Google Cloud services.
- **Pricing:** **$19 per user/month** (annual commitment) or **$22.80/user/month** (monthly plan).
- **Get Started:** [codeassist.google](https://codeassist.google/)

---

## Copilot IDE Integration {#Microsoft-Copilot}

- **Deep VS Code, Visual Studio, GitHub & Azure integration** — inline coding, repo-aware reasoning, PR help, CLI workflows.
- **Works with third-party tools** via extensions, APIs, GitHub Actions, and cloud deployment hooks.
- **Cost:**
  - **Copilot Pro:** $20/month
  - **GitHub Copilot Enterprise:** $39/user/month
- **Get started:** [aka.ms/copilot-vscode](https://aka.ms/copilot-vscode)
- Explore topics: IDE integration, tooling workflows, Copilot pricing
