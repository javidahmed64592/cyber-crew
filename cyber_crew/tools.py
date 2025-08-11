"""Tools for the CyberSec Crew."""

import re

from crewai import Agent, Task
from crewai.tools import tool

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


def generate_mission_outcome_summary(report_writer_agent: Agent) -> None:
    """Generate a summary of the mission outcomes and send it to the ReportWriterAgent.

    :param Agent report_writer_agent: The ReportWriterAgent instance.
    """
    report_task = Task(
        agent=report_writer_agent,
        name="Generate Mission Report",
        expected_output="A Markdown document outlining the mission outcomes. Save it in `mission_report.md`.",
        description=(
            "You are a technical documentation specialist responsible for writing a Markdown report that summarizes the"
            "outcome of a cybersecurity mission.\n"
            "Your task is to:\n"
            "1. Ask the ManagerAgent for the following information:\n"
            "- The original mission prompt\n"
            "- The flags or answers discovered\n"
            "- A summary of the crew's approach\n"
            "- Reasoning behind key decisions\n"
            "- Any challenges encountered\n"
            "2. Use that information to generate a Markdown report with the following sections:\n"
            "- Mission Prompt\n"
            "- Flags Found\n"
            "- Approach\n"
            "- Reasoning\n"
            "- Challenges (optional)\n"
            "Format the report clearly using Markdown syntax. Use bullet points, headings, and code blocks where"
            "appropriate.\n"
        ),
    )
    report_writer_agent.execute_task(report_task)


@tool
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


@tool
def gobuster_scan(url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt") -> str:
    """Perform a Gobuster directory scan on the specified URL.

    :param str url: The target URL for the scan.
    :param str wordlist: The wordlist to use for the scan.
    :return str: The output of the Gobuster scan.
    """
    cmd = f"gobuster dir -u {url} -w {wordlist}"
    return str(run_command(cmd))


@tool
def nikto_scan(target: str) -> str:
    """Perform a Nikto scan on the specified target.

    :param str target: The target URL for the scan.
    :return str: The output of the Nikto scan.
    """
    cmd = f"nikto -h {target}"
    return str(run_command(cmd))


@tool
def nmap_scan(target: str) -> str:
    """Perform an Nmap scan on the specified target.

    :param str target: The target URL for the scan.
    :return str: The output of the Nmap scan.
    """
    cmd = f"nmap -Pn -sV {target}"
    return str(run_command(cmd))


@tool
def fetch_url(url: str) -> str:
    """Fetch the content of a URL.

    :param str url: The URL to fetch.
    :return str: The content of the fetched URL.
    """
    cmd = f"curl -s {url}"
    return str(run_command(cmd))


@tool
def search_exploit(query: str) -> str:
    """Search for exploits related to the specified query.

    :param str query: The search query.
    :return str: The search results.
    """
    cmd = f"searchsploit {query}"
    return str(run_command(cmd))


@tool
def find_vulnerable_suids() -> str:
    """Find files with the SUID bit set.

    :return str: The output of the find command.
    """
    cmd = "find / -perm -4000 -type f 2>/dev/null"
    return str(run_command(cmd))


@tool
def check_file_exists(path: str) -> str:
    """Check if a file exists at the specified path.

    :param str path: The file path to check.
    :return str: The result of the file existence check.
    """
    cmd = f"test -f {path} && echo FOUND || echo NOT_FOUND"
    return str(run_command(cmd))


@tool
def list_files(path: str = "/") -> str:
    """List all files in the specified directory.

    :param str path: The directory path to list files from.
    :return str: The list of files in the directory.
    """
    cmd = f"ls -Rla {path}"
    return str(run_command(cmd))


@tool
def read_file(path: str) -> str:
    """Read the contents of a file at the specified path.

    :param str path: The file path to read.
    :return str: The contents of the file.
    """
    cmd = f"cat {path}"
    return str(run_command(cmd))


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file at the specified path.

    :param str path: The file path to write to.
    :param str content: The content to write to the file.
    :return str: Confirmation message or error.
    """
    escaped_content = content.replace("'", "'\"'\"'")
    cmd = f"echo '{escaped_content}' > {path}"
    return str(run_command(cmd))
