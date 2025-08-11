"""Utility functions for the Cyber Crew."""

import re

from crewai import Agent, Task

from cyber_crew.shell import InteractiveShell

_manager_agent: Agent | None = None
_shell: InteractiveShell | None = None


def set_global_vars(manager_agent: Agent | None = None, shell: InteractiveShell | None = None) -> None:
    """Set global variables for the Manager Agent and shell.

    :param Agent | None manager_agent: The Manager Agent instance.
    :param InteractiveShell | None shell: The InteractiveShell instance.
    """
    global _manager_agent, _shell  # noqa: PLW0603
    _manager_agent = manager_agent or _manager_agent
    _shell = shell or _shell


def get_shell() -> InteractiveShell | None:
    """Get the InteractiveShell instance."""
    return _shell


def extract_decision(text: str) -> str:
    """Extract the approval decision from the Manager Agent's response.

    :param str text: The text to extract the decision from.
    :return str: The extracted approval decision.
    """
    match = re.search(r"\b(APPROVED|BLOCKED)\b", text.upper())
    return match.group(1) if match else "BLOCKED"


def request_command_review(cmd: str) -> str:
    """Request approval from the Manager Agent to execute the specified command.

    :param str cmd: The shell command to be executed.
    :return str: The approval decision from the Manager Agent.
    """
    if not _manager_agent:
        msg = "Manager Agent is not set. Please initialize it before requesting command review."
        raise ValueError(msg)

    review_task = Task(
        agent=_manager_agent,
        name="Review Shell Command",
        expected_output="APPROVED or BLOCKED",
        description=(
            f"Evaluate the following shell command for any potential malicious or harmful behavior.\n"
            f"The command must only be used to work towards the mission objective.\n"
            f"It must not be used to interact with any other systems.\n"
            f"Command: `{cmd}`\n"
            f"Should this command be executed? Respond with 'APPROVED' or 'BLOCKED'."
        ),
    )
    decision = _manager_agent.execute_task(review_task)
    return extract_decision(decision)


def run_command(cmd: str) -> str:
    """Execute a shell command after Manager Agent review.

    :param str cmd: The shell command to be executed.
    :return str: The output of the shell command or an error message.
    """
    if not _shell:
        msg = "InteractiveShell is not set. Please initialize it before running commands."
        raise ValueError(msg)

    decision = request_command_review(cmd)
    if decision != "APPROVED":
        return f"Command blocked by Manager Agent: `{cmd}`"
    output = _shell.run_command(cmd)
    return output.strip() or "Command executed successfully."
