<div align="center">

# no-yapping-benchmark

**The receipts behind [no-yapping](https://github.com/viktornorman/no-yapping).**

Same agent, same prompts, with the skill and without. Graded on objective rules. Reproducible.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

</div>

---

## Headline

|                                                                       | With `no-yapping` | Baseline (no skill) |
| --------------------------------------------------------------------- | ----------------- | ------------------- |
| **Behavioral conformance** — reply takes the intended shape (7 cases) | **100%**          | 59.8%               |
| **Avg words — build/redirect prompts**                                | **42**            | 357                 |
| **Avg words — "explain / architecture" prompts**                      | 496               | 499                 |

Two numbers tell the whole story: on prompts where you just want the change, the skill is **~8.5× shorter**. On prompts where you explicitly ask _why_ or for an architecture call, it's **the same length** as baseline — it cuts the chatter, not the substance.

### Output size & run cost

Output size is what you actually read and pay for on output. Estimated output tokens (≈ chars/4), skill vs baseline:

| Prompts | With `no-yapping` | Baseline | Reduction |
| --- | --- | --- | --- |
| All 7 | ~1,875 | ~4,510 | **−58%** |
| Build / redirect (5) | ~362 | ~2,954 | **−88%** |
| Explain / architecture (2) | ~1,513 | ~1,556 | −3% |

On build prompts that's **~1,580 fewer words to read** — roughly 7 minutes at 220 wpm across those five replies. On explain/architecture prompts the cost is essentially identical, by design: the skill doesn't trim those.

**On run-time and total tokens:** each run's wall-clock (`duration_ms`) and full processing tokens (`total_tokens`) are recorded in the per-run `timing.json` — but they are **not a fair head-to-head**. The with-skill runs additionally load the skill files and make extra tool calls inside this eval rig, which inflates both. They measure the harness, not real usage, so the honest cost figure is output size above.

### What the pass rate is — and isn't

It measures whether each reply takes the **shape the skill prescribes**: short on build prompts, leads with a code block, names a concrete file/function, flags a real bug, presents a menu for bundled asks, and stays substantive when you explicitly ask to explain. The rules are deterministic and reproducible ([`grade.py`](grade.py)) — anyone gets the same number.

But they score **form and behavior, not the correctness or quality of the code/advice.** "Names the file" just checks the filename appears; it doesn't verify the suggestion is good. Both runs use the **same model**, so engineering quality is roughly held constant — what the skill changes is the _shape_ and the _length_, which is exactly what it's for. For a quality read, open the actual responses in [`results/iteration-3/`](results/iteration-3/), or run an independent blind A/B judge (not done here).

Why the gap isn't just "shorter = wins": cases 3 and 4 (explain + architecture) **reward length** — the baseline scores 100% on both, tying the skill. The whole gap comes from the build prompts, where taking the terse shape is the intended behavior.

---

## The 7 cases

| #   | Case                                                     | With — words / pass | Baseline — words / pass |
| --- | -------------------------------------------------------- | ------------------- | ----------------------- |
| 0   | Vague "clean up this component"                          | **26** / 100%       | 465 / 40%               |
| 1   | Four changes bundled in one ask                          | **34** / 100%       | 510 / 40%               |
| 2   | "Add a 300ms debounce"                                   | **78** / 100%       | 194 / 25%               |
| 3   | "Why useReducer? explain the tradeoffs" (ripcord)        | 492 / 100%          | 613 / 100%              |
| 4   | "Shard, replicas, or event sourcing? what would you do?" | 500 / 100%          | 386 / 100%              |
| 5   | Sloppy file with a hidden XSS bug                        | **40** / 100%       | 366 / 80%               |
| 6   | "Our data layer feels off, thoughts?"                    | **31** / 100%       | 251 / 33%               |

Cases 3 and 4 are the control: when the user _asks_ for reasoning, `no-yapping` steps aside (rule 8) and answers in full — so it scores the same as baseline there. The win is concentrated where it should be: the build prompts (0, 1, 2, 5, 6).

---

## Method

1. **7 prompts** ([`evals/evals.json`](evals/evals.json)), each referencing a real input file in [`inputs/`](inputs/) where relevant (a messy checkout form, an auth module, a search input, a deliberately awful `dashboard.js`).
2. Each prompt is answered twice by the **same model**: once with the `no-yapping` skill loaded, once with no skill (baseline).
3. Every response is saved verbatim ([`results/iteration-3/eval-*/`](results/iteration-3/)) and graded against **objective assertions** in [`grade.py`](grade.py) — word-count bounds, filler-phrase detection, "leads with a code block", "presents a numbered menu", "names a concrete file", "flags a real bug", "honors the ripcord", etc.
4. Baseline = no skill, so the delta is the skill's effect, not prompt wording.

Reproduce:

```bash
python grade.py            # re-grades the committed responses → grading.json + summary
```

To run it against your own model: keep the prompts/inputs, drop your agent's responses into `results/<your-run>/eval-*/<with_skill|without_skill>/run-1/outputs/response.md`, point `grade.py` at that folder.

---

## Honest caveats

- **Small n.** 7 prompts, one run each. This is a directional signal, not a paper.
- **Proxy metrics.** `no-yapping` is a _style_ skill; the assertions are heuristics (word count, phrase detection). The real evidence is the responses themselves — read them in [`results/iteration-3/`](results/iteration-3/).
- **Model- and version-dependent.** Results were generated with the model noted in the run logs; a different model may behave differently.
- **The grader's bug example is intentionally unrelated** (SQL injection) to the test case (XSS) so the skill is tested on generalization, not memorization.

---

## License

MIT — see [LICENSE](LICENSE).

Skill: **https://github.com/viktornorman/no-yapping**
