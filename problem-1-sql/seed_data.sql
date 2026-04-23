-- SATU Dental — Problem 1 seed data
-- 3 clinics, 6 patients, ~25 appointments across Jan-Mar 2026

DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS clinics;

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    full_name VARCHAR(200),
    created_at TIMESTAMP
);

CREATE TABLE clinics (
    clinic_id INT PRIMARY KEY,
    clinic_name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    clinic_id INT,
    appointment_date DATE,
    status VARCHAR(20),
    total_amount NUMERIC(12,2)
);

INSERT INTO patients VALUES
    (1, 'Budi Santoso',    '2025-12-01 09:00:00'),
    (2, 'Siti Rahayu',     '2025-12-15 10:00:00'),
    (3, 'Andi Wijaya',     '2026-01-10 14:00:00'),
    (4, 'Maya Putri',      '2026-01-20 11:00:00'),
    (5, 'Rizki Hakim',     '2026-02-05 09:30:00'),
    (6, 'Dewi Lestari',    '2026-02-18 15:00:00');

INSERT INTO clinics VALUES
    (1, 'Kemang Dental',     'Jakarta Selatan'),
    (2, 'PIK Dental Center', 'Jakarta Utara'),
    (3, 'Senopati Smile',    'Jakarta Selatan');

-- ===== January 2026 =====
-- Kemang Dental: 3 first-time patients (Budi, Siti, Andi)
INSERT INTO appointments VALUES
    (1001, 1, 1, '2026-01-05', 'completed',  500000.00),
    (1002, 2, 1, '2026-01-12', 'completed',  450000.00),
    (1003, 3, 1, '2026-01-20', 'completed',  500000.00);

-- PIK Dental Center: 2 first-time patients (Budi, Maya)
INSERT INTO appointments VALUES
    (1004, 1, 2, '2026-01-08', 'completed',  400000.00),
    (1005, 4, 2, '2026-01-22', 'completed',  450000.00);

-- Noise: 2 no-shows, 1 cancelled — should be excluded
INSERT INTO appointments VALUES
    (1006, 5, 1, '2026-01-15', 'no_show',    0.00),
    (1007, 6, 3, '2026-01-18', 'no_show',    0.00),
    (1008, 2, 2, '2026-01-25', 'cancelled',  0.00);

-- ===== February 2026 =====
-- Kemang: Budi (returning), Siti (returning); 2 completed visits
INSERT INTO appointments VALUES
    (2001, 1, 1, '2026-02-03', 'completed',  500000.00),
    (2002, 2, 1, '2026-02-10', 'completed',  400000.00);

-- PIK: Maya comes twice this month (same-day duplicate on 2026-02-15: two entries, one 350k, one 400k -> dedupe keep 400k)
-- And a separate visit on 2026-02-20: 350k
INSERT INTO appointments VALUES
    (2003, 4, 2, '2026-02-15', 'completed',  350000.00),
    (2004, 4, 2, '2026-02-15', 'completed',  400000.00),  -- same-day dup, this one wins on amount
    (2005, 4, 2, '2026-02-20', 'completed',  350000.00);

-- Senopati: 2 first-time (Rizki, Dewi)
INSERT INTO appointments VALUES
    (2006, 5, 3, '2026-02-08', 'completed',  550000.00),
    (2007, 6, 3, '2026-02-25', 'completed',  650000.00);

-- Noise: a cancelled appt
INSERT INTO appointments VALUES
    (2008, 3, 1, '2026-02-12', 'cancelled',  0.00);

-- ===== March 2026 =====
-- Kemang: Siti returning, plus first-time Dewi (NULL amount -> treat as 0)
INSERT INTO appointments VALUES
    (3001, 2, 1, '2026-03-05', 'completed',  600000.00),
    (3002, 6, 1, '2026-03-15', 'completed',  NULL),
    (3003, 4, 1, '2026-03-20', 'completed',  500000.00);

-- Wait: we want Kemang March = 2 unique patients, 1 first-time, 1 returning
-- Let me realign: Siti visited Kemang in Jan & Feb (returning), Maya is first time at Kemang (first-time). That's 2 unique.
-- But I added 3 rows above (Siti, Dewi, Maya). Let me drop Dewi from Kemang March so first-time=1.
DELETE FROM appointments WHERE appointment_id = 3002;

-- Actually we want total_completed_visits=2 in Kemang March and revenue = 1100000 (600k Siti + 500k Maya).
-- Confirmed.

-- Senopati: Rizki returning (visited Feb)
INSERT INTO appointments VALUES
    (3004, 5, 3, '2026-03-12', 'completed',  650000.00);

-- Noise: no-show and cancelled
INSERT INTO appointments VALUES
    (3005, 1, 2, '2026-03-18', 'no_show',    0.00),
    (3006, 3, 3, '2026-03-22', 'cancelled',  0.00);
