-- =============================================================================
-- ZZZ Accounting Legacy Database - CLEAN SCHEMA
-- =============================================================================
-- This is the "good" database with proper naming conventions, normalized
-- structure, and consistent data. Students will use this as a reference
-- for what proper database design looks like.
-- =============================================================================

-- Enable UUID extension for future compatibility
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- CLIENTS TABLE - Primary customer records
-- =============================================================================
CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    tax_id VARCHAR(20) UNIQUE,
    contact_first_name VARCHAR(50),
    contact_last_name VARCHAR(50),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    address_street VARCHAR(200),
    address_city VARCHAR(100),
    address_state CHAR(2),
    address_zip VARCHAR(10),
    industry VARCHAR(50),
    client_status VARCHAR(20) DEFAULT 'active',
    annual_revenue DECIMAL(15, 2),
    employee_count INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_accountant VARCHAR(100)
);

-- =============================================================================
-- SERVICES TABLE - Services we provide
-- =============================================================================
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    service_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    hourly_rate DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT true
);

-- =============================================================================
-- ENGAGEMENTS TABLE - Client service contracts
-- =============================================================================
CREATE TABLE engagements (
    engagement_id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(client_id),
    service_id INTEGER REFERENCES services(service_id),
    start_date DATE NOT NULL,
    end_date DATE,
    contract_value DECIMAL(15, 2),
    billing_frequency VARCHAR(20), -- monthly, quarterly, annually
    status VARCHAR(20) DEFAULT 'active',
    notes TEXT
);

-- =============================================================================
-- INVOICES TABLE - Billing records
-- =============================================================================
CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(20) UNIQUE NOT NULL,
    client_id INTEGER REFERENCES clients(client_id),
    engagement_id INTEGER REFERENCES engagements(engagement_id),
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending', -- pending, paid, overdue, cancelled
    payment_date DATE,
    payment_method VARCHAR(50)
);

-- =============================================================================
-- EMPLOYEES TABLE - Internal staff
-- =============================================================================
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    job_title VARCHAR(100),
    department VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(12, 2),
    manager_id INTEGER REFERENCES employees(employee_id),
    is_active BOOLEAN DEFAULT true
);

-- =============================================================================
-- TIME_ENTRIES TABLE - Billable hours tracking
-- =============================================================================
CREATE TABLE time_entries (
    entry_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    client_id INTEGER REFERENCES clients(client_id),
    engagement_id INTEGER REFERENCES engagements(engagement_id),
    entry_date DATE NOT NULL,
    hours DECIMAL(4, 2) NOT NULL,
    description TEXT,
    billable BOOLEAN DEFAULT true,
    billed BOOLEAN DEFAULT false,
    invoice_id INTEGER REFERENCES invoices(invoice_id)
);

-- =============================================================================
-- AUDIT_LOG TABLE - Track changes
-- =============================================================================
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    record_id INTEGER,
    action VARCHAR(20), -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- CREATE INDEXES
