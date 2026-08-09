from openmoses.domain.models import Agent, AgentStatus, ChatMessage, Task

AGENTS = (
    Agent(
        name="Moses",
        role="Orchestrator",
        model="Claude Sonnet 4.5",
        status=AgentStatus.WORKING,
        accent="#d6ff52",
    ),
    Agent(
        name="Ada",
        role="Frontend",
        model="Claude Sonnet 4.5",
        accent="#e8a5ff",
    ),
    Agent(
        name="Linus",
        role="Backend",
        model="Kimi K2",
        status=AgentStatus.WAITING,
        accent="#79c8ff",
    ),
    Agent(
        name="Vitruvius",
        role="Architect",
        model="GPT-5.2",
        accent="#ffb86b",
    ),
)

TASKS = (
    Task("Map the repository", "Moses", "done"),
    Task("Define TUI foundation", "Ada", "active"),
    Task("Design provider contract", "Linus", "queued"),
)

MESSAGES = (
    ChatMessage(
        author="Moses",
        body=(
            "I mapped the goal into a terminal-first workspace. We can build the product in "
            "small slices and keep every decision visible before agents change the code."
        ),
    ),
    ChatMessage(
        author="You",
        body="Organize the frontend first. I want each evolution to be easy to review and commit.",
        is_user=True,
    ),
    ChatMessage(
        author="Moses",
        body=(
            "Understood. Ada owns the TUI shell while I keep the provider and runtime "
            "boundaries out of the interface layer."
        ),
    ),
)
