"""Unit tests for the cyber_crew.main module."""

import os
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from cyber_crew.main import cleanup, create_shell, crew_test, get_context_dictionary, parse_args, replay, run, train


@pytest.fixture
def mock_set_global_vars() -> Generator[MagicMock, None, None]:
    """Fixture for mocking global variables."""
    with patch("cyber_crew.main.set_global_vars") as mock:
        yield mock


class TestArgs:
    """Unit tests for argument parsing."""

    def test_parse_args_with_all_arguments(self) -> None:
        """Test parse_args with all arguments provided."""
        test_args = [
            "--username",
            "test_user",
            "--password",
            "test_pass",
            "--prompt",
            "Test mission prompt",
            "--config",
            "custom_config.yaml",
            "--n_iterations",
            "5",
            "--filename",
            "output.json",
        ]

        with patch("sys.argv", ["main.py", *test_args]):
            args = parse_args()

            assert args.username == "test_user"
            assert args.password == "test_pass"  # noqa: S105
            assert args.prompt == "Test mission prompt"
            assert args.config == "custom_config.yaml"
            assert args.n_iterations == 5  # noqa: PLR2004
            assert args.filename == "output.json"

    def test_parse_args_with_short_flags(self) -> None:
        """Test parse_args with short flag arguments."""
        test_args = [
            "-u",
            "short_user",
            "-p",
            "short_pass",
            "-m",
            "Short mission prompt",
            "-c",
            "short_config.yaml",
            "-n",
            "5",
            "-f",
            "short_output.json",
        ]

        with patch("sys.argv", ["main.py", *test_args]):
            args = parse_args()

            assert args.username == "short_user"
            assert args.password == "short_pass"  # noqa: S105
            assert args.prompt == "Short mission prompt"
            assert args.config == "short_config.yaml"
            assert args.n_iterations == 5  # noqa: PLR2004
            assert args.filename == "short_output.json"

    def test_parse_args_with_defaults(self) -> None:
        """Test parse_args with default values when not provided."""
        test_args = ["--username", "default_user", "--password", "default_pass", "--prompt", "Default mission prompt"]

        with patch("sys.argv", ["main.py", *test_args]):
            args = parse_args()

            assert args.username == "default_user"
            assert args.password == "default_pass"  # noqa: S105
            assert args.prompt == "Default mission prompt"
            assert args.config == "config.yaml"
            assert args.n_iterations == 1
            assert args.filename == "training_data.json"

    def test_parse_args_missing_required_username(self) -> None:
        """Test parse_args raises SystemExit when username is missing."""
        test_args = ["--password", "test_pass", "--prompt", "Test mission prompt"]

        with patch("sys.argv", ["main.py", *test_args]):
            with pytest.raises(SystemExit):
                parse_args()

    def test_parse_args_missing_required_password(self) -> None:
        """Test parse_args raises SystemExit when password is missing."""
        test_args = ["--username", "test_user", "--prompt", "Test mission prompt"]

        with patch("sys.argv", ["main.py", *test_args]):
            with pytest.raises(SystemExit):
                parse_args()

    def test_parse_args_missing_required_prompt(self) -> None:
        """Test parse_args raises SystemExit when prompt is missing."""
        test_args = ["--username", "test_user", "--password", "test_pass"]

        with patch("sys.argv", ["main.py", *test_args]):
            with pytest.raises(SystemExit):
                parse_args()


