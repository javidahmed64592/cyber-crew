"""Unit tests for the cyber_crew.tools.run_command module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from crewai.tools import BaseTool
from pydantic import BaseModel

from cyber_crew.tools.run_command import RunCommand, RunCommandInput


@pytest.fixture
def mock_run_command() -> Generator[MagicMock, None, None]:
    """Mock the run_command utility function."""
    with patch("cyber_crew.tools.run_command.run_command") as mock:
        yield mock


class TestRunCommandInput:
    """Unit tests for the RunCommandInput model."""

    def test_init(self) -> None:
        """Test creating RunCommandInput with a valid command."""
        command = "echo 'Hello World'"
        input_data = RunCommandInput(cmd=command)

        assert isinstance(input_data, BaseModel)
        assert input_data.cmd == command


class TestRunCommand:
    """Unit tests for the RunCommand tool."""

    def test_init(self) -> None:
        """Test that the RunCommand tool initializes with correct attributes."""
        tool = RunCommand()

        assert isinstance(tool, BaseTool)
        assert tool.name == "Run Command"
        assert "Tool to run a shell command." in tool.description
        assert tool.args_schema == RunCommandInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test running a valid command."""
        command = "echo 'Hello World'"
        output = "Command output"
        mock_run_command.return_value = output
        tool = RunCommand()

        result = tool._run(command)

        mock_run_command.assert_called_once_with(command)
        assert result == output
