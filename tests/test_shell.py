"""Unit tests for the cyber_crew.shell module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pexpect
import pytest

from cyber_crew.shell import InteractiveShell

MOCK_USERNAME = "test_user"
MOCK_PASSWORD = "test_password"  # noqa: S105
MOCK_PROMPT = r"[$#]\s*"


@pytest.fixture
def mock_spawn_shell() -> Generator[MagicMock, None, None]:
    """Fixture to create a mock spawn_shell function."""
    with patch("cyber_crew.shell.InteractiveShell.spawn_shell", return_value=MagicMock()) as mock_shell:
        yield mock_shell


@pytest.fixture
def mock_interactive_shell(mock_spawn_shell: MagicMock) -> InteractiveShell:
    """Fixture to create a mock InteractiveShell instance."""
    shell = InteractiveShell(MOCK_USERNAME, MOCK_PASSWORD, MOCK_PROMPT)
    shell.child = mock_spawn_shell.return_value
    return shell


class TestInteractiveShell:
    """Unit tests for the InteractiveShell class."""

    def test_init(self, mock_interactive_shell: InteractiveShell, mock_spawn_shell: MagicMock) -> None:
        """Test the initialization of the InteractiveShell."""
        shell = mock_spawn_shell.return_value
        assert mock_interactive_shell.child == shell

        # Check that the expected method calls were made during initialization
        shell.expect.assert_any_call(mock_interactive_shell.prompt)
        shell.sendline.assert_any_call(f"echo 'Starting session for user {mock_interactive_shell.username}'")
        shell.expect.assert_any_call(f"Starting session for user {mock_interactive_shell.username}")
        shell.sendline.assert_any_call(f"su {mock_interactive_shell.username}")
        shell.expect.assert_any_call("Password:")
        shell.sendline.assert_any_call(mock_interactive_shell.password)

    def test_run_command(self, mock_interactive_shell: InteractiveShell) -> None:
        """Test the run_command method of the InteractiveShell."""
        command = "ls -la"
        mock_interactive_shell.run_command(command)

        # Check that the expected method calls were made
        shell = mock_interactive_shell.child
        shell.sendline.assert_any_call(command)
        shell.expect.assert_any_call(mock_interactive_shell.prompt)

    def test_close(self, mock_interactive_shell: InteractiveShell) -> None:
        """Test the close method of the InteractiveShell."""
        mock_interactive_shell.close()

        # Check that the expected method calls were made
        shell = mock_interactive_shell.child
        shell.sendline.assert_any_call("exit")
        shell.expect.assert_any_call(mock_interactive_shell.prompt, timeout=5)
        shell.sendline.assert_any_call("exit")
        shell.expect.assert_any_call(pexpect.EOF, timeout=5)

        # Verify that the child process is terminated
        assert shell.terminate.call_count == 1