-- =============================================================================
CREATE INDEX idx_clients_tax_id ON clients(tax_id);
CREATE INDEX idx_clients_company_name ON clients(company_name);
CREATE INDEX idx_clients_status ON clients(client_status);
CREATE INDEX idx_invoices_client ON invoices(client_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_due_date ON invoices(due_date);
CREATE INDEX idx_time_entries_date ON time_entries(entry_date);
CREATE INDEX idx_time_entries_employee ON time_entries(employee_id);

-- =============================================================================
-- SEED DATA - Clean, consistent records
-- =============================================================================

-- Services
INSERT INTO services (service_name, service_code, description, hourly_rate) VALUES
('Tax Preparation - Individual', 'TAX-IND', 'Personal tax return preparation and filing', 150.00),
('Tax Preparation - Business', 'TAX-BUS', 'Corporate tax return preparation and filing', 250.00),
('Bookkeeping', 'BOOK', 'Monthly bookkeeping and reconciliation', 85.00),
('Payroll Services', 'PAYROLL', 'Payroll processing and tax deposits', 75.00),
('Financial Audit', 'AUDIT', 'Annual financial statement audit', 300.00),
('Business Consulting', 'CONSULT', 'Strategic business advisory services', 275.00),
('CFO Services', 'CFO', 'Fractional CFO and financial leadership', 350.00),
('QuickBooks Setup', 'QB-SETUP', 'QuickBooks implementation and training', 125.00);

-- Employees (ZZZ Accounting staff)
INSERT INTO employees (first_name, last_name, email, phone, job_title, department, hire_date, salary) VALUES
('Robert', 'Zhang', 'rzhang@zzzaccounting.com', '555-100-0001', 'Managing Partner', 'Executive', '2010-03-15', 285000.00),
('Sarah', 'Williams', 'swilliams@zzzaccounting.com', '555-100-0002', 'CFO', 'Executive', '2012-06-01', 245000.00),
('Michael', 'Johnson', 'mjohnson@zzzaccounting.com', '555-100-0003', 'Senior Accountant', 'Accounting', '2015-01-10', 95000.00),
('Emily', 'Chen', 'echen@zzzaccounting.com', '555-100-0004', 'Staff Accountant', 'Accounting', '2019-08-15', 65000.00),
('David', 'Martinez', 'dmartinez@zzzaccounting.com', '555-100-0005', 'Tax Manager', 'Tax', '2014-04-01', 125000.00),
('Jennifer', 'Lee', 'jlee@zzzaccounting.com', '555-100-0006', 'Payroll Specialist', 'Payroll', '2018-02-20', 55000.00),
('Thomas', 'Brown', 'tbrown@zzzaccounting.com', '555-100-0007', 'IT Manager', 'Technology', '2016-09-01', 110000.00),
('Amanda', 'Garcia', 'agarcia@zzzaccounting.com', '555-100-0008', 'Office Manager', 'Admin', '2017-11-15', 65000.00);

-- Update manager relationships
UPDATE employees SET manager_id = 1 WHERE employee_id IN (2, 5, 7);
UPDATE employees SET manager_id = 2 WHERE employee_id IN (3, 4);
UPDATE employees SET manager_id = 5 WHERE employee_id = 6;
UPDATE employees SET manager_id = 7 WHERE employee_id = 8;

-- Clients (Well-formatted, consistent data)
INSERT INTO clients (company_name, tax_id, contact_first_name, contact_last_name, contact_email, contact_phone, address_street, address_city, address_state, address_zip, industry, annual_revenue, employee_count, assigned_accountant) VALUES
('Acme Corporation', '12-3456789', 'John', 'Smith', 'jsmith@acmecorp.com', '555-201-0001', '123 Main Street', 'Austin', 'TX', '78701', 'Manufacturing', 5500000.00, 45, 'Michael Johnson'),
('TechStart Solutions', '23-4567890', 'Lisa', 'Wong', 'lwong@techstart.io', '555-201-0002', '456 Innovation Way', 'Austin', 'TX', '78702', 'Technology', 2800000.00, 28, 'Emily Chen'),
('Green Valley Farms', '34-5678901', 'Mark', 'Peterson', 'mpetersen@greenvalley.com', '555-201-0003', '789 Rural Route 5', 'Round Rock', 'TX', '78664', 'Agriculture', 1200000.00, 15, 'Michael Johnson'),
('Downtown Dental Group', '45-6789012', 'Dr. Susan', 'Park', 'spark@downtowndental.com', '555-201-0004', '321 Medical Plaza', 'Austin', 'TX', '78703', 'Healthcare', 3200000.00, 22, 'David Martinez'),
('Lone Star Construction', '56-7890123', 'Robert', 'Torres', 'rtorres@lonestarcon.com', '555-201-0005', '555 Builder Lane', 'Pflugerville', 'TX', '78660', 'Construction', 8900000.00, 85, 'Sarah Williams'),
('Austin Art Gallery', '67-8901234', 'Michelle', 'Adams', 'madams@austinart.org', '555-201-0006', '777 Gallery Row', 'Austin', 'TX', '78704', 'Arts', 450000.00, 8, 'Emily Chen'),
('Southwest Auto Repair', '78-9012345', 'Carlos', 'Ramirez', 'cramirez@swautorepair.com', '555-201-0007', '888 Mechanic Street', 'Austin', 'TX', '78745', 'Automotive', 1800000.00, 12, 'Michael Johnson'),
('Hill Country Winery', '89-0123456', 'Victoria', 'Hill', 'vhill@hillcountrywine.com', '555-201-0008', '999 Vineyard Road', 'Fredericksburg', 'TX', '78624', 'Food & Beverage', 2100000.00, 18, 'David Martinez'),
('Capital City Law Firm', '90-1234567', 'James', 'Morrison', 'jmorrison@capitalcitylaw.com', '555-201-0009', '100 Legal Plaza', 'Austin', 'TX', '78701', 'Legal', 4500000.00, 35, 'Sarah Williams'),
('Sunset Real Estate', '01-2345678', 'Patricia', 'Young', 'pyoung@sunsetrealty.com', '555-201-0010', '200 Property Lane', 'Austin', 'TX', '78746', 'Real Estate', 6200000.00, 42, 'David Martinez'),
('Austin Pet Hospital', '11-3456789', 'Dr. Kevin', 'Murphy', 'kmurphy@austinpet.com', '555-201-0011', '300 Animal Care Way', 'Austin', 'TX', '78731', 'Healthcare', 1900000.00, 16, 'Emily Chen'),
('Tech Gadgets Plus', '22-4567890', 'Brian', 'Kim', 'bkim@techgadgets.com', '555-201-0012', '400 Electronics Blvd', 'Cedar Park', 'TX', '78613', 'Retail', 980000.00, 9, 'Michael Johnson'),
('Fresh Fitness Gym', '33-5678901', 'Rachel', 'Green', 'rgreen@freshfitness.com', '555-201-0013', '500 Workout Way', 'Austin', 'TX', '78757', 'Fitness', 750000.00, 11, 'Emily Chen'),
('Premier Plumbing Services', '44-6789012', 'Daniel', 'White', 'dwhite@premierplumb.com', '555-201-0014', '600 Pipe Street', 'Austin', 'TX', '78748', 'Services', 1350000.00, 14, 'Michael Johnson'),
('Bright Future Academy', '55-7890123', 'Sandra', 'Thompson', 'sthompson@brightfuture.edu', '555-201-0015', '700 Education Lane', 'Round Rock', 'TX', '78681', 'Education', 2400000.00, 32, 'David Martinez');

-- Engagements
INSERT INTO engagements (client_id, service_id, start_date, end_date, contract_value, billing_frequency, status) VALUES
(1, 2, '2024-01-01', '2024-12-31', 15000.00, 'quarterly', 'active'),
(1, 3, '2024-01-01', NULL, 1020.00, 'monthly', 'active'),
(2, 2, '2024-01-01', '2024-12-31', 12000.00, 'quarterly', 'active'),
(2, 8, '2024-02-15', '2024-03-15', 2500.00, 'one-time', 'completed'),
(3, 2, '2024-01-01', '2024-12-31', 8000.00, 'quarterly', 'active'),
(4, 4, '2024-01-01', NULL, 900.00, 'monthly', 'active'),
(5, 5, '2024-06-01', '2024-08-31', 45000.00, 'one-time', 'active'),
(5, 7, '2024-01-01', NULL, 4200.00, 'monthly', 'active'),
(6, 1, '2024-01-01', '2024-04-15', 1500.00, 'one-time', 'completed'),
(7, 2, '2024-01-01', '2024-12-31', 6000.00, 'quarterly', 'active'),
(8, 3, '2024-01-01', NULL, 1275.00, 'monthly', 'active'),
(9, 5, '2024-09-01', '2024-11-30', 60000.00, 'one-time', 'active'),
(10, 2, '2024-01-01', '2024-12-31', 18000.00, 'quarterly', 'active'),
(10, 6, '2024-03-01', '2024-03-31', 8250.00, 'one-time', 'completed');

-- Invoices
INSERT INTO invoices (invoice_number, client_id, engagement_id, issue_date, due_date, amount, tax_amount, status, payment_date, payment_method) VALUES
('INV-2024-0001', 1, 1, '2024-01-15', '2024-02-14', 3750.00, 0, 'paid', '2024-02-10', 'ACH'),
('INV-2024-0002', 1, 2, '2024-01-31', '2024-02-28', 1020.00, 0, 'paid', '2024-02-25', 'ACH'),
('INV-2024-0003', 2, 3, '2024-01-15', '2024-02-14', 3000.00, 0, 'paid', '2024-02-12', 'Check'),
('INV-2024-0004', 2, 4, '2024-03-15', '2024-04-14', 2500.00, 0, 'paid', '2024-04-01', 'Credit Card'),
('INV-2024-0005', 3, 5, '2024-01-15', '2024-02-14', 2000.00, 0, 'paid', '2024-02-10', 'Check'),
('INV-2024-0006', 4, 6, '2024-01-31', '2024-02-28', 900.00, 0, 'paid', '2024-02-20', 'ACH'),
('INV-2024-0007', 5, 7, '2024-06-30', '2024-07-30', 15000.00, 0, 'pending', NULL, NULL),
('INV-2024-0008', 5, 8, '2024-01-31', '2024-02-28', 4200.00, 0, 'paid', '2024-02-28', 'ACH'),
('INV-2024-0009', 6, 9, '2024-04-15', '2024-05-15', 1500.00, 0, 'paid', '2024-05-10', 'Check'),
('INV-2024-0010', 7, 10, '2024-04-15', '2024-05-15', 1500.00, 0, 'paid', '2024-05-01', 'ACH');

-- Time entries (sample)
INSERT INTO time_entries (employee_id, client_id, engagement_id, entry_date, hours, description, billable, billed) VALUES
(3, 1, 1, '2024-01-10', 4.00, 'Q4 2023 tax preparation', true, true),
(3, 1, 1, '2024-01-11', 3.50, 'Q4 2023 tax preparation continued', true, true),
(4, 2, 3, '2024-01-08', 2.00, 'Monthly bookkeeping review', true, true),
(5, 5, 7, '2024-06-15', 8.00, 'Audit planning and fieldwork', true, false),
(5, 5, 7, '2024-06-16', 8.00, 'Audit fieldwork - inventory', true, false),
(3, 7, 10, '2024-03-15', 3.00, 'Tax return preparation', true, true),
(2, 5, 8, '2024-01-20', 4.00, 'CFO advisory meeting', true, true),
(4, 1, 2, '2024-01-31', 2.00, 'January bookkeeping', true, true);

-- Audit log entries
INSERT INTO audit_log (table_name, record_id, action, new_values, changed_by, changed_at) VALUES
('clients', 1, 'INSERT', '{"company_name": "Acme Corporation"}', 'system', '2024-01-01 09:00:00'),
('clients', 2, 'INSERT', '{"company_name": "TechStart Solutions"}', 'system', '2024-01-01 09:05:00'),
('invoices', 1, 'UPDATE', '{"status": "paid", "payment_date": "2024-02-10"}', 'swilliams', '2024-02-10 14:30:00');

-- =============================================================================
-- GRANT PERMISSIONS
-- =============================================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO zzz_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO zzz_admin;
