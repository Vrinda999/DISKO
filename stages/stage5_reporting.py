from fpdf import FPDF
from datetime import datetime
import os
import matplotlib.pyplot as plt
import tempfile

REPORTS_DIR = "output_files/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)
title = "Disk Forensic Report"

class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(40, 40, 40)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 12, title, ln=True, align="C", fill=True)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_metadata(self, disk_image_path, timestamp):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0)
        self.cell(0, 10, f"Image Path: {disk_image_path}", ln=True)
        self.cell(0, 10, f"Generated At: {timestamp}", ln=True)
        self.ln(5)

    def add_table(self, data_dict):
        self.set_fill_color(200, 220, 255)
        self.set_text_color(0)
        self.set_font("Helvetica", "B", 11)
        self.cell(60, 8, "Category", 1, 0, "C", True)
        self.cell(40, 8, "File Count", 1, 1, "C", True)

        self.set_font("Helvetica", "", 10)
        for category, files in data_dict.items():
            count = len(files.splitlines())
            self.cell(60, 8, category, 1)
            self.cell(40, 8, str(count), 1, 1)

        self.ln(10)

    def add_section(self, title, content):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(33, 33, 33)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, f"{title}", ln=True, fill=True)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0)

        # Clean and format the filenames
        cleaned_lines = []
        for line in content.splitlines():
            parts = line.split(":\t")
            if len(parts) == 2:
                cleaned_lines.append(parts[1])
            else:
                cleaned_lines.append(line)

        display_text = "\n".join(cleaned_lines) if cleaned_lines else "None found."
        self.multi_cell(0, 6, display_text)
        self.ln(5)

def generate_pie_chart(data_dict):
    labels = []
    sizes = []
    for category, content in data_dict.items():
        count = len(content.splitlines())
        if count > 0:
            labels.append(f"{category} ({count})")
            sizes.append(count)

    if not sizes:
        return None

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis("equal")

    tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.savefig(tmp_file.name, bbox_inches="tight")
    plt.close()
    return tmp_file.name

def generate_report(disk_image_path, categorized_output):
    ''' 
                    file_types, matching_files, 
                    keywords, kw_res,
                    ans, media_file_types):
    '''
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base_name = os.path.basename(disk_image_path)
    report_name = f"report_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_name)

    pdf = PDFReport()
    pdf.set_title(title)
    pdf.add_page()

    # Metadata
    pdf.add_metadata(disk_image_path, timestamp)

    # Visual Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Visual Summary", ln=True)
    pdf.ln(2)

    pdf.add_table(categorized_output)

    # Pie chart
    chart_path = generate_pie_chart(categorized_output)
    if chart_path:
        pdf.image(chart_path, w=100, x=(210-100)//2)
        os.unlink(chart_path)  # cleanup

    # Sections
    for category, content in categorized_output.items():
        pdf.add_section(f"{category} Files", content)

    pdf.output(report_path)
    print(f"\n✅ PDF report generated: {report_path}")
    return report_path

# For testing
# if __name__ == "__main__":
#     sample_data = {
#         "Deleted": "-/r * 8791378:\t$OrphanFiles/UINPUT~1.UDE\n-/r * 14770951:\t$OrphanFiles/DEFAUL~1.DOW",
#         "Encrypted": "0       0x0             Encrypted data, encrypted",
#         "Current": "-/r * 1001234:\t/home/user/document.txt\n-/r * 1001235:\t/home/user/photo.jpg",
#         "Hidden": "-/r * 1001250:\t.$secret_config\n-/r * 1001251:\t.hiddenfile.log"
#     }
#     generate_report("output_files/sample.img", sample_data)
