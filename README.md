# Cisco CLI Command Center

A web-based learning and productivity tool for Cisco IOS-style CLI commands. It provides a searchable command library, common routing command generation, and a small rule-based CLI troubleshooting helper.

> Important: Cisco command availability and syntax can vary by hardware, software family, and IOS/IOS XE release. Verify commands against the documentation and platform you are using.

## Features

- Search Cisco-style commands by keyword and category.
- Command detail pages with mode, syntax, example and platform notes.
- Static route, default route, OSPF and RIPv2 command generator.
- Offline rule-based troubleshooting for pasted CLI output.
- FastAPI backend and SQLite database.
- Vanilla HTML/CSS/JavaScript dashboard.
- Pytest test suite.

## Structure

```text
cisco-cli-command-center/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routers/
│   └── services/
├── data/
├── dashboard/
├── tests/
├── requirements.txt
├── run_project.bat
└── README.md
```

## Windows setup

From the project root in VS Code Terminal:

```cmd
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

Start everything with:

```cmd
run_project.bat
```

Or manually:

```cmd
uvicorn backend.main:app --reload
```

In another terminal:

```cmd
cd dashboard
python -m http.server 8080
```

Open:

- Dashboard: http://127.0.0.1:8080
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Tests

```cmd
python -m pytest -q
```

## Data

The included `data/commands.json` is a starter dataset of common Cisco IOS/IOS XE-style commands for learning and demonstrations. Expand it carefully and verify each entry against Cisco documentation for the target platform/release.

## Safety

This project is an educational command reference and troubleshooting assistant. It does not automate unauthorized device access or offensive network activity.
