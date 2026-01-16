-- =============================================================================
-- BBB Construction Legacy Database - DIFFERENT SCHEMA
-- =============================================================================
-- This database uses:
-- - UUIDs instead of integers for primary keys
-- - JSON/JSONB columns for semi-structured data
-- - Construction industry terminology (contractors, projects, certificates)
-- - Different date formats (Unix timestamps mixed with ISO)
-- - Completely different table structure than ZZZ or AAA
--
-- Students will learn to map different schemas to a unified model!
-- =============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- CONTRACTORS - Primary entity (equivalent to clients)
-- =============================================================================
CREATE TABLE contractors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_name VARCHAR(200) NOT NULL,
    dba_name VARCHAR(200),  -- "Doing Business As"
    federal_id VARCHAR(50),  -- EIN/Tax ID
    contractor_license VARCHAR(50),
    license_state CHAR(2),
    primary_contact JSONB,  -- Nested: {name, email, phone, title}
    billing_address JSONB,  -- Nested: {street, city, state, zip, country}
    mailing_address JSONB,  -- Might be different
    company_type VARCHAR(50),  -- LLC, Corp, Sole Prop, Partnership
    specialties JSONB,  -- Array of specialties
    insurance_info JSONB,  -- {provider, policy_num, expiry, coverage_amount}
    bonding_info JSONB,
    safety_rating FLOAT,
    prequalified BOOLEAN DEFAULT false,
    approved_date BIGINT,  -- Unix timestamp!
    status VARCHAR(20) DEFAULT 'active',
    metadata JSONB,  -- Catch-all for random data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- PROJECTS - Construction projects
-- =============================================================================
CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_code VARCHAR(50) UNIQUE,
    project_name VARCHAR(200) NOT NULL,
    client_name VARCHAR(200),  -- Not linked to contractors!
    site_address JSONB,
    project_type VARCHAR(50),  -- Commercial, Residential, Industrial, etc.
    contract_value DECIMAL(15, 2),
    start_date BIGINT,  -- Unix timestamp
    estimated_completion BIGINT,
    actual_completion BIGINT,
    status VARCHAR(30),  -- Bidding, Awarded, InProgress, Complete, OnHold, Cancelled
    project_manager UUID,  -- References team_members
    superintendent UUID,
    budget_data JSONB,  -- Complex nested budget structure
    change_orders JSONB,  -- Array of change orders
    notes TEXT[]  -- PostgreSQL array of notes
);

-- =============================================================================
-- PROJECT_CONTRACTORS - Many-to-many relationship
-- =============================================================================
CREATE TABLE project_contractors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(project_id),
    contractor_id UUID REFERENCES contractors(id),
    role VARCHAR(100),  -- General, Electrical, Plumbing, HVAC, etc.
    contract_amount DECIMAL(15, 2),
    contract_signed BIGINT,  -- Unix timestamp
    work_start BIGINT,
    work_complete BIGINT,
    payment_terms VARCHAR(100),
    retainage_percent FLOAT,
    status VARCHAR(20),
    documents JSONB  -- Links to contracts, insurance certs, etc.
);

-- =============================================================================
-- INVOICES - Payment requests from contractors
-- =============================================================================
CREATE TABLE invoices (
    invoice_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_number VARCHAR(50),
    project_id UUID REFERENCES projects(project_id),
    contractor_id UUID REFERENCES contractors(id),
    invoice_date BIGINT,  -- Unix timestamp
    due_date BIGINT,
    period_start BIGINT,
    period_end BIGINT,
    gross_amount DECIMAL(15, 2),
    retainage_held DECIMAL(15, 2),
    net_amount DECIMAL(15, 2),
    line_items JSONB,  -- Array of {description, quantity, unit, unit_price, total}
    approved_by VARCHAR(100),
    approved_date BIGINT,
    paid_date BIGINT,
    check_number VARCHAR(50),
    status VARCHAR(20)  -- Submitted, Approved, Rejected, Paid, Partial
);

-- =============================================================================
-- CERTIFICATES - Insurance, licenses, bonds tracking
-- =============================================================================
CREATE TABLE certificates (
    cert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contractor_id UUID REFERENCES contractors(id),
    cert_type VARCHAR(50),  -- Insurance, License, Bond, Safety, OSHA
    cert_name VARCHAR(200),
    issuing_authority VARCHAR(200),
    cert_number VARCHAR(100),
    issue_date BIGINT,
    expiry_date BIGINT,
    coverage_amount DECIMAL(15, 2),
    document_url TEXT,
    verified BOOLEAN DEFAULT false,
    verified_by VARCHAR(100),
    verified_date BIGINT,
    notes TEXT
);

