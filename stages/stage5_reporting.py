import subprocess
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

OUTPUT_DIR = "output_files"  # Folder where disk images are stored
VALID_EXTENSIONS = [".dd", ".E01", ".img"]  # Supported image formats

def run_command(command):
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        return None

def generate_report(deleted_files, encrypted_files, current_files, hidden_files, report_filename="categorized_data_report.pdf"):
    """Generates a PDF report with categorized data."""
    pdf = canvas.Canvas(report_filename, pagesize=letter)
    width, height = letter  # Default letter size is 8.5 x 11 inches

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, height - 72, "Disk Forensics - Categorized Data Report")

    # Category Headers
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, height - 120, "Deleted Files:")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(72, height - 140, deleted_files if deleted_files else "No deleted files found.")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, height - 180, "Encrypted Files:")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(72, height - 200, encrypted_files if encrypted_files else "No encrypted files found.")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, height - 240, "Current Files:")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(72, height - 260, current_files if current_files else "No current files found.")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, height - 300, "Hidden Files:")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(72, height - 320, hidden_files if hidden_files else "No hidden files found.")

    # Save the PDF file
    pdf.save()
    print(f"Report generated: {report_filename}")

def generate_categorized_report(image_path, start_sector):
    """Generates the categorized report based on categorized data."""
    if not os.path.exists(image_path):
        print(f"Error: Disk image '{image_path}' not found.")
        return

    print(f"\nUsing Disk Image: {image_path}")
    print("\n--- Categorizing Data ---")

    # Deleted files
    print("\n--- Deleted Files ---")
    deleted_files = run_command(f"fls -o {start_sector} -r -p {image_path} -d")
    if not deleted_files:
        print("No deleted files found.")
        deleted_files = "No deleted files found."

    # Encrypted files
    print("\n--- Encrypted Files ---")
    encrypted_files = run_command(f"binwalk -E {image_path}")
    if not encrypted_files:
        print("No encrypted data found.")
        encrypted_files = "No encrypted data found."

    # Current files (active files)
    print("\n--- Current Files ---")
    current_files = run_command(f"fls -o {start_sector} -r -p {image_path}")
    if not current_files:
        print("No current files found.")
        current_files = "No current files found."

    # Hidden files
    print("\n--- Hidden Files ---")
    hidden_files = run_command(f"fls -o {start_sector} -r -p {image_path} | grep '\\.'")
    if not hidden_files:
        print("No hidden files found.")
        hidden_files = "No hidden files found."

    # Generate the report in PDF format
    generate_report(deleted_files, encrypted_files, current_files, hidden_files)


# Main Execution
if __name__ == "__main__":
    image_path = input("Enter the disk image path: ").strip()
    start_sector = input("Enter the start sector of partition 002: ").strip()

    if image_path and start_sector:
        generate_categorized_report(image_path, start_sector)
    else:
        print("No disk image or start sector provided. Exiting.")
