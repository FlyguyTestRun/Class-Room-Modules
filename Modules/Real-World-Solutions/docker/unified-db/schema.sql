-- =============================================================================
-- ZZZ Unified Database - Clean Merged Schema
-- =============================================================================
-- This is the TARGET database for the ETL process. All data from ZZZ, AAA,
-- and BBB will be cleaned, normalized, and loaded here.
--
-- Design principles:
-- - Consistent naming conventions (snake_case)
-- - Proper data types (no money as floats!)
-- - Referential integrity with foreign keys
-- - Audit trail for compliance
-- - Source tracking for data lineage
-- =============================================================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text matching

-- =============================================================================
-- LOOKUP TABLES
-- =============================================================================

-- Source systems for data lineage
CREATE TABLE source_systems (
    source_id SERIAL PRIMARY KEY,
    source_code VARCHAR(10) UNIQUE NOT NULL,  -- ZZZ, AAA, BBB
    source_name VARCHAR(100) NOT NULL,
    description TEXT,
    connection_info JSONB,
    last_sync TIMESTAMP
);

INSERT INTO source_systems (source_code, source_name, description) VALUES
('ZZZ', 'ZZZ Accounting', 'Primary accounting system - clean data'),
('AAA', 'AAA Accounting', 'Acquired company - legacy system'),
('BBB', 'BBB Construction', 'Partner company - construction focus');

-- Industry classifications
CREATE TABLE industries (
    industry_id SERIAL PRIMARY KEY,
    industry_code VARCHAR(20) UNIQUE NOT NULL,
    industry_name VARCHAR(100) NOT NULL,
    parent_industry_id INTEGER REFERENCES industries(industry_id)
);

INSERT INTO industries (industry_code, industry_name) VALUES
('TECH', 'Technology'),
('MANU', 'Manufacturing'),
('CONS', 'Construction'),
('HLTH', 'Healthcare'),
('FINA', 'Financial Services'),
('RETA', 'Retail'),
('SERV', 'Professional Services'),
('REAL', 'Real Estate'),
('EDUC', 'Education'),
('FOOD', 'Food & Beverage'),
('AUTO', 'Automotive'),
('AGRI', 'Agriculture'),
('ARTS', 'Arts & Entertainment'),
('LEGA', 'Legal');

-- Service types
CREATE TABLE service_types (
    service_type_id SERIAL PRIMARY KEY,
    service_code VARCHAR(20) UNIQUE NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    default_rate DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT true
);

INSERT INTO service_types (service_code, service_name, description, default_rate) VALUES
('TAX-IND', 'Individual Tax Preparation', 'Personal tax return preparation', 175.00),
('TAX-BUS', 'Business Tax Preparation', 'Corporate/business tax returns', 275.00),
('BOOK', 'Bookkeeping', 'Monthly bookkeeping services', 90.00),
('PAYROLL', 'Payroll Services', 'Payroll processing and tax deposits', 80.00),
('AUDIT', 'Financial Audit', 'Annual audit services', 325.00),
('CONSULT', 'Business Consulting', 'Advisory and consulting', 275.00),
('CFO', 'Fractional CFO', 'Part-time CFO services', 375.00),
('PROJMGMT', 'Project Accounting', 'Construction/project accounting', 150.00);

-- =============================================================================
-- CORE ENTITIES
-- =============================================================================

-- Organizations (unified clients/contractors/customers)
CREATE TABLE organizations (
    org_id SERIAL PRIMARY KEY,
    org_uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    legal_name VARCHAR(200) NOT NULL,
    dba_name VARCHAR(200),
    tax_id VARCHAR(20),  -- Cleaned, consistent format
    org_type VARCHAR(20) NOT NULL,  -- CLIENT, CONTRACTOR, VENDOR, PARTNER
    entity_type VARCHAR(20),  -- LLC, CORP, SOLE_PROP, PARTNERSHIP, INDIVIDUAL
    industry_id INTEGER REFERENCES industries(industry_id),
    annual_revenue DECIMAL(15, 2),
    employee_count INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    merged_from JSONB  -- Track which source records were merged
);

-- Organization source mappings (for data lineage)
CREATE TABLE org_source_mappings (
    mapping_id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(org_id),
    source_id INTEGER REFERENCES source_systems(source_id),
    source_record_id TEXT NOT NULL,  -- Original ID from source system
    source_record_data JSONB,  -- Original data snapshot
    mapped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mapped_by VARCHAR(100),
    confidence_score FLOAT,  -- How confident is the match?
    UNIQUE(source_id, source_record_id)
);

