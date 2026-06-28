# %% [markdown]
# # AI Report Generator for Data Analytics
# This script demonstrates how to integrate a Large Language Model (LLM) API with tabular summaries
# to auto-generate structured JSON reports.
#
# Aligns with **DeepLearning.AI Short Courses** (LLM API integrations & Prompt Engineering).

# %%
import os
import json
import httpx
import pandas as pd

# %% [markdown]
# ## 1. Load Data Summary
# We load the dataset and compute summary stats that we will feed to the LLM.

# %%
csv_path = "../data/student_performance.csv"
if not os.path.exists(csv_path):
    csv_path = "data/student_performance.csv"

df = pd.read_csv(csv_path)

# Calculate summary aggregates for the AI context
total_students = len(df)
avg_study_hours = float(df["study_hours"].mean())
avg_attendance = float(df["attendance_pct"].mean())
pass_rate = float((df["passed"] == "Yes").mean() * 100)

data_summary = f"""
Total Cohort size: {total_students} students
Average Weekly Study Hours: {avg_study_hours:.2f} hours
Average Attendance Percentage: {avg_attendance:.2f}%
Overall Pass Rate: {pass_rate:.2f}%
"""
print("Calculated summary aggregates for the LLM:")
print(data_summary)

# %% [markdown]
# ## 2. Formulate Prompt with XML Tags (DeepLearning.AI Best Practice)
# We structure instructions, schema definitions, and the data context inside XML tags to optimize LLM performance.

# %%
system_prompt = (
    "You are an AI Education Consultant. Your role is to analyze course statistics "
    "and output a structured report in JSON format."
)

user_prompt = f"""
<instructions>
Analyze the statistics provided in the <data_summary> block.
Provide:
1. A brief summary of the cohort performance.
2. An assessment of whether attendance or study hours are the main drivers of success.
3. 2 actionable recommendations for teachers to improve student performance.

Your output must be strictly a valid JSON object matching this schema:
{{
  "cohort_summary": "string",
  "key_drivers": "string",
  "recommendations": ["string", "string"]
}}
Do not include any explanation or markdown formatting other than the JSON itself.
</instructions>

<data_summary>
{data_summary}
</data_summary>
"""

# %% [markdown]
# ## 3. Query LLM API
# We will show how to query Hugging Face's serverless Inference API (which hosts Llama/Mistral models)
# or fallback to a simulated response if no internet/API keys are configured.

# %%
# Hugging Face Free serverless model endpoint
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
hf_token = os.environ.get("HUGGINGFACE_API_KEY") # You can get a free token at huggingface.co

try:
    if hf_token:
        print("\nSending request to Hugging Face Inference API...")
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Format input prompt matching model expectations
        payload = {
            "inputs": f"<s>[INST] {system_prompt}\n\n{user_prompt} [/INST]",
            "parameters": {"max_new_tokens": 500, "return_full_text": False}
        }
        
        response = httpx.post(HF_API_URL, json=payload, headers=headers, timeout=20.0)
        
        if response.status_code == 200:
            result = response.json()
            raw_text = result[0]['generated_text'].strip()
            
            # Clean up potential markdown code block wrappers
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:-3].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:-3].strip()
                
            parsed_json = json.loads(raw_text)
            print("\n=== AI GENERATED STRUCTURED REPORT ===")
            print(json.dumps(parsed_json, indent=2))
        else:
            print(f"HF API returned status code: {response.status_code}")
            print(response.text)
            raise Exception("API failure")
            
    else:
        print("\n(Skipping API call because HUGGINGFACE_API_KEY is not set).")
        print("Here is a simulation of the structured JSON report Claude/Llama would return:")
        
        simulated_json = {
            "cohort_summary": f"The cohort comprises {total_students} students with a healthy pass rate of {pass_rate:.1f}%. However, attendance averages {avg_attendance:.1f}%, leaving room for improvement.",
            "key_drivers": "Historical correlations show that students studying over 12 hours per week have a near-100% pass rate, making study time the dominant driver.",
            "recommendations": [
                "Implement weekly mandatory study group hours for students studying less than 8 hours.",
                "Introduce attendance tracking alerts at the 80% mark to trigger early counseling."
            ]
        }
        
        print("\n=== SIMULATED AI RESPONSE ===")
        print(json.dumps(simulated_json, indent=2))
        
except Exception as e:
    print(f"\nAPI execution failed or timed out: {e}")
