# Session 3: Classroom Deployment Preparation

## Current Status (Post-Session 2)
✅ Production-grade stability (restart policies, connection pooling)
✅ Comprehensive monitoring (Prometheus + Grafana with 8 panels)
✅ Environment variable management (.env template)
✅ All containers healthy and metrics flowing
✅ GitHub repo ready for cloning

## Session 3 Goals

Focus on making the system classroom-ready for Cloudshare VMs.

### 1. Documentation Enhancement 📚
**Priority: HIGH**

#### README Updates:
- Add architecture diagram (mermaid or ASCII)
- Add screenshots of Grafana dashboard
- Update quick start for VM deployment
- Add troubleshooting section

#### Deployment Guide:
- Create DEPLOYMENT.md with VM setup steps
- Document port requirements (5000, 3000, 9090, 5432, 6379)
- Docker pre-cache instructions
- Student access instructions

**Files:**
- `README.md` - enhance with visuals
- `DEPLOYMENT.md` - new VM deployment guide
- `TROUBLESHOOTING.md` - common issues + fixes

---

### 2. Testing & Validation 🧪
**Priority: MEDIUM**

#### End-to-End Testing:
- Test full student creation workflow (API → Redis → PowerShell)
- Verify job status tracking works
- Load test with 10-20 concurrent requests
- Verify metrics appear correctly in Grafana

#### Container Restart Testing:
- Kill containers and verify auto-restart
- Test DB connection pool under restart scenarios
- Verify Redis persistence (AOF)

**Validation Checklist:**
- [ ] POST student → job queued
- [ ] Worker processes job from Redis
- [ ] Job status updates correctly
- [ ] Metrics show in Grafana within 15s
- [ ] Container restart recovery < 30s

---

### 3. Performance Baseline 📊
**Priority: MEDIUM**

Establish baseline metrics for classroom use:
- API response time under normal load
- Connection pool utilization
- Memory usage per container
- Startup time from `docker-compose up`

**Create:** `PERFORMANCE_BASELINE.md`

---

### 4. Student Lab Materials 🎓
**Priority: LOW (Optional)**

If time permits, create basic lab exercises:
- Lab 1: Use API to create student accounts
- Lab 2: Query Grafana for API metrics
- Lab 3: Inspect Redis job queue
- Lab 4: Modify PowerShell automation module

**Files:**
- `labs/lab1-api-basics.md`
- `labs/lab2-monitoring.md`

---

## Session 3 Task Order

**Estimated Time: 60-90 minutes**

1. Test end-to-end student creation workflow (15 min)
2. Take Grafana dashboard screenshots (5 min)
3. Update README with screenshots and architecture (20 min)
4. Create DEPLOYMENT.md for VM setup (15 min)
5. Create TROUBLESHOOTING.md with common issues (10 min)
6. Run load test and document performance baseline (15 min)
7. Optional: Create lab1-api-basics.md (15 min)
8. Commit and push all documentation (5 min)

---

## Deferred to Future Sessions

### Not Critical for Initial Classroom Use:
- API authentication/authorization
- HTTPS/TLS setup
- Advanced logging aggregation
- RAG system integration
- Pester test suite for PowerShell
- CI/CD pipeline
- Container image optimization

### When Needed:
- Training module content (post-pilot)
- Video tutorials (post-pilot)
- Assessment rubrics (post-pilot)

---

## Success Criteria for Session 3

**Documentation:**
- ✅ README has screenshots and clear quick start
- ✅ DEPLOYMENT.md exists with VM instructions
- ✅ TROUBLESHOOTING.md covers common issues

**Testing:**
- ✅ End-to-end student creation verified
- ✅ Grafana shows all 8 panels with data
- ✅ Load test completed with no errors

**Deliverable:**
- System ready for instructor to image Cloudshare VMs
- Student-facing documentation complete
- Performance expectations documented

---

**Ready to make this classroom-ready!**
