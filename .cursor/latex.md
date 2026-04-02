# Mintlify LaTeX / KaTeX Rules (add to .cursor/rules.md)

- Inline math → always use single $...$  (example: $n = \max(n_{\text{econ}}, n_{\text{risk}})$)
- Display / block math → always use $$...$$  (example: $$ E = mc^2 $$)
- Never leave \binom, \sum, \ceil, \text etc. without delimiters
- For multi-line: use \begin{align} ... \end{align} inside $$
- Literal dollar → escape as \$ or use code span
- Preferred over \[ \] or \( \) → stick to $ and $$