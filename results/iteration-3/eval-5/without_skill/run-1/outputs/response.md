Happy to help clean it up. Before I rewrite anything, I want to make sure we agree on what "sort it out" means here, because there are a few different problems tangled together and the right fix depends on your constraints.

Here's what I'm seeing in `dashboard.js`:

**Real bugs / risks**
1. **XSS vulnerability.** Lines 16, 18, 34 build HTML by string-concatenating `data[i].name` and amounts straight into `innerHTML`. If any of that data is user-controlled, that's a script-injection hole. This is the thing I'd want to fix first regardless of anything else.
2. **Divide-by-zero / empty-state bug.** Line 23 does `total / data.length`. If `items` comes back empty, `avg` becomes `NaN` and renders as "Avg: NaN". There's also no handling for the list being empty.
3. **Shared mutable `data`.** The module-level `var data` (line 1) gets overwritten on every call. If two dashboards ever load concurrently, they stomp each other.
4. **Inconsistent error handling.** The outer request reports errors via `cb`, but the inner chart request (lines 29-39) silently does nothing on failure or non-200 — and the callback never fires, so the caller hangs forever.

**Style / modernization**
5. Raw `XMLHttpRequest`, `var`, `==`, and nested callbacks. This could be a lot smaller and clearer with `fetch` + `async/await`, or kept as-is if you have an older-browser support requirement.
6. Rendering logic and data fetching are interleaved, which makes both harder to test.

So a couple of questions before I touch it:

- **Is `data[i].name` ever user-supplied?** (Determines how hard I lean on the XSS fix vs. just escaping.)
- **Do you need to support old browsers / no build step,** or can I move this to `fetch` + `async/await`?
- **Scope:** do you want me to just fix the bugs (XSS, empty-state, error handling) and leave the structure mostly intact, or do a fuller refactor — separate fetch from render, dedupe the two requests, drop the global, modernize syntax?

If you just want me to run with it, I'd default to: switch to `fetch`/`async`, escape or build DOM nodes instead of `innerHTML`, guard the empty case, and propagate errors from both requests. Tell me which way you'd like to go and I'll make the changes.
