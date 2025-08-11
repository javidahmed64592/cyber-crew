"""Unit tests for the cyber_crew.tools module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from cyber_crew import tools

MOCK_TARGET = "123.123.123.123"


@pytest.fixture
def mock_task() -> Generator[MagicMock, None, None]:
    """Mock the Task class."""
    with patch("cyber_crew.tools.Task", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_manager_agent() -> MagicMock:
    """Mock the manager_agent."""
    return MagicMock()


@pytest.fixture
def mock_shell() -> MagicMock:
    """Mock the shell."""
    return MagicMock()


@pytest.fixture(autouse=True)
def mock_set_global_vars(mock_manager_agent: MagicMock, mock_shell: MagicMock) -> None:
    """Mock the set_global_vars function."""
    tools.set_global_vars(mock_manager_agent, mock_shell)


class TestUtils:
    """Unit tests for the crew utility tools."""

    @pytest.mark.parametrize(
        ("text", "expected_decision"),
        [
            ("The command is APPROVED", "APPROVED"),
            ("The command is BLOCKED", "BLOCKED"),
            ("No decision provided", "BLOCKED"),
            ("This is a random text", "BLOCKED"),
        ],
    )
    def test_extract_decision(self, text: str, expected_decision: str) -> None:
        """Test the extract_decision function."""
        assert tools.extract_decision(text) == expected_decision

    @pytest.mark.parametrize(
        ("decision"),
        [
            ("APPROVED"),
            ("BLOCKED"),
        ],
    )
    def test_request_command_review(self, decision: str, mock_task: MagicMock, mock_manager_agent: MagicMock) -> None:
        """Test the request_command_review function."""
        mock_manager_agent.execute_task.return_value = decision
        result = tools.request_command_review("echo 'Hello World'")
        mock_task.assert_called_once()
        assert result == decision

    def test_generate_mission_outcome_summary(self, mock_task: MagicMock) -> None:
        """Test the generate_mission_outcome_summary function."""
        mock_reporter = MagicMock()
        tools.generate_mission_outcome_summary(mock_reporter)
        mock_task.assert_called_once()
        mock_reporter.execute_task.assert_called_once_with(mock_task.return_value)


class TestTools:
    """Unit tests for the shell command tools."""

    @pytest.fixture
    def mock_request_cmd_review(self) -> Generator[MagicMock, None, None]:
        """Mock the request_command_review function."""
        with patch("cyber_crew.tools.request_command_review", return_value="APPROVED") as mock:
            yield mock

    @pytest.fixture
    def mock_run_command(self) -> Generator[MagicMock, None, None]:
        """Mock the run_command function."""
        with patch("cyber_crew.tools.run_command") as mock:
            yield mock

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
        mock_shell.run_command = MagicMock(return_value=shell_output)
        command = "echo 'Hello World'"

        result = tools.run_command.func(command)
        assert expected_output in result

    def test_gobuster_scan(self, mock_run_command: MagicMock) -> None:
        """Test the gobuster_scan function."""
        mock_run_command.return_value = "Gobuster scan completed."
        result = tools.gobuster_scan.func(MOCK_TARGET)
        mock_run_command.assert_called_once_with(
            f"gobuster dir -u {MOCK_TARGET} -w /usr/share/wordlists/dirb/common.txt"
        )
        assert result == "Gobuster scan completed."

    def test_nikto_scan(self, mock_run_command: MagicMock) -> None:
        """Test the nikto_scan function."""
        mock_run_command.return_value = "Nikto scan completed."
        result = tools.nikto_scan.func(MOCK_TARGET)
        mock_run_command.assert_called_once_with(f"nikto -h {MOCK_TARGET}")
        assert result == "Nikto scan completed."

    def test_nmap_scan(self, mock_run_command: MagicMock) -> None:
        """Test the nmap_scan function."""
        mock_run_command.return_value = "Nmap scan completed."
        result = tools.nmap_scan.func(MOCK_TARGET)
        mock_run_command.assert_called_once_with(f"nmap -Pn -sV {MOCK_TARGET}")
        assert result == "Nmap scan completed."

    def test_fetch_url(self, mock_run_command: MagicMock) -> None:
        """Test the fetch_url function."""
        mock_run_command.return_value = "Fetched content."
        result = tools.fetch_url.func(MOCK_TARGET)
        mock_run_command.assert_called_once_with(f"curl -s {MOCK_TARGET}")
        assert result == "Fetched content."

    def test_search_exploit(self, mock_run_command: MagicMock) -> None:
        """Test the search_exploit function."""
        mock_run_command.return_value = "Search results."
        result = tools.search_exploit.func("example")
        mock_run_command.assert_called_once_with("searchsploit example")
        assert result == "Search results."

    def test_find_vulnerable_suids(self, mock_run_command: MagicMock) -> None:
        """Test the find_vulnerable_suids function."""
        mock_run_command.return_value = "Vulnerable SUIDs found."
        result = tools.find_vulnerable_suids.func()
        mock_run_command.assert_called_once_with("find / -perm -4000 -type f 2>/dev/null")
        assert result == "Vulnerable SUIDs found."

    def test_check_file_exists(self, mock_run_command: MagicMock) -> None:
        """Test the check_file_exists function."""
        mock_run_command.return_value = "File exists."
        result = tools.check_file_exists.func("example.txt")
        mock_run_command.assert_called_once_with("test -f example.txt && echo FOUND || echo NOT_FOUND")
        assert result == "File exists."

    def test_list_files(self, mock_run_command: MagicMock) -> None:
        """Test the list_files function."""
        mock_run_command.return_value = "file1.txt\nfile2.txt\nfile3.txt"
        result = tools.list_files.func("example_dir")
        mock_run_command.assert_called_once_with("ls -Rla example_dir")
        assert result == "file1.txt\nfile2.txt\nfile3.txt"

    def test_read_file(self, mock_run_command: MagicMock) -> None:
        """Test the read_file function."""
        mock_run_command.return_value = "File content."
        result = tools.read_file.func("example.txt")
        mock_run_command.assert_called_once_with("cat example.txt")
        assert result == "File content."

    def test_write_file(self, mock_run_command: MagicMock) -> None:
        """Test the write_file function."""
        mock_run_command.return_value = "File written."
        result = tools.write_file.func("example.txt", "New content.")
        mock_run_command.assert_called_once_with("echo 'New content.' > example.txt")
        assert result == "File written."
