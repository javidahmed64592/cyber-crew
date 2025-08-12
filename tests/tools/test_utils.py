"""Unit tests for the cyber_crew.tools.utils module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from cyber_crew.tools.utils import (
    extract_decision,
    get_manager_agent,
    get_shell,
    request_command_review,
    run_command,
    set_global_vars,
)


@pytest.fixture
def mock_task() -> Generator[MagicMock, None, None]:
    """Mock the Task class."""
    with patch("cyber_crew.tools.utils.Task", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_manager_agent() -> Generator[MagicMock, None, None]:
    """Mock the manager_agent."""
    with patch("cyber_crew.tools.utils.get_manager_agent", return_value=MagicMock()) as mock:
        yield mock


@pytest.fixture
def mock_shell() -> Generator[MagicMock, None, None]:
    """Mock the shell."""
    with patch("cyber_crew.tools.utils.get_shell", return_value=MagicMock()) as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_set_global_vars(mock_manager_agent: MagicMock, mock_shell: MagicMock) -> None:
    """Mock the set_global_vars function."""
    set_global_vars(mock_manager_agent, mock_shell)


@pytest.fixture
def mock_request_cmd_review() -> Generator[MagicMock, None, None]:
    """Mock the request_command_review function."""
    with patch("cyber_crew.tools.utils.request_command_review", return_value="APPROVED") as mock:
        yield mock


class TestSetGlobalVars:
    """Unit tests for the set_global_vars function."""

    def test_set_global_vars(self, mock_manager_agent: MagicMock, mock_shell: MagicMock) -> None:
        """Test setting global variables."""
        set_global_vars(mock_manager_agent, mock_shell)
        assert get_manager_agent() == mock_manager_agent
        assert get_shell() == mock_shell


class TestUtils:
    """Unit tests for the utility functions."""

    @pytest.mark.parametrize(
        ("decision", "expected"),
        [
            ("APPROVED", "APPROVED"),
            ("COMMAND APPROVED", "APPROVED"),
            ("BLOCKED", "BLOCKED"),
            ("Unknown", "BLOCKED"),
        ],
    )
    def test_extract_decision(self, decision: str, expected: str) -> None:
        """Test the extract_decision function."""
        assert extract_decision(decision) == expected

    @pytest.mark.parametrize(
        ("decision"),
        [
            ("APPROVED"),
            ("BLOCKED"),
        ],
    )
    def test_request_command_review(self, decision: str, mock_task: MagicMock, mock_manager_agent: MagicMock) -> None:
        """Test the request_command_review function."""
        mock_manager_agent.return_value.execute_task.return_value = decision
        result = request_command_review("echo 'Hello World'")
        mock_task.assert_called_once()
        mock_manager_agent.return_value.execute_task.assert_called_once_with(mock_task.return_value)
        assert result == decision

    def test_request_command_review_no_manager(self, mock_manager_agent: MagicMock) -> None:
        """Test the request_command_review function with no manager."""
        mock_manager_agent.return_value = None
        with pytest.raises(ValueError, match="Manager Agent is not set."):
            request_command_review("echo 'Hello World'")

    @pytest.mark.parametrize(
        ("decision", "shell_output", "expected_output"),
        [
            ("BLOCKED", "", "Command blocked by Manager Agent:"),
            ("APPROVED", "", "Command executed successfully."),
            ("APPROVED", "Tool output", "Tool output"),
        ],
    )
    def test_run_command(
        self,
        decision: str,
        shell_output: str,
        expected_output: str,
        mock_request_cmd_review: MagicMock,
        mock_shell: MagicMock,
    ) -> None:
        """Test the run_command function."""
        mock_request_cmd_review.return_value = decision
        mock_shell.return_value.run_command.return_value = shell_output
        command = "echo 'Hello World'"

        result = run_command(command)
        assert expected_output in result

    def test_run_command_no_shell(self, mock_shell: MagicMock) -> None:
        """Test the run_command function with no shell."""
        mock_shell.return_value = None
        with pytest.raises(ValueError, match="InteractiveShell is not set."):
            run_command("echo 'Hello World'")
