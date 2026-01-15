# Grafana Monitoring Setup

## Access Grafana

**URL:** http://localhost:3000

**Login:**
- Username: `admin`
- Password: `admin`

(Change password on first login)

## What's Monitoring

- **Prometheus:** http://localhost:9090
- **Targets:** PostgreSQL, Redis, API Gateway

## Quick Test

1. Open http://localhost:3000
2. Login with admin/admin
3. Go to Explore
4. Select Prometheus datasource
5. Run query: `up` (shows all targets)

## System Overview

Grafana pulls metrics from:
- Container stats (CPU, RAM)
- Application metrics
- Database connections
- Job queue length

## Dashboards

Grafana auto-provisions:
- System Health
- API Performance
- Job Queue Status

## Stop Monitoring

```powershell
cd docker/monitoring
docker-compose -f docker-compose.monitoring.yml down
```

## Resume Monitoring

```powershell
cd docker/monitoring
docker-compose -f docker-compose.monitoring.yml up -d
```
