-- =============================================================================
-- AAA Accounting Legacy Database - MESSY SCHEMA
-- =============================================================================
-- This database intentionally has:
-- - Poor naming conventions (cust_master, CUST_NUM, etc.)
-- - Inconsistent data formats (phone, dates, names)
-- - Multiple columns for same data (email1, email2, email3)
-- - Missing foreign key relationships
-- - Data quality issues (duplicates, nulls, typos)
--
-- Students will learn to identify and clean these issues!
-- =============================================================================

-- No extensions - this is a legacy system that was never upgraded

-- =============================================================================
-- CUST_MASTER - Customer master file (legacy naming)
-- =============================================================================
CREATE TABLE cust_master (
    CUST_NUM INTEGER,  -- No auto-increment, no primary key initially
    cust_name TEXT,    -- Inconsistent formatting
    ein TEXT,          -- Tax ID but named differently
    CONTACT_NM TEXT,   -- Full name in one field
    email1 TEXT,
    email2 TEXT,
    email3 TEXT,       -- Why do we need 3 email columns?
    phone TEXT,        -- Mixed formats
    fax TEXT,          -- Remember fax machines?
    addr TEXT,         -- Full address crammed into one field
    CUST_TYPE TEXT,    -- B=Business, I=Individual, ?=Unknown
    ACCT_MGR TEXT,     -- Account manager name (not ID)
    YR_START INTEGER,  -- Year became customer
    ACTIVE_FLAG CHAR(1), -- Y or N or sometimes NULL
    NOTES TEXT,
    LAST_UPD TEXT      -- Date stored as text!
);

-- Add a primary key after the fact (common in legacy systems)
ALTER TABLE cust_master ADD CONSTRAINT pk_cust PRIMARY KEY (CUST_NUM);

-- =============================================================================
-- INVS - Invoices table (abbreviated names)
-- =============================================================================
CREATE TABLE invs (
    inv_no TEXT,       -- Not numeric!
    cust TEXT,         -- References cust_master.CUST_NUM but stored as text
    inv_dt TEXT,       -- Date as text
    due_dt TEXT,       -- Date as text
    amt FLOAT,         -- Using float for money (bad practice!)
    tax FLOAT,
    tot FLOAT,
    pd_dt TEXT,        -- Payment date as text
    pd_amt FLOAT,
    stat TEXT,         -- P=Paid, O=Open, V=Void, X=???
    memo TEXT
);

-- =============================================================================
-- SRVCS - Services offered (more abbreviations)
-- =============================================================================
CREATE TABLE srvcs (
    svc_cd TEXT PRIMARY KEY,
    svc_nm TEXT,
    rt FLOAT,  -- Rate
    actv TEXT  -- 1 or 0 or Y or N
);

-- =============================================================================
-- EMP_TBL - Employee table
-- =============================================================================
CREATE TABLE emp_tbl (
    emp_id TEXT,  -- Text ID like "E001"
    nm TEXT,      -- Full name
    ttl TEXT,     -- Title
    dept TEXT,
    hire TEXT,    -- Hire date as text
    sal FLOAT,
    mgr TEXT,     -- Manager emp_id
    email TEXT,
    phone TEXT
);

-- =============================================================================
-- SEED DATA - Intentionally messy and inconsistent
-- =============================================================================

-- Services (inconsistent data)
INSERT INTO srvcs (svc_cd, svc_nm, rt, actv) VALUES
('TX', 'Tax prep', 175, 'Y'),
('BK', 'bookkeeping', 90, '1'),
('PAY', 'PAYROLL', 80, 'y'),
('AUD', 'audit services', 325, 'Y'),
('CON', 'consulting', 250, NULL);

