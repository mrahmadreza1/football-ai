# ⚽ Football AI — Persian Football News Pipeline

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Status](https://img.shields.io/badge/status-active-brightgreen)

An automated pipeline that fetches football news, translates it into natural
Persian with an LLM, scores it with an "AI editor", and publishes only
high-value stories to a Telegram channel.

## Features
- RSS ingestion (BBC Sport Football) with image extraction
- LLM translation to fluent, conversational Persian (faithful, no added facts)
- AI scoring: importance (0–100) and virality (0–100)
- Configurable publish rule (default: importance ≥ 70 and virality ≥ 60)
- Idempotent storage: no duplicates, no double publishing
- Media-aware Telegram posts (photo / video / text)

## Tech Stack
Python · PostgreSQL 16 · Groq API (`openai/gpt-oss-20b`) · feedparser ·
psycopg2 · Telegram Bot API · Docker Compose

## Architecture
```mermaid
flowchart LR
  A[BBC RSS] --> B[Fetch]
  B --> C[Translate - Groq LLM]
  C --> D[(PostgreSQL)]
  D --> E[AI Editor - Scoring]
  E --> D
  D --> F[Publisher]
  F --> G[Telegram Channel]
```

## Getting Started
```bash
git clone https://github.com/mrahmadreza1/<repo-name>.git
cd <repo-name>
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
docker compose up -d
cp .env.example .env   # fill in values
python run.py
```

`.env`:
```
DATABASE_URL=postgresql://football_user:football_pass@localhost:5432/football_db
GROQ_API_KEY=...
BOT_TOKEN=...
CHANNEL_ID=...
```

## Usage
- Full pipeline: `python run.py`
- Individual stages: `python -m app.collectors.news`,
  `python -m app.process_news`, `python -m app.publisher`
- Inspect DB: `python check_news.py`

## API Documentation
This project has no HTTP API; it is a CLI/batch pipeline.

## Project Structure
```
app/
  config.py  database.py  ai_editor.py  translator.py
  process_news.py  publisher.py  collectors/news.py
run.py
docker-compose.yml
```

## Design Decisions
- PostgreSQL as shared state between stages, so each stage can run independently
- `UNIQUE(url)` + `ON CONFLICT DO NOTHING` for idempotent runs
- Deterministic publish rule applied in code on top of LLM scores
- Low temperature (0.2) for stable translation and scoring

## Roadmap
- [ ] Score first, translate only selected stories
- [ ] JSON-mode / Pydantic validation of LLM output
- [ ] Escape HTML, enforce caption limits, retries with backoff
- [ ] Scheduler (cron / GitHub Actions), structured logging
- [ ] Multiple sources, pytest suite with mocked LLM

## Contributing
Issues and PRs are welcome.

## License
MIT

## Contact
Ahmadreza Menati — ahmadrezamenati@gmail.com — github.com/mrahmadreza1
