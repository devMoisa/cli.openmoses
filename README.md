# Openmoses

Openmoses is a terminal-first workspace for coordinating specialized AI coding
agents. It is being built in small, reviewable milestones.

## Current milestone: TUI foundation

The first milestone establishes the visual language and information architecture:

- project and session navigation;
- central orchestration chat;
- visible orchestrator, specialist agents, and task queue;
- keyboard-first interaction;
- domain models kept separate from UI widgets.

The agents and conversation are simulated in this milestone. No API keys are read
and no model provider is called yet.

## Run locally

```bash
uv sync
uv run openmoses
```

Inside the app, use `Ctrl+N` for a new session, `Ctrl+P` for the command palette,
and `Ctrl+Q` to quit.

## Planned milestones

1. TUI foundation and product shell.
2. Local configuration for providers, models, and agent profiles.
3. OpenRouter client with streaming responses.
4. Orchestrator that plans and delegates work.
5. Parallel agent runs with isolated workspaces and live logs.
6. Review, diff, approval, and Git workflow.

# cli.openmoses