-- Employees (some messy data)
INSERT INTO emp_tbl (emp_id, nm, ttl, dept, hire, sal, mgr, email, phone) VALUES
('E001', 'Anderson, Margaret', 'Owner/Partner', 'EXEC', '1998-03-15', 195000, NULL, 'manderson@aaaaccounting.net', '5559990001'),
('E002', 'Bob Williams', 'Senior Accountant', 'Acct', '3/15/2008', 88000, 'E001', 'bwilliams@aaaaccounting.net', '555-999-0002'),
('E003', 'Chen, Lisa M.', 'Staff Acct', 'accounting', '2015-06-01', 58000, 'E002', 'lchen@aaaaccounting.net', '(555) 999-0003'),
('E004', 'DAVID GARCIA', 'Tax Preparer', 'Tax', '01/15/2019', 52000, 'E002', 'dgarcia@aaaaccounting.net', '555.999.0004'),
('E005', 'emily jones', 'Admin', 'admin', '2020-8-1', 42000, 'E001', 'ejones@aaaaccounting.net', '5559990005');

-- Customers (VERY messy - this is where students learn!)
INSERT INTO cust_master (CUST_NUM, cust_name, ein, CONTACT_NM, email1, email2, email3, phone, fax, addr, CUST_TYPE, ACCT_MGR, YR_START, ACTIVE_FLAG, NOTES, LAST_UPD) VALUES
-- Clean-ish record
(1001, 'Smith Hardware LLC', '11-1111111', 'Tom Smith', 'tsmith@smithhw.com', NULL, NULL, '555-111-0001', NULL, '100 Main St, Austin TX 78701', 'B', 'Bob Williams', 2015, 'Y', NULL, '2024-01-15'),

-- Duplicate of ZZZ client with different formatting
(1002, 'ACME Corp', '12-3456789', 'JOHN SMITH', 'JSMITH@ACMECORP.COM', 'john.smith@acme.com', NULL, '(555) 201-0001', '555-201-0099', '123 main street, austin, TX  78701', 'B', 'Margaret Anderson', 2018, 'Y', 'BIG CLIENT', '01/20/2024'),

-- Same company, different entry (duplicate!)
(1003, 'Acme Corporation', '123456789', 'J. Smith', 'jsmith@acmecorp.com', NULL, NULL, '5552010001', NULL, '123 Main Street, Austin, Texas 78701', 'B', 'Bob Williams', 2019, 'Y', 'transferred from Margaret', '2024-01-15'),

-- Messy phone and address
(1004, 'techstart solutions', '23-4567890', 'Lisa Wong', 'lwong@techstart.io', 'lisa@techstart.io', 'lisawong@gmail.com', '555.201.0002', NULL, '456 Innovation Way Austin TX', 'B', 'Lisa Chen', 2020, 'Y', NULL, '2024/02/10'),

-- Missing data
(1005, 'Green Valley', NULL, 'Mark P.', 'mpetersen@greenvalley.com', NULL, NULL, '', NULL, 'Round Rock TX', 'B', 'Bob Williams', 2021, 'Y', 'needs tax id!', '2024-01-01'),

-- Inactive with weird status
(1008, 'Old Client Inc', '99-9999999', 'N/A', NULL, NULL, NULL, 'N/A', NULL, 'UNKNOWN', 'B', NULL, 2010, 'N', 'went out of business', '2019-12-31'),

-- Individual client
(1010, 'Johnson, Robert', '***-**-1234', 'self', 'rjohnson99@email.com', NULL, NULL, '555 123 4567', NULL, '789 Oak Lane, Round Rock, TX 78681', 'I', 'David Garcia', 2022, 'Y', 'personal taxes only', '2024-02-01'),

-- More duplicates and variations
(1012, 'downtown dental', '45-6789012', 'susan park', 'spark@downtowndental.com', NULL, NULL, '555-201-0004', NULL, '321 medical plaza austin tx 78703', 'B', 'Margaret Anderson', 2017, 'Y', NULL, '2023-12-15'),

(1015, 'Downtown Dental Group', '456789012', 'Dr. S. Park', 'dr.park@downtowndental.com', 'spark@downtowndental.com', NULL, '(555) 201-0004', '555-201-0040', '321 Medical Plaza, Ste 100, Austin, TX 78703', 'B', 'Bob Williams', 2019, 'Y', 'duplicate? check with Margaret', '2024-01-30'),

