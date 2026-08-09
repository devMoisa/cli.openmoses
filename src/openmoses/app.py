from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Input, Label, ListView, Static

from openmoses.data import AGENTS
from openmoses.domain.models import ChatMessage
from openmoses.widgets import CommandMenuItem, MessageCard


class DashboardScreen(Screen[None]):
    """Keyboard-first home inspired by editor dashboards."""

    ART = """\
⠀⠀⢀⡾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣻
⠀⠀⣾⢰⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⡟⣵⣿
⠀⣾⣿⣿⣿⣿⣿⠀⠀⠀⠀⣀⡀⠀⠀⢤⣠⣾⣿⣧⣤⡀
⢰⣿⡇⣿⣿⢟⣭⣖⣂⣀⣐⣶⣿⣿⣿⣿⣿⣿⣿⣿⡟⣛⢷⡀
⣼⣿⣇⣘⣵⣿⣿⣿⣿⣿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⠀⠿⠑⡹⣆
⣿⣿⣿⣿⣿⣿⣿⡟⠩⢾⡏⠉⠉⠦⢹⣿⣿⣿⣿⡿⢆⠀⠀⢈⣿⣧⣀
⣿⣿⣿⢿⣿⣿⣿⣃⣀⣀⣀⠀⠀⠀⢷⣿⣿⣯⣀⣀⡀⣿⣶⣿⣿⣿⣿⣏⡀
⠋⣁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣟⣿⣿⣿⣿⣿
⣾⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣉⣤⣤⡙⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿
⡟⠉⣠⣿⣿⣿⣿⣿⣿⡿⢋⡤⣫⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣠⣿⣿⡿⢿⣿⣿⠋⣴⡟⣴⣿⣿⣿⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⠀⠙⠻⠛⠀⣼⡿⢣⣾⡟⢱⣿⣿⣿⠟⠏⢿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣛⠁"""

    BINDINGS = [
        Binding("n", "new_chat", "New chat", show=False),
        Binding("a", "open_section('agents')", "Agents", show=False),
        Binding("m", "open_section('models')", "Models", show=False),
        Binding("s", "open_section('skills')", "Skills", show=False),
        Binding("t", "open_section('tools')", "Tools", show=False),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("q", "app.quit", "Quit", show=False),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="dashboard"):
            with Vertical(id="dashboard-content"):
                yield Static(self.ART, id="dashboard-art")
                yield Static("OPENMOSES", id="wordmark")
                yield Label("orchestrate code from your terminal", id="tagline")
                yield ListView(
                    CommandMenuItem("n", "New chat", "Start an orchestration", "new-chat"),
                    CommandMenuItem("a", "Agents", "Roles and model assignments", "agents"),
                    CommandMenuItem("m", "Models", "Providers and routing", "models"),
                    CommandMenuItem("s", "Skills", "Reusable instructions", "skills"),
                    CommandMenuItem("t", "Tools", "Agent capabilities", "tools"),
                    id="dashboard-menu",
                )
                yield Label("↑↓ / j k  move     enter  select     q  quit", id="dashboard-hint")
            yield Label("v0.1  ·  local mode  ·  no provider connected", id="dashboard-status")

    def on_mount(self) -> None:
        self.query_one("#dashboard-menu", ListView).focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id
        if item_id == "new-chat":
            self.action_new_chat()
        elif item_id is not None:
            self.action_open_section(item_id)

    def action_cursor_down(self) -> None:
        menu = self.query_one("#dashboard-menu", ListView)
        menu.action_cursor_down()

    def action_cursor_up(self) -> None:
        menu = self.query_one("#dashboard-menu", ListView)
        menu.action_cursor_up()

    def action_new_chat(self) -> None:
        self.app.push_screen(ChatScreen())

    def action_open_section(self, section: str) -> None:
        self.app.push_screen(SettingsScreen(section))


