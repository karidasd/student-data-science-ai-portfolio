# main.py
# End-to-End Orchestrator for the Data Science & AI Pipeline
# This script executes the local database imports, runs EDA, saves plots, and triggers the AI report.

import os
import subprocess
import sys

def run_step(step_name, command_args):
    """Utility to run a script and handle logs."""
    print(f"\n[RUNNING] Step: {step_name}...")
    try:
        subprocess.run([sys.executable] + command_args, check=True)
        print(f"[SUCCESS] Step '{step_name}' completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error in Step '{step_name}': {e}")
        return False

def main():
    print("="*60)
    print("AUTOMATED DATA SCIENCE & AI PORTFOLIO PIPELINE")
    print("="*60)

    # Step 1: Initialize Database and run SQL queries
    if not run_step("Database Import & Relational Querying", ["setup_db.py"]):
        print("Pipeline aborted due to step 1 failure.")
        sys.exit(1)

    # Step 2: Exploratory Data Analysis & plotting
    # We execute eda_visualization.py as a script
    if not run_step("Exploratory Data Analysis & Seaborn Visualizations", ["notebooks/eda_visualization.py"]):
        print("Pipeline aborted due to step 2 failure.")
        sys.exit(1)

    # Step 3: Run AI Report Generator
    if not run_step("AI-Driven Report Generation", ["ai_agent/ai_report_generator.py"]):
        print("Pipeline aborted due to step 3 failure.")
        sys.exit(1)

    print("\n" + "="*60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("   Visualizations saved in 'plots/' directory.")
    print("   Run this script anytime you swap your CSV dataset to update the portfolio.")
    print("="*60)

if __name__ == "__main__":
    main()
