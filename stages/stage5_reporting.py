from fpdf import FPDF
from datetime import datetime
import os
import matplotlib.pyplot as plt
import tempfile
import subprocess
import re

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
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(33, 33, 33)
        self.cell(0, 5, f"{title}", fill=True, ln=True)
        self.cell(0, 2, "", ln=True)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0)


        if title.lower() == "encrypted files":
            self.set_fill_color(200, 220, 255)
            self.set_text_color(0)
            self.set_font("Helvetica", "B", 11)
            self.cell(30, 8, "Decimal", 1, 0, "C", True)
            self.cell(30, 8, "Hexadecimal", 1, 0, "C", True)
            self.cell(80, 8, "Entropy", 1, 1, "C", True)

            self.set_font("Helvetica", "", 10)
            self.set_fill_color(240, 240, 240)

            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                
                self.set_fill_color(240, 240, 240)
                parts = re.split(r'\s+', line)
                if len(parts) >= 6:
                    dec = parts[0]
                    hexadec = parts[1]
                    entropy = " ".join(parts[2:])

                    self.cell(30, 8, dec, 1, 0, "C", True)
                    self.cell(30, 8, hexadec, 1, 0, "C", True)
                    self.cell(80, 8, entropy, 1, 1, "C", True)
            self.ln(10)

        else:
            cleaned_lines = []
            for line in content.splitlines():
                parts = line.split(":\t")
                if len(parts) == 2:
                    cleaned_lines.append(parts[1])
                else:
                    cleaned_lines.append(line)

            if not cleaned_lines:
                self.multi_cell(0, 5, "None found.")
                self.ln(5)
                return

            for line in cleaned_lines:
                self.multi_cell(0, 5, f"{line}")
                if include_metadata:
                    metadata = get_metadata(line)
                    if metadata:
                        self.set_font("Helvetica", "I", 9)
                        self.set_text_color(100)
                        self.multi_cell(0, 5, f"Metadata:\n{metadata}")
                        self.set_font("Helvetica", "", 10)
                        self.set_text_color(0)
                        self.cell(0, 2, "", ln=True)
                    else:
                        self.cell(0, 2, "", ln=True)

            self.ln(5)
    
    def set_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(33, 33, 33)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, ln=True, fill=True)
        return super().set_title(title)

    def set_content(self):
        self.set_font("Helvetica", "", 10)


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



def generate_report(disk_image_path, mmls_output, categorized_output, filtered_output=None, keyword_hits=None, filtered_only=False, include_metadata=False):
    from subprocess import run
    import json

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base_name = os.path.basename(disk_image_path)
    report_name = f"report_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_name)

    final_output = {}

    pdf = PDFReport()
    pdf.add_page()
    pdf.add_metadata(disk_image_path, timestamp)

    
    pdf.set_title("Partition Table")
    pdf.set_content
    
    pdf.set_fill_color(200, 220, 255)
    pdf.set_text_color(0)
    pdf.set_font("Helvetica", "B", 11)
    # pdf.cell(40, 8, "Slot", 1, 0, "C", True)
    # pdf.cell(50, 8, "Start Sector", 1, 0, "C", True)
    # pdf.cell(40, 8, "Description", 1, 1, "C", True)

    pdf.cell(20, 8, "Slot", 1, 0, "C", True)
    pdf.cell(30, 8, "Start Sector", 1, 0, "C", True)
    pdf.cell(30, 8, "End", 1, 0, "C", True)
    pdf.cell(30, 8, "Length", 1, 0, "C", True)
    pdf.cell(40, 8, "Description", 1, 1, "C", True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_fill_color(240, 240, 240)
    for line in mmls_output.splitlines():
        line = line.strip()
        if not line:
            continue
        
        pdf.set_fill_color(240, 240, 240)
        parts = re.split(r'\s+', line)
        if len(parts) >= 6:
            slot = parts[0].strip(":")
            start_sector = parts[2]
            end = parts[3]
            length = parts[4]
            description = " ".join(parts[5:])

            pdf.cell(20, 8, slot, 1, 0, "C", True)
            pdf.cell(30, 8, start_sector, 1, 0, "C", True)
            pdf.cell(30, 8, end, 1, 0, "C", True)
            pdf.cell(30, 8, length, 1, 0, "C", True)
            pdf.cell(40, 8, description, 1, 1, "C", True)
    pdf.ln(10)

    # Table and pie chart
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Visual Summary", ln=True)
    pdf.ln(2)
    pdf.add_table(categorized_output)

    chart_path = generate_pie_chart(categorized_output)
    if chart_path:
        pdf.image(chart_path, w=100, x=(210 - 100) // 2)
        os.unlink(chart_path)

    if filtered_output and isinstance(filtered_output, dict):
        pdf.set_title("Files Filtered by Extension")
        pdf.ln(2)
        for ext, files in filtered_output.items():
            pdf.cell(0, 2, "", ln=True)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 5, ext, ln=True)
            pdf.set_content()
            if files == []:
                pdf.cell(0, 5, "No Files with this Extension Present", ln=True)
            else:
                for file in files:
                    pdf.multi_cell(0, 5, file)
        pdf.cell(0, 5, "", ln=True)

    if keyword_hits and isinstance(keyword_hits, dict):
        pdf.set_title("Keywords")
        pdf.set_content()
        pdf.ln(2)
        
        for kw, hit_list in keyword_hits.items():
            pdf.cell(0, 2, "", ln=True)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 5, kw, ln=True)
            pdf.set_content()

            if isinstance(hit_list, str) or len(hit_list) == 1 and isinstance(hit_list[0], str):
                pdf.cell(0, 5, f'Keyword "{kw}" Not Present.')
                pdf.cell(0, 5, "", ln=True)
            else:
                for path, sent in hit_list:
                    pdf.set_fill_color(240, 240, 240)
                    pdf.set_font("Helvetica", "B", 10)
                    pdf.multi_cell(0, 5, f"File Path: {path}", align="L")
                    pdf.set_font("Helvetica", "", 10)
                    pdf.multi_cell(0, 5, f"Sentence: {sent}", align="L")
                    pdf.cell(0, 2, "", ln=True)
            pdf.cell(0, 5, "", ln=True)

    if filtered_only == False:
        # Add sections with optional metadata
        pdf.set_title("Categorised Files")
        pdf.set_content()
        pdf.ln(2)
        
        for category, content in categorized_output.items():
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
        pdf.add_page()

    pdf.output(report_path)
    print(f"\n✅ PDF report generated: {report_path}")
    return report_path