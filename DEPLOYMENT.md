# CoreSkills4ai Deployment Guide

> **Target:** Cloudshare VM classroom deployment
> **Audience:** Instructors and IT administrators
> **Last Updated:** January 15, 2026

---

## Quick Start (TL;DR)

```bash
# 1. Clone the repository
git clone https://github.com/FlyguyTestRun/Class-Room-Modules.git
cd Class-Room-Modules

# 2. Copy environment template
cp .env.template .env

# 3. Start all services
docker-compose up -d
cd docker/monitoring && docker-compose -f docker-compose.monitoring.yml --env-file ../../.env up -d

# 4. Verify
curl http://localhost:5000/health
```

**Access Points:**
- API: http://localhost:5000
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

---

## Prerequisites

### Required Software
| Software | Version | Purpose |
|----------|---------|---------|
| Docker Desktop | 4.0+ | Container runtime |
| Git | 2.30+ | Repository cloning |
| curl or Postman | Any | API testing |

### System Requirements
| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 4 GB | 8 GB |
| CPU | 2 cores | 4 cores |
| Disk | 5 GB | 10 GB |
| OS | Windows 10/11, Ubuntu 20.04+ | Windows 11 |

### Network Ports
Ensure these ports are available:
| Port | Service | Protocol |
|------|---------|----------|
| 5000 | Flask API | HTTP |
| 5432 | PostgreSQL | TCP |
| 6379 | Redis | TCP |
| 3000 | Grafana | HTTP |
| 9090 | Prometheus | HTTP |

---

## Step-by-Step Deployment

### Step 1: Prepare the VM

**For Cloudshare Windows VM:**
1. Start the VM and connect via RDP
2. Open PowerShell as Administrator
3. Verify Docker is running:
   ```powershell
   docker --version
   docker-compose --version
   ```

**If Docker is not installed:**
```powershell
# Download Docker Desktop installer
# Or use winget:
winget install Docker.DockerDesktop
# Restart and enable WSL2 when prompted
```

### Step 2: Clone the Repository

```bash
# Navigate to desired location
cd C:\Projects  # or your preferred directory

# Clone the repo
git clone https://github.com/FlyguyTestRun/Class-Room-Modules.git

# Enter the directory
cd Class-Room-Modules
```

### Step 3: Configure Environment

```bash
# Copy the template
cp .env.template .env

# (Optional) Edit passwords - defaults work for classroom use
notepad .env
```

**Default .env values:**
```ini
POSTGRES_DB=eduops
POSTGRES_USER=eduops_user
POSTGRES_PASSWORD=changeme123
REDIS_HOST=redis
GF_SECURITY_ADMIN_PASSWORD=admin
API_PORT=5000
```

### Step 4: Start Core Services

```bash
# Start main application stack
docker-compose up -d

# Verify containers are running
docker ps
```

**Expected output:**
```
NAMES               STATUS
eduops-api          Up (healthy)
eduops-postgres     Up (healthy)
eduops-redis        Up (healthy)
eduops-automation   Up
```

### Step 5: Start Monitoring Stack

```bash
# Navigate to monitoring directory
cd docker/monitoring

# Start Grafana and Prometheus
docker-compose -f docker-compose.monitoring.yml --env-file ../../.env up -d

# Return to root
cd ../..
```

### Step 6: Verify Deployment

**Test API:**
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}
```

**Test Grafana:**
1. Open browser: http://localhost:3000
2. Login: admin / admin
3. Navigate to Dashboards → CoreSkills4ai Command Center
4. Verify panels show data

---

## Cloudshare-Specific Instructions

### VM Template Setup (For Instructors)

If creating a master VM image for students:

1. **Pre-pull Docker images** (saves ~5 min per student):
   ```bash
   docker-compose pull
   cd docker/monitoring && docker-compose -f docker-compose.monitoring.yml pull
   ```

2. **Pre-clone repository:**
   ```bash
   cd C:\Projects
   git clone https://github.com/FlyguyTestRun/Class-Room-Modules.git
   ```

3. **Create .env file** with default values

4. **Snapshot/Image the VM** before class

### Student Quick Start

If VM is pre-configured:
```bash
cd C:\Projects\Class-Room-Modules
docker-compose up -d
cd docker/monitoring && docker-compose -f docker-compose.monitoring.yml --env-file ../../.env up -d
```

**Time to operational:** ~30 seconds (with pre-pulled images)

---

## Service Management

### Start All Services
```bash
# From project root
docker-compose up -d
cd docker/monitoring && docker-compose -f docker-compose.monitoring.yml --env-file ../../.env up -d
```

### Stop All Services
```bash
cd docker/monitoring && docker-compose -f docker-compose.monitoring.yml down
cd ../..
docker-compose down
```

### View Logs
```bash
# All containers
docker-compose logs

# Specific container
docker logs eduops-api
docker logs eduops-grafana
```

### Restart a Service
```bash
docker restart eduops-api
docker restart eduops-grafana
```

### Full Reset (Clears Data)
```bash
# Stop and remove volumes
docker-compose down -v
cd docker/monitoring && docker-compose -f docker-compose.monitoring.yml down -v
```

---

## Validation Checklist

Run through this checklist after deployment:

| Check | Command/Action | Expected Result |
|-------|----------------|-----------------|
| Containers running | `docker ps` | 6 containers UP |
| API health | `curl localhost:5000/health` | `{"status":"healthy"}` |
| Database connected | Check API health response | `"database":"connected"` |
| Redis connected | Check API health response | `"redis":"connected"` |
| Grafana accessible | Browser: localhost:3000 | Login page loads |
| Grafana dashboard | Navigate to CoreSkills4ai | Panels show data |
| Prometheus targets | Browser: localhost:9090/targets | api-gateway: UP |

---

## Common Deployment Issues

### Issue: "Port already in use"
```bash
# Find what's using the port
netstat -ano | findstr :5000

# Kill the process or change API_PORT in .env
```

### Issue: "Cannot connect to Docker daemon"
```bash
# Ensure Docker Desktop is running
# On Windows: Start Docker Desktop application
# Then retry
```

### Issue: "Image pull failed"
```bash
# Check internet connectivity
ping github.com

# Try pulling manually
docker pull postgres:15-alpine
docker pull redis:7-alpine
```

### Issue: "Grafana shows 'No data'"
1. Verify Prometheus is running: `docker ps | grep prometheus`
2. Check Prometheus targets: http://localhost:9090/targets
3. Ensure API is healthy: `curl localhost:5000/health`
4. Wait 30 seconds and refresh Grafana

---

## Architecture Reference

```
┌─────────────────────────────────────────────────────────────┐
│                   CoreSkills4ai Platform                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Student Browser]                                          │
│        │                                                    │
│        ▼                                                    │
│  [Flask API :5000] ──────► [Grafana :3000]                  │
│        │                         ▲                          │
│        │                         │                          │
│        ▼                   [Prometheus :9090]               │
│  [Redis :6379] ◄──► [PowerShell Worker]                    │
│        │                         │                          │
│        ▼                         ▼                          │
│  [PostgreSQL :5432] ◄────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Support

**Documentation:**
- README.md - Project overview
- NEXT_STEPS.md - Current development status
- TROUBLESHOOTING.md - Detailed issue resolution

**Repository:**
- https://github.com/FlyguyTestRun/Class-Room-Modules

---

**Deployment Guide Version:** 1.0
**Last Tested:** January 15, 2026
