import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import os

# Load data
data = pd.read_csv("dataSet.csv")

# Create output directories
os.makedirs("outputs", exist_ok=True)
os.makedirs("outputs/plots", exist_ok=True)

# --- Analysis ---
summary = data.describe().to_html(classes='table table-striped', border=0)
missing = data.isnull().sum().to_frame("Missing Values")
missing_html = missing.to_html(classes='table table-bordered', border=0)

# --- Visualizations ---
plots = []

# Histogram for each numerical column
for col in data.select_dtypes(include='number').columns:
    plt.figure()
    sns.histplot(data[col].dropna(), kde=True, bins=20)
    plt.title(f"Histogram of {col}")
    plot_path = f"outputs/plots/hist_{col}.png"
    plt.savefig(plot_path)
    plt.close()
    plots.append(plot_path)

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
heatmap_path = "outputs/plots/correlation_heatmap.png"
plt.title("Correlation Heatmap")
plt.savefig(heatmap_path)
plt.close()
plots.append(heatmap_path)

# --- Report Template ---
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Automated Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; }
        .table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        img { max-width: 600px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>📊 Automated Data Report</h1>

    <h2>1. Summary Statistics</h2>
    {{ summary_table | safe }}

    <h2>2. Missing Value Report</h2>
    {{ missing_table | safe }}

    <h2>3. Visualizations</h2>
    {% for plot in plots %}
        <img src="{{ plot }}" alt="plot">
    {% endfor %}
</body>
</html>
"""

template = Template(html_template)

report_html = template.render(
    summary_table=summary,
    missing_table=missing_html,
    plots=plots
)

with open("outputs/report.html", "w", encoding="utf-8") as f:
    f.write(report_html)

print("✅ Report generated: outputs/report.html")
