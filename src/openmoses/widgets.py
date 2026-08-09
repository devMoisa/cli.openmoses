from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, ListItem, Static

from openmoses.domain.models import ChatMessage


class CommandMenuItem(ListItem):
    """Dashboard option with a keyboard shortcut and supporting copy."""

    def __init__(self, key: str, title: str, description: str, item_id: str) -> None:
        super().__init__(id=item_id, classes="dashboard-menu-item")
        self.shortcut = key
        self.title_text = title
        self.description = description

    def compose(self) -> ComposeResult:
        yield Label(self.shortcut, classes="menu-key")
        with Vertical(classes="menu-copy"):
            yield Label(self.title_text, classes="menu-title")
            yield Label(self.description, classes="menu-description")
        yield Label("›", classes="menu-arrow")


class MessageCard(Static):
    """One compact message in the chat timeline."""

    def __init__(self, message: ChatMessage) -> None:
        classes = "message user-message" if message.is_user else "message assistant-message"
        super().__init__(classes=classes)
        self.message_data = message

    def compose(self) -> ComposeResult:
        with Horizontal(classes="message-header"):
            yield Label(self.message_data.author, classes="message-author")
            yield Label("you" if self.message_data.is_user else "openmoses", classes="message-role")
        yield Static(self.message_data.body, classes="message-body")