class TestSetup:
    """Unit tests for the setup process."""

    @pytest.fixture
    def mock_interactive_shell(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock the InteractiveShell class."""
        with patch("cyber_crew.main.InteractiveShell", autospec=True) as mock_shell:
            yield mock_shell

    @pytest.fixture
    def mock_get_shell(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock the get_shell function."""
        with patch("cyber_crew.main.get_shell") as mock_shell:
            yield mock_shell

    def test_get_context_dictionary(self) -> None:
        """Test get_context_dictionary returns the correct values."""
        context = get_context_dictionary(MagicMock(prompt="Default mission prompt"))
        assert context == {
            "mission_prompt": "Default mission prompt",
        }

    def test_create_shell(self, mock_set_global_vars: MagicMock, mock_interactive_shell: MagicMock) -> None:
        """Test create_shell calls set_global_vars with the correct arguments."""
        username = "test_user"
        password = "test_pass"  # noqa: S105

        create_shell(MagicMock(username=username, password=password))
        mock_interactive_shell.assert_called_once_with(username=username, password=password)
        mock_set_global_vars.assert_called_once_with(shell=mock_interactive_shell.return_value)

    def test_cleanup(self, mock_get_shell: MagicMock) -> None:
        """Test cleanup calls close on the shell if it exists."""
        mock_get_shell.return_value = MagicMock()

        cleanup()

        mock_get_shell.assert_called_once()
        mock_get_shell.return_value.close.assert_called_once()


class TestMain:
    """Unit tests for the main entry points."""

    @pytest.fixture
    def mock_args(self) -> Generator[MagicMock, None, None]:
        """Fixture for mocking command line arguments."""
        with patch("cyber_crew.main.parse_args") as mock:
            yield mock

    @pytest.fixture
    def mock_get_context_dictionary(self) -> Generator[MagicMock, None, None]:
        """Fixture for mocking the get_context_dictionary function."""
        with patch("cyber_crew.main.get_context_dictionary") as mock:
            yield mock

    @pytest.fixture
    def mock_create_shell(self) -> Generator[MagicMock, None, None]:
        """Fixture for mocking the create_shell function."""
        with patch("cyber_crew.main.create_shell") as mock:
            yield mock

    @pytest.fixture
    def mock_cleanup(self) -> Generator[MagicMock, None, None]:
        """Fixture for mocking the cleanup function."""
        with patch("cyber_crew.main.cleanup") as mock:
            yield mock

    @pytest.fixture
    def mock_cyber_crew(self) -> Generator[MagicMock, None, None]:
        """Fixture for mocking the CyberCrew class."""
        with patch("cyber_crew.main.CyberCrew", autospec=True) as mock:
            yield mock

    def test_run(
        self,
        mock_args: MagicMock,
        mock_get_context_dictionary: MagicMock,
        mock_create_shell: MagicMock,
        mock_cleanup: MagicMock,
        mock_cyber_crew: MagicMock,
    ) -> None:
        """Test the run function."""
        run()
        mock_args.assert_called_once()
        mock_get_context_dictionary.assert_called_once_with(args=mock_args.return_value)
        mock_create_shell.assert_called_once_with(args=mock_args.return_value)
        mock_cyber_crew.assert_called_once()
        mock_cyber_crew.return_value.crew.assert_called_once()
        mock_cyber_crew.return_value.crew.return_value.kickoff.assert_called_once_with(
            inputs=mock_get_context_dictionary.return_value
        )
        mock_cleanup.assert_called_once()

    def test_train(
        self,
        mock_args: MagicMock,
        mock_get_context_dictionary: MagicMock,
        mock_create_shell: MagicMock,
        mock_cleanup: MagicMock,
        mock_cyber_crew: MagicMock,
    ) -> None:
        """Test the train function."""
        train()
        mock_args.assert_called_once()
        mock_get_context_dictionary.assert_called_once_with(args=mock_args.return_value)
        mock_create_shell.assert_called_once_with(args=mock_args.return_value)
        mock_cyber_crew.assert_called_once()
        mock_cyber_crew.return_value.crew.assert_called_once()
        mock_cyber_crew.return_value.crew.return_value.train.assert_called_once_with(
            n_iterations=int(mock_args.return_value.n_iterations),
            filename=mock_args.return_value.filename,
            inputs=mock_get_context_dictionary.return_value,
        )
        mock_cleanup.assert_called_once()

    def test_replay(
        self,
        mock_args: MagicMock,
        mock_create_shell: MagicMock,
        mock_cleanup: MagicMock,
        mock_cyber_crew: MagicMock,
    ) -> None:
        """Test the replay function."""
        replay()
        mock_args.assert_called_once()
        mock_create_shell.assert_called_once_with(args=mock_args.return_value)
        mock_cyber_crew.assert_called_once()
        mock_cyber_crew.return_value.crew.assert_called_once()
        mock_cyber_crew.return_value.crew.return_value.replay.assert_called_once_with(
            task_id=mock_args.return_value.task_id
        )
        mock_cleanup.assert_called_once()

    def test_crew_test(
        self,
        mock_args: MagicMock,
        mock_get_context_dictionary: MagicMock,
        mock_create_shell: MagicMock,
        mock_cleanup: MagicMock,
        mock_cyber_crew: MagicMock,
    ) -> None:
        """Test the crew_test function."""
        crew_test()
        mock_args.assert_called_once()
        mock_get_context_dictionary.assert_called_once_with(args=mock_args.return_value)
        mock_create_shell.assert_called_once_with(args=mock_args.return_value)
        mock_cyber_crew.assert_called_once()
        mock_cyber_crew.return_value.crew.assert_called_once()
        mock_cyber_crew.return_value.crew.return_value.test.assert_called_once_with(
            n_iterations=int(mock_args.return_value.n_iterations),
            eval_llm=os.environ.get("MODEL"),
            inputs=mock_get_context_dictionary.return_value,
        )
        mock_cleanup.assert_called_once()
