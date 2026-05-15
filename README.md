# Yum Agent Company

Personal local AI development company for VS Code/Cursor. It runs a small team of local AI employees that can plan, write files, use tools, keep memory, and move work toward real deliverables.

Current version: `2.100.0`

## What It Is

Yum Agent Company is moving from "agents answer questions" toward a practical software factory:

- 13 development-company employees: CEO, senior dev, frontend, backend, DevOps, designer, QA, writer, researcher, secretary, junior dev, accountant, lawyer
- local-first operation through Ollama or LM Studio
- company memory in `_company/`
- reusable agent skills in `_agents/<agent>/skills/`
- bundled tool seeds in `_agents/<agent>/tools/`
- skill-pack modes such as Caveman and Superpowers
- project switching and factory queue MVP

## Main Commands

Commands work from Telegram and from the extension chat input unless noted.

In the extension chat input, press the `/` command button or type `/` to open command cards. Click a card to insert the command into the input, then press Enter. New slash commands should be added to the sidebar `COMMAND_CARDS` registry so they stay visible in this panel.

### Skill Packs

Skill Packs are reusable behavior packs injected into every agent prompt.

```text
/skillpacks
/superpowers on
/superpowers off
/caveman on
/caveman off
```

Natural language also works:

```text
슈퍼파워 적용
슈퍼파워 꺼
케이브맨 모드 켜
케이브맨 꺼
일반 모드로
```

What they do:

- `Superpowers`: planning, systematic debugging, code review, verification-before-completion workflow
- `Caveman`: terse high-signal response style for token saving

Files created:

```text
_company/_skillpacks/enabled.json
_company/_skillpacks/caveman/SKILL.md
_company/_skillpacks/superpowers/SKILL.md
```

### Project Workspace Manager

Use this when you want to stop one project, switch to another, or start fresh without mixing context.

```text
/project status
/project list
/project create <name>
/project switch <name>
/project pause [name]
/project archive <name>
```

Examples:

```text
/project create saas-mvp
/project switch saas-mvp
/project pause saas-mvp
/project create game-app
/project archive old-demo
```

Files created:

```text
_company/projects/current.json
_company/projects/<project>/vision.md
_company/projects/<project>/architecture.md
_company/projects/<project>/decision-log.md
_company/projects/<project>/release-notes.md
_company/projects/<project>/backlog.json
_company/projects/<project>/sessions/
_company/projects/<project>/artifacts/
```

The active project is injected into every agent prompt so employees focus on the current product instead of mixing old work into new work.

### Factory Queue

Use this when you want the company to behave more like a production line.

```text
/factory status
/factory on
/factory auto
/factory pause
/factory stop
/factory seed
/factory tick
/factory review
/factory add <ticket title>
```

Examples:

```text
/factory add Build login page with email/password flow
/factory add Add README install guide and screenshots section
/factory auto
/factory seed
/factory tick
/factory review
/factory status
/factory pause
```

Files created:

```text
_company/factory/state.json
_company/factory/backlog.json
```

Factory states:

- `running`: factory mode enabled
- `paused`: queue preserved, work paused
- `stopped`: active `doing` tickets are marked `blocked`

`/factory auto` sets the factory to `running`. While the extension is active, a 5-minute loop checks the queue. If no dispatch is running, it reviews completed tickets first, seeds a few starter tickets when the queue is empty, then runs one backlog ticket with `/factory tick`.

Ticket flow target:

```text
backlog -> doing -> review -> shipped
```

The MVP stores the queue, injects factory status into agent prompts, and `/factory tick` runs one ticket through the CEO dispatch path. A successful run moves the ticket to `review` and records evidence pointing at the saved session manifest. `/factory review` checks review tickets: evidence present means `shipped`; missing evidence means `blocked`.

### Existing Work Commands

```text
/done <id>
/cancel <id>
/skill
/skills [agent_id]
/approve <id>
/reject <id>
/help
```

What they do:

- `/done`, `/cancel`: close tracked work
- `/skill`: save the last specialist output as a reusable skill
- `/skills`: list saved skills
- `/approve`, `/reject`: approve or reject risky pending actions
- `/help`: show Telegram command help

## Current Stage

The app can already:

- answer through specialists
- use agent-specific tools
- save memories and skills
- inject Superpowers/Caveman workflow packs
- keep active project context
- store a factory queue

This is still not a fully autonomous factory. It is now the foundation: agents can see the current project and the production queue, but timed autonomous production loops still need another layer.

## Factory Roadmap

### 1. Work Queue

Current user requests should become tickets:

```text
backlog -> doing -> review -> shipped
```

Needed details per ticket:

- task id
- assigned employee
- target deliverable
- acceptance criteria
- evidence path
- current status

Primary file:

```text
_company/factory/backlog.json
```

### 2. Deliverable Criteria

"I worked on it" is not enough. A ticket should only move forward when there is evidence:

- changed files
- generated app/code/document
- test or compile result
- session manifest
- QA note

Target evidence:

```text
_company/projects/<project>/sessions/<run>/manifest.json
```

### 3. Shift Loop

Factory mode needs a heartbeat:

- CEO checks queue every N minutes
- idle employees pick next valuable ticket
- blocked work gets reassigned
- daily report summarizes shipped/blocked/next work

Suggested commands:

```text
/factory on
/factory pause
/factory status
```

### 4. Review Gate

Quality control prevents junk output.

Suggested gate:

```text
senior_dev review -> qa test -> shipped
```

Optional specialist gates:

- lawyer: policy/legal risk
- accountant: pricing/cost/revenue logic
- devops: deployment risk

### 5. Product Memory

Agents need stable product direction:

```text
_company/projects/<project>/vision.md
_company/projects/<project>/roadmap.md
_company/projects/<project>/architecture.md
_company/projects/<project>/decision-log.md
_company/projects/<project>/release-notes.md
```

## Recommended Next MVP

Project Workspace Manager is now started:

```text
/project create <name>
/project switch <name>
/project pause
/project status
/project archive <name>
```

Next build target:

- LLM QA review: QA/senior_dev reads the manifest and final report before shipping
- smarter backlog generation: CEO creates custom tickets from project vision when the queue is empty
- CEO decomposes vague work into 3-7 small tickets when backlog is empty
- shipped tickets update project release notes

## Build

```bash
npm install
npm run compile
npm run test:permission
npm run test:guard
```

Windows VSIX build:

```powershell
./build.ps1
```

or double-click:

```text
build.bat
```

## Privacy

The extension is local-first. It uses your configured local model server such as Ollama or LM Studio. Company memory, projects, factory queue, skills, and tool configs live on your machine under the configured company/brain folder.
