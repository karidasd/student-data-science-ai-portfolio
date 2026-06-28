-- 01_schema_setup.sql
-- Coursera / Google Data Analytics Project Structure Style
-- This script sets up a mock relational schema to store student performance metrics.

-- Create Students Performance Table
CREATE TABLE IF NOT EXISTS student_performance (
    student_id INT PRIMARY KEY,
    study_hours DECIMAL(4, 2),
    attendance_pct DECIMAL(5, 2),
    extracurricular VARCHAR(3), -- 'Yes' or 'No'
    exam_score INT,
    passed VARCHAR(3) -- 'Yes' or 'No'
);

-- Mock insertions (simulating importing data from Kaggle CSV)
INSERT INTO student_performance (student_id, study_hours, attendance_pct, extracurricular, exam_score, passed) VALUES
(1001, 15.00, 92.00, 'Yes', 85, 'Yes'),
(1002, 5.00, 70.00, 'No', 48, 'No'),
(1003, 12.00, 88.00, 'Yes', 78, 'Yes'),
(1004, 4.00, 65.00, 'No', 40, 'No'),
(1005, 18.00, 95.00, 'No', 92, 'Yes'),
(1006, 8.00, 82.00, 'Yes', 65, 'Yes'),
(1007, 10.00, 75.00, 'No', 58, 'No'),
(1008, 14.00, 90.00, 'Yes', 82, 'Yes'),
(1009, 6.00, 60.00, 'No', 45, 'No'),
(1010, 20.00, 98.00, 'Yes', 96, 'Yes');
