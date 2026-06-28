# setup_db.py
# Automated SQLite Local Database Setup & SQL Runner
# This script imports data from your CSV into a local SQLite database and runs educational SQL queries.

import os
import sqlite3
import pandas as pd
# No external tabulate dependency needed - using pandas native formatting

DB_NAME = "students.db"
CSV_PATH = "data/student_performance.csv"

def init_database():
    """Initializes the database and populates it with records from the CSV."""
    print(f"Initializing local SQLite database: {DB_NAME}...")
    
    # Remove existing database to ensure fresh run
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV data not found at {CSV_PATH}.")
        return False

    # Connect to SQLite (creates file automatically)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Load CSV data using Pandas
    df = pd.read_csv(CSV_PATH)
    
    # Save DataFrame into SQL Table
    df.to_sql("student_performance", conn, index=False, if_exists="replace")
    print("[SUCCESS] CSV data imported successfully into SQL table 'student_performance'.")
    
    conn.commit()
    conn.close()
    return True

def run_exploratory_queries():
    """Reads SQL queries from 02_exploratory_queries.sql and runs them against SQLite."""
    if not os.path.exists(DB_NAME):
        print("Error: Database has not been initialized.")
        return

    print("\nRunning SQL Queries from 'sql_queries/02_exploratory_queries.sql':")
    conn = sqlite3.connect(DB_NAME)
    
    # Define the queries directly for SQLite execution (SQLite matches standard SQL syntax)
    queries = {
        "Query 1: Study Cohorts and Pass Rates (CTE)": """
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
        """,
        "Query 2: Extracurricular Impact on Scores and Attendance": """
            SELECT 
                extracurricular,
                COUNT(student_id) AS student_count,
                ROUND(AVG(exam_score), 2) AS avg_exam_score,
                ROUND(AVG(attendance_pct), 2) AS avg_attendance_pct
            FROM student_performance
            GROUP BY extracurricular;
        """,
        "Query 3: Dense Rank Window Function Partitioned by Study Type": """
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
        """
    }

    for name, sql in queries.items():
        print("\n" + "-" * 60)
        print(f"[SQL] {name}")
        print("-" * 60)
        try:
            # Query into Pandas to print nicely
            result_df = pd.read_sql_query(sql, conn)
            print(result_df.to_string(index=False))
        except Exception as e:
            print(f"SQL execution error on query: {e}")

    conn.close()

if __name__ == "__main__":
    if init_database():
        run_exploratory_queries()
