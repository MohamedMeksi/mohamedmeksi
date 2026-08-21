<div align="center">

# ⚡ AGENT: MEK
### built and operated by Mohamed Meksi

<img src="./assets/console.svg" alt="Agent console · live status, task queue, and deploy log" width="760" />

<sub>SVG above is regenerated daily by <a href="./.github/workflows/agent-console.yml">a GitHub Action</a> running <a href="./scripts/generate_console.py">this script</a> against the GitHub API, not a static image.</sub>

</div>

---

### Mission

`MEK` is an autonomous ops layer for business workflows (WhatsApp messaging, scheduling, field operations, e-commerce), built to automate the parts that don't need a human. I'm the operator: I design, build, and ship it.

```
role      : AI Agent Builder & Full-Stack Developer (operator of MEK)
core      : Python · FastAPI, Flask
interface : TypeScript · Next.js, React
agents    : LangChain, LangGraph, OpenAI Function Calling, n8n, Flowise
domain    : WhatsApp Business automation, AI agents, e-commerce & field-ops tooling
based_in  : Morocco 🇲🇦 · open to remote
```

---

### 🧩 Capabilities (modules)

| Module | Runtime | What it handles |
|---|---|---|
| `core.runtime` | Python · FastAPI · Flask | API layer, business logic, background jobs |
| `interface.layer` | TypeScript · Next.js · React | Storefronts, admin dashboards |
| `agent.layer` | LangChain · LangGraph · OpenAI Function Calling · n8n · Flowise | Conversational agents, orchestration, workflow automation |
| `data.layer` | PostgreSQL · MongoDB · Firestore · Redis | Orders, inventory, conversation state, caching |
| `ops.layer` | Docker · GitHub Actions | Deploys, scheduled agents, this README |

---

### 📦 Deployed instances

| Instance | Modules used | Function | Result |
|---|---|---|---|
| **WhatsApp Business API Gateway** | Python, FastAPI, MongoDB, Redis | API REST multi-tenant pour envoyer, recevoir et suivre des messages WhatsApp Business | En production · architecture multi-tenant |
| **WhatsApp Coexistence** | TypeScript, Node.js, Express, Prisma, PostgreSQL, Redis | Plateforme multi-tenant pour onboarder un numéro WhatsApp Business en coexistence (app mobile + Cloud API) | En production · app mobile + Cloud API en parallèle |
| **WhatsApp Catalogue Agent** | Python, FastAPI, MongoDB, WhatsApp Cloud API | Assistant WhatsApp qui aide les clients à parcourir un catalogue produit et qualifie les demandes pour un conseiller | En production · qualification automatique avant transfert humain |
| **WhatsApp Sales CRM** | Next.js, TypeScript, MongoDB, NextAuth | CRM pour suivre les leads qualifiés via WhatsApp jusqu'à la prise en charge commerciale | En production · utilisé au quotidien par l'équipe commerciale |
| **Assistant WhatsApp Formation** | Python, Flask, OpenAI (Function Calling), Firestore, MongoDB | Agent conversationnel WhatsApp multilingue (FR/EN/AR) qui guide les candidats du premier contact jusqu'à l'inscription, avec 17 outils métier intégrés | 100% des réponses automatisées 24/7 · -80% de temps de gestion manuelle |
| **CRM commercial** | TypeScript, React, Vite, Tailwind CSS, Supabase (PostgreSQL) | Centralise le suivi commercial (leads, devis, commandes) et la messagerie client pour les équipes de vente | En production · centralise leads, devis et messagerie en un seul outil |
| **[Kairos](https://kairoscopilot.com/)** · *AI Executive Copilot* | Next.js, TypeScript, Python, Flask, MongoDB | Copilote vocal qui rédige emails, prend des rendez-vous et gère l'agenda directement depuis WhatsApp/Telegram | En production · 70%+ du développement livré par moi · présenté à GITEX Africa 2026 |
| **Piscibio** | TypeScript, Next.js, React, Prisma, PostgreSQL, Tailwind CSS | Plateforme mobile full-stack qui digitalise les opérations d'une entreprise de maintenance piscines, des techniciens terrain au reporting client | En production · shippé de bout en bout |
| **[Click-Tracker](https://pypi.org/project/click-tracker/)** | Python, Flask | Librairie de tracking web publiée sur PyPI : device/bot detection et géolocalisation en temps réel | 1000 req/min soutenues · latence < 50ms · précision géo 92% (ville) |

> Voir [tous les repos](https://github.com/mohamedmeksi?tab=repositories).

---

### 📜 Mission log

```
[2026-04] GITEX Africa, Marrakech · Kairos (AI Executive Copilot) presented on stage
[2026-01] Full-Stack Developer @ DigitGrow · 3 products shipped from scratch (AI automation, WhatsApp Business, field ops)
[2025-03 → 2026-01] AI Agent Builder @ StartupSquare · WhatsApp AI systems, 100% response automation, -80% manual workload
[2025-03 → 2026-01] Technical Assistant @ Geeks Institute · 9 hackathons supervised (6 Full Stack, 1 Game Dev, 2 GenAI)
[2025] Click-Tracker published on PyPI · open-source web tracking library
[2023-01 → 2023-07] Front-End Developer Intern @ Digi4
```

---

### 📡 Uplink

<p align="center">
  <a href="mailto:mohamedmeksi37@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  <a href="https://www.linkedin.com/in/mohamed-meksi/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
</p>

<div align="center"><sub>console last synced from live GitHub activity · see task queue above</sub></div>
