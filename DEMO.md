# CoreSkills4ai Demo Script

## Prerequisites
```powershell
docker-compose up -d
docker-compose ps  # Verify all containers running
```

## Demo Flow (5 minutes)

### 1. System Health Check (30 seconds)
```bash
curl http://localhost:5000/health
```
**Expected:** `{"status":"healthy","service":"api-gateway"}`

### 2. Single Student Creation (1 minute)
```powershell
docker exec eduops-automation pwsh -Command "
  Import-Module /automation/modules/KISDIdentity.psm1 -Force
  New-KISDStudentAccount -StudentID 'S2024100' -FirstName 'Alice' -LastName 'Martinez' -GradeLevel 11 -GraduationYear 2026
"
```
**Shows:**
- ✓ Username generation: amartinez4100
- ✓ Email: amartinez4100@students.keller.edu
- ✓ OU placement: OU=Grade11,OU=Students

### 3. Batch Processing (2 minutes)
```powershell
# Show CSV
cat automation/powershell/test_data/students.csv

# Process batch
docker exec eduops-automation pwsh /automation/scripts/New-StudentBatch.ps1 -CsvPath /automation/test_data/students.csv
```
**Shows:**
- Processes 5 students from CSV
- Success count
- Account details

### 4. API Integration (1 minute)
```bash
# Queue job via API
curl -X POST http://localhost:5000/api/v1/users/student \
  -H "Content-Type: application/json" \
  -d '{"student_id":"S999","first_name":"Demo","last_name":"User","grade_level":9,"graduation_year":2028}'

# Get job status
curl http://localhost:5000/api/v1/jobs/<job_id>
```

### 5. Database Verification (30 seconds)
```bash
docker exec eduops-postgres psql -U eduops_user -d eduops -c "SELECT COUNT(*) FROM users;"
```

## Talking Points

**Enterprise Scale:**
- "This system handles 2,000+ users and 8,000+ devices across 34 campuses"
- "Reduces provisioning from 45 minutes to 8 minutes"

**Production Quality:**
- "Multi-stage Docker builds for security"
- "Health checks and service dependencies"
- "Error handling with audit logging"

**Skills Demonstrated:**
- PowerShell module development
- Docker containerization
- REST API design
- Database schema design
- System integration

## Troubleshooting

**Container not running:**
```powershell
docker-compose logs <service-name>
docker-compose restart <service-name>
```

**Module not loading:**
```powershell
docker exec eduops-automation pwsh -Command "Get-Module -ListAvailable"
```
