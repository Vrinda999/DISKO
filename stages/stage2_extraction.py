import subprocess
import re
import os
from pathlib import Path

OUTPUT_DIR = "output_files"  # Folder where stage1 saves images
VALID_EXTENSIONS = [".dd", ".E01", ".img"]  # Supported image formats

def run_command(command):
    """Helper function to execute a command and return its output"""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        return None

def get_latest_disk_image():
    """Finds the most recent disk image in output_files/ with valid extensions"""
    try:
        image_files = sorted(
            [file for ext in VALID_EXTENSIONS for file in Path(OUTPUT_DIR).glob(f"*{ext}")],
            key=lambda f: os.path.getmtime(f),
            reverse=True
        )
        return str(image_files[0]) if image_files else None
    except Exception as e:
        print(f"Error finding latest disk image: {e}")
        return None

def get_partition_start_sector(mmls_output):
    """Extract the start sector of partition 002"""
    for line in mmls_output.splitlines():
        match = re.match(r"\s*002:\s+\d+:\d+\s+(\d+)", line)  # Adjusted regex
        if match:
            return match.group(1)
    return None

def analyze_disk_image(image_path):
    """Extracts partition info and file metadata using The Sleuth Kit"""

    if not os.path.exists(image_path):
        print(f"Error: Disk image '{image_path}' not found.")
        return None

    print(f"\nUsing Disk Image: {image_path}")

    print("\n--- Partition Table Information ---")
    mmls_output = run_command(f"mmls {image_path}")
    if not mmls_output:
        print("Error: mmls command failed.")
        return None

    print(mmls_output)

    start_sector = get_partition_start_sector(mmls_output)
    if not start_sector:
        print("Error: Could not determine start sector.")
        return None

    print(f"\n--- Extracted Start Sector: {start_sector} ---")

    print("\n--- File System Information ---")
    fsstat_output = run_command(f"fsstat -o {start_sector} {image_path}")
    if fsstat_output:
        print(fsstat_output)
    else:
        print("Error: fsstat command failed.")

    print("\n--- Listing Root Directory Files ---")
    fls_output = run_command(f"fls -r -o {start_sector} {image_path}")
    if fls_output:
        print(fls_output)
    else:
        print("Error: fls command failed.")

    return start_sector

# Main Execution
if __name__ == "__main__":
    image_path = get_latest_disk_image()
    if not image_path:
        image_path = input("No disk image found in output_files/. Enter image path manually: ").strip()

    if image_path:
        analyze_disk_image(image_path)
    else:
        print("No disk image provided. Exiting.")
