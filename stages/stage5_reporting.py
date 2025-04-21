from fpdf import FPDF
from datetime import datetime
import os
import matplotlib.pyplot as plt
import tempfile
import subprocess

REPORTS_DIR = "output_files/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(40, 40, 40)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 12, "Disk Forensics Report", ln=True, align="C", fill=True)
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

    def add_section(self, title, content, include_metadata=True):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(33, 33, 33)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, f"{title}", ln=True, fill=True)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0)

        cleaned_lines = []
        for line in content.splitlines():
            parts = line.split(":\t")
            if len(parts) == 2:
                cleaned_lines.append(parts[1])
            else:
                cleaned_lines.append(line)

        if not cleaned_lines:
            self.multi_cell(0, 6, "None found.")
            self.ln(5)
            return

        for line in cleaned_lines:
            self.multi_cell(0, 6, f"{line}")
            if include_metadata:
                metadata = get_metadata(line)
                if metadata:
                    self.set_font("Helvetica", "I", 9)
                    self.set_text_color(100)
                    self.multi_cell(0, 5, f"Metadata:\n{metadata}")
                    self.set_font("Helvetica", "", 10)
                    self.set_text_color(0)
                else:
                    self.multi_cell(0, 5, "Metadata: Not available.")
            self.ln(1)

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

def get_metadata(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        result = subprocess.run(["exiftool", file_path], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def generate_report(disk_image_path, categorized_output, filtered_output=None, keyword_hits=None, filtered_only=False, include_metadata=False):
    from subprocess import run
    import json

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base_name = os.path.basename(disk_image_path)
    report_name = f"report_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_name)

    final_output = {}

    if filtered_only:
        if filtered_output:
            for ext, files in filtered_output.items():
                final_output[f"Filtered by Type ({ext})"] = "\n".join(files)
        if keyword_hits:
            # Flatten and stringify keyword hits
            all_hits = []
            for hit_list in keyword_hits.values():
                for hit in hit_list:
                    if isinstance(hit, tuple):
                        all_hits.append(f"{hit[0]} (in {hit[1]})")
                    else:
                        all_hits.append(str(hit))
            final_output["Keyword Hits"] = "\n".join(all_hits)
    else:
        final_output = categorized_output


    pdf = PDFReport()
    pdf.add_page()
    pdf.add_metadata(disk_image_path, timestamp)

    # Table and pie chart
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Visual Summary", ln=True)
    pdf.ln(2)
    pdf.add_table(final_output)

    chart_path = generate_pie_chart(final_output)
    if chart_path:
        pdf.image(chart_path, w=100, x=(210 - 100) // 2)
        os.unlink(chart_path)

    # Add sections with optional metadata
    for category, content in final_output.items():
        pdf.add_section(f"{category} Files", content)

        if include_metadata:
            lines = content.splitlines()
            for file_path in lines:
                if os.path.isfile(file_path):
                    try:
                        meta = run(["exiftool", "-j", file_path], capture_output=True, text=True)
                        if meta.stdout:
                            metadata_json = json.loads(meta.stdout)[0]
                            meta_text = "\n".join([f"{k}: {v}" for k, v in metadata_json.items()])
                            pdf.add_section(f"Metadata for {os.path.basename(file_path)}", meta_text)
                    except Exception as e:
                        pdf.add_section(f"Metadata Error for {os.path.basename(file_path)}", str(e))

    pdf.output(report_path)
    print(f"\n✅ PDF report generated: {report_path}")
    return report_path