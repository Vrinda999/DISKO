from stages.stage1_disk_imaging import run_dcfldd
from stages.stage2_extraction import analyze_disk_image
from stages.stage3_categorization import categorize_data
from stages.stage5_reporting import generate_categorized_report

def main():
    print("Disk Forensics Tool - CLI Version")

    # Stage 1: Disk Imaging or Provide Existing Image
    disk_image = run_dcfldd()
    if not disk_image:
        print("Disk imaging failed or cancelled. Exiting...")
        return

    print(f"Using Disk Image: {disk_image}")

    # Stage 2: Analyze Disk Image
    print("\nProceeding to disk image analysis...")
    # Analyze the disk image and get the start sector of partition 002
    start_sector = analyze_disk_image(disk_image)
    if not start_sector:
        print("Disk image analysis failed. Exiting...")
        return

    # Stage 3: Categorization
    print("\nProceeding to data categorization...")
    categorize_data(disk_image, start_sector)

    # Stage 4: Generate Categorized Data Report
    print("\nProceeding to generate categorized data report...")
    generate_categorized_report(disk_image, start_sector)

if __name__ == "__main__":
    main()
