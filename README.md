# Openmoses

Openmoses is a terminal-first workspace for coordinating specialized AI coding
agents. It is being built in small, reviewable milestones.

## Current milestone: TUI foundation

The first milestone establishes a compact, keyboard-first product shell:

- Neovim-inspired launch dashboard;
- distraction-free, full-width orchestration chat;
- slash commands for agents, models, skills, and tools;
- keyboard and mouse navigation;
- domain models kept separate from UI widgets.

The agents and conversation are simulated in this milestone. No API keys are read
and no model provider is called yet.

## Run locally

```bash
make setup
make dev
```

`make dev` opens the Openmoses interface directly in the current terminal.

Inside the dashboard, navigate with `↑`/`↓` or `j`/`k`, and press `Enter` to
select. Direct shortcuts `n`, `a`, `m`, `s`, and `t` open each destination. In
chat, use `/help` to list commands, `Esc` to return home, and `Ctrl+Q` to quit.
`Ctrl+C` also closes the application immediately.

## Planned milestones

1. TUI foundation and product shell.
2. Local configuration for providers, models, and agent profiles.
3. OpenRouter client with streaming responses.
4. Orchestrator that plans and delegates work.
5. Parallel agent runs with isolated workspaces and live logs.
6. Review, diff, approval, and Git workflow.

# cli.openmoses
