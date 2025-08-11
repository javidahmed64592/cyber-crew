"""Pytest fixtures for the Cyber Crew unit tests."""

import sys
from unittest.mock import MagicMock

# Mock pexpect on Windows since it's Unix-only
if sys.platform == "win32":
    mock_pexpect = MagicMock()
    mock_pexpect.spawn = MagicMock()
    mock_pexpect.EOF = Exception("EOF")
    mock_pexpect.TIMEOUT = Exception("TIMEOUT")
    sys.modules["pexpect"] = mock_pexpect