class SettingsScreen(Screen[None]):
    """Compact read-only preview of a configuration section."""

    BINDINGS = [Binding("escape", "app.pop_screen", "Back", show=True)]

    SECTION_CONTENT = {
        "agents": (
            "Agents",
            "Specialists available to the orchestrator",
            tuple(f"{agent.name}  ·  {agent.role}  ·  {agent.model}" for agent in AGENTS),
        ),
        "models": (
            "Models & providers",
            "Routing will be configured through OpenRouter",
            (
                "OpenRouter  ·  not connected",
                "Orchestrator  ·  Claude Sonnet 4.5",
                "Frontend  ·  Claude Sonnet 4.5",
                "Backend  ·  Kimi K2",
                "Architect  ·  GPT-5.2",
            ),
        ),
        "skills": (
            "Skills",
            "Reusable context loaded only when an agent needs it",
            (
                "No project skills configured yet",
                "Next: discover .openmoses/skills/*.md",
            ),
        ),
        "tools": (
            "Tools",
            "Capabilities that can be granted per agent",
            (
                "filesystem  ·  read and edit project files",
                "shell  ·  execute approved commands",
                "git  ·  inspect diffs and repository state",
            ),
        ),
    }

    def __init__(self, section: str) -> None:
        super().__init__()
        self.section = section

    def compose(self) -> ComposeResult:
        title, description, items = self.SECTION_CONTENT[self.section]
        with Vertical(id="settings-page"):
            with Horizontal(classes="minimal-header"):
                yield Label("OM", classes="mini-brand")
                yield Label(title, classes="minimal-title")
                yield Label("esc  back", classes="minimal-action")
            with Vertical(id="settings-content"):
                yield Label(title, id="settings-title")
                yield Label(description, id="settings-description")
                with Vertical(id="settings-list"):
                    for item in items:
                        yield Static(item, classes="settings-item")
                yield Label(
                    "Configuration editing arrives in the next milestone.",
                    id="settings-note",
                )
        yield Footer()


class ChatScreen(Screen[None]):
    """Minimal full-width orchestration chat."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Home", show=True),
        Binding("ctrl+l", "clear_chat", "Clear", show=True),
    ]

    COMMANDS = {
        "/help": (
            "Commands",
            "/agents  /models  /skills  /tools  /clear  /home",
        ),
        "/agents": (
            "Agents",
            "\n".join(f"• {agent.name} — {agent.role} · {agent.model}" for agent in AGENTS),
        ),
        "/models": (
            "Models",
            "OpenRouter is not connected yet. Model routing will be configured locally.",
        ),
        "/skills": (
            "Skills",
            "No skills configured yet. Project skills will live in .openmoses/skills/.",
        ),
        "/tools": (
            "Tools",
            "filesystem · shell · git\nPermissions will be configurable per agent.",
        ),
    }

    def compose(self) -> ComposeResult:
        with Vertical(id="chat-page"):
            with Horizontal(classes="minimal-header"):
                yield Label("OM", classes="mini-brand")
                yield Label("New orchestration", classes="minimal-title")
                yield Label("Moses  ·  local", classes="minimal-action")
            with ScrollableContainer(id="conversation"):
                yield Static(
                    "What do you want to build?\n"
                    "Moses can plan the work and delegate it to specialized agents.",
                    id="chat-empty-state",
                )
            with Vertical(id="composer-wrap"):
                yield Input(
                    placeholder="Message Moses or type / for commands",
                    id="composer",
                )
                with Horizontal(id="composer-meta"):
                    yield Label("/agents  /models  /skills  /tools", classes="command-hints")
                    yield Label("enter  send", classes="send-hint")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#composer", Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return

        event.input.value = ""
        if text == "/clear":
            await self.action_clear_chat()
            return
        if text == "/home":
            self.app.pop_screen()
            return

        conversation = self.query_one("#conversation", ScrollableContainer)
        for empty_state in self.query("#chat-empty-state"):
            await empty_state.remove()

        if command := self.COMMANDS.get(text.lower()):
            title, body = command
            await conversation.mount(MessageCard(ChatMessage(author=title, body=body)))
        else:
            await conversation.mount(
                MessageCard(ChatMessage(author="You", body=text, is_user=True))
            )
            await conversation.mount(
                MessageCard(
                    ChatMessage(
                        author="Moses",
                        body=(
                            "Provider connection is not enabled yet. In the next milestone, "
                            "I will stream the orchestrator response here."
                        ),
                    )
                )
            )
        conversation.scroll_end(animate=True)

    async def action_clear_chat(self) -> None:
        conversation = self.query_one("#conversation", ScrollableContainer)
        await conversation.remove_children()
        await conversation.mount(
            Static(
                "Chat cleared. Start a new request or type /help.",
                id="chat-empty-state",
            )
        )


class OpenMosesApp(App[None]):
    """Terminal workspace for orchestrating coding agents."""

    CSS_PATH = "styles.tcss"
    TITLE = "Openmoses"

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("ctrl+q", "quit", "Quit", show=True, priority=True),
    ]

    def on_mount(self) -> None:
        self.push_screen(DashboardScreen())


def main() -> None:
    OpenMosesApp().run()


if __name__ == "__main__":
    main()
