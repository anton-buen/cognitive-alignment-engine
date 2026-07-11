# Cognitive Alignment Engine

### The Precursor to Naur (Archived & Evolved)

* **Current Status:** Archived / Legacy Prototype
* **Successor:** [Project Naur (MCP Edition)](https://github.com/anton-buen/Project-Naur)

This repository holds the architectural history and original prototype of what eventually became Naur. While I have abandoned this codebase, the false starts, design flaws, and unexpected breakthroughs documented here directly shaped my 2026 IBM AI Builders Challenge wildcard entry. If you want to see why I ended up building an autonomous Model Context Protocol (MCP) linter, this is the trail of broken code that got me there.

---

## Chapter 0: Chasing "Cognitive Alignment"

Before I built an MCP server, I started with a basic premise: engineering teams rarely fail because they can't write code. They fail because they aren't picturing the same product. Whether you are grinding through a 48-hour hackathon or managing a corporate project, you quickly run into what I called the Alignment Tax. I lifted that phrase from AI safety literature to describe human communication friction.

When product managers, designers, and backend engineers try to plan features, they speak fundamentally different dialects. They talk past each other, accumulating Comprehension Debt—my slightly dramatic name for the illusion of mutual understanding. The Cognitive Alignment Engine was my first stab at creating an AI translator to fix this intent gap in real-time.

---
[...]
---

## What We Carried Forward

Even though the code in this specific repository is deprecated, I stripped out the core logic and ported it directly into the active version of Naur.

For instance, I kept the Missing Chair Principle, which is just my custom IF/THEN check that looks at who is active in a conversation. If backend and product start making UI choices without a designer present, the engine flags it.

I also preserved the 3-Tiered Translation Engine. This prompting structure forces the LLM to guess the structural impact of a proposal and break it down into explicit engineering requirements, technical justifications, and jargon-free business consequences.

Finally, my early scripts for Ubiquitous Language Enforcement survived. These tools stop people from using the same word—like "cache"—to mean entirely different things, instantly forcing the terms into a shared project glossary.

---

## Archival Notice

This repository remains public as a historical map for anyone interested in seeing how a traditional REST and RAG architecture evolves into an agentic MCP workflow.

To see these same concepts running in a functional workspace managed by IBM Bob, check out the active repository:
👉 **[Explore the Active Naur Repository](https://github.com/anton-buen/Project-Naur)**
