# Next Development Steps

## Current Status
✅ Docker stack running (6 containers)
✅ Flask API with endpoints
✅ PowerShell automation module
✅ Redis job queue
✅ Grafana monitoring (basic health only)
✅ PostgreSQL database
✅ GitHub repo synced

## Immediate Priorities (Session 2)

### 1. Stability Improvements ⚡ HIGH PRIORITY
**Time:** ~45 minutes

#### A. Add Docker Health Checks
- API Gateway: Check `/health` + DB connection
- Automation Engine: Check PowerShell process
- Add to docker-compose.yml

#### B. Add Auto-Restart Policies
- `restart: unless-stopped` for all services
- Prevents container failures during class

#### C. Connection Pooling
- Add SQLAlchemy connection pool to API
- Config: min=5, max=20 connections
- Reuse DB connections instead of creating new ones

**File Changes:**
- `docker-compose.yml` - health checks + restart policies
- `docker/api-gateway/app.py` - connection pooling

---

### 2. Prometheus Metrics Export 📊
**Time:** ~30 minutes

Add `prometheus-flask-exporter` to API:
- Track: request count, response time, error rate
- Endpoint: `/metrics` for Prometheus scraping
- Enable detailed graphs in Grafana

**What This Adds:**
- API request rate (req/sec) graph
- Response time (ms) graph
- Error rate % graph
- HTTP status code breakdown

**File Changes:**
- `docker/api-gateway/requirements.txt` - add prometheus-flask-exporter
- `docker/api-gateway/app.py` - integrate metrics
- `docker/monitoring/prometheus.yml` - add scrape config
- `docker/monitoring/provisioning/dashboards/coreskills-dashboard.json` - add metric panels

---

### 3. Environment Variables & Docker Secrets 🔒
**Time:** ~20 minutes

Move hardcoded passwords to secure storage:
- Create `.env.template` (committed)
- Create `.env` (gitignored) with actual passwords
- Update docker-compose to use env vars
- Add to `.gitignore`

**File Changes:**
- `.env.template` - example values
- `.env` - actual passwords (NOT committed)
- `docker-compose.yml` - use `${POSTGRES_PASSWORD}` syntax
- `.gitignore` - add `.env`

---

## Session 2 Task Order

**Start here:**
1. ✅ Add health checks to docker-compose (2 min)
2. ✅ Add restart policies to docker-compose (1 min)
3. ✅ Add connection pooling to API (15 min)
4. ✅ Test stability improvements (5 min)
5. ✅ Add Prometheus metrics to API (20 min)
6. ✅ Update Grafana dashboard with metric panels (10 min)
7. ✅ Create .env template and migrate passwords (15 min)
8. ✅ Test full system (10 min)
9. ✅ Commit to GitHub
10. ✅ Take screenshots for README

**Total Time:** ~90 minutes

---

## Why These Changes Matter

**Stability:**
- Health checks = Docker knows if container is actually working
- Auto-restart = No manual intervention during class
- Connection pooling = Faster API, no "too many connections" errors

**Monitoring:**
- See actual request volume during class
- Detect performance issues (slow endpoints)
- Track error rates in real-time

**Security (minimal for classroom):**
- Passwords not in git history
- Can share repo without exposing credentials
- Still using Docker network isolation

---

## Notes for Classroom Use

**Deployment Strategy:**
- VMs auto-clear after use ✅
- GitHub repo clones to fresh VM ✅
- Docker images cached = fast startup ✅
- No persistent state needed ✅

**This means:**
- No need for complex secrets management
- Basic .env file is sufficient
- Focus on stability over security
- Image VMs with Docker pre-installed

---

## Deferred Items (Post-Session 2)

### Nice to Have (Not Critical)
- API authentication (not needed for sandbox)
- HTTPS/SSL (internal network only)
- Rate limiting (classroom traffic is low)
- Logging aggregation (can use `docker logs`)
- Backup strategy (ephemeral data is fine)

### Future Enhancements
- Cloudshare VM deployment guide
- Training module content
- RAG system with local embeddings
- Pester tests for PowerShell
- Student lab exercises

---

## Files to Update Next Session

**Priority 1:**
- `docker-compose.yml` - health checks, restart, env vars
- `docker/api-gateway/app.py` - connection pooling, metrics
- `docker/api-gateway/requirements.txt` - add prometheus library

**Priority 2:**
- `.env.template` - create
- `.env` - create (local only)
- `.gitignore` - add .env
- `docker/monitoring/prometheus.yml` - scrape API metrics
- `docker/monitoring/provisioning/dashboards/coreskills-dashboard.json` - add panels

**Documentation:**
- `README.md` - add screenshots
- `BUILD_LOG.md` - update progress
- Commit message with all changes

---

**Ready to start Session 2 with these priorities!**
