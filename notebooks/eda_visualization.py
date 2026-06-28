# %% [markdown]
# # Student Performance Exploratory Data Analysis
# This script covers data cleaning, statistics, and visualizations using Seaborn and Matplotlib.
# Aligns with the **Kaggle Learn** and **freeCodeCamp** curriculum.
#
# ## Objectives:
# 1. Load and inspect the student performance dataset.
# 2. Compute descriptive statistics and correlation matrices.
# 3. Save publication-quality Seaborn visualizations.

# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ## 1. Load and Inspect Dataset
# We load the dataset that was generated from our Kaggle-style CSV file.

# %%
csv_path = "../data/student_performance.csv"
if not os.path.exists(csv_path):
    # Fallback for execution from root directory
    csv_path = "data/student_performance.csv"

df = pd.read_csv(csv_path)
print("First 5 records:")
print(df.head())
print("\nDataset Shape:", df.shape)

# %% [markdown]
# ## 2. Statistical Analysis
# Let's check summary statistics and compute correlations.

# %%
print("\nSummary Statistics:")
print(df.describe())

# Compute correlation matrix for numeric columns
numeric_df = df.select_dtypes(include=[np.number])
corr_matrix = numeric_df.corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

# %% [markdown]
# ## 3. Data Visualization
# Create a directory to store visualizations, then generate a scatter plot and a correlation heatmap.

# %%
plots_dir = "../plots"
if not os.path.exists(plots_dir) and not os.path.exists("plots"):
    os.makedirs("plots", exist_ok=True)
    plots_dir = "plots"
elif os.path.exists("plots"):
    plots_dir = "plots"

# Set style
sns.set_theme(style="whitegrid")

# %% [markdown]
# ### Visualization A: Study Hours vs. Exam Score
# We use Seaborn to draw a scatter plot and color code by whether the student passed.

# %%
plt.figure(figsize=(7, 5))
sns.scatterplot(
    data=df, 
    x="study_hours", 
    y="exam_score", 
    hue="passed", 
    palette={"Yes": "forestgreen", "No": "crimson"},
    style="passed",
    s=100, 
    alpha=0.8
)
plt.title("Study Hours vs. Exam Score", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Hours Studied per Week", fontsize=11)
plt.ylabel("Exam Score (0-100)", fontsize=11)
plt.legend(title="Passed")
plt.tight_layout()

scatter_filename = os.path.join(plots_dir, "study_hours_vs_score.png")
plt.savefig(scatter_filename, dpi=150)
print(f"Saved scatter plot to: {scatter_filename}")
plt.close()

# %% [markdown]
# ### Visualization B: Correlation Heatmap
# Drawing a correlation heatmap to show correlation values.

# %%
plt.figure(figsize=(6, 4.5))
sns.heatmap(
    corr_matrix, 
    annot=True, 
    cmap="coolwarm", 
    vmin=-1, 
    vmax=1, 
    fmt=".2f", 
    linewidths=0.5
)
plt.title("Correlation Matrix Heatmap", fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()

heatmap_filename = os.path.join(plots_dir, "correlation_heatmap.png")
plt.savefig(heatmap_filename, dpi=150)
print(f"Saved heatmap to: {heatmap_filename}")
plt.close()
