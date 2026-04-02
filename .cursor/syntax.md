# Cursor Rules: Mintlify MDX Best Practices & Error Prevention
# Apply these rules whenever editing .mdx files in this project

## Core Principle
Mintlify uses a custom MDX pipeline (remark + rehype + next-mdx-remote-client + Shiki + KaTeX).
It is stricter than GitHub-flavored markdown and more sensitive than plain @mdx-js/mdx in some cases.

Goal: Write MDX that compiles cleanly on first try in Mintlify preview & build.

## 1. Never use raw < or > in prose / tables / headings (they are parsed as JSX)

❌ Bad (breaks parser):

```text
deviation >δ
slippage <1%
n > n/2
price >$100K
(e.g., < 0.5%)   ← leading < in parentheses can still be parsed as JSX
```

✅ Good:
- deviation &gt; δ  (prefer HTML entities in prose)
- slippage &lt; 1%
- price &gt; $100K
- (e.g., &lt; 0.5%)

✅ Also acceptable when space is unambiguous:

```text
deviation > δ
slippage < 1%
n > n/2
```

Rule: **Prefer HTML entities `&lt;` and `&gt;`** for comparisons in prose so the parser never treats them as JSX. Use space around < and > only when you are sure the context is safe (e.g. inside code or math). In tables and list items, always use entities.

## 2. Use proper math delimiters – prefer $$ for display, $ for inline

Preferred patterns:

- Inline: Euler's identity: $e^{i\pi} + 1 = 0$
- Display (centered, larger):

$$
n = \max(n_{\text{econ}}, n_{\text{risk}}, n_{\text{ops}})
$$

- Multi-line aligned equations:

$$
\begin{align}
n_{\text{econ}} &= \left\lceil \frac{\log(V \cdot f / D \cdot c)}{\log \kappa} \right\rceil + 1 \\
n_{\text{risk}} &= \min\left\{ n : \sum_{k=\lceil n/2 \rceil +1}^{n} \binom{n}{k} p^k (1-p)^{n-k} < \epsilon \right\} + \phi
\end{align}
$$

Never leave unmatched { } or \ inside text — always wrap in $…$ or $$…$$.

## 3. Tables and leading pipes: Keep content safe from JSX and table parsing

### Tables
- Never start a cell with < or >
- In table cells, use HTML entities for comparisons: `&lt;`, `&gt;`
- Avoid raw percentages or inequalities without space

❌ Bad:
| Pair      | Depth     | Condition          |
|-----------|-----------|--------------------|
| BTC/USDC  | $50M     | depth >$50M       |

✅ Good:
| Pair      | Depth     | Condition              |
|-----------|-----------|------------------------|
| BTC/USDC  | $50M     | depth &gt; $50M       |

### Leading pipe in prose
A line that **starts with `|`** (e.g. absolute value or notation) can be parsed as a Markdown table row.

❌ Bad (may render as table):
- **Guard**: |price - oracle| < 1%

✅ Good (escape the pipes or use math):
- **Guard**: \|price − oracle\| &lt; 1%
- Or in math: $|p - \text{oracle}| < 1\%$

## 4. JSX Components – only use Mintlify built-ins

Safe / recommended Mintlify components:

<Callout type="info" title="Important">
Content here
</Callout>

<Accordion title="Click to expand">
Details...
</Accordion>

<Tabs>
<Tab title="Tab 1">...</Tab>
<Tab title="Tab 2">...</Tab>
</Tabs>

<Steps>
<Step title="Step 1">...</Step>
</Steps>

Do NOT invent custom tags like `Warning` or `FormulaBlock` (do not use angle-bracket component names you did not import) — they will fail.

## 5. Avoid bare `*` between variables in prose (parsed as emphasis)

In Markdown, `*text*` is italic and `**text**` is bold. A bare `*` between numbers or variables can start emphasis.

❌ Bad (may italicize or break):
- V * f > c * V
- shard_capacity * 10

✅ Good:
- V × f &gt; c × V   (use × for multiplication in prose)
- shard_capacity × 10
- Or use math: $V \cdot f > c \cdot V$

## 6. Frontmatter must be perfect YAML

--- at top and bottom, no extra spaces/lines inside.

Example:

---
title: "Mathematical Model for Minimum Number of Market Makers"
sidebarTitle: "Mathematical model (min MMs)"
description: "Rigorous mathematical model for determining the minimum number of market makers required for safe pure CLOB engine operation"
---

No trailing content after final ---.

## 7. Quick Checklist before commit / Mintlify preview

- [ ] All < and > in prose/tables use HTML entities (&lt;, &gt;) or are inside math/code
- [ ] No line in prose starts with `|` unless pipes are escaped (\|) or inside code/math
- [ ] Multiplication in prose uses × (or math) not bare `*`
- [ ] All math is wrapped in $…$ or $$…$$
- [ ] No raw HTML tags unless inside code blocks
- [ ] Tables do not contain unescaped < > or look like JSX
- [ ] No unmatched braces in LaTeX
- [ ] Frontmatter is valid YAML and cleanly terminated
- [ ] Only use known Mintlify components from docs.mintlify.com

## Bonus: When suggesting fixes in Cursor

Prefer suggesting:
- **Use HTML entities for comparisons in prose** (&gt;, &lt;) — most reliable for MDX
- Add space around comparison operators only when context is clearly safe
- Escape leading pipes in notation: \|x - y\| &lt; 1%
- Use × for multiplication in prose; wrap real formulas in $…$ or $$…$$
- Wrap math in proper delimiters; break long formulas into align environments

Follow these rules strictly when editing or generating .mdx content.