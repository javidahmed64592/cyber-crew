[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-Optimized-557C94?style=flat&logo=kalilinux&logoColor=white)](https://www.kali.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Powered-FF6B35?style=flat&logo=ai&logoColor=white)](https://www.crewai.com/)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- omit from toc -->
# Cyber Crew

An AI-powered cybersecurity automation framework built with CrewAI that orchestrates specialized agents to conduct penetration testing and capture-the-flag (CTF) challenges. The Cyber Crew consists of expert AI agents working collaboratively to perform reconnaissance, vulnerability analysis, exploitation, privilege escalation, and comprehensive reporting.

## Features

- **Specialized AI Agents**: Eight expert agents with distinct cybersecurity roles
- **Coordinated Operations**: Hierarchical management with shared context awareness
- **Comprehensive Toolset**: Network scanning, vulnerability assessment, exploitation, and file system analysis
- **Professional Reporting**: Automated generation of industry-standard engagement reports
- **Safety First**: Built-in command review and safety mechanisms

## Meet the Crew

- **Manager Agent**: Senior operations coordinator ensuring mission success and safety
- **Recon Specialist**: Advanced network reconnaissance and stealth enumeration
- **Vulnerability Analyst**: Deep vulnerability research and exploit chain development
- **Exploit Engineer**: Custom payload crafting and exploitation techniques
- **Access Broker**: Authentication bypass and initial access establishment
- **Privilege Escalator**: System privilege elevation and lateral movement
- **File Mapper**: Digital forensics and file system analysis
- **Flag Hunter**: Mission objective extraction and verification
- **Report Writer**: Professional cybersecurity documentation specialist

## Architecture

- **Hierarchical Process**: Manager agent coordinates specialist teams
- **Shared Context**: Agents build upon each other's discoveries
- **Tool Integration**: Nmap, Gobuster, Nikto, custom exploit tools
- **Safety Mechanisms**: Command review prevents destructive operations
- **Flexible Workflows**: Context-aware task dependencies for complex missions

## Security Notice

**IMPORTANT: Legal and Ethical Use Only**

This tool is designed **exclusively for educational purposes, authorized penetration testing, and legitimate cybersecurity research**. By using this software, you acknowledge and agree to the following:

### Authorized Use Cases
- **Educational Learning**: Cybersecurity training and skill development
- **Authorized Penetration Testing**: Testing systems you own or have explicit written permission to test
- **CTF Competitions**: Capture-the-flag challenges and cybersecurity competitions
- **Security Research**: Legitimate vulnerability research in controlled environments
- **Professional Assessments**: Licensed security assessments with proper authorization

### Prohibited Activities
- **Unauthorized Access**: Testing systems without explicit permission
- **Malicious Activities**: Any form of cyber attack or harmful exploitation
- **Illegal Purposes**: Activities that violate local, state, or federal laws
- **Data Theft**: Unauthorized access to or exfiltration of sensitive information
- **Service Disruption**: Causing denial of service or system damage

### User Responsibilities
- **Obtain Proper Authorization**: Ensure you have written permission before testing any system
- **Respect Privacy**: Do not access, modify, or steal personal or confidential data
- **Follow Laws**: Comply with all applicable cybersecurity and computer crime laws
- **Use Responsibly**: Employ this tool only for constructive and legal purposes

<!-- omit from toc -->
## Table of Contents
- [Features](#features)
- [Meet the Crew](#meet-the-crew)
- [Architecture](#architecture)
- [Security Notice](#security-notice)
  - [Authorized Use Cases](#authorized-use-cases)
  - [Prohibited Activities](#prohibited-activities)
  - [User Responsibilities](#user-responsibilities)
- [uv](#uv)
- [Installing Dependencies](#installing-dependencies)
- [Configuration](#configuration)
  - [Custom Tools](#custom-tools)
- [Safety Features](#safety-features)
- [Testing, Linting, and Type Checking](#testing-linting-and-type-checking)
- [License](#license)

## uv
This repository is managed using the `uv` Python project manager: https://docs.astral.sh/uv/

To install `uv`:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh                                    # Linux/Mac
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
```

## Installing Dependencies
Install the required dependencies using `uv`:

    uv sync

To install with `dev` dependencies:

    uv sync --extra dev

## Configuration

The crew behavior is defined in YAML configuration files:

- `cyber_crew/config/agents.yaml`: Agent roles, goals, and backstories
- `cyber_crew/config/tasks.yaml`: Task descriptions and expected outputs

### Custom Tools

The crew uses specialized tools located in `cyber_crew/tools/`:

- **Network Tools**: Nmap, Gobuster, Nikto scanning capabilities
- **Vulnerability Tools**: Exploit database search and SUID binary detection
- **File System Tools**: Directory listing, file reading, and existence checking
- **Command Execution**: Safe shell command execution with review mechanisms

## Safety Features

- **Command Review**: Manager agent reviews all shell commands before execution
- **Destructive Command Prevention**: Blocks operations that could damage systems
- **Access Coordination**: Prevents conflicts between shared shell sessions

## Testing, Linting, and Type Checking

- **Run tests:** `uv run pytest`
- **Lint code:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Type check:** `uv run mypy .`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
