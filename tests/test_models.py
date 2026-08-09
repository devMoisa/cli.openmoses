from openmoses.data import AGENTS
from openmoses.domain.models import AgentStatus


def test_orchestrator_is_the_first_agent() -> None:
    assert AGENTS[0].role == "Orchestrator"
    assert AGENTS[0].status is AgentStatus.WORKING


def test_agent_names_are_unique() -> None:
    names = [agent.name for agent in AGENTS]
    assert len(names) == len(set(names))
