import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF

# Load data
df = pd.read_csv("data.csv")

# Create directories
os.makedirs("outputs/plots", exist_ok=True)

# === Generate Plots ===
# Histogram for Age
plt.figure()
df["Age"].hist(bins=10, color='skyblue')
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.grid(True)
age_plot = "outputs/plots/age_histogram.png"
plt.savefig(age_plot)
plt.close()

# Correlation Heatmap
plt.figure(figsize=(6, 5))
plt.matshow(df.select_dtypes(include='number').corr(), cmap='coolwarm', fignum=1)
plt.title("Correlation Heatmap", pad=20)
plt.colorbar()
plt.tight_layout()
heatmap_plot = "outputs/plots/correlation_heatmap.png"
plt.savefig(heatmap_plot)
plt.close()

# === Generate PDF Report ===
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Automated Data Analysis Report", ln=True, align='C')

    def chapter_title(self, title):
        self.set_font("Arial", 'B', 12)
        self.ln(10)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, body):
        self.set_font("Arial", '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

    def insert_image(self, img_path, w=160, h=100):
        self.image(img_path, x=25, w=w, h=h)
        self.ln(10)

# Create PDF
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.chapter_title("1. Summary Statistics")
summary_stats = df.describe().round(2).to_string()
pdf.chapter_body(summary_stats)

pdf.chapter_title("2. Missing Values")
missing = df.isnull().sum()
missing_text = missing.to_string()
pdf.chapter_body(missing_text)

pdf.chapter_title("3. Visualizations")
pdf.insert_image(age_plot)
pdf.insert_image(heatmap_plot)

# Save PDF
pdf.output("outputs/report.pdf")
print("✅ PDF report saved as outputs/report.pdf")
