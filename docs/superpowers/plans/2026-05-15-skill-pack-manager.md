# Skill Pack Manager Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add built-in Superpowers and Caveman skill packs that Yum Agent Company can inject into agent prompts.

**Architecture:** Store built-in pack markdown under the user's company folder in `_skillpacks`. Keep activation state in `_skillpacks/enabled.json`, inject enabled packs through `readAgentSharedContext`, and expose simple slash commands for Telegram and sidebar chat.

**Tech Stack:** VS Code extension TypeScript, existing company folder storage, existing prompt context pipeline.

---

### Task 1: Built-In Skill Packs

**Files:**
- Modify: `src/extension.ts`

- [x] Add `BUILTIN_SKILL_PACKS` with `caveman` and `superpowers`.
- [x] Seed `_skillpacks/<id>/SKILL.md` and `_skillpacks/enabled.json` from `ensureCompanyStructure`.
- [x] Read enabled packs and append them to each agent prompt context.

### Task 2: Commands

**Files:**
- Modify: `src/extension.ts`

- [x] Add `/skillpacks`, `/caveman on|off`, and `/superpowers on|off`.
- [x] Handle commands from Telegram and local sidebar prompts.
- [x] Update help text.

### Task 3: Version And Verification

**Files:**
- Modify: `package.json`
- Modify: `CLAUDE.md`
- Modify: `src/agents.ts`

- [x] Bump version to `2.94.0`.
- [x] Run compile and existing tests.
