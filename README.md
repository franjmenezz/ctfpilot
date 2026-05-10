# 🧭 CTFPilot

> Your co-pilot for CTFs and HackTheBox machines

CTFPilot is a professional CLI tool designed to assist pentesters during CTF competitions and HackTheBox machines. It automates the tedious parts — reconnaissance, suggestions, documentation — so you can focus on what matters: thinking and exploiting.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey)

---

## Features

- Auto-detection of target platform (HTB, THM, CTF)
- Automated port scanning with Nmap
- CVE lookup via NVD API based on detected service versions
- Intelligent attack vector suggestions per port and port combinations
- Session management with SQLite (start, note, flag, finish)
- Session history and active session timer
- Wordlist recommendations by service type
- Report generation in HTML, PDF and Markdown formats
- Clean, professional terminal output with Rich

---

## Installation

```bash
git clone https://github.com/franjmenezz/ctfpilot.git
cd ctfpilot
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install -e .
```

> Requires Nmap installed on the system: https://nmap.org/download.html

---

## Usage

```bash
# Start a new session (auto-detects HTB/THM)
ctfpilot start --target 10.10.11.25 --name "MachineName"

# Add notes during the session
ctfpilot note "Found /admin directory exposed"

# Register a captured flag
ctfpilot flag --type user --value "a3f5c8d1..."

# Check session status and elapsed time
ctfpilot status
ctfpilot timer

# Get wordlist suggestions
ctfpilot wordlist http
ctfpilot wordlist smb

# Generate report
ctfpilot report --format html
ctfpilot report --format md
ctfpilot report --format pdf

# View session history
ctfpilot history

# Finish active session
ctfpilot finish
```

---

## Commands

| Command | Description |
|---|---|
| `start` | Start a new pentesting session |
| `note` | Add a note to the active session |
| `flag` | Register a captured flag |
| `status` | Show active session details |
| `timer` | Show elapsed time in active session |
| `finish` | Close the active session |
| `history` | Show all past sessions |
| `wordlist` | Get wordlist suggestions by service |
| `report` | Generate HTML, PDF or Markdown report |

---

## Report Example

Reports are automatically saved to `~/Desktop/CTFPilot/` and include:

- Target information and platform
- Captured flags
- Session notes with timestamps
- Timeline of the session

---

## Roadmap

- [x] CLI base with session management
- [x] Automated port scanning with CVE lookup
- [x] Intelligent suggestion engine
- [x] Multi-format report generation
- [x] Wordlist recommendations
- [x] Session timer
- [ ] Docker support
- [ ] CI/CD pipeline with security scanning
- [ ] Kubernetes manifests
- [ ] AI-powered suggestions via Ollama

---

## Author

**Francisco Jiménez** — Pentester & Full Stack Developer oriented to DevSecOps

[![GitHub](https://img.shields.io/badge/GitHub-franjmenezz-black)](https://github.com/franjmenezz)

---

## License

MIT License — feel free to use and contribute.
=======

>>>>>>> ad5cf7db39143abcbbe95db627f4bc9d9c025817
