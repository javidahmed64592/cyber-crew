"""Unit tests for the cyber_crew.tools.filesystem module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from crewai.tools import BaseTool
from pydantic import BaseModel

from cyber_crew.tools.filesystem import (
    CheckFileExists,
    CheckFileExistsInput,
    ListFiles,
    ListFilesInput,
    ReadFile,
    ReadFileInput,
)


@pytest.fixture
def mock_run_command() -> Generator[MagicMock, None, None]:
    """Mock the run_command utility function."""
    with patch("cyber_crew.tools.filesystem.run_command") as mock:
        yield mock


class TestCheckFileExistsInput:
    """Unit tests for the CheckFileExistsInput model."""

    def test_init(self) -> None:
        """Test creating CheckFileExistsInput with a valid path."""
        path = "/path/to/file.txt"
        input_data = CheckFileExistsInput(path=path)

        assert isinstance(input_data, BaseModel)
        assert input_data.path == path


class TestCheckFileExists:
    """Unit tests for the CheckFileExists tool."""

    def test_init(self) -> None:
        """Test that the CheckFileExists tool initializes with correct attributes."""
        tool = CheckFileExists()

        assert isinstance(tool, BaseTool)
        assert tool.name == "Check File Exists"
        assert "Tool to check a file's existence." in tool.description
        assert tool.args_schema == CheckFileExistsInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test checking if a file exists."""
        path = "/path/to/file.txt"
        output = "Command output"
        mock_run_command.return_value = output
        tool = CheckFileExists()

        result = tool._run(path)

        expected_cmd = f"test -f {path} && echo FOUND || echo NOT_FOUND"
        mock_run_command.assert_called_once_with(expected_cmd)
        assert result == output


class TestListFilesInput:
    """Unit tests for the ListFilesInput model."""

    def test_init(self) -> None:
        """Test creating ListFilesInput with a valid path."""
        path = "/path/to/directory"
        input_data = ListFilesInput(path=path)

        assert isinstance(input_data, BaseModel)
        assert input_data.path == path


class TestListFiles:
    """Unit tests for the ListFiles tool."""

    def test_init(self) -> None:
        """Test that the ListFiles tool initializes with correct attributes."""
        tool = ListFiles()

        assert isinstance(tool, BaseTool)
        assert tool.name == "List Files"
        assert "Tool to list the files in a directory." in tool.description
        assert tool.args_schema == ListFilesInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test listing files in a directory."""
        path = "/path/to/directory"
        output = "Command output"
        mock_run_command.return_value = output
        tool = ListFiles()

        result = tool._run(path)

        expected_cmd = f"ls -Rla {path}"
        mock_run_command.assert_called_once_with(expected_cmd)
        assert result == output


class TestReadFileInput:
    """Unit tests for the ReadFileInput model."""

    def test_init(self) -> None:
        """Test creating ReadFileInput with a valid path."""
        path = "/path/to/file.txt"
        input_data = ReadFileInput(path=path)

        assert isinstance(input_data, BaseModel)
        assert input_data.path == path


class TestReadFile:
    """Unit tests for the ReadFile tool."""

    def test_init(self) -> None:
        """Test that the ReadFile tool initializes with correct attributes."""
        tool = ReadFile()

        assert isinstance(tool, BaseTool)
        assert tool.name == "Read File"
        assert "Tool to read a file." in tool.description
        assert tool.args_schema == ReadFileInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test reading a file."""
        path = "/path/to/file.txt"
        output = "Command output"
        mock_run_command.return_value = output
        tool = ReadFile()

        result = tool._run(path)

        expected_cmd = f"cat {path}"
        mock_run_command.assert_called_once_with(expected_cmd)
        assert result == output
