"""Interactive shell for Cyber Crew."""

import pexpect


class InteractiveShell:
    """Interactive shell session."""

    def __init__(self, username: str, password: str, prompt: str = r"[$#]\s*") -> None:
        r"""Initialize an interactive SSH shell session.

        :param str username: The username to authenticate with.
        :param str password: The password for the user.
        :param str prompt: The shell prompt to expect (default: r"[$#]\s*").
        """
        self.username = username
        self.password = password
        self.prompt = prompt
        self.child = InteractiveShell.spawn_shell()
        self.child.expect(self.prompt)
        self.child.sendline(f"echo 'Starting session for user {self.username}'")
        self.child.expect(f"Starting session for user {self.username}")
        self.child.sendline(f"su {self.username}")
        self.child.expect("Password:")
        self.child.sendline(self.password)
        self.child.expect(self.prompt)

    @staticmethod
    def spawn_shell() -> pexpect.spawn:
        """Spawn a new shell session."""
        return pexpect.spawn("/bin/bash", encoding="utf-8")

    def run_command(self, cmd: str) -> str:
        """Run a command in the persistent shell session.

        :param str cmd: The command to run.
        :return str: The output of the command.
        """
        self.child.sendline(cmd)
        self.child.expect(self.prompt)
        return str(self.child.before).strip()

    def close(self) -> None:
        """Close the shell session."""
        try:
            self.child.sendline("exit")
            self.child.expect(self.prompt, timeout=5)

            self.child.sendline("exit")
            self.child.expect(pexpect.EOF, timeout=5)
        except (pexpect.TIMEOUT, pexpect.EOF):
            pass
        finally:
            if self.child.isalive():
                self.child.terminate(force=True)
