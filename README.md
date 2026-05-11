# 🧭 CTFPilot

> Your co-pilot for CTFs and HackTheBox machines

![CTFPilot Banner](docs/CTFPilot_1.png)

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Kali-red)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)

CTFPilot is a professional CLI tool designed to assist pentesters during CTF competitions and HackTheBox machines. It automates the tedious parts — reconnaissance, CVE lookup, attack suggestions, documentation — so you can focus on what matters: thinking and exploiting.

---

## 📸 Screenshots

![Recon and AI suggestions](docs/CTFPilot_2.png)

![HTML Report](docs/CTFPilot_3.png)

---

## ✨ Features

- **Auto-detection** of target platform (HTB, THM, CTF) from IP range
- **Automated port scanning** with Nmap integration
- **CVE lookup** via NVD API based on detected service versions
- **Intelligent attack vector suggestions** per port and port combinations
- **AI-powered analysis** via Groq API (llama-3.3-70b-versatile)
- **Session management** with SQLite (start, note, flag, finish)
- **Session history** and active session timer
- **Wordlist recommendations** by service type
- **Multi-format reports**: HTML, PDF and Markdown
- **Clean, professional terminal output** with Rich

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| Language | Python 3.11+ | Core development |
| CLI | Typer + Rich | Terminal interface |
| Database | SQLite | Session persistence |
| Port scanning | python-nmap | Nmap wrapper |
| CVE lookup | NVD API | Vulnerability database |
| AI suggestions | Groq API | Intelligent analysis |
| Reports | Jinja2 + WeasyPrint | HTML/PDF generation |
| Container | Docker | Portability |
| CI/CD | GitHub Actions | Automation pipeline |
| SAST | Bandit | Static code analysis |
| Dependency scan | Safety | Vulnerability check |
| Image scan | Trivy | Container security |
| Orchestration | Kubernetes | Deployment manifests |
| Monitoring | Prometheus + Grafana | Metrics and dashboards |

---

## 📦 Installation

### From source

```bash
git clone https://github.com/franjmenezz/ctfpilot.git
cd ctfpilot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install hatchling
python -m hatchling build -t wheel
pip install dist/*.whl
```

### With Docker

```bash
docker pull franjmenezz/ctfpilot:latest
docker run --rm --network host franjmenezz/ctfpilot:latest start --target 10.10.11.25 --name "MachineName"
```

> **Requirements:** Nmap must be installed on the system. On Kali Linux it comes pre-installed.

---

## 🚀 Usage

### Start a new session

```bash
# Auto-detects platform from IP (HTB, THM, CTF)
ctfpilot start --target 10.10.11.25 --name "MachineName"

# Or specify platform manually
ctfpilot start --target 10.10.11.25 --name "MachineName" --platform htb
```

### During the session

```bash
# Add notes
ctfpilot note "Found /admin directory exposed"
ctfpilot note "SSH on port 22, trying default credentials"

# Register captured flags
ctfpilot flag --type user --value "a3f5c8d1b2e4..."
ctfpilot flag --type root --value "9f2e1a4b7c8d..."

# Check session status
ctfpilot status

# Check elapsed time
ctfpilot timer

# Re-run reconnaissance manually
ctfpilot recon
ctfpilot recon --target 10.10.11.25
```

### Wordlist suggestions

```bash
ctfpilot wordlist http
ctfpilot wordlist smb
ctfpilot wordlist ssh
ctfpilot wordlist ftp
ctfpilot wordlist dns
ctfpilot wordlist user
ctfpilot wordlist pass
```

### Generate reports

```bash
# HTML report (saved to ~/Desktop/CTFPilot/)
ctfpilot report --format html

# PDF report
ctfpilot report --format pdf

# Markdown writeup template
ctfpilot report --format md
```

### Session management

```bash
# View all past sessions
ctfpilot history

# Close active session
ctfpilot finish
```

### AI setup

```bash
# Configure Groq API key (free at console.groq.com)
ctfpilot ai-setup
```

---

## 📋 Commands Reference

| Command | Options | Description |
|---|---|---|
| `start` | `--target`, `--name`, `--platform` | Start a new pentesting session |
| `note` | `[content]` | Add a note to the active session |
| `flag` | `--value`, `--type` | Register a captured flag |
| `status` | — | Show active session details |
| `timer` | — | Show elapsed time in active session |
| `recon` | `--target` (optional) | Re-run reconnaissance |
| `finish` | — | Close the active session |
| `history` | — | Show all past sessions |
| `wordlist` | `[service]` | Get wordlist suggestions by service |
| `report` | `--format` | Generate HTML, PDF or Markdown report |
| `ai-setup` | — | Configure Groq API key for AI suggestions |

---

## 🔒 DevSecOps Pipeline

Every push to main triggers the full CI/CD pipeline:

```
Push to main
    ↓
Tests & Code Quality (pytest)
    ↓
SAST - Static Analysis (Bandit)
    ↓
Dependency Vulnerability Check (Safety)
    ↓
Docker Build & Security Scan (Trivy)
    ↓
Kubernetes Manifest Validation (kubeconform)
```

---

## 🐳 Docker

```bash
# Build the image
docker build -t ctfpilot:latest .

# Run a command
docker run --rm ctfpilot:latest --help
```

---

## ☸️ Kubernetes

Manifests available in `k8s/`:

```bash
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/pvc.yml
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/network-policy.yml
```

---

## 📊 Monitoring

```bash
cd monitoring
docker compose -f docker-compose.monitoring.yml up -d
```

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/ctfpilot)

---

## 👤 Author

**Francisco Jiménez** — Pentester & Full Stack Developer oriented to DevSecOps

[![GitHub](https://img.shields.io/badge/GitHub-franjmenezz-black)](https://github.com/franjmenezz)

---

## 📄 License

MIT License — feel free to use and contribute.

---

*[Versión en Español](README.es.md)*
