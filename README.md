<div align="center">

# 🤖 Agent Skills

**A collection of specialized skills for AI agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/archsoft-labs/skills/pulls)

🇺🇸 [English](README.md) · 🇧🇷 [Português](README.pt-br.md)

</div>

---

**Agent Skills** by Archsoft® Labs is a public collection of specialized skills designed to extend the capabilities of AI agents or automated systems.

Each skill is self-contained and can be triggered automatically by AI agents to perform specific tasks — from document conversion to repository management.

---

## 🗂️ Project Structure

Skills are organized into individual directories under `skills/`. Each skill contains a `SKILL.md` file with metadata and trigger conditions, plus a `scripts/` folder with the implementation logic.

---

## 🛠️ Available Skills

Below is the current catalog of available skills in this repository:

| Category | Skill | Description |
|:---------|:------|:------------|
| PDF | 📄 [MD to PDF](skills/pdf/md-to-pdf/SKILL.md) | Converts Markdown (.md) files to A4-formatted PDF using Playwright/Chromium. |

---

## 🚀 How to Use

Copy the desired skill folder into your agent's skills directory. The skill will be automatically detected and available for triggering.

**Claude Code example:**
```
.claude/skills/pdf/md-to-pdf/
```

> Each agent may have a different skills directory path. Refer to your agent's documentation for the correct location.

---

## 🤝 Contributing

Contributions are welcome! If you have a useful skill for automated agents:

1. **Fork** the repository
2. Make your **changes**
3. Open a **Pull Request**

---

## 📜 License

Distributed under the **MIT** License. See the [`LICENSE`](LICENSE) file for more information.

---

<div align="center">

**Maintained with ☕ by [Archsoft® Labs](https://github.com/archsoft-labs)**

</div>
