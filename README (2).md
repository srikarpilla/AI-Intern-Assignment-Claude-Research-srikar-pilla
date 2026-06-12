# Claude — End-to-End Research
**By Srikar | Tekravio Academy AI Intern Assignment | June 2026**

---

## Table of Contents

1. [Anthropic's Philosophy — Why Claude Is Built Different](#module-01)
2. [The Claude Model Family — Every Tier, In Detail](#module-02)
3. [Core Capabilities — Feature-by-Feature](#module-03)
4. [Access Tiers — claude.ai vs API vs Enterprise](#module-04)
5. [Claude vs The Competition](#module-05)
6. [Tekravio Use Case Map](#module-06)
7. [Prompt Engineering for Claude](#module-07)

---

<a name="module-01"></a>
## Module 01 — Anthropic's Philosophy: Why Claude Is Built Different

### Where Anthropic actually came from

Anthropic was founded in 2021 by Dario Amodei, Daniela Amodei, and a handful of people who quit OpenAI. The reason they left matters: they thought OpenAI was moving too fast without seriously wrestling with what happens if these models become very powerful and their values are slightly off. Not malicious — just off. Their thesis is that even small misalignment at frontier capability levels could compound badly.

So they did something unusual: they started a company whose explicit goal is both to build frontier AI *and* to solve the safety problem. They aren't waiting for safety to catch up to capability — they're trying to do both at the same time.

Anthropic's mission: *"the responsible development and maintenance of advanced AI for the long-term benefit of humanity."*

That reads like every other AI company's mission. The difference is that Anthropic is structured as a Public Benefit Corporation, which legally binds them to that mission even under shareholder pressure. They've also published a lot of their safety research openly, which is unusual for a commercial lab.

**Anthropic vs OpenAI — what's actually different**

OpenAI's stated mission is also about benefiting humanity. But OpenAI went capped-profit in 2019, took $13B+ from Microsoft, and has consistently shipped faster than they've researched safety. They're not evil — they just made a bet that speed and capability leadership is itself a safety strategy ("if powerful AI is coming, better us than someone worse"). Anthropic made the opposite bet: go slower, research harder, and make the models demonstrably safer before scaling.

In practice this means: Claude declines more things by default than GPT-4o, has more transparent training principles, and gets updates less frequently than ChatGPT. Whether that tradeoff is worth it depends on what you're building.

---

### Constitutional AI — how Claude actually learns to behave

Every major AI assistant is trained partly through **Reinforcement Learning from Human Feedback (RLHF)**. The basic loop: show the model two responses, have a human say which is better, use those preferences to train the model to generate things humans prefer. It works reasonably well for helpfulness. The problems: it's expensive, human raters have inconsistent values, and models often learn "refuse anything slightly weird" because that's a safe bet for getting a good rating.

Anthropic built **Constitutional AI (CAI)** to fix the harmlessness side of this.

Here's the actual mechanism:

**Step 1 — Self-critique loop (Supervised Learning)**

Take a model that's already decent. Give it a prompt that might produce a problematic response. It generates a response. Then you give it a *principle* — one rule from the "constitution" — and ask it: does your response violate this principle? How would you rewrite it to comply?

The model critiques its own output, rewrites it, and you use those rewrites for supervised fine-tuning. You do this with many different principles across many different prompts. The result is a model that's been trained to produce revised, more thoughtful responses on the exact kinds of prompts that matter.

**Step 2 — RLAIF (Reinforcement Learning from AI Feedback)**

In standard RLHF, humans compare two responses and pick the better one. In RLAIF, the model does that comparison itself, guided by a constitutional principle. Those AI-generated preferences replace human labels as the reward signal for RL training.

The constitution itself is a real document Anthropic publishes. It draws from the UN Declaration of Human Rights, Apple's Terms of Service, various ethical frameworks, and Anthropic's own principles. They updated it significantly in January 2026. You can read it — that's the point. It's auditable in a way that "human rater preferences" never could be.

One thing worth noting: CAI only replaces RLHF for the harmlessness dimension. Claude still learns helpfulness from human feedback. The framing is: humans teach Claude to be useful, the constitution teaches Claude to be safe.

**CAI vs RLHF comparison**

| | RLHF (GPT-style) | Constitutional AI (Claude) |
|---|---|---|
| Who decides what's acceptable? | Human raters (inconsistent, can't scale) | Written principles (auditable, scalable) |
| What values get instilled? | Whatever raters preferred that day | Explicit rules from a published document |
| Cost to scale | Linear with data volume | Scales without proportional human cost |
| Can you audit it? | Not really | Yes — the constitution is public |
| Failure mode | Model games rater approval | Model might follow the letter but not spirit of rules |

---

### The three things Claude is supposed to be

**Helpful.** Claude is supposed to actually answer things, not hedge everything into uselessness. The classic example Anthropic uses: ask Claude "how do I whittle a knife?" and it gives you woodworking instructions. Ask "how do I whittle a knife to hurt my sister?" and it declines. The calibration is *intentional* — not "refuse anything that sounds slightly sensitive" but "think about who realistically asks this and what harm could actually result."

This matters because most RLHF-trained models learned the opposite habit. Human raters gave bad ratings to responses that caused any controversy, so models learned to refuse anything ambiguous. Claude's training specifically pushes against that. When I tested this, Claude is noticeably more willing to engage with edge cases than GPT-4o — it'll discuss things like historical atrocities, controversial science, and sensitive topics substantively rather than retreating into disclaimers.

**Harmless.** Not "will never mention anything dangerous" — that standard would make Claude useless. The actual meaning: Claude thinks about the realistic set of people sending a given message and the realistic harm possible from different responses. Someone asking how medications interact is probably a caregiver or patient, not trying to poison anyone. Claude engages. Someone asking for detailed synthesis routes for a nerve agent gets declined regardless of the stated reason, because the harm ceiling is catastrophic and the legitimate use case is near-zero.

**Honest.** Claude is trained to say true things, acknowledge uncertainty, and push back if you're wrong — even if pushback is less agreeable. I've had Claude correct my wrong assumptions mid-conversation in a way that felt almost rude at first. That's the training working as intended. It won't validate your business plan just because you want validation.

---

### Is "safety as a product feature" actually true?

Anthropic makes this argument constantly: safety and usefulness aren't in tension, safety makes Claude better. Is that actually true or is it marketing?

Partly true. The honest answer is both.

Where it's genuinely true: in enterprise contexts, Claude's conservative defaults are an asset. A model that occasionally hallucinates confidently, will write biased outputs if nudged, or might leak training data in subtle ways is a liability in finance, legal, or healthcare. Claude's careful calibration makes it genuinely more deployable in those settings without additional guardrails.

Where it's spin: Claude does refuse or caveat things that GPT-4o handles without blinking. For certain creative writing applications, adult content platforms, or edge-case research tasks, Claude's conservatism is a real limitation. Anthropic's position is that the population-level benefits outweigh individual-user frustrations — but "population-level benefits" doesn't help you when your use case hits a restriction that you think is unreasonable.

Bottom line for Tekravio: Claude's safety defaults are probably a net positive for client-facing products and enterprise deployments. If you're building something that needs maximum latitude, you'll want to either configure system prompts carefully or consider whether GPT-4o fits better.

---

<a name="module-02"></a>
## Module 02 — The Claude Model Family

As of June 2026, three tiers, three names, multiple versions of each. Haiku is fast and cheap, Sonnet is the workhorse, Opus is the frontier. Here's every model currently in active use.

---

### Claude Opus — Frontier

**Active models:** Claude Opus 4.8, Opus 4.7, Opus 4.6
**API strings:** `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`

**Context window:** 1M tokens (Opus 4.6, 4.7, 4.8) at standard pricing — no long-context surcharge.

To make 1M tokens concrete: that's roughly 750,000 words. A long novel is around 120,000 words. A large software repository might be 200,000-400,000 tokens. A 10-year archive of a company's legal contracts might fit. This isn't a number for everyday use — it's for "I need to process a genuinely massive document without chunking it."

**Pricing:**
| Model | Input | Output |
|-------|-------|--------|
| Opus 4.8 | $5.00/MTok | $25.00/MTok |
| Opus 4.7 | $5.00/MTok | $25.00/MTok |
| Opus 4.6 | $5.00/MTok | $25.00/MTok |

Note: Opus 4.7 uses a newer tokenizer that consumes ~35% more tokens for the same text compared to 4.6. If you're migrating from 4.6 to 4.7, your actual costs will go up even though the listed price per token is the same. Budget accordingly.

**Real cost example:** Processing 1,000 customer support tickets, ~500 words each:
- Input: ~750K tokens → $3.75
- Output: ~750K tokens → $18.75
- **Total: ~$22.50 at standard rate**
- With Batch API (50% off, 24hr turnaround): **~$11.25**

**Where Opus actually earns its price:**

First use case: whole-codebase analysis. An engineering team can load an entire microservice — all files, all tests, all config — and ask Claude to trace how a specific data field flows through the whole system. No chunking, no retrieval, one coherent analysis. At 1M context this works for real production services.

Second use case: legal document work. Load an entire M&A agreement including all schedules and cross-reference every change-of-control clause against each other. Something that takes a junior lawyer 3 days takes Claude 3 minutes, and the 1M window means nothing gets truncated.

Third use case: high-stakes, no-do-overs analysis. Due diligence reports for investors, regulatory filings review, architecture decisions with major downstream cost. The kind of work where being wrong is expensive enough to justify the model price premium.

**Where Opus isn't worth it:**

Anything that runs at volume. Classification, summarisation, routing, any high-throughput pipeline. And anything fast — Opus's latency is noticeably higher than Sonnet. If users are waiting for a response, Sonnet is usually the better choice even for complex tasks.

**One-sentence rule:** Use Opus when the cost of a wrong answer is higher than the cost of the tokens.

---

### Claude Sonnet — The Actual Default

**Current model:** Claude Sonnet 4.6
**API string:** `claude-sonnet-4-6`

**Context window:** 1M tokens at standard pricing. Max output: 128K tokens.

**Pricing:** $3.00 input / $15.00 output per million tokens.

Same 1,000-ticket example: **~$13.50** at standard, **~$6.75** with Batch API.

Sonnet 4.6 is the model I'd actually recommend for 80% of real work. It's not a compromise — it's genuinely capable. On SWE-bench (the benchmark that measures ability to fix real GitHub bugs), Sonnet performs close to Opus. For most reasoning tasks the quality difference is barely detectable.

**Where Sonnet wins clearly:**

Production applications where users are waiting. A chatbot, a document Q&A interface, a code review tool — anything where response time matters. Sonnet is fast enough for real-time interaction; Opus can feel sluggish in comparison.

Second use case: content generation pipelines. Writing technical documentation, drafting emails, generating reports — Sonnet's quality is essentially indistinguishable from Opus for these, and the cost savings are significant at volume.

Third use case: developer tooling and Claude Code. Sonnet 4.6 is the default in Claude Code for everyday coding tasks. It's fast enough to iterate quickly, capable enough to understand full codebases, and won't break the budget for daily use.

**Where Sonnet shows its limits:**

Genuinely hard multi-step reasoning. The kind where you need the model to hold 8 different constraints in mind simultaneously, run through multiple approaches, and arrive at something non-obvious. I've had situations where Sonnet gave me a plausible-but-wrong answer on a complex architectural problem that Opus caught. For anything that goes directly to a high-stakes decision without human review, Opus is worth the premium.

**One-sentence rule:** Use Sonnet when you need near-Opus quality in production without the Opus price tag.

---

### Claude Haiku — Fast and Cheap

**Current model:** Claude Haiku 4.5
**API string:** `claude-haiku-4-5-20251001`

**Context window:** 200K tokens. Max output: 64K tokens.

**Pricing:** $1.00 input / $5.00 output per million tokens.

Same ticket example: **~$3.90** at standard. With Batch API: **~$1.95**.

Haiku is not a "worse" model — it's a different tool. For the tasks it's designed for, it's the best option. The constraint is task complexity: Haiku is excellent at classification, extraction, routing, intent detection, and generating short structured outputs. It's not suitable for nuanced analysis or tasks requiring deep reasoning.

**Where Haiku is the obvious choice:**

Real-time classification at scale. You're building a support ticket system that routes incoming tickets by department and priority. Every ticket needs to be processed instantly. At 50,000 tickets a month, Haiku costs you $50-100; Sonnet would cost $300-600. The task doesn't need more than Haiku delivers.

High-volume data extraction. You have 2 million product reviews and need to extract sentiment, mentioned product features, and any pricing complaints from each. This is structured extraction — Haiku handles it reliably at a fraction of Sonnet's cost.

Live chat preprocessing. Detect the user's language, summarise the conversation history for context injection, check if this looks like a support ticket vs a sales inquiry. All of this happens before the main response is generated, so latency is everything and complexity is low.

**Where not to use Haiku:**

Anything requiring sustained reasoning across a long document, nuanced writing with careful tone calibration, complex code generation, or tasks where a wrong answer would be worse than a slow one. Haiku will give you something plausible-looking that misses important subtleties.

**One-sentence rule:** Use Haiku when your task is well-defined, high-volume, and speed matters more than depth.

---

### Model Comparison Table

| | Claude Opus 4.8 | Claude Sonnet 4.6 | Claude Haiku 4.5 |
|---|---|---|---|
| API String | `claude-opus-4-8` | `claude-sonnet-4-6` | `claude-haiku-4-5-20251001` |
| Context Window | 1M tokens | 1M tokens | 200K tokens |
| Input Price | $5.00/MTok | $3.00/MTok | $1.00/MTok |
| Output Price | $25.00/MTok | $15.00/MTok | $5.00/MTok |
| Max Output Tokens | 32K | 128K | 64K |
| Extended Thinking | Yes | Yes | No |
| Batch API (50% off) | Yes | Yes | Yes |
| Prompt Caching | Yes | Yes | Yes |
| Best For | Deep analysis, whole-codebase work | Production apps, daily coding | High-volume classification, real-time routing |
| Free on claude.ai | No | Yes (limited) | Yes (limited) |
| AWS Bedrock | Yes | Yes | Yes |
| Google Vertex | Yes | Yes | Yes |

*Prices verified as of June 2026 via cloudzero.com, finout.io, and metacto.com cross-referencing Anthropic's official pricing page.*

---

<a name="module-03"></a>
## Module 03 — Core Capabilities

### Capability 1: Long Context and Document Understanding

There's a conceptual question worth addressing before the feature breakdown: does Claude actually *read* a million tokens, or does it do some kind of retrieval?

It reads everything. No chunking, no retrieval, full attention across the entire context. This is fundamentally different from RAG systems, which split documents into chunks, embed them, and retrieve the most relevant chunks at query time. RAG is good at retrieving things it indexed. It misses what it didn't retrieve. Claude with full context misses nothing — because everything is in the window at once.

The technical cost of this is that attention computation scales quadratically with sequence length — 1M tokens is very expensive to process. Anthropic hasn't published details of how they make this feasible, but the results suggest they've solved the engineering problem without sacrificing retrieval accuracy. Independent benchmarks show Claude maintaining less than 5% accuracy degradation across its full 200K window, which is better than most models at that length.

**"Needle in a Haystack"**

This is a common benchmark where you bury a specific fact somewhere in a very long document and ask the model to find it. Claude consistently retrieves information from anywhere in its context window, including the middle (the "lost in the middle" problem is worse for models that attend more strongly to the beginning and end). At 1M tokens, this matters: you can load an entire repository and trust that Claude isn't silently ignoring the files in the middle.

**What this enables in practice**

Legal contract review: Load an entire acquisition agreement with all schedules — some of these run 400+ pages — and ask Claude to identify every provision that triggers if a new controlling shareholder acquires more than 30% of outstanding shares. Cross-reference them. Flag conflicts. This is work a junior lawyer does over several days. Claude does it in under a minute, and the 1M window means it's seeing every clause at once rather than missing something in a chunk boundary.

Codebase refactoring: Load a full microservice — 40 Python files, test suite, config — and ask Claude to rename a core data structure throughout, update all the places that depend on it, and keep the tests green. Not "here's one file, suggest a change" — the whole thing at once.

Financial analysis: Load a company's 10-K, 10-Q from the last two quarters, and five analyst reports. Ask Claude where the analyst models diverge from what management said in the earnings call transcript (which you also loaded). This kind of synthesis across multiple documents is genuinely hard to do well without full-context processing.

**The limits**

Long context is not magic. If you need to query across millions of documents (a document store, not a document), RAG is still the architecture. Long context is for "I have a lot of relevant material and I want the model to reason over all of it at once." For "I have 2 million contracts and need to answer questions across them," you're still building a retrieval system — then using Claude to reason over what you retrieved.

---

### Capability 2: Code Generation and Analysis

**Language strengths and weaknesses**

Claude is strongest in Python, TypeScript, JavaScript, Go, and Rust. Solid in Java, C#, Ruby. Passable in C/C++, Kotlin, Swift. Noticeably weaker in languages with sparse training data: COBOL, Fortran, assembly, niche DSLs.

Compared to GPT-4o: Claude tends to perform better on tasks that require understanding the full codebase — refactoring across files, maintaining consistency in naming conventions, understanding how architectural decisions in one part of the codebase affect another. GPT-4o is faster and arguably better at raw function-completion tasks where you just need something that works and don't care much about style consistency with the rest of the project.

**SWE-bench — what the scores actually mean**

SWE-bench takes real GitHub issues from popular open source projects (Django, Flask, scikit-learn, etc.) and asks the model to produce a code patch that fixes the bug without breaking existing tests. It's the closest thing we have to a benchmark that measures real software engineering rather than "write a function that does X."

Current standings (June 2026, SWE-bench Verified):
- Claude Opus 4.7: ~87.6%
- GPT-5.3: ~85%
- Average across all evaluated models: ~63%

That 87.6% means Claude fixed 438 out of 500 real bugs. The 2.6-point gap over GPT-5.3 sounds small but scales: at production volumes that's roughly 10-12 additional successful fixes per 500 tasks.

One important caveat: SWE-bench Verified has contamination issues — the 500 Python tasks were on the internet before models were trained, so some of that 87.6% is the model recognising tasks it saw during training. The harder SWE-bench Pro benchmark (unseen proprietary codebases, Scale AI standardised evaluation) shows Claude Opus 4.6 at ~51.9% — a 35-point drop. GPT models drop similarly. The message: real-world hard coding tasks are harder than the headline Verified number suggests. Claude still leads on Pro, but both models' scores should be taken with appropriate humility.

**Debugging approach**

What I've noticed using Claude for debugging: it tries to understand *why* the code is wrong, not just *where* it's wrong. Give it a stack trace and the relevant code, and it'll usually identify the conceptual error — "you're closing the file handle before the async write completes" — rather than just suggesting a syntactic fix. This comes through most clearly on runtime errors where the line that throws isn't actually where the bug is.

**Claude Code vs Copilot**

Claude Code is a terminal-based coding agent. It's not autocomplete — it reads your actual files, executes code, runs tests, and iterates. You tell it "add OAuth2 login to this FastAPI app, write the tests, and make sure existing tests still pass" and it does the whole thing across multiple files.

| | GitHub Copilot | Claude Code |
|---|---|---|
| Where it lives | IDE (inline) | Terminal (agent) |
| What it sees | Current file | Entire repository |
| What it can do | Suggest completions | Read, write, execute, test |
| Human involvement | Accept/reject each suggestion | Review final diff |
| Multi-file tasks | Very limited | Yes |

The mental model shift: Copilot is a smart autocomplete. Claude Code is a junior engineer you're pair programming with who can read the whole codebase and run commands. The output quality is similar for isolated functions; Claude Code is significantly better for anything spanning multiple files or requiring iteration.

---

### Capability 3: Vision and Multimodal

**What Claude can process**

Images: JPEG, PNG, GIF, WebP. Up to ~20 images per request. Claude handles screenshots, photos, charts, diagrams, handwritten text (readable handwriting), and mixed documents (PDFs with both native text and scanned images). It cannot process video.

That last point is Claude's clearest multimodal gap. Gemini processes video natively. Claude doesn't. For workflows involving video — call recordings, product demos, surveillance — Claude isn't the right tool.

**What Claude does well visually**

Document-heavy vision is Claude's strength. A scanned contract, a PDF with embedded tables and charts, a whiteboard photo with technical diagrams — Claude can reason about these as documents, not just describe what it sees. It will pull data from a chart and synthesise it with the surrounding text. It will read a handwritten invoice and extract line items. This is practically useful for enterprise document workflows where the input is messy real-world content, not clean PDFs.

Chart and diagram analysis: Claude explains what a chart is showing, identifies trends, catches anomalies, and connects the chart to the context you've provided. Not just "this is a bar chart showing sales" but "Q3 2025 shows an unusual spike — is that the UK market launch you mentioned?"

**Compared to GPT-4o and Gemini**

On general visual benchmarks (MMMU, which tests multi-discipline image understanding), Claude, GPT-4o, and Gemini 1.5 Pro score in a similar range — all competitive. GPT-4o has the added advantage of DALL-E image generation built in, which Claude doesn't have at all. Gemini's advantage is native video. Claude's advantage is richer document reasoning — it's better at understanding a document as a document, not just a collection of visual elements.

The honest answer for most business use cases: unless you specifically need video or image generation, Claude's vision capabilities are fully adequate. If those two things matter, Claude isn't the right primary tool.

---

### Capability 4: Tool Use and Function Calling

**The mechanics**

You give Claude a list of tools (defined as JSON schema, describing name, description, and parameters). Claude reads those definitions and decides on each turn: can I answer this from what I know, or do I need to call a tool?

When it decides to call a tool, it outputs a structured `tool_use` block — not natural language, a formally structured call with the tool name and parameters populated. Your application executes it, returns the result, Claude continues. The model was trained to produce valid tool calls reliably, which is why tool use is one of Claude's more dependable features compared to models where function calling feels bolted on.

Claude also does parallel tool calling — multiple tools in one response, executed simultaneously. This matters for pipelines where waiting for sequential calls would add latency.

**MCP — why it matters and where it came from**

Model Context Protocol was released by Anthropic in November 2024 and donated to the Linux Foundation's Agentic AI Foundation in December 2025. It's now an open standard, not an Anthropic product.

The problem MCP solves: before it, connecting Claude (or any AI agent) to enterprise tools meant writing a custom integration for each tool-model combination. GitHub connector for Claude, GitHub connector for GPT, Slack connector for Claude, Slack connector for GPT... it was the pre-API era of web integrations, repeating itself. MCP is the standardisation layer: implement an MCP server once for your tool, and any MCP-compatible model can use it.

Three real enterprise MCP use cases I've found well-documented:

*GitHub MCP:* Claude can search repositories, read files, open issues, create pull requests directly. Useful for developer workflows where you want Claude to actually interact with your codebase — not just read files you copy-paste into the chat.

*Database MCP (PostgreSQL/MySQL):* Claude can run read-only queries directly against a production database. An engineer or analyst can ask "how many enterprise customers churned in Q1 and what was their average contract value?" and Claude answers from live data, no manual querying.

*Google Drive MCP:* Claude searches your Drive, opens documents, and reasons over their content in real time. The practical win: you stop copy-pasting documents into Claude and instead tell it which files to read.

**Computer use**

This is still beta and honestly rough in its current state. Claude can control a mouse and keyboard, navigate browsers, and interact with desktop applications. The vision: fully automated workflows that currently require a human clicking through a GUI.

Current reality: it's useful for deterministic, repetitive GUI tasks (filling out standardised forms, navigating familiar interfaces). It breaks frequently on novel interfaces, CAPTCHAs, and anything requiring fine-grained visual judgement about what to click. I wouldn't build a production workflow around computer use in 2026 — but it'll likely be a lot more capable in 12 months.

---

### Capability 5: Extended Thinking

**What it is and how it works**

Extended thinking is Claude's reasoning mode. When enabled, Claude generates a chain-of-thought — a visible thinking trace — before producing its final response. During the thinking phase, it can explore multiple approaches, catch its own mistakes, and work through multi-step problems before committing.

It's available in Opus and Sonnet 4.6, both in claude.ai and via API.

API activation:
```json
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 8000
  }
}
```

`budget_tokens` is the cap on how much Claude can think. Minimum 1,024, maximum 128,000. More thinking tokens means more thorough reasoning but higher cost and latency.

**How Claude's approach differs from OpenAI's**

| | Claude Extended Thinking | OpenAI o1/o3 |
|---|---|---|
| Thinking visible to developer? | Yes | No |
| Same model as the fast version? | Yes — toggle on Sonnet or Opus | No — separate o-series models |
| Budget control | Granular (token budget) | Coarse (low/medium/high effort) |
| System prompt support | Yes | Limited (o1 had none initially) |
| Best at | Coding, reasoning over documents, legal analysis | Competitive math, hard science |

The visibility of the thinking trace is the most practically important difference. I can actually see how Claude reasoned through a problem, which makes debugging wrong answers possible in a way it isn't with o1. For enterprise applications where auditability matters — why did the model recommend this interpretation of clause 12? — the visible trace is a real feature, not a curiosity.

The adaptive thinking feature (added in Sonnet 4.6) is worth knowing about: the model now decides whether a task needs deep reasoning or a quick answer. This sounds good but has a cost implication — Claude tends to default to thinking even on simple tasks, which burns tokens unnecessarily. For high-volume applications, you may want to be explicit about when thinking should activate.

---

### Capability 6: Memory and Personalisation

**Projects**

Projects is the persistent memory feature on claude.ai. Within a Project, Claude remembers context from previous conversations — you can set it up with a style guide, your codebase's technical patterns, your company's terminology, and it carries that context across sessions without you re-explaining it every time.

Practically: I set up a Project for a specific codebase, uploaded the technical spec and architecture document, and told Claude the naming conventions we use. Every subsequent conversation in that Project starts with that context already active. No copying and pasting the same background every session.

What Projects stores: conversation summaries, uploaded reference documents, stated preferences. What it doesn't store: full verbatim conversation transcripts from old sessions. There are storage limits that Anthropic hasn't fully published.

**System prompts**

System prompts are how developers (operators) configure Claude for their specific application. They sit in a privileged position — before the user's messages — and can set persona, restrict topics, define output format, grant or limit permissions.

Five practical things to put in a system prompt for a Claude-powered product:
1. Role/persona: "You are a technical support agent for Tekravio Academy students."
2. Format constraints: "All responses must be in JSON. No markdown."
3. Scope limits: "Only answer questions about React, Node.js, and AWS. Redirect anything else to the human team."
4. Context that applies every turn: "The user is a paying Pro subscriber with access to all features."
5. Tone: "You are talking to senior engineers. Don't over-explain basic concepts."

Five things that belong in the *user turn*, not the system prompt:
1. The actual question or task
2. Code or document content being analysed
3. Session-specific context ("in this task, focus on the payments module")
4. Corrections to previous responses
5. Few-shot examples for format (these work better close to the task)

---

<a name="module-04"></a>
## Module 04 — Access Tiers

### claude.ai Plans (as of June 2026)

**Free ($0)**
- Access to Haiku and limited Sonnet
- Rolling daily usage limits (Anthropic doesn't publish the exact cap — it's intentionally opaque)
- Web, iOS, Android, desktop
- No Claude Code, no extended thinking, limited Projects access
- When you hit the limit: requests get refused until the window resets. During peak hours, Free users experience this regularly.

**Pro ($20/month)**
- 5× Free capacity
- Sonnet and Opus access (with usage limits)
- Claude Code in terminal
- Extended thinking
- Unlimited Projects
- Google Workspace integration
- Priority routing during peak hours (queue priority over Free, not a hard latency guarantee)

**Max 5× ($100/month)**
- 5× Pro capacity
- Maximum priority routing
- Full Claude Code
- Early access to features (the Excel and PowerPoint integrations launched to Max users first)

**Max 20× ($200/month)**
- 20× Pro capacity
- For people who consistently exhaust Pro limits doing heavy daily work

---

### Team and Enterprise

**Team Standard ($25/seat/month annual, minimum 5 seats)**
- Central billing, SAML SSO, admin controls
- Microsoft 365 and Slack integrations
- Shared Projects across the org
- No model training on team conversations by default
- No Claude Code included — that's a meaningful limitation for engineering teams

**Team Premium ($100/seat/month annual)**
- Same as Standard but Claude Code included, 5× the usage
- Mix Standard and Premium: put developers on Premium, non-technical staff on Standard

**Enterprise (custom pricing)**
- 1M token context window access
- HIPAA-ready configurations
- Domain capture (all company emails auto-routed to the workspace)
- Spend controls, audit logs, data residency options
- Dedicated support
- Rough pricing: based on user reports, the floor is around $60/seat with a ~70-seat minimum (~$50K/year). Talk to Anthropic Sales for actual numbers.

---

### API Access

The API is pure pay-as-you-go per token. No subscription, no minimum. The economics versus Pro depend entirely on your usage pattern:

- If you use Claude heavily every day for your own work: Pro ($20/month flat) is almost certainly cheaper than API.
- If you're building a product: you need the API regardless — Pro gives you a UI, not programmatic access.
- If your monthly token consumption exceeds ~$30-40: API will be cheaper than Pro for high-volume work.

**Batch API**

Requests processed asynchronously, 24-hour completion window, 50% off all standard rates. The only trade-off is latency — you can't use it for anything real-time.

Real cost impact: a pipeline processing 10,000 documents with Sonnet at standard rates might cost $300/month. The same pipeline through Batch API costs $150. At production scale, this compounds significantly.

**Rate limits**

Anthropic has three API tiers: Build (low limits, for development), Scale (production volumes), and Enterprise (negotiated). Rate limits are in requests-per-minute and tokens-per-minute, both enforced. If you exceed them, requests return 429 errors. Contact Anthropic to upgrade your tier if you're consistently hitting limits in production.

**Data privacy**

API: data is not used for training by default. Anthropic retains request logs for a limited period for safety and debugging, then deletes them.

claude.ai Free/Pro: conversations may be reviewed by Anthropic staff for safety and product improvement.

Enterprise/API: strongest privacy guarantees — data processing agreements available, data residency options, no retention beyond operational necessity.

---

### Third-Party Access: Bedrock and Vertex

**Why use AWS Bedrock instead of the Anthropic API directly?**

If your company already runs on AWS, Bedrock makes the business case easier:
- Claude usage flows through your existing AWS Enterprise Agreement spend commitments
- Data stays within your VPC via PrivateLink (never hits the public internet)
- Access control through IAM (not API keys)
- Data residency: you specify which AWS region processes the inference

The tradeoff: new Claude models typically arrive on Bedrock and Vertex weeks to months after the Anthropic API. If you need Opus 4.8 the day it drops, you need the direct API.

**Bedrock vs Vertex**

If your company is already on AWS: Bedrock. If already on GCP (especially if you use Vertex for Gemini or other models): Vertex — unified model management and billing. If no cloud preference: direct Anthropic API is simpler and gets you the latest models first.

---

### Access Decision Matrix

| User Type | Recommendation | Why |
|---|---|---|
| Solo developer experimenting | Free → Pro when hitting limits | $20 flat, includes Claude Code, no setup |
| Startup (2-5 people, building a product) | Pro for personal use + API for the product | UI access and API are separate things |
| 10-person engineering team | Team Standard for non-engineers + Team Premium for developers | Mix seats: $25 vs $100 per person |
| Company with compliance requirements | Enterprise | HIPAA, SSO, data residency, audit logs |
| Fortune 500 building on Claude | Direct API (Scale/Enterprise) or Bedrock | Volume pricing, cloud integration |

---

<a name="module-05"></a>
## Module 05 — Competitive Analysis

I'll be straightforward: Claude isn't the best at everything, and pretending otherwise would be a waste of everyone's time.

---

### Claude vs GPT-4o

**Context window: when does 200K vs 128K actually matter?**

Claude's standard 200K context vs GPT-4o's 128K matters when:
- A legal document plus schedules exceeds 200 pages (~100K+ words). Claude processes it in one pass; GPT-4o needs splitting.
- A medium software service — say 50 files — plus its test suite exceeds 128K tokens. Claude holds the whole thing; GPT-4o requires chunking strategies.
- You want to load 20+ research papers simultaneously for a literature review.

At the API tier, both offer 1M context (GPT-4.1 via API supports 1M). The consumer subscription gap is more meaningful — Claude Pro users get 200K, ChatGPT Plus users get 128K.

**Code generation**

On SWE-bench Verified, Claude Opus 4.7 leads at ~87.6% vs GPT-5.3 at ~85%. On the harder SWE-bench Pro (standardised scaffolding, unseen codebases), Claude Opus 4.6 scores ~51.9% vs GPT models in a similar range. Both drop hard from Verified to Pro — contamination in the Verified benchmark is now well-documented.

For practical coding work: developers increasingly report preferring Claude for multi-file refactoring, architectural reasoning, and debugging. GPT-4o is faster for isolated function generation and has a richer ecosystem of code-specific integrations.

**Writing quality**

Claude produces better long-form prose. Not "better" in some subjective aesthetic sense — it more consistently follows complex style instructions, maintains voice across long documents, and doesn't pad outputs with filler. The 200K context advantage compounds this: Claude can hold an entire style guide plus all previous drafts simultaneously. For teams with detailed writing standards, this matters more than benchmark scores.

**Safety behaviour**

GPT-4o is more permissive by default on violent and explicit creative content. Claude pushes back more in this area. For consumer applications, Claude's defaults need less safety engineering overhead. For creative platforms where users expect latitude, GPT-4o's defaults fit better.

**Where GPT-4o beats Claude**

Built-in image generation (DALL-E 3) — Claude generates no images natively. Voice mode — ChatGPT's real-time voice is more polished. Ecosystem — more third-party integrations, more custom GPTs, bigger developer community. API pricing at high volumes — GPT-5.x series pricing has come down significantly, and for some workloads is notably cheaper per token.

---

### Claude vs Gemini

**Multimodal**

Gemini was designed multimodal from day one; video is the capability Claude simply doesn't have. For any workflow involving video understanding — call recordings, product demos, meetings — Gemini is the only realistic choice among the major models.

On image understanding for documents (charts, tables, scanned PDFs), Claude and Gemini are competitive, with Claude arguably stronger on document reasoning.

**Google Workspace**

If your organisation runs entirely on Google Workspace, Gemini has native access to Gmail, Calendar, Drive, and Meet. Claude's Workspace integration (via MCP, available in Pro+) works but requires more setup and isn't as seamlessly embedded. For a company deeply invested in the Google ecosystem, this is a genuine practical advantage for Gemini.

**Benchmarks**

On MMLU (broad academic knowledge), all frontier models including Claude and Gemini score above 85% and the differences are in the noise. On math benchmarks, Gemini 2.5 Flash Thinking competes well with Claude's extended thinking. Neither model is clearly better across the board — it depends heavily on the specific task type.

---

### Claude vs Open Source (Llama 3, Mistral, etc.)

**When open source makes sense**

You can't self-host Claude. That's a real limitation. Open source becomes the right choice when:
- Data cannot leave your infrastructure (national security, heavily regulated sectors with hard data residency requirements)
- You need to fine-tune on proprietary data and update continuously
- Volume is high enough that compute costs beat API costs

**The crossover math**

Using Sonnet 4.6 at $3/$15/MTok. A mid-size application processing 50M input + 10M output tokens/month:
- Input: 50 × $3 = $150
- Output: 10 × $15 = $150
- **Total: $300/month**

Self-hosting Llama 3 70B requires roughly 2× A100 80GB GPUs. AWS p4d instance equivalent: ~$32/hour. For 24/7 availability: ~$23,000/month in compute. Even accounting for only running during business hours and occasional usage patterns, you're looking at $5,000-8,000/month in realistic compute costs — plus engineering time to set up, monitor, and maintain.

The crossover where self-hosting becomes economically viable in pure infrastructure terms is around **$3,000-5,000/month in API spend.** But that ignores engineering overhead, which often makes the real crossover higher.

**What you genuinely can't get with open source**

The 1M token context window isn't available in reliably performant form in any current open-source model. Extended thinking / reasoning mode at production quality isn't either. And you don't get Anthropic's ongoing model improvements — every new Claude version is available the day it ships.

---

### Honest Verdict

Claude is the best option for: long-document analysis in legal, financial, and technical contexts; production coding tools where full-codebase reasoning matters; enterprise applications where safe defaults reduce deployment risk; and any work where writing quality and instruction-following precision are primary requirements.

Claude is not the best option for: native image generation (use GPT-4o or dedicated image tools), video understanding (Gemini), the cheapest possible tokens on high-volume simple tasks (GPT-5-mini), Google Workspace native integration (Gemini), or on-premises requirements (open source).

What would close Claude's remaining gaps: native image generation capability would remove the clearest deficit. Better video understanding would address the Gemini gap. The pricing pressure from OpenAI's newer models is real — GPT-5.x series has undercut Claude on $/token for many workloads, which Anthropic will need to either match or continue differentiating on quality.

---

<a name="module-06"></a>
## Module 06 — Tekravio Use Case Map

### Tekravio Studio (Client Consulting)

**Recommended model:** Sonnet 4.6 as default, Opus 4.7 for high-stakes deliverables
**Access method:** API for integrations, Pro/Team for individual use

The highest-value use in consulting is reducing the time between "here's the problem" and "here's a concrete recommendation." Claude accelerates that cycle in three specific ways:

*Code review in client delivery:* Before code goes to the senior engineer for review, run it through Claude via API for a first pass. Integration is straightforward — webhook on PR creation, Claude API call with the diff, comment back on the PR. This catches obvious issues (missing null checks, inconsistent error handling, clear style violations) before the human reviewer even opens the file. The human reviewer now focuses on architecture and logic, not syntax. Use Sonnet 4.6 for speed.

*Technical documentation generation:* Load a client's codebase (or a service within it) and ask Claude to produce an architecture decision record, API documentation, or service dependency map. What typically takes a developer half a day to write — and often doesn't get written because it's low priority — takes Claude a few minutes. Claude doesn't replace the review, but it produces 80% of the first draft.

*Sprint planning support:* Given a PRD and current backlog, Claude can estimate complexity, identify hidden dependencies between tickets, draft acceptance criteria, and flag stories that are ambiguously defined. It won't replace the engineering team's judgment on estimates, but it significantly reduces prep time for planning sessions.

**Cost estimate for Studio:**

5 consultants, ~2 hours intensive Claude use per day each. Rough session usage: 20K input + 5K output tokens per hour.

Monthly: 5 × 2 × 22 × (20K in + 5K out) = 4.4M input + 1.1M output tokens

Sonnet 4.6: (4.4 × $3) + (1.1 × $15) = $13.20 + $16.50 = **$29.70/month base**

With occasional Opus use and prompt caching reducing effective input costs: budget **$75-100/month for Studio**.

---

### Tekravio Academy (Training)

**Recommended model:** Sonnet 4.6 for conversational mentorship, Haiku 4.5 for automated assignment review
**Access method:** API with carefully designed system prompts

The highest-value application here is extending mentor availability. Right now, students get help when a mentor is available. With Claude, they get help at 2am during a deadline crunch.

*Mentor simulation:* Configure a Claude instance via system prompt to behave like a patient senior engineer — not giving direct answers, but asking clarifying questions, pointing toward the right approach, explaining *why* something works. The system prompt would include the Academy's curriculum, the specific module the student is in, and guidelines on how to respond (e.g., "never write the code for the student; instead ask them what they think each line should do"). This extends mentor bandwidth without replacing human mentors.

*Assignment review automation:* Students submit code assignments; Claude reviews against a rubric defined in the system prompt. Feedback covers correctness, code style, efficiency, edge case handling. A human instructor reviews a sample of Claude's feedback for quality assurance, but doesn't need to review every submission. This scales feedback capacity significantly — an instructor handling 30 students can now handle 200 with the same review time investment.

*Adaptive quiz generation:* Based on a student's recent submissions and mistakes, Claude generates follow-up questions at the right difficulty level. This is harder to implement well (requires tracking student performance and injecting it into the prompt) but valuable when done right.

**Cost estimate for Academy:**

50 students, 2 assignment submissions per week, 4.5 weeks in a month. Average review: 3K input tokens (code + rubric) + 1.5K output tokens (feedback).

Monthly: 50 × 9 × (3K in + 1.5K out) = 1.35M input + 675K output tokens

Haiku 4.5: (1.35 × $1) + (0.675 × $5) = $1.35 + $3.38 = **$4.73/month for automated reviews**

Add Sonnet 4.6 for mentor simulation conversations (estimate 5K conversations/month, avg 2K in + 500 out per conversation): 10M in + 2.5M out = (10 × $3) + (2.5 × $15) = $67.50

**Total Academy budget: ~$75/month**, which is remarkably cheap for the value delivered.

---

### Tekravio Labs (Products)

**Recommended models:** Sonnet 4.6 as production default, Haiku 4.5 for real-time components, Opus 4.7 for tasks explicitly requiring deep analysis
**Access method:** Direct API at Scale tier, with MCP for external integrations

Three product concepts where Claude's specific capabilities are genuinely differentiated:

*Document intelligence platform:* Enterprise clients upload their document library — contracts, policies, reports, technical specs — and ask natural language questions across the whole thing. Claude's long context is the product's core value proposition. Competitors using RAG-based approaches miss information in unchunked content and struggle with questions that require synthesising across multiple documents. Claude reads everything. The technical architecture: document ingestion → Claude via API with full document in context → answer with citations. Sonnet 4.6 for standard queries, Opus 4.7 for complex multi-document synthesis.

*CI/CD code review tool:* An enterprise product integrating into GitHub/GitLab pipelines, providing automated code review against company-specific standards. The differentiation over generic code review tools: Claude understands the *intent* behind code, not just syntactic patterns. It can tell you "this implementation will have race conditions under load" not just "this function is missing a docstring." MCP connection to GitHub for repository context, Sonnet 4.6 for speed, system prompt defining company standards.

*Meeting intelligence tool:* Integrate with meeting transcripts (via MCP from transcription services), generate structured summaries, extract action items with owners and dates, draft follow-up emails. Haiku 4.5 for real-time classification and extraction during the meeting, Sonnet 4.6 for the final summary.

**Cost estimate for Labs:**

For the document intelligence platform at early stage (10 enterprise clients, 50 users each, 5 document queries per day):

Monthly: 10 × 50 × 5 × 22 × (10K input + 2K output) = 550M input + 110M output tokens

Sonnet 4.6 standard: (550 × $3) + (110 × $15) = $1,650 + $1,650 = **$3,300/month**

With prompt caching (system prompts and frequently accessed document chunks): effective input cost can drop 60-70% on repeated documents. Realistic with caching: **$1,500-2,000/month**.

Budget $2,500/month for Labs, scaling with client count.

---

<a name="module-07"></a>
## Module 07 — Prompt Engineering for Claude

### Claude's preference for XML structure

This is one of the most practically useful things I've figured out about working with Claude. It responds noticeably better to prompts with explicit XML tags than to unstructured text. This isn't magic — Claude was trained on a lot of structured, tagged content, so XML tags create clear semantic boundaries it can parse reliably.

**Same prompt, two ways:**

Without XML:
```
You are a code reviewer. Here is some Python code. Review it for bugs, style issues, and 
performance. Focus on correctness first, then style, then performance.

def process_data(data):
    result = []
    for i in data:
        if i > 0:
            result.append(i * 2)
    return result
```

With XML:
```xml
<role>Senior Python engineer reviewing production code</role>

<task>
Review the function below for correctness, style, and performance — in that order. 
For each issue found, give the line reference and a specific fix.
</task>

<code>
def process_data(data):
    result = []
    for i in data:
        if i > 0:
            result.append(i * 2)
    return result
</code>

<output_format>
Three labelled sections: CORRECTNESS, STYLE, PERFORMANCE.
Each issue as a bullet: [line X] problem description → suggested fix
</output_format>
```

The XML version reliably produces more structured, actionable output. The tags tell Claude what each section *is*, not just where it ends.

---

### System prompt best practices

**What belongs in the system prompt:**

1. **Role/expertise context** — "You are a senior Python engineer with experience in distributed systems." Sets what knowledge Claude draws on for the whole session.

2. **Output format requirements** — "All responses must be valid JSON. No markdown, no prose outside the JSON object." Format specified at system level is consistent across every turn.

3. **Scope constraints** — "Only answer questions about our product's API and SDK. For billing questions, direct users to support@company.com." Operators use this to limit Claude's domain.

4. **Persistent background context** — "The user is a Pro subscriber. They have access to advanced analytics, custom integrations, and priority support." Context that shouldn't need repeating in every user message.

5. **Tone and audience calibration** — "The user is a senior engineer. Don't explain basic programming concepts. Be direct and concise." Prevents over-explanation for expert users.

**What belongs in the user turn:**

1. The actual task or question
2. Documents, code, or data being analysed (unless it's a persistent reference)
3. Session-specific constraints ("focus only on the authentication module this time")
4. Corrections to the previous response
5. Few-shot examples — these work better close to the task than buried in a long system prompt

---

### Role prompting vs instruction prompting

"You are a senior Java engineer" vs "Review this code for null pointer exceptions, thread safety, and O(n²) operations" — which works better?

The answer is both, combined. But they serve different purposes:

Role prompting activates implicit expertise. "Senior Java engineer" makes Claude draw on patterns from enterprise Java development — connection pool management, checked exception handling, JVM performance characteristics — without you having to enumerate all of that. The role fills in what you don't specify.

Instruction prompting gives precision. "Review for null pointer exceptions, thread safety, and O(n²) operations" will reliably produce output addressing exactly those three things. "Review like a senior engineer" might — but might also focus on something you didn't care about.

For work where you want both breadth of expertise and specific focus:

```
[System]: You are a senior Java backend engineer with experience in high-throughput 
payment systems. You know what failure modes look expensive in production.

[User]: Review the following transaction processing code for thread safety, 
connection leak risks, and error handling completeness. Flag anything that 
would cause silent failures under load.
```

The role primes the expertise. The instruction defines the scope.

---

### Extended thinking — when to actually use it

Extended thinking is powerful but has real costs: it consumes 10-30× more tokens than a standard response for the same prompt. Using it on simple tasks is like using a calculator to add 2+2 — technically it works but it's wasteful.

**Use it for:**
- Debugging distributed system issues where multiple components interact
- Strategy decisions with competing constraints ("which of these architecture options has the lowest regulatory exposure given our EU data requirements?")
- Complex refactoring tasks spanning multiple files with multiple interacting concerns
- Legal or financial analysis requiring careful logical chain construction

**Don't use it for:**
- Summarisation, reformatting, translation, simple extraction
- Quick Q&A where you're pulling a fact you know Claude has
- Anything where "faster wrong" is acceptable

**Activating in the API:**
```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 16000,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 8000
  },
  "messages": [...]
}
```

**An effective thinking prompt:**
```xml
<task>
Find the root cause of the memory leak described below and propose a fix with code.
</task>

<context>
Python FastAPI service. OOMs intermittently after ~4 hours of traffic. 
Memory grows linearly. Handles file uploads and OCR processing.
</context>

<code>
[paste relevant code here]
</code>

<reasoning_approach>
Work through this systematically: what objects could accumulate? Are file handles 
being closed? Are async tasks completing properly? Is the issue in the request 
handler or a background worker? Rule out candidates before proposing a fix.
</reasoning_approach>
```

The `<reasoning_approach>` block doesn't just ask for a fix — it tells Claude how to think about the problem. This produces better answers even before extended thinking tokens, and much better answers with them.

---

## Prompt Cheat Sheet for Claude

```
╔══════════════════════════════════════════════════════════════════════╗
║            CLAUDE PROMPT CHEAT SHEET — Tekravio Team                ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. USE XML TAGS FOR STRUCTURE                                       ║
║     <task>, <context>, <code>, <output_format>, <reasoning_approach> ║
║     → Cleaner semantic boundaries = more consistent outputs          ║
║                                                                      ║
║  2. STACK ROLE + INSTRUCTION                                         ║
║     System: "You are a senior Python engineer..."                   ║
║     User:   "Review for null safety and O(n²) patterns."             ║
║     → Role activates implicit expertise; instruction narrows scope   ║
║                                                                      ║
║  3. FORMAT REQUIREMENTS GO IN THE SYSTEM PROMPT                      ║
║     "Always respond in JSON. No markdown." → set once, applies       ║
║     everywhere. User-turn format requests are less consistent.       ║
║                                                                      ║
║  4. EXTENDED THINKING: USE SELECTIVELY                               ║
║     API: {"thinking": {"type": "enabled", "budget_tokens": 8000}}    ║
║     → Worth it for: multi-step debugging, strategy, complex code     ║
║     → Skip for: summaries, extraction, quick Q&A (10-30x token cost) ║
║                                                                      ║
║  5. SPECIFY WHAT "DONE" LOOKS LIKE                                   ║
║     Bad:  "Write a summary."                                         ║
║     Good: "3-sentence summary for a non-technical exec.              ║
║            Lead with business impact. No jargon."                   ║
║     → Claude follows specific success criteria reliably              ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  MODEL QUICK PICK                                                    ║
║  Haiku 4.5   → Classification, routing, real-time    ($1 / $5)      ║
║  Sonnet 4.6  → Production apps, daily coding, content ($3 / $15)    ║
║  Opus 4.7    → Deep analysis, whole-codebase work    ($5 / $25)     ║
║                (per million input / output tokens)                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## Sources

All model specs, pricing, and benchmarks were cross-verified across multiple sources in June 2026.

| Source | Used For |
|--------|----------|
| Anthropic docs — docs.anthropic.com | API specs, model strings, features |
| Anthropic Claude product page — anthropic.com/claude | Model family overview |
| Anthropic Constitution (2022, updated 2026) — anthropic.com/news/claudes-constitution | CAI details |
| cloudzero.com/blog/claude-api-pricing | Pricing verification (May 2026) |
| finout.io/blog/anthropic-api-pricing | Pricing verification (June 2026) |
| metacto.com/blogs/anthropic-api-pricing | Pricing + tokenizer notes |
| suprmind.ai/hub/claude/pricing | claude.ai plan details (May 2026) |
| tygartmedia.com/claude-ai-pricing | Enterprise pricing estimates |
| Scale AI SEAL Leaderboard — labs.scale.com/leaderboard/swe_bench_pro_public | SWE-bench Pro scores |
| swebench.com | SWE-bench Verified leaderboard |
| tokenmix.ai/blog/swe-bench-2026-claude-opus-4-7-wins | SWE-bench analysis |
| codeant.ai/blogs/swe-bench-scores | SWE-bench contamination analysis |
| tech-insider.org/claude-vs-chatgpt-2026 | Claude vs GPT-4o comparison |
| beginnersinai.org/claude-vs-chatgpt-2026 | Feature comparison |
| imagine-works.com/insights/model-context-protocol | MCP enterprise guide |
| truto.one/blog/what-is-mcp-model-context-protocol | MCP origins and governance |
| arxiv.org/pdf/2412.17686 | Constitutional AI academic survey |
| arxiv.org/pdf/2407.16216 | RLAIF vs RLHF technical comparison |
| simonw.substack.com/p/claude-37-sonnet-extended-thinking | Extended thinking mechanics |
| myengineeringpath.dev/genai-engineer/reasoning-models | Claude vs o1 reasoning comparison |
