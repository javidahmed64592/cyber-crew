"""Unit tests for the cyber_crew.tools.network module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from crewai.tools import BaseTool
from pydantic import BaseModel

from cyber_crew.tools.network import (
    FetchUrl,
    FetchUrlInput,
    GobusterScan,
    GobusterScanInput,
    NiktoScan,
    NiktoScanInput,
    NmapScan,
    NmapScanInput,
)


@pytest.fixture
def mock_run_command() -> Generator[MagicMock, None, None]:
    """Mock the run_command utility function."""
    with patch("cyber_crew.tools.network.run_command") as mock:
        yield mock


class TestFetchUrlInput:
    """Unit tests for the FetchUrlInput model."""

    def test_init(self) -> None:
        """Test creating FetchUrlInput with a valid URL."""
        url = "https://example.com"
        input_data = FetchUrlInput(url=url)

        assert isinstance(input_data, BaseModel)
        assert input_data.url == url


class TestFetchUrl:
    """Unit tests for the FetchUrl tool."""

    def test_init(self) -> None:
        """Test that the FetchUrl tool initializes with correct attributes."""
        tool = FetchUrl()

        assert isinstance(tool, BaseTool)
        assert tool.name == "Fetch URL"
        assert "Tool to fetch the content of a URL." in tool.description
        assert tool.args_schema == FetchUrlInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test fetching a URL."""
        url = "https://example.com"
        output = "Command output"
        mock_run_command.return_value = output
        tool = FetchUrl()

        result = tool._run(url)

        expected_cmd = f"curl -s {url}"
        mock_run_command.assert_called_once_with(expected_cmd)
        assert result == output


class TestGobusterScanInput:
    """Unit tests for the GobusterScanInput model."""

    def test_init(self) -> None:
        """Test creating GobusterScanInput with valid parameters."""
        url = "https://example.com"
        wordlist = "/path/to/wordlist.txt"
        input_data = GobusterScanInput(url=url, wordlist=wordlist)

        assert isinstance(input_data, BaseModel)
        assert input_data.url == url
        assert input_data.wordlist == wordlist


class TestGobusterScan:
    """Unit tests for the GobusterScan tool."""

    def test_init(self) -> None:
        """Test that the GobusterScan tool initializes with correct attributes."""
        tool = GobusterScan()

        assert isinstance(tool, BaseTool)
        assert tool.name == "Gobuster Scan"
        assert "Tool to run a Gobuster scan." in tool.description
        assert tool.args_schema == GobusterScanInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test running a Gobuster scan."""
        url = "https://example.com"
        wordlist = "/path/to/wordlist.txt"
        output = "Command output"
        mock_run_command.return_value = output
        tool = GobusterScan()

        result = tool._run(url, wordlist)

        expected_cmd = f"gobuster dir -u {url} -w {wordlist}"
        mock_run_command.assert_called_once_with(expected_cmd)
        assert result == output


class TestNiktoScanInput:
    """Unit tests for the NiktoScanInput model."""

    def test_init(self) -> None:
        """Test creating NiktoScanInput with a valid URL."""
        url = "https://example.com"
        input_data = NiktoScanInput(url=url)

        assert isinstance(input_data, BaseModel)
        assert input_data.url == url


class TestNiktoScan:
    """Unit tests for the NiktoScan tool."""

    def test_init(self) -> None:
        """Test that the NiktoScan tool initializes with correct attributes."""
        tool = NiktoScan()

        assert isinstance(tool, BaseTool)
        assert tool.name == "Nikto Scan"
        assert "Tool to run a Nikto scan." in tool.description
        assert tool.args_schema == NiktoScanInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test running a Nikto scan."""
        url = "https://example.com"
        output = "Command output"
        mock_run_command.return_value = output
        tool = NiktoScan()

        result = tool._run(url)

        expected_cmd = f"nikto -h {url}"
        mock_run_command.assert_called_once_with(expected_cmd)
        assert result == output


class TestNmapScanInput:
    """Unit tests for the NmapScanInput model."""

    def test_init(self) -> None:
        """Test creating NmapScanInput with a valid URL."""
        url = "123.123.123.123"
        input_data = NmapScanInput(url=url)

        assert isinstance(input_data, BaseModel)
        assert input_data.url == url


class TestNmapScan:
    """Unit tests for the NmapScan tool."""

    def test_init(self) -> None:
        """Test that the NmapScan tool initializes with correct attributes."""
        tool = NmapScan()

        assert isinstance(tool, BaseTool)
        assert tool.name == "Nmap Scan"
        assert "Tool to run a Nmap scan." in tool.description
        assert tool.args_schema == NmapScanInput

    def test_run(self, mock_run_command: MagicMock) -> None:
        """Test running a Nmap scan."""
        url = "123.123.123.123"
        output = "Command output"
        mock_run_command.return_value = output
        tool = NmapScan()

        result = tool._run(url)

        expected_cmd = f"nmap -Pn -sV {url}"
        mock_run_command.assert_called_once_with(expected_cmd)
        assert result == output
