<div align="center">

# 🤖 Skills para Agentes (Agent Skills)

**Uma coleção de skills especializadas para agentes de IA**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/archsoft-labs/skills/pulls)

🇺🇸 [English](README.md) · 🇧🇷 [Português](README.pt-br.md)

</div>

---

**Agent Skills** da Archsoft® Labs é uma coleção pública de skills especializadas projetadas para estender as capacidades de agentes de IA ou sistemas automatizados.

Cada skill é independente e pode ser acionada automaticamente por agentes de IA para realizar tarefas específicas — desde conversão de documentos até gerenciamento de repositórios.

---

## 🗂️ Estrutura do Projeto

As skills são organizadas em diretórios individuais dentro de `skills/`. Cada skill contém um arquivo `SKILL.md` com metadados e condições de acionamento, além de uma pasta `scripts/` com a lógica de implementação.

---

## 🛠️ Skills Disponíveis

Abaixo está o catálogo atual de skills disponíveis neste repositório:

| Categoria | Skill | Descrição |
|:----------|:------|:----------|
| PDF | 📄 [MD to PDF](skills/pdf/md-to-pdf/SKILL.md) | Converte arquivos Markdown (.md) em PDF no formato A4 usando Playwright/Chromium. |

---

## 🚀 Como Usar

Copie a pasta da skill desejada para o diretório de skills do seu agente. A skill será detectada automaticamente e ficará disponível para ser acionada.

**Exemplo com Claude Code:**
```
.claude/skills/pdf/md-to-pdf/
```

> Cada agente pode ter um caminho diferente para o diretório de skills. Consulte a documentação do seu agente para o local correto.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você tiver uma skill útil para agentes automatizados:

1. Faça um **fork** do repositório
2. Faça suas **mudanças**
3. Abra um **Pull Request**

---

## 📜 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.

---

<div align="center">

**Mantido com ☕ pela [Archsoft® Labs](https://github.com/archsoft-labs)**

</div>