-- Addresses (normalized)
CREATE TABLE addresses (
    address_id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(org_id),
    address_type VARCHAR(20),  -- BILLING, MAILING, SITE, PRIMARY
    street_line1 VARCHAR(200),
    street_line2 VARCHAR(200),
    city VARCHAR(100),
    state CHAR(2),
    zip_code VARCHAR(10),
    country VARCHAR(50) DEFAULT 'USA',
    is_primary BOOLEAN DEFAULT false,
    validated BOOLEAN DEFAULT false,
    validation_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contacts (people associated with organizations)
CREATE TABLE contacts (
    contact_id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(org_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    title VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),  -- Normalized format: +1-555-123-4567
    phone_type VARCHAR(20),  -- OFFICE, MOBILE, FAX
    is_primary BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees (internal staff)
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    job_title VARCHAR(100),
    department VARCHAR(50),
    hire_date DATE,
    termination_date DATE,
    manager_id INTEGER REFERENCES employees(employee_id),
    is_active BOOLEAN DEFAULT true,
    source_system VARCHAR(10),  -- Which system they came from
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- SERVICE & ENGAGEMENT TRACKING
-- =============================================================================

-- Engagements (service contracts)
CREATE TABLE engagements (
    engagement_id SERIAL PRIMARY KEY,
    engagement_uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    org_id INTEGER REFERENCES organizations(org_id),
    service_type_id INTEGER REFERENCES service_types(service_type_id),
    assigned_employee_id INTEGER REFERENCES employees(employee_id),
    start_date DATE NOT NULL,
    end_date DATE,
    contract_value DECIMAL(15, 2),
    billing_frequency VARCHAR(20),  -- MONTHLY, QUARTERLY, ANNUALLY, ONE_TIME
    status VARCHAR(20) DEFAULT 'ACTIVE',  -- ACTIVE, COMPLETED, SUSPENDED, CANCELLED
    notes TEXT,
    source_system VARCHAR(10),
    source_engagement_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- FINANCIAL TRACKING
-- =============================================================================

-- Invoices (unified billing)
CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    invoice_uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    org_id INTEGER REFERENCES organizations(org_id),
    engagement_id INTEGER REFERENCES engagements(engagement_id),
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    subtotal DECIMAL(15, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(15, 2) NOT NULL,
    amount_paid DECIMAL(15, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'PENDING',  -- PENDING, PARTIAL, PAID, OVERDUE, VOID
    payment_date DATE,
    payment_method VARCHAR(50),
    source_system VARCHAR(10),
    source_invoice_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Invoice line items
CREATE TABLE invoice_lines (
    line_id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(invoice_id),
    description TEXT NOT NULL,
    quantity DECIMAL(10, 2) DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    total DECIMAL(15, 2) NOT NULL,
    service_type_id INTEGER REFERENCES service_types(service_type_id)
);

-- Payments received
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    payment_uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    invoice_id INTEGER REFERENCES invoices(invoice_id),
    payment_date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    payment_method VARCHAR(50),  -- CHECK, ACH, WIRE, CREDIT_CARD
    reference_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- CONSTRUCTION-SPECIFIC (from BBB)
-- =============================================================================

-- Projects (construction projects)
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    project_code VARCHAR(50) UNIQUE,
    project_name VARCHAR(200) NOT NULL,
    client_org_id INTEGER REFERENCES organizations(org_id),
    project_type VARCHAR(50),
    contract_value DECIMAL(15, 2),
    start_date DATE,
    estimated_completion DATE,
    actual_completion DATE,
    status VARCHAR(30),
    project_manager_id INTEGER REFERENCES employees(employee_id),
    site_address_id INTEGER REFERENCES addresses(address_id),
    source_system VARCHAR(10),
    source_project_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project contractors
CREATE TABLE project_contractors (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(project_id),
    contractor_org_id INTEGER REFERENCES organizations(org_id),
    role VARCHAR(100),
    contract_amount DECIMAL(15, 2),
    contract_date DATE,
    status VARCHAR(20)
);

-- Certificates/Insurance tracking
CREATE TABLE certifications (
    cert_id SERIAL PRIMARY KEY,
    org_id INTEGER REFERENCES organizations(org_id),
    cert_type VARCHAR(50),  -- INSURANCE, LICENSE, BOND, SAFETY
    cert_name VARCHAR(200),
    issuing_authority VARCHAR(200),
    cert_number VARCHAR(100),
    issue_date DATE,
    expiry_date DATE,
    coverage_amount DECIMAL(15, 2),
    document_url TEXT,
    verified BOOLEAN DEFAULT false,
    verified_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- AUDIT & COMPLIANCE
-- =============================================================================

-- Data quality log (track issues found during ETL)
CREATE TABLE data_quality_log (
    log_id SERIAL PRIMARY KEY,
    source_system VARCHAR(10),
    source_table VARCHAR(100),
    source_record_id TEXT,
    issue_type VARCHAR(50),  -- DUPLICATE, MISSING, INVALID_FORMAT, ENCODING, etc.
    issue_description TEXT,
    resolution VARCHAR(50),  -- MERGED, CLEANED, IGNORED, MANUAL_REVIEW
    resolved_at TIMESTAMP,
    resolved_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit trail
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    record_id INTEGER,
    action VARCHAR(20),  -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(10),
    batch_id UUID  -- Group related changes
);

-- ETL batch tracking
CREATE TABLE etl_batches (
    batch_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_system VARCHAR(10),
    batch_type VARCHAR(50),  -- FULL, INCREMENTAL, CORRECTION
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    records_processed INTEGER,
    records_inserted INTEGER,
    records_updated INTEGER,
    records_failed INTEGER,
    status VARCHAR(20),  -- RUNNING, COMPLETED, FAILED
    error_message TEXT
);

-- =============================================================================
-- INDEXES
-- =============================================================================

-- Organizations
CREATE INDEX idx_org_tax_id ON organizations(tax_id);
CREATE INDEX idx_org_legal_name ON organizations USING gin(legal_name gin_trgm_ops);
CREATE INDEX idx_org_type ON organizations(org_type);
CREATE INDEX idx_org_active ON organizations(is_active);

-- Contacts
CREATE INDEX idx_contacts_org ON contacts(org_id);
CREATE INDEX idx_contacts_email ON contacts(email);

-- Invoices
CREATE INDEX idx_invoices_org ON invoices(org_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_due ON invoices(due_date);

-- Projects
CREATE INDEX idx_projects_client ON projects(client_org_id);
CREATE INDEX idx_projects_status ON projects(status);

-- Data quality
CREATE INDEX idx_dq_source ON data_quality_log(source_system);
CREATE INDEX idx_dq_type ON data_quality_log(issue_type);

-- Certifications
CREATE INDEX idx_cert_org ON certifications(org_id);
CREATE INDEX idx_cert_expiry ON certifications(expiry_date);

-- =============================================================================
-- VIEWS
-- =============================================================================

-- Active clients with primary contact
CREATE VIEW v_active_clients AS
SELECT
    o.org_id,
    o.legal_name,
    o.dba_name,
    o.tax_id,
    i.industry_name,
    c.first_name || ' ' || c.last_name AS primary_contact,
    c.email AS contact_email,
    c.phone AS contact_phone,
    o.annual_revenue,
    o.employee_count
FROM organizations o
LEFT JOIN industries i ON o.industry_id = i.industry_id
LEFT JOIN contacts c ON o.org_id = c.org_id AND c.is_primary = true
WHERE o.org_type = 'CLIENT' AND o.is_active = true;

-- Outstanding invoices
CREATE VIEW v_outstanding_invoices AS
SELECT
    i.invoice_id,
    i.invoice_number,
    o.legal_name AS client_name,
    i.issue_date,
    i.due_date,
    i.total_amount,
    i.amount_paid,
    i.total_amount - i.amount_paid AS balance_due,
    i.status,
    CASE
        WHEN i.due_date < CURRENT_DATE AND i.status != 'PAID' THEN true
        ELSE false
    END AS is_overdue
FROM invoices i
JOIN organizations o ON i.org_id = o.org_id
WHERE i.status NOT IN ('PAID', 'VOID');

-- Expiring certificates (next 90 days)
CREATE VIEW v_expiring_certificates AS
SELECT
    o.legal_name,
    c.cert_type,
    c.cert_name,
    c.expiry_date,
    c.expiry_date - CURRENT_DATE AS days_until_expiry
FROM certifications c
JOIN organizations o ON c.org_id = o.org_id
WHERE c.expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '90 days'
ORDER BY c.expiry_date;

-- Data quality summary
CREATE VIEW v_data_quality_summary AS
SELECT
    source_system,
    issue_type,
    COUNT(*) AS issue_count,
    COUNT(*) FILTER (WHERE resolution IS NOT NULL) AS resolved_count
FROM data_quality_log
GROUP BY source_system, issue_type
ORDER BY source_system, issue_count DESC;

-- =============================================================================
-- PERMISSIONS
-- =============================================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO unified_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO unified_admin;
