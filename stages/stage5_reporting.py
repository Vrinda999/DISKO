from fpdf import FPDF
from datetime import datetime
import os

REPORTS_DIR = "output_files/reports"
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

def generate_report(disk_image_path, categorized_output):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(disk_image_path)
    report_name = f"report_{base_name}_{timestamp}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_name)

    pdf = PDFReport()
    pdf.add_page()

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Image Path: {disk_image_path}", ln=True)
    pdf.cell(0, 10, f"Generated At: {timestamp}", ln=True)
    pdf.ln(5)

    # Add sections
    for category, output in categorized_output.items():
        pdf.add_section(category, output)

    pdf.output(report_path)
    print(f"\n✅ PDF report generated: {report_path}")
    return report_path