-- =============================================================================
-- TEAM_MEMBERS - BBB internal staff
-- =============================================================================
CREATE TABLE team_members (
    member_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_code VARCHAR(20),
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    role VARCHAR(100),
    department VARCHAR(50),
    hire_date BIGINT,  -- Unix timestamp
    certifications JSONB,
    emergency_contact JSONB,
    is_active BOOLEAN DEFAULT true
);

-- =============================================================================
-- PAYMENTS - Outgoing payments to contractors
-- =============================================================================
CREATE TABLE payments (
    payment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES invoices(invoice_id),
    payment_date BIGINT,
    amount DECIMAL(15, 2),
    payment_method VARCHAR(50),  -- Check, ACH, Wire
    reference_number VARCHAR(100),
    bank_account VARCHAR(50),
    memo TEXT,
    created_by VARCHAR(100)
);

-- =============================================================================
-- SEED DATA
-- =============================================================================

-- Team Members first (for references)
INSERT INTO team_members (member_id, employee_code, full_name, email, phone, role, department, hire_date, is_active) VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'BBB-001', 'William Baker', 'wbaker@bbbconstruction.com', '555-300-0001', 'President', 'Executive', 1104537600, true),
('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'BBB-002', 'Patricia Stone', 'pstone@bbbconstruction.com', '555-300-0002', 'CFO', 'Finance', 1199145600, true),
('c3d4e5f6-a7b8-9012-cdef-123456789012', 'BBB-003', 'Michael Rivers', 'mrivers@bbbconstruction.com', '555-300-0003', 'Project Manager', 'Operations', 1325376000, true),
('d4e5f6a7-b8c9-0123-defa-234567890123', 'BBB-004', 'Sarah Wood', 'swood@bbbconstruction.com', '555-300-0004', 'Superintendent', 'Field', 1420070400, true);

-- Contractors (with JSON data)
INSERT INTO contractors (id, business_name, dba_name, federal_id, contractor_license, license_state, primary_contact, billing_address, company_type, specialties, insurance_info, prequalified, approved_date, status) VALUES
-- Duplicate of ZZZ/AAA client Lone Star
('11111111-1111-1111-1111-111111111111', 'Lone Star Construction Company', 'Lone Star Construction', '56-7890123', 'TXC-789012', 'TX',
 '{"name": "Roberto Torres", "email": "rtorres@lonestarcon.com", "phone": "555-201-0005", "title": "Owner"}',
 '{"street": "555 Builder Lane", "city": "Pflugerville", "state": "TX", "zip": "78660"}',
 'LLC', '["General Contracting", "Commercial", "Renovation"]',
 '{"provider": "Texas Builders Insurance", "policy_num": "TBI-2024-5678", "expiry": 1735689600, "coverage": 5000000}',
 true, 1609459200, 'active'),

-- Electrical contractor
('22222222-2222-2222-2222-222222222222', 'Spark Electric Inc', NULL, '66-6666666', 'ELEC-12345', 'TX',
 '{"name": "James Spark", "email": "jspark@sparkelectric.com", "phone": "(512) 666-1234", "title": "President"}',
 '{"street": "100 Volt Avenue", "city": "Austin", "state": "TX", "zip": "78745"}',
 'Corporation', '["Electrical", "Commercial Electrical", "Industrial Electrical"]',
 '{"provider": "Contractor Shield", "policy_num": "CS-EL-9999", "expiry": 1740787200, "coverage": 2000000}',
 true, 1577836800, 'active'),

-- Plumbing contractor
('33333333-3333-3333-3333-333333333333', 'FlowRight Plumbing LLC', 'FlowRight', '77-7777777', 'PLB-54321', 'TX',
 '{"name": "Maria Flow", "email": "mflow@flowrightplumb.com", "phone": "512.777.5432"}',
 '{"street": "200 Pipe St", "city": "Round Rock", "state": "TX", "zip": "78681"}',
 'LLC', '["Plumbing", "Commercial Plumbing", "New Construction"]',
 '{"provider": "Trade Pro Insurance", "policy_num": "TPI-PLB-2024", "expiry": 1727740800, "coverage": 1500000}',
 true, 1609459200, 'active'),

-- HVAC contractor (different data format)
('44444444-4444-4444-4444-444444444444', 'Cool Air Systems', 'CAS HVAC', '88-8888888', 'HVAC-99999', 'TX',
 '{"name": "David Cool", "email": "dcool@coolairsystems.com", "phone": "5128889999", "title": "Owner/Operator"}',
 '{"street": "300 Climate Ctrl Blvd", "city": "Cedar Park", "state": "TX", "zip": "78613", "country": "USA"}',
 'Sole Proprietorship', '["HVAC", "Heating", "Air Conditioning", "Ventilation"]',
 '{"provider": "HVAC Pros Insurance", "policy_num": "HPI-2024-001", "expiry": 1735689600, "coverage": 1000000}',
 true, 1625097600, 'active'),

-- Expired insurance (problem contractor)
('55555555-5555-5555-5555-555555555555', 'Budget Builders', NULL, '55-5555555', 'GEN-11111', 'TX',
 '{"name": "Cheap Charlie", "email": "charlie@budgetbuild.com", "phone": "555-555-5555"}',
 '{"street": "999 Low Bid Lane", "city": "Austin", "state": "TX", "zip": "78701"}',
 'LLC', '["General", "Residential"]',
 '{"provider": "Minimum Coverage Inc", "policy_num": "MCI-0001", "expiry": 1672531200, "coverage": 500000}',  -- EXPIRED!
 false, 1577836800, 'inactive'),

-- Pending approval
('66666666-6666-6666-6666-666666666666', 'New Build Partners', 'NBP Construction', '99-9999999', 'PENDING', 'TX',
 '{"name": "New Guy", "email": "info@newbuild.com"}',
 '{"street": "TBD", "city": "Austin", "state": "TX"}',
 'Partnership', '["General Contracting"]',
 NULL,
 false, NULL, 'pending');

-- Projects
INSERT INTO projects (project_id, project_code, project_name, client_name, site_address, project_type, contract_value, start_date, estimated_completion, status, project_manager, superintendent) VALUES
('aaaa0000-0000-0000-0000-000000000001', 'PRJ-2024-001', 'Austin Office Complex', 'Acme Corporation',
 '{"street": "500 Commerce Drive", "city": "Austin", "state": "TX", "zip": "78701"}',
 'Commercial', 2500000.00, 1704067200, 1735689600, 'InProgress',
 'c3d4e5f6-a7b8-9012-cdef-123456789012', 'd4e5f6a7-b8c9-0123-defa-234567890123'),

('aaaa0000-0000-0000-0000-000000000002', 'PRJ-2024-002', 'TechStart HQ Renovation', 'TechStart Solutions',
 '{"street": "456 Innovation Way", "city": "Austin", "state": "TX", "zip": "78702"}',
 'Commercial Renovation', 850000.00, 1709251200, 1725148800, 'InProgress',
 'c3d4e5f6-a7b8-9012-cdef-123456789012', NULL),

('aaaa0000-0000-0000-0000-000000000003', 'PRJ-2023-015', 'Hill Country Winery Expansion', 'Hill Country Winery',
 '{"street": "999 Vineyard Road", "city": "Fredericksburg", "state": "TX", "zip": "78624"}',
 'Industrial', 1200000.00, 1672531200, 1688169600, 'Complete',
 'c3d4e5f6-a7b8-9012-cdef-123456789012', 'd4e5f6a7-b8c9-0123-defa-234567890123'),

('aaaa0000-0000-0000-0000-000000000004', 'PRJ-2024-003', 'Downtown Dental Clinic Buildout', 'Downtown Dental Group',
 '{"street": "321 Medical Plaza", "city": "Austin", "state": "TX", "zip": "78703"}',
 'Healthcare', 450000.00, 1714521600, NULL, 'Bidding',
 NULL, NULL);

-- Project Contractors (linking tables)
INSERT INTO project_contractors (project_id, contractor_id, role, contract_amount, contract_signed, status) VALUES
('aaaa0000-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111', 'General Contractor', 2000000.00, 1701388800, 'Active'),
('aaaa0000-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222', 'Electrical', 180000.00, 1704067200, 'Active'),
('aaaa0000-0000-0000-0000-000000000001', '33333333-3333-3333-3333-333333333333', 'Plumbing', 120000.00, 1704067200, 'Active'),
('aaaa0000-0000-0000-0000-000000000001', '44444444-4444-4444-4444-444444444444', 'HVAC', 200000.00, 1704153600, 'Active'),
('aaaa0000-0000-0000-0000-000000000002', '11111111-1111-1111-1111-111111111111', 'General Contractor', 680000.00, 1706659200, 'Active'),
('aaaa0000-0000-0000-0000-000000000002', '22222222-2222-2222-2222-222222222222', 'Electrical', 85000.00, 1709251200, 'Active'),
('aaaa0000-0000-0000-0000-000000000003', '11111111-1111-1111-1111-111111111111', 'General Contractor', 960000.00, 1669852800, 'Complete');

-- Invoices from contractors
INSERT INTO invoices (invoice_number, project_id, contractor_id, invoice_date, due_date, gross_amount, retainage_held, net_amount, line_items, status) VALUES
('LS-2024-001', 'aaaa0000-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111',
 1706659200, 1709337600, 150000.00, 15000.00, 135000.00,
 '[{"description": "Site prep and foundation", "amount": 100000}, {"description": "Framing Phase 1", "amount": 50000}]',
 'Paid'),
('LS-2024-002', 'aaaa0000-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111',
 1709337600, 1712016000, 200000.00, 20000.00, 180000.00,
 '[{"description": "Framing Phase 2", "amount": 80000}, {"description": "Rough-in coordination", "amount": 120000}]',
 'Approved'),
('SE-2024-001', 'aaaa0000-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222',
 1707868800, 1710547200, 45000.00, 4500.00, 40500.00,
 '[{"description": "Rough electrical Phase 1", "amount": 45000}]',
 'Paid'),
('FR-2024-001', 'aaaa0000-0000-0000-0000-000000000001', '33333333-3333-3333-3333-333333333333',
 1708473600, 1711152000, 35000.00, 3500.00, 31500.00,
 '[{"description": "Rough plumbing Phase 1", "amount": 35000}]',
 'Submitted');

-- Certificates
INSERT INTO certificates (contractor_id, cert_type, cert_name, issuing_authority, cert_number, issue_date, expiry_date, coverage_amount, verified, verified_by, verified_date) VALUES
('11111111-1111-1111-1111-111111111111', 'Insurance', 'General Liability', 'Texas Builders Insurance', 'TBI-2024-5678', 1704067200, 1735689600, 5000000.00, true, 'Patricia Stone', 1704153600),
('11111111-1111-1111-1111-111111111111', 'License', 'General Contractor', 'Texas Dept of Licensing', 'TXC-789012', 1609459200, 1767225600, NULL, true, 'Patricia Stone', 1609545600),
('22222222-2222-2222-2222-222222222222', 'Insurance', 'General Liability', 'Contractor Shield', 'CS-EL-9999', 1709251200, 1740787200, 2000000.00, true, 'Patricia Stone', 1709337600),
('22222222-2222-2222-2222-222222222222', 'License', 'Electrical Contractor', 'TDLR', 'ELEC-12345', 1577836800, 1735689600, NULL, true, 'Patricia Stone', 1577923200),
('33333333-3333-3333-3333-333333333333', 'Insurance', 'General Liability', 'Trade Pro Insurance', 'TPI-PLB-2024', 1696118400, 1727740800, 1500000.00, true, 'Patricia Stone', 1696204800),
-- Expired certificate
('55555555-5555-5555-5555-555555555555', 'Insurance', 'General Liability', 'Minimum Coverage Inc', 'MCI-0001', 1640995200, 1672531200, 500000.00, true, 'Patricia Stone', 1641081600);

-- Payments
INSERT INTO payments (invoice_id, payment_date, amount, payment_method, reference_number, memo, created_by) VALUES
((SELECT invoice_id FROM invoices WHERE invoice_number = 'LS-2024-001'), 1708300800, 135000.00, 'ACH', 'ACH-2024-0015', 'Lone Star - January pay app', 'Patricia Stone'),
((SELECT invoice_id FROM invoices WHERE invoice_number = 'SE-2024-001'), 1709510400, 40500.00, 'Check', 'CHK-10234', 'Spark Electric - Rough-in Phase 1', 'Patricia Stone');

-- =============================================================================
-- Create indexes
-- =============================================================================
CREATE INDEX idx_contractors_federal_id ON contractors(federal_id);
CREATE INDEX idx_contractors_status ON contractors(status);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_client ON projects(client_name);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_certificates_expiry ON certificates(expiry_date);

-- =============================================================================
-- Views for common queries
-- =============================================================================
CREATE VIEW v_active_contractors AS
SELECT
    id,
    business_name,
    federal_id,
    primary_contact->>'name' as contact_name,
    primary_contact->>'email' as contact_email,
    primary_contact->>'phone' as contact_phone,
    insurance_info->>'expiry' as insurance_expiry,
    prequalified,
    status
FROM contractors
WHERE status = 'active';

CREATE VIEW v_expiring_certificates AS
SELECT
    c.business_name,
    cert.cert_type,
    cert.cert_name,
    cert.expiry_date,
    TO_TIMESTAMP(cert.expiry_date) as expiry_readable
FROM certificates cert
JOIN contractors c ON cert.contractor_id = c.id
WHERE cert.expiry_date < EXTRACT(EPOCH FROM NOW() + INTERVAL '90 days')
ORDER BY cert.expiry_date;

-- =============================================================================
-- Grant permissions
-- =============================================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bbb_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO bbb_admin;
