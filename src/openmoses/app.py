from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widgets import Button, Footer, Input, Label, Static

from openmoses.data import AGENTS, MESSAGES, TASKS
from openmoses.domain.models import ChatMessage
from openmoses.widgets import AgentRow, Brand, MessageCard, SectionLabel, Stat, TaskRow


class OpenMosesApp(App[None]):
    """Terminal workspace for orchestrating coding agents."""

    CSS_PATH = "styles.tcss"
    TITLE = "Openmoses"
    SUB_TITLE = "agentic workspace"

    BINDINGS = [
        Binding("ctrl+n", "new_session", "New session", show=True),
        Binding("ctrl+p", "command_palette", "Commands", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal(id="topbar"):
            yield Brand()
            yield Label("~/projects/openmoses", id="project-path")
            with Horizontal(id="connection-status"):
                yield Label("●", classes="online-dot")
                yield Label("LOCAL MODE")

        with Horizontal(id="workspace"):
            with Vertical(id="sidebar"):
                yield Button("＋  New session", id="new-session", variant="primary")
                yield SectionLabel("WORKSPACE", classes="section-label")
                yield Static("◆  Orchestrate", classes="nav-item active")
                yield Static("◇  Agents", classes="nav-item")
                yield Static("◇  Providers", classes="nav-item")
                yield Static("◇  Runs", classes="nav-item")
                yield SectionLabel("SESSIONS", classes="section-label sessions-label")
                yield Static(
                    "Frontend foundation\n[dim]3 messages · now[/]",
                    classes="session active-session",
                )
                yield Static(
                    "Provider architecture\n[dim]12 messages · yesterday[/]", classes="session"
                )
                yield Static("CLI command design\n[dim]8 messages · 2d[/]", classes="session")
                yield Static("v0.1  ·  local", id="version")

            with Vertical(id="main-panel"):
                with Horizontal(id="session-header"):
                    with Vertical(id="session-title-group"):
                        yield Label("Frontend foundation", id="session-title")
                        yield Label("Moses is coordinating 3 specialists", id="session-subtitle")
                    yield Button("⋯", id="session-menu")

                with ScrollableContainer(id="conversation"):
                    yield Static(
                        "ORCHESTRATION  /  SESSION 001",
                        classes="conversation-kicker",
                    )
                    for message in MESSAGES:
                        yield MessageCard(message)

                with Vertical(id="composer-wrap"):
                    yield Input(
                        placeholder="Ask Moses to plan, delegate, or review…",
                        id="composer",
                    )
                    with Horizontal(id="composer-meta"):
                        yield Label("@ agent   / command   # context")
                        yield Label("ENTER to send", classes="send-hint")

            with Vertical(id="inspector"):
                yield SectionLabel("ORCHESTRATOR", classes="section-label inspector-label")
                with Vertical(id="orchestrator-card"):
                    with Horizontal(classes="orchestrator-heading"):
                        yield Label("M", classes="orchestrator-avatar")
                        with Vertical(classes="orchestrator-copy"):
                            yield Label("Moses", classes="orchestrator-name")
                            yield Label("Claude Sonnet 4.5", classes="orchestrator-model")
                    yield Static(
                        "Decomposes goals, assigns specialists, and asks before "
                        "applying risky changes.",
                        classes="orchestrator-description",
                    )
                    with Horizontal(classes="stats"):
                        yield Stat("3", "agents")
                        yield Stat("1", "active")
                        yield Stat("0", "blocked")

                yield SectionLabel("AGENTS", classes="section-label inspector-label")
                with Vertical(id="agent-list"):
                    for agent in AGENTS[1:]:
                        yield AgentRow(agent)

                with Horizontal(id="queue-heading"):
                    yield SectionLabel("TASK QUEUE", classes="section-label inspector-label")
                    yield Label("3 items", classes="queue-count")
                with Vertical(id="task-list"):
                    for index, task in enumerate(TASKS, start=1):
                        yield TaskRow(task, index)

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#composer", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return
        conversation = self.query_one("#conversation", ScrollableContainer)
        conversation.mount(MessageCard(ChatMessage(author="You", body=text, is_user=True)))
        event.input.value = ""
        conversation.scroll_end(animate=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new-session":
            self.action_new_session()

    def action_new_session(self) -> None:
        composer = self.query_one("#composer", Input)
        composer.value = ""
        composer.placeholder = "Describe what you want the team to build…"
        composer.focus()


def main() -> None:
    OpenMosesApp().run()


if __name__ == "__main__":
    main()
