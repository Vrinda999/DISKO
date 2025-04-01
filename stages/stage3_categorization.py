import subprocess
import os
import re
from pathlib import Path

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

def get_latest_disk_image():
    """Finds the most recent disk image in output_files/ with valid extensions."""
    image_files = sorted(
        [file for ext in VALID_EXTENSIONS for file in Path(OUTPUT_DIR).glob(f"*{ext}")],
        key=os.path.getmtime,
        reverse=True
    )
    return str(image_files[0]) if image_files else None

def categorize_data(image_path, start_sector):
    """Categorizes deleted, encrypted, current, and hidden data."""
    if not os.path.exists(image_path):
        print(f"Error: Disk image '{image_path}' not found.")
        return

    print(f"\nUsing Disk Image: {image_path}")
    print("\n--- Categorizing Data ---")

    # Deleted files
    print("\n--- Deleted Files ---")
    deleted_files = run_command(f"fls -o {start_sector} -r -p {image_path} -d")
    if deleted_files:
        print(deleted_files)
    else:
        print("No deleted files found.")

    # Encrypted files
    print("\n--- Encrypted Files ---")
    encrypted_files = run_command(f"binwalk -E {image_path}")
    if encrypted_files:
        print(encrypted_files)
    else:
        print("No encrypted data found.")

    # Current files (active files)
    print("\n--- Current Files ---")
    current_files = run_command(f"fls -o {start_sector} -r -p {image_path}")
    if current_files:
        print(current_files)
    else:
        print("No current files found.")

    # Hidden files
    print("\n--- Hidden Files ---")
    hidden_files = run_command(f"fls -o {start_sector} -r -p {image_path} | grep '\\.'")
    if hidden_files:
        print(hidden_files)
    else:
        print("No hidden files found.")

# Main Execution
if __name__ == "__main__":
    image_path = get_latest_disk_image()
    if not image_path:
        image_path = input("No disk image found in output_files/. Enter image path manually: ").strip()

    start_sector = input("Enter the start sector of partition 002: ").strip()

    if image_path and start_sector:
        categorize_data(image_path, start_sector)
    else:
        print("No disk image or start sector provided. Exiting.")
