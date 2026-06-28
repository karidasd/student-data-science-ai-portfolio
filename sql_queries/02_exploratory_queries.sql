-- 02_exploratory_queries.sql
-- Coursera / Google Data Analytics Project Structure Style
-- Advanced SQL queries showing Joins, CTEs, and Window Functions for data analysis.

-- Query 1: Categorize students into Study cohorts using a CTE and calculate pass rates
WITH study_cohorts AS (
    SELECT 
        student_id,
        passed,
        CASE 
            WHEN study_hours < 8 THEN 'Low Study (<8h)'
            WHEN study_hours BETWEEN 8 AND 14 THEN 'Medium Study (8-14h)'
            ELSE 'High Study (>14h)'
        END AS cohort
    FROM student_performance
)
SELECT 
    cohort,
    COUNT(student_id) AS total_students,
    SUM(CASE WHEN passed = 'Yes' THEN 1 ELSE 0 END) AS passed_students,
    ROUND(SUM(CASE WHEN passed = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(student_id) * 100, 2) AS pass_rate_pct
FROM study_cohorts
GROUP BY cohort
ORDER BY pass_rate_pct DESC;


-- Query 2: Extracurricular impact on average scores and attendance
SELECT 
    extracurricular,
    COUNT(student_id) AS student_count,
    ROUND(AVG(exam_score), 2) AS avg_exam_score,
    ROUND(AVG(attendance_pct), 2) AS avg_attendance_pct
FROM student_performance
GROUP BY extracurricular;


-- Query 3: Rank students by exam scores within their study time categories using Window Functions
WITH categorized_students AS (
    SELECT 
        student_id,
        study_hours,
        exam_score,
        CASE 
            WHEN study_hours < 10 THEN 'Short Study Hours'
            ELSE 'Long Study Hours'
        END AS study_type
    FROM student_performance
)
SELECT 
    student_id,
    study_type,
    exam_score,
    DENSE_RANK() OVER (PARTITION BY study_type ORDER BY exam_score DESC) as rank_within_type
FROM categorized_students
ORDER BY study_type, rank_within_type;
