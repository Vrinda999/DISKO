# from jinja2 import Environment, FileSystemLoader
# from datetime import datetime
# from weasyprint import HTML
# import os

# def generate_report(image_info, categorized_data):
#     env = Environment(loader=FileSystemLoader('stages/'))
#     template = env.get_template("template.html")

#     html_out = template.render(
#         date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         image=image_info,
#         categorized=categorized_data
#     )

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     report_filename = f"forensic_report_{timestamp}.pdf"
#     report_path = os.path.join("output_files", report_filename)

#     HTML(string=html_out).write_pdf(report_path)
#     print(f"✅ Report saved to {report_path}")
    
# if __name__ == "__main__":
#     sample_image_info = {
#         "name": "sample_image.dd",
#         "hash": "abc123hashvalue",
#         "size": "2.3GB"
#     }

#     categorized_output = {
#         "Deleted Files": ["file1.txt", "file2.doc", "file3.jpg"],
#         "Encrypted Files": ["Encrypted data segment found at 0x0001A000"],
#         "Current Files": ["Documents/report.docx", "Images/photo.png"],
#         "Hidden Files": [".hidden_file", ".system_config"]
#     }

#     generate_report(sample_image_info, categorized_output, "output_files/reports/report.pdf")