-- Non-ASCII characters (encoding issues)
(1020, 'García & Söns LLC', '77-7777777', 'José García', 'jose@garciasons.com', NULL, NULL, '555-777-0001', NULL, '500 Main St, Austin TX 78701', 'B', 'David Garcia', 2021, 'Y', 'Übersetzung needed', '2024-02-01'),

-- Empty/placeholder data
(1025, 'TBD', 'TBD', 'TBD', 'TBD', NULL, NULL, 'TBD', NULL, 'TBD', '?', NULL, 2024, NULL, 'placeholder - remove?', '2024-01-01'),

-- Very old client with old formats
(1030, 'AUSTIN AUTO WORKS', '33-3333333', 'BILL JONES', NULL, NULL, NULL, '512-333-4444', '512-333-4445', 'P.O. BOX 333, AUSTIN TX 78799', 'B', 'Margaret Anderson', 1999, 'Y', 'LONGTIME CLIENT - ALL CAPS DATA FROM OLD SYSTEM', '12/31/2023'),

-- Partial data
(1035, 'New Client Pending', NULL, NULL, 'newclient@temp.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 2024, 'Y', 'onboarding in progress', '2024-02-15'),

-- Lone Star appears in both systems
(1040, 'LONE STAR CONSTRUCTION CO', '56-7890123', 'R. Torres', 'rtorres@lonestarcon.com', 'bob@lonestarcon.com', NULL, '555-201-0005', NULL, '555 Builder Lane, Pflugerville TX 78660', 'B', 'Margaret Anderson', 2016, 'Y', 'BIG CONSTRUCTION COMPANY', '2024-01-20');

-- Invoices with inconsistent data
INSERT INTO invs (inv_no, cust, inv_dt, due_dt, amt, tax, tot, pd_dt, pd_amt, stat, memo) VALUES
('A-2024-001', '1001', '01/15/2024', '02/15/2024', 1500.00, 0, 1500.00, '02/10/2024', 1500.00, 'P', NULL),
('A-2024-002', '1002', '2024-01-20', '2024-02-20', 5000, NULL, 5000, '2024-02-18', 5000, 'P', 'ACME quarterly'),
('A2024003', '1003', '1/25/24', '2/25/24', 2500.50, 0, 2500.5, NULL, NULL, 'O', 'acme monthly??'),
('A-2024-004', '1004', '02-01-2024', '03-01-2024', 1750.00, 0, 1750.00, NULL, 0, 'O', NULL),
('2024-005', '1012', '2024-01-31', '2024-02-28', 800, 0, 800, '2024-02-25', 800, 'P', 'dental monthly'),
('INV2024006', '1040', '2024-02-01', '2024-03-01', 12500.00, 0, 12500.00, NULL, NULL, 'O', 'Lone Star audit prep'),
-- Void invoice
('A-2024-007', '1008', '2024-01-01', '2024-02-01', 500, 0, 500, NULL, NULL, 'V', 'VOIDED - client closed'),
-- Duplicate invoice numbers (oops!)
('A-2024-001', '1010', '2024-02-01', '2024-03-01', 350.00, 0, 350.00, NULL, NULL, 'O', 'personal tax prep');

-- Create some problematic indexes that might slow queries
CREATE INDEX idx_cust_name ON cust_master(cust_name);  -- On TEXT column!
CREATE INDEX idx_inv_cust ON invs(cust);  -- Text reference

-- =============================================================================
-- VIEWS (Legacy systems love views)
-- =============================================================================
CREATE VIEW v_active_customers AS
SELECT * FROM cust_master WHERE ACTIVE_FLAG = 'Y' OR ACTIVE_FLAG = 'y';

CREATE VIEW v_open_invoices AS
SELECT * FROM invs WHERE stat = 'O';

-- =============================================================================
-- Grant permissions
-- =============================================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aaa_user;
GRANT SELECT ON v_active_customers TO aaa_user;
GRANT SELECT ON v_open_invoices TO aaa_user;
