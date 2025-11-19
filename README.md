# Knit 🧶

[![Build Status](https://github.com/Solenya-AIaaS/knit/actions/workflows/ci.yml/badge.svg)](https://github.com/Solenya-AIaaS/knit/actions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://github.com/Solenya-AIaaS/knit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Knit** is a tool for dynamically generating and maintaining markdown files using references to commands and external sources.

## 🤖 Why Knit?

We are entering the **Agentic Era**. 

In this new paradigm, documentation is no longer just for humans, it's the primary interface for AI Agents. In addition to the existing set of `README.md`s you have in your codebase, you now need files like `AGENTS.md`, `CLAUDE.md`, and GitHub's instruction files, all critical for guiding autonomous agents.

The quality of an agent's output can degrade significantly if there is outdated or false context in your documentation. 

**Knit** solves this by allowing you to "knit" your documentation together from the source of truth. Instead of copy-pasting output, you define *how* to generate it, ensuring your docs are always 100% accurate.

## ✨ Extensions

Knit is designed around **Extensions**. It comes with powerful built-ins, but you can easily write your own in Python.

### 🌳 Tree Extension

Automatically visualize your directory structure. It's smart enough to pull descriptions from nested `README.md` files to annotate your tree.

```markdown
<!-- docs TREE path="." depth=2 dirs_only=true -->
.
├── services
│   ├── api # FastAPI GraphQL service
│   └── model # ML inference service
└── zoo
    └── lion # The king of the jungle
<!-- /docs -->
```

### 🤖 Just Extension

Embed recipes from your `justfile` directly into your docs. Perfect for "Quick Start" sections.

```markdown
<!-- docs JUST recipe="test" -->
Run all tests (taste test everything 🧪)

```bash
just test
```
<!-- /docs -->
```

### 🔌 Extensible

Add your own extensions by defining a Python function.

```python
# scripts/extensions.py
from knit import register_extension

@register_extension("HELLO")
def hello(content, options, file_path):
    name = options.get("name", "World")
    return f"Hello {name}!"
```

Usage:
```markdown
<!-- docs HELLO name="Knit" -->
Hello Knit!
<!-- /docs -->
```

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Solenya-AIaaS/knit&type=Date)](https://star-history.com/#Solenya-AIaaS/knit&Date)
