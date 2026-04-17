# tado-data

A read-only Python CLI tool for reporting on Tado smart heating system status.

## Features

- Battery status report for all devices
- Home info and device counts
- OAuth2 authentication with automatic token refresh

## Usage

```bash
uv run python tado.py auth        # Authenticate (opens browser)
uv run python tado.py battery     # Battery status report
uv run python tado.py status      # Home info and device counts
```

## Authentication

Uses OAuth2 Device Code Grant flow. Run `auth` to open a browser login page — tokens are saved locally to `tokens.json` and refreshed automatically.

## Dependencies

- Python 3.12+
- `click` — CLI framework
- `requests` — HTTP client

Install dependencies with `uv sync`.
