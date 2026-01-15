# Development Recommendations

## ✅ What You Have Now (Session 2 Complete)

- **Startup/Shutdown**: `start.py`, `stop.py` - One-click VM startup
- **Testing**: `test_api.py` - Validates all API endpoints
- **Infrastructure**: Docker stack with auto-restart and monitoring
- **Monitoring**: Grafana dashboards with 8 panels
- **Documentation**: BUILD_LOG, NEXT_STEPS, SESSION_3_PLAN

---

## 🎯 High Priority (Build These Next)

### 1. Sample Data Loaders ⭐⭐⭐
**Why:** Students need realistic data to interact with
**Build Now:** Debug/seed data for demonstrations

**Create:**
```
scripts/
  └── seed_database.py       # Load sample students, devices, policies
  └── sample_data/
      ├── students.json      # 20-30 test students
      ├── devices.json       # 10-15 test devices
      └── policies.json      # 5-10 compliance policies
```

**Rationale:**
- Empty database = boring demos
- Consistent data across all VMs
- Students can experiment without breaking things
- Easier to demonstrate monitoring/metrics with real traffic

---

### 2. Health Check Script ⭐⭐⭐
**Why:** Quick validation that everything works after VM startup
**Build Now:** Catches issues before students notice them

**Create:**
```
scripts/
  └── health_check.py        # Comprehensive system validation
```

**Should Check:**
- All 6 containers running
- API responding (all endpoints)
- Database has seed data
- Redis queue working
- Grafana accessible
- Metrics flowing to Prometheus

**Output:** Pass/Fail report with remediation suggestions

---

### 3. Quick Demo Script ⭐⭐⭐
**Why:** Instructors need a 5-minute "it works" demo
**Build Now:** Confidence builder for classroom use

**Create:**
```
scripts/
  └── demo.py                # Automated demo sequence
```

**Should Do:**
1. Create 3 students via API
2. Show jobs in Redis
3. Show results in database
4. Generate traffic for Grafana
5. Open browser to dashboard (optional)

---

## 🔄 Medium Priority (Build After Testing)

### 4. Reset/Cleanup Script ⭐⭐
**Why:** Students will break things, need fresh start
**Build Later:** After you understand common failure modes

**Create:**
```
scripts/
  └── reset.py               # Nuclear option - fresh state
```

**Should Do:**
- Stop all containers
- Remove volumes (optional flag)
- Rebuild containers
- Re-seed database
- Verify health

---

### 5. Student Lab Data ⭐⭐
**Why:** Students need hands-on exercises
**Build Later:** After finalizing curriculum

**Create:**
```
labs/
  └── data/
      ├── lab1_students.csv  # Exercise 1 data
      ├── lab2_devices.csv   # Exercise 2 data
      └── lab3_batch.csv     # Exercise 3 data
```

---

### 6. Integration Tests ⭐⭐
**Why:** Catch regressions before deployment
**Build Later:** After core features stable

**Create:**
```
tests/
  └── integration/
      ├── test_student_workflow.py
      ├── test_redis_queue.py
      └── test_metrics_collection.py
```

**Use:** pytest framework (already have it)

---

## ⏳ Low Priority (Can Wait)

### 7. Unit Tests ⭐
**Why:** Good engineering practice
**Build Much Later:** After feature-complete

**Create:**
```
tests/
  └── unit/
      ├── test_api_routes.py
      ├── test_powershell_module.pester.ps1
      └── test_database_schema.py
```

---

### 8. Performance Testing ⭐
**Why:** Understand system limits
**Build Later:** If performance issues arise

**Create:**
```
tests/
  └── performance/
      ├── load_test.py       # Use locust or k6
      └── stress_test.py
```

---

### 9. Configuration Profiles ⭐
**Why:** Different deployment scenarios
**Build Much Later:** Only if needed

**Create:**
```
config/
  ├── development.env
  ├── classroom.env
  └── demo.env
```

---

## 🚫 Don't Build (Yet)

### ❌ Complex Authentication
- Classroom sandbox doesn't need OAuth/JWT
- VM network isolation is sufficient
- Adds complexity for minimal security gain

### ❌ Advanced Logging/Observability
- `docker logs` is sufficient for classroom
- Don't add ELK/Loki/Splunk
- Grafana handles metrics needs

### ❌ CI/CD Pipeline
- Manual deployment is fine for pilot
- GitHub Actions overkill for classroom use
- Add only if maintaining long-term

### ❌ Multi-tenancy
- Each VM = isolated environment
- Don't need tenant separation
- Keep architecture simple

---

## 📋 Recommended Build Order (Next 2 Sessions)

### Session 3 (Documentation & Validation):
1. ✅ `start.py` (done)
2. ✅ `stop.py` (done)
3. ✅ `test_api.py` (done)
4. 🔨 `scripts/seed_database.py` + sample data JSONs
5. 🔨 `scripts/health_check.py`
6. 🔨 `scripts/demo.py`
7. 📖 Update README with screenshots
8. 📖 Create DEPLOYMENT.md
9. 📖 Create TROUBLESHOOTING.md

### Session 4 (Refinement):
1. Test all scripts on fresh VM
2. Create `scripts/reset.py`
3. Document performance baseline
4. Create lab exercise data (if curriculum ready)
5. Polish documentation based on testing

---

## 💡 Key Principles

**Keep It Simple:**
- Classroom != Production
- Favor working over perfect
- Students need usability > features

**Make It Debuggable:**
- Clear error messages
- Health checks with specific failures
- Logs that make sense

**Make It Repeatable:**
- One-command startup
- Deterministic seed data
- Idempotent operations

**Make It Fast:**
- VMs auto-clear = fast startup matters
- Cache Docker images
- Pre-seed common data

---

## 🎓 Classroom-Specific Considerations

**Student Access Level:**
- Read-only Grafana? (no accidental deletes)
- API-only access? (no direct DB access)
- PowerShell module exposed? (depends on curriculum)

**Failure Recovery:**
- Students WILL break things
- Every lab should have "reset" instructions
- Make recovery faster than troubleshooting

**Time Constraints:**
- 50-minute class periods
- Allow 5-10 minutes for startup/issues
- 5 minutes for cleanup
- 30-35 minutes actual work time

---

## ✅ Summary: Build This Next

**Immediate (Session 3):**
1. `scripts/seed_database.py` with sample JSON data
2. `scripts/health_check.py` for validation
3. `scripts/demo.py` for quick demos
4. Documentation updates (README, DEPLOYMENT, TROUBLESHOOTING)

**Soon (Session 4):**
1. `scripts/reset.py` for student recovery
2. Integration test suite (optional)
3. Lab exercise data files

**Later (Post-Pilot):**
1. Unit tests
2. Performance baseline documentation
3. Student assessment rubrics

**Never (For Classroom):**
- Complex auth systems
- Advanced observability stacks
- Multi-tenancy
- CI/CD pipelines (unless scaling)

---

**Focus: Get 20 working VMs for students ASAP, polish later**
