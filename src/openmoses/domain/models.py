from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AgentStatus(StrEnum):
    READY = "ready"
    WORKING = "working"
    WAITING = "waiting"


@dataclass(frozen=True, slots=True)
class Agent:
    name: str
    role: str
    model: str
    status: AgentStatus = AgentStatus.READY
    accent: str = "#a7f3d0"


@dataclass(frozen=True, slots=True)
class Task:
    title: str
    owner: str
    state: str


@dataclass(frozen=True, slots=True)
class ChatMessage:
    author: str
    body: str
    is_user: bool = False
