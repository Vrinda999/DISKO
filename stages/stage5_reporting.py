from fpdf import FPDF
from datetime import datetime
import os
import matplotlib.pyplot as plt

REPORTS_DIR = "output_files/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "DISKO Report", ln=True, align="C")
        self.ln(10)

    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, content if content else "None found.")
        self.ln(5)
        
    def add_pie_chart(self, chart_path):
        self.image(chart_path, x=40, w=130)
        self.ln(10)
        
def create_pie_chart(categorized_output, chart_path):
    labels = []
    sizes = []

    for category, content in categorized_output.items():
        count = len(content.strip().splitlines()) if content else 0
        labels.append(category)
        sizes.append(count)

    # Define autopct function to show count + percentage
    def autopct_func(pct):
        total = sum(sizes)
        count = int(round(pct * total / 100.0))
        return f"{count} ({pct:.1f}%)"

    colors = ['#003f5c', '#7a5195', '#ef5675', '#ffa600']
    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, colors=colors, autopct=autopct_func, startangle=140)
    plt.axis("equal")
    plt.title("Summary of File Categories", fontsize=12)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()


def generate_report(disk_image_path, categorized_output):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(disk_image_path)
    report_name = f"report_{base_name}_{timestamp}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_name)
    
    # Chart
    chart_path = os.path.join(REPORTS_DIR, f"chart_{timestamp}.png")
    create_pie_chart(categorized_output, chart_path)

    pdf = PDFReport()
    pdf.add_page()

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Image Path: {disk_image_path}", ln=True)
    pdf.cell(0, 10, f"Generated At: {timestamp}", ln=True)
    pdf.ln(5)
    
    pdf.add_section("Visual Summary", "")
    pdf.ln(5)
    pdf.image(chart_path, w=100)
    pdf.ln(10)

    # Add sections
    for category, output in categorized_output.items():
        pdf.add_section(category, output)

    pdf.output(report_path)
    print(f"\n✅ PDF report generated: {report_path}")
    return report_path

# if __name__ == "__main__":
#     # Sample data for testing
#     test_disk_image = "output_files/sample_test.img"
#     sample_output = {
#         "Deleted Files": "\n".join([f"Deleted_File_{i}.txt" for i in range(10)]),
#         "Encrypted Files": "\n".join([f"Encrypted_Block_{i}" for i in range(3)]),
#         "Current Files": "\n".join([f"File_{i}.docx" for i in range(25)]),
#         "Hidden Files": "\n".join([f".hidden_{i}.cfg" for i in range(5)])
#     }

#     generate_report(test_disk_image, sample_output)