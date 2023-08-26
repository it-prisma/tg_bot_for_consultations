# Telegram Bot for Anonymous Consultations

## Description

<a href="https://github.com/Ileriayo/markdown-badges">
  <p align="center">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
    <img alt="Postgres" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
    <img alt="Redis" src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white"/>
    <img alt="GitHub" src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/>
    <img alt="GitHub Actions" src="https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white"/>
    <img alt="Grafana" src="https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white"/>
    <img alt="Prometheus" src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white"/>
  </p>
</a>

## Installation

For running and building app you need to get source code of this repo:

```bash
git clone https://github.com/it-prisma/tg_bot_for_consultations
```

## Settings

For configuring project you need to create file with envrionment variables from `.env.dev`.

If you want to use database other database (not from `docker-compose.yaml`) remember to set `POSTGRES_HOST` and `POSTGRES_PORT`.

```bash
cp .env.dev .env
```

```bash
POSTGRES_USER     # user for connection to DB
POSTGRES_PASSWORD # password for connection to DB
POSTGRES_HOST     # domen or IP-address to DB
POSTGRES_DB       # database name for project
POSTGRES_PORT     # port DB

REDIS_HOST        # domen or IP-address to cache
REDIS_PORT        # port to cache
REDIS_PASSWORD    # password to cache
```

## Running

### Docker

### Database Migrations

## Using

