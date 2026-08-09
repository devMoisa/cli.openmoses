from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Label, Static

from openmoses.domain.models import Agent, ChatMessage, Task


class Brand(Static):
    def compose(self) -> ComposeResult:
        yield Label("OM", classes="brand-mark")
        with Vertical(classes="brand-copy"):
            yield Label("OPENMOSES", classes="brand-name")
            yield Label("agentic workspace", classes="brand-caption")


class SectionLabel(Label):
    pass


class MessageCard(Static):
    def __init__(self, message: ChatMessage) -> None:
        super().__init__(classes="message user-message" if message.is_user else "message")
        self.message = message

    def compose(self) -> ComposeResult:
        with Horizontal(classes="message-meta"):
            yield Label(self.message.author, classes="message-author")
            yield Label("you" if self.message.is_user else "orchestrator", classes="message-role")
        yield Static(self.message.body, classes="message-body")


class AgentRow(Static):
    def __init__(self, agent: Agent) -> None:
        super().__init__(classes="agent-row")
        self.agent = agent

    def compose(self) -> ComposeResult:
        yield Label("●", classes=f"agent-dot status-{self.agent.status}")
        with Vertical(classes="agent-copy"):
            with Horizontal(classes="agent-heading"):
                yield Label(self.agent.name, classes="agent-name")
                yield Label(self.agent.role, classes="agent-role")
            yield Label(self.agent.model, classes="agent-model")


class TaskRow(Static):
    def __init__(self, task: Task, index: int) -> None:
        super().__init__(classes=f"task-row task-{task.state}")
        self.task_data = task
        self.index = index

    def compose(self) -> ComposeResult:
        yield Label(f"{self.index:02}", classes="task-index")
        with Vertical(classes="task-copy"):
            yield Label(self.task_data.title, classes="task-title")
            yield Label(f"{self.task_data.owner}  ·  {self.task_data.state}", classes="task-owner")


class Stat(Widget):
    def __init__(self, value: str, label: str) -> None:
        super().__init__(classes="stat")
        self.value = value
        self.label = label

    def compose(self) -> ComposeResult:
        yield Label(self.value, classes="stat-value")
        yield Label(self.label, classes="stat-label")
