from fpdf import FPDF
from datetime import datetime
import os
import re
import matplotlib.pyplot as plt

REPORTS_DIR = "output_files/reports"
CHART_PATH = os.path.join(REPORTS_DIR, "chart.png")
os.makedirs(REPORTS_DIR, exist_ok=True)

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Disk Forensics Categorization Report", ln=True, align="C")
        self.ln(10)

    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, content if content else "None found.")
        self.ln(5)

    def add_visual_summary(self, category_counts):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Visual Summary", ln=True)
        self.ln(5)

        # Add Pie Chart
        if os.path.exists(CHART_PATH):
            self.image(CHART_PATH, x=30, w=150)
            self.ln(5)
        else:
            self.set_font("Arial", "", 10)
            self.cell(0, 10, "No chart available.", ln=True)

def generate_pie_chart(category_counts):
    labels = [f"{cat} ({count})" for cat, count in category_counts.items()]
    sizes = list(category_counts.values())
    colors = ['#003f5c', '#7a5195', '#ef5675', '#ffa600']

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors)
    plt.axis("equal")
    plt.title("Categorized Data Overview")
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()

def clean_output_text(raw_text):
    """
    Removes forensic prefixes like '-/r * 8791378:' and returns only filenames.
    """
    cleaned_lines = []
    for line in raw_text.splitlines():
        match = re.search(r':\s+(.*)', line)
        if match:
            cleaned_lines.append(match.group(1))
        else:
            cleaned_lines.append(line.strip())
    return "\n".join(cleaned_lines)

def generate_report(disk_image_path, categorized_output):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(disk_image_path)
    report_name = f"report_{base_name}_{timestamp}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_name)

    # Count items in each category
    category_counts = {
        category: len(output.splitlines()) if output else 0
        for category, output in categorized_output.items()
    }

    # Generate chart
    generate_pie_chart(category_counts)

    # Generate PDF
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Image Path: {disk_image_path}", ln=True)
    pdf.cell(0, 10, f"Generated At: {timestamp}", ln=True)
    pdf.ln(5)

    # Add visual chart summary
    pdf.add_visual_summary(category_counts)

    # Add detailed sections
    for category, output in categorized_output.items():
        cleaned_output = clean_output_text(output)
        pdf.add_section(category, cleaned_output)

    pdf.output(report_path)
    print(f"\n✅ PDF report generated: {report_path}")
    return report_path


# Sample Data
# if __name__ == "__main__":
#     test_image_path = "output_files/sample_image.img"
#     categorized_output = {
#         "Deleted Files": "-/r * 8791378:  $OrphanFiles/UINPUT~1.UDE\n-/r * 8791384:  $OrphanFiles/XFS-MO~1.UDE",
#         "Encrypted Files": "-/r * 14770951: $OrphanFiles/DEFAUL~1.DOW",
#         "Current Files": "-/r 8791390:  /Documents/report.docx\n-/r * 8791395:  /Documents/image.png",
#         "Hidden Files": "-/r * 8791399:  /Hidden/.secretfile\n-/r * 8791400:  /Hidden/.hiddenlog"
#     }

#     generate_report(test_image_path, categorized_output)
