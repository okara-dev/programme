# Programs and Automation

This folder brings together personal programs, helper tools, bots, games, and small utilities for everyday use, automation, and creative experiments. The projects are intentionally designed to be fairly self-contained and can run with Python, Node.js, PowerShell, or other local tools depending on their purpose.

## Overview

This directory contains several categories of projects:

- Bots and automation for information gathering, processing, and output
- Command-line tools for recurring tasks in everyday development work
- Small games and interactive experiments
- Practical Windows shell helpers
- Personal prototypes and mini-tools

## Structure

### `bots/`
This is where automated programs live. They often handle tasks such as fetching data, processing information, or generating reports. The content is usually logic- and workflow-oriented and can function as lightweight background or runtime tools.

### `cli/`
This area contains command-line utilities for tasks like file organization, analysis, conversion, checking, and helper functions. Many projects here are compact and focused on a specific problem.

### `desktop-cat/`
A personal desktop project with its own interface or interactive application. It shows that visual or system-level experiments can also be part of this workspace.

### `games/`
Games and playful projects, including smaller finished projects and experiments using different techniques and design ideas.

### `shell-befehle/`
A collection of PowerShell helpers and everyday tools for Windows environments. The main entry point is the file `shell_toolbox.ps1`.

## Typical Technology Stack

- Python for bots, data processing, and automation
- Node.js and JavaScript for CLI tools and small server environments
- PowerShell for Windows automation and system commands
- Game and UI prototypes depending on project needs
- local configuration files such as `config.json`, `requirements.txt`, or similar

## How I start a project

Each project can have its own dependencies and startup flow. In general:

1. Read the project README
2. Check the relevant configuration or dependency files
3. Install the required packages or libraries
4. Run the startup command for that project

### Python projects

```bash
pip install -r requirements.txt
python main.py
```

### Node.js projects

```bash
npm install
npm start
```

### PowerShell helpers

```powershell
.\shell_toolbox.ps1
```

## Notes

- Some projects require API keys, local paths, or configuration values.
- This information should not be hardcoded in the source but provided through `config.json`, environment variables, or local files.
- If a project has its own structure with multiple files or subfolders, that project README is the most important reference.

This directory serves as a collection of practical, self-developed tools and experiments, with a focus on useful automation, CLI helpers, and small personal applications.