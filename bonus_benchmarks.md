

 Benchmark 1: SWE-bench

 What it actually measures

SWE-bench was created by Princeton researchers in 2024. The setup: take a real GitHub issue from a real open-source project (Django, Flask, scikit-learn, and others), give the model the issue description and the codebase, and ask it to produce a patch that fixes the bug without breaking any existing tests.

This is meaningfully harder than every coding benchmark that came before it because:
- The model has to understand an existing codebase it didn't write
- The bug might be anywhere in the codebase, not just the file you'd guess
- The fix has to be correct enough to pass automated tests that the model can't see or modify
- There's no "close enough" — the tests pass or they don't

The two main variants: SWE-bench Verified (500 hand-reviewed tasks from popular Python repos) and SWE-bench Pro (Scale AI's harder version with unseen proprietary codebases, standardised scaffolding).

 Claude's score

Claude Opus 4.7 (April 2026):
- SWE-bench Verified: 87.6% — first place among non-preview models
- SWE-bench Pro: 64.3% — first place, ahead of GPT-5.4 (57.7%) and Gemini 3.1 Pro (54.2%)

For context on the Verified score: OpenAI's GPT-5.3 scored 85.0%, and the average across all 83 evaluated models is around 63%. The 87.6% means Claude correctly fixed 438 out of 500 real bugs.

The SWE-bench Pro jump from Opus 4.6 to 4.7 — 53.4% to 64.3%, a 10.9-point gain in a single release — is notable. For context, the jump from Opus 4.5 to 4.6 was about 5 points on Verified. The pace of improvement is accelerating.

 What the score doesn't tell you

Contamination is real and documented. OpenAI's internal audit found that frontier models, including Claude, can reproduce verbatim patches for some Verified tasks — because the 500 Python tasks appeared on the internet before these models were trained. They're partly recalling answers, not solving from scratch. This is why the Verified-to-Pro drop is so large (87.6% → 64.3%): Pro tasks come from proprietary codebases that couldn't have been in training data.

Scaffolding matters enormously. The same base model scores very differently depending on the agent harness around it — how the tools are set up, how many retries it gets, whether it can run tests in a sandbox. Anthropic's own "Claude Fable 5" scaffold reportedly scores 80.3% — that's not a different model, it's the same model in a better harness. When you see a vendor-reported score, assume it includes scaffolding optimised for the benchmark. Scale AI's standardised evaluation (the Pro leaderboard) is more trustworthy because every model uses the same setup.

Python-only (mostly) and specific repo patterns. The popular repos in Verified have particular bug patterns, code styles, and test structures that are now well-represented in training data. A model scoring 87% on Django bugs is not the same as a model that scores 87% on your proprietary TypeScript monorepo. The real-world task of "fix bugs in our codebase" correlates with SWE-bench — but not 1:1.

Practical implication for Tekravio: SWE-bench is the best signal available for coding quality, and Claude's lead on the Pro variant (which is harder to game) is meaningful. For a client project involving Python and well-established frameworks, Claude's SWE-bench performance is reasonably predictive. For a proprietary TypeScript codebase, treat the score as a directional indicator rather than a guarantee.



 Benchmark 2: GPQA Diamond

 What it actually measures

GPQA stands for Graduate-Level Google-Proof Q&A. It was designed with a specific goal: create questions that require genuine expert-level knowledge, not Google-search-level knowledge. The "Google-proof" part matters — the questions are designed to be unsolvable by finding the right search result or Wikipedia article.

The "Diamond" subset is the hardest 198 questions from the full 448-question set. These are multiple-choice questions in physics, chemistry, and biology written by PhD-level domain experts. The benchmark was calibrated against humans: domain experts with PhDs score around 65% on their own subject area. Non-expert PhD holders score around 34% even with full web access.

This is the benchmark Anthropic explicitly positioned as measuring "the knowledge and reasoning required to be a useful AI for scientific research."

 Claude's score

Claude Opus 4.7 (April 2026): 94.2% on GPQA Diamond

Current top scores (June 2026):
- Claude Mythos Preview: 94.6% (not public)
- Gemini 3.1 Pro: 94.3%
- Claude Opus 4.7: 94.2%
- GPT-5.5 (high): 93.2%

Average across 220 evaluated models: ~70%

Claude Opus 4.7 scores 94.2% on questions that human PhD experts only get 65% of. That is the correct interpretation of this number — and it is not a small gap.

The trajectory is also significant: Claude 3 Opus (early 2024) scored about 50% on GPQA. Opus 4.7 scores 94.2%. In roughly two years, Claude went from "slightly above expert level on its best day" to "reliably better than experts on average."

 What the score doesn't tell you

Multiple choice is not the same as open-ended scientific reasoning. GPQA Diamond is a 4-option multiple choice test. The model has to identify the right answer, not derive a solution, explain its reasoning, or propose an experiment. A model that scores 94% on GPQA might still produce wrong but convincing-sounding explanations when asked to explain *why* the answer is correct. The format collapses the difficulty of scientific reasoning significantly.

It tests recall and pattern-matching alongside reasoning. Some GPQA questions require genuine scientific reasoning from first principles. Others can be answered by recognising patterns a model has seen many times during training. It's hard to distinguish which type any particular question is without domain expertise, which is precisely the catch.

94% doesn't mean "reliable for medical diagnosis." The questions are about graduate-level science, not applied clinical decisions. A model that gets 94% of GPQA's chemistry questions right might still give a dangerous answer on a medication interaction question that wasn't in its training distribution, or that involves a patient-specific factor the benchmark doesn't test.

The saturation problem is approaching. When every frontier model scores 93-94% on the same benchmark, it stops being useful for differentiation. GPQA Diamond appears to be approaching saturation for frontier models in the same way MMLU did earlier. The field will need harder benchmarks (Humanity's Last Exam is an attempt) to maintain signal.

Practical implication for Tekravio: For a consulting firm doing research-heavy work — synthesising scientific literature, analysing technical reports, reasoning about complex systems — GPQA's score gives real confidence that Claude can engage with expert-level content meaningfully. It doesn't mean you can skip human review on anything with safety implications. But it does mean Claude is a legitimate research partner, not just a document formatting tool.



 Benchmark 3: BIG-Bench Hard (BBH)

 What it actually measures

BIG-Bench Hard is a curated subset of 23 tasks from the larger BIG-Bench benchmark suite, specifically chosen because they were tasks where language models had historically *failed to outperform average human raters*. When BIG-Bench was first published, these 23 tasks were the hard cases — the ones that revealed the limits of models that aced everything else.

The tasks span a deliberately wide range:
- Logical deduction — given a set of constraints ("A is to the left of B, C is not adjacent to A..."), determine the arrangement
- Causal reasoning — identify cause-and-effect relationships in multi-step narratives
- Algorithmic problems — tracking state through a series of operations
- Temporal reasoning — "If today is Tuesday and three days ago was Sunday, what day was it five days before yesterday?"
- Multi-step arithmetic in context — embedded in word problems with irrelevant information
- Disambiguation in unusual sentences — understanding reference and scope in edge cases

The defining feature: BBH was designed to require chain-of-thought reasoning. Models that answer without thinking through the problem systematically perform significantly worse than models that reason step-by-step. This makes it more predictive of real-world performance on structured reasoning tasks than benchmarks where pattern matching is sufficient.

 Claude's score

Frontier model BBH scores as of April-May 2026:
- Claude Opus 4.7: ~92%+ (precise published figure varies by test harness; consistently above 90%)
- GPT-5.4: comparable range
- Gemini 3.1 Pro: comparable range

Historical reference point from the Claude 3 system card (March 2024): Claude 3 Opus scored 86.8% on BBH. The jump to 92%+ in two years reflects real improvement in structured reasoning, not just a different benchmark.

On the specific dimension where Claude 4.7 pulls ahead of competitors — in evaluations like BBH and instruction-following benchmarks, Claude maintains an advantage "particularly when the prompt contains implicit requirements or when the task requires holding a complex set of constraints simultaneously." That's the practical translation of a BBH lead: Claude is better at tasks where the instructions have dependencies, conditions, and edge cases that need to be tracked throughout the response.

 What the score doesn't tell you

BBH is from 2022 and is increasingly in training data. The 23 tasks are publicly known, widely discussed, and have appeared in AI research papers, tutorials, and educational content. Models trained after 2022 may have seen many of these tasks and correct solutions during pre-training. This doesn't mean the scores are fake — a model still needs to generalise the reasoning patterns, not just memorise specific answers — but it means the difficulty has shifted since BBH was first published.

Performance is highly sensitive to prompting. BBH was specifically designed for chain-of-thought prompting. The same model with "let's think step by step" versus without can swing 10-15 percentage points on BBH tasks. Published scores almost always use chain-of-thought. A model that scores 92% on BBH with CoT might score 78% without it. For production use cases where you can't guarantee the user will prompt in CoT style, the gap matters.

23 tasks is not a large coverage area. BBH's 23 categories cover a specific slice of reasoning — logical, causal, temporal, algorithmic. They don't cover spatial reasoning, probabilistic reasoning, planning, or reasoning that requires domain-specific knowledge. A model that scores 92% on BBH might still struggle with reasoning tasks outside those 23 categories.

All frontier models are in a narrow band. Claude, GPT-5.x, and Gemini 3.1 Pro are all scoring in the 90-93% range on BBH. The differences are small enough to be within the noise of different evaluation setups. BBH is useful for ruling out clearly weak models; it doesn't meaningfully differentiate the top three.

Practical implication for Tekravio: BBH's score gives confidence that Claude handles the multi-constraint, multi-step reasoning that comes up constantly in real work — following a complex brief, maintaining consistency across a long document, applying a set of rules without missing edge cases. The benchmark isn't as predictive as SWE-bench for specific task domains, but it's a reasonable proxy for "can Claude actually follow complex instructions reliably?"



 The overall picture

The three benchmarks together tell a coherent story about Claude:

Claude's strongest verified advantage is in coding (SWE-bench Pro, where contamination is minimal and it leads clearly). Its scientific reasoning is frontier-competitive, approaching GPQA saturation alongside Gemini and GPT. Its structured reasoning (BBH) is strong but barely distinguishable from peers.

The honest summary: benchmarks tell you Claude is a capable frontier model. They don't tell you it will work for your specific problem. The only reliable test is running your actual use case on your actual data and measuring what matters to you.



*Sources: vellum.ai/blog/claude-opus-4-7-benchmarks-explained, llm-stats.com/benchmarks/gpqa, mindstudio.ai/blog/claude-opus-47-benchmark-breakdown, buildfastwithai.com/blogs/claude-opus-4-7-review-benchmarks-2026, tokenmix.ai/blog/swe-bench-2026-claude-opus-4-7-wins, codeant.ai/blogs/swe-bench-scores, lxt.ai/blog/llm-benchmarks*
