import os

from stages.stage1_disk_imaging import run_dcfldd
from stages.stage2_extraction import analyze_disk_image
from stages.stage3_categorization import categorize_data
from stages.stage4_filtering import get_files_by_type
from stages.stage4_2_keyword import MasterFunc
from stages.stage5_reporting import generate_report


def main():
    print("🔍 DISKO: Disk Operation Tool for Data Categorization and Keyword Filtering - CLI Version")

    # Stage 1: Disk Imaging or Use Existing Image
    disk_image = run_dcfldd()
    if not disk_image:
        print("❌ Disk imaging failed or cancelled. Exiting...")
        return

    print(f"\n✅ Using Disk Image: {disk_image}")

    # Stage 2: Partition Analysis (Get start sector)
    print("\n📊 Analyzing disk image to identify partition...")
    start_sector = analyze_disk_image(disk_image)
    if not start_sector:
        print("❌ Disk image analysis failed. Exiting...")
        return

    # Stage 3: Data Categorization
    print("\n📂 Proceeding to data categorization...")
    categorized_output = categorize_data(disk_image, start_sector)
    if not categorized_output:
        print("❌ Categorization failed. Exiting...")
        return

    # Stage 4
    print("\n📂 Proceeding to Filtering...")
    
    # File type filtering
    file_types = input("Enter file types (comma-separated, e.g., .pdf, .png): ").split(",")
    if file_types[0] == '':
        print("No File Type Selected")
    else:
        matching_files = get_files_by_type(disk_image, categorized_output['current'], file_types)
        if matching_files:
            print("\nMatching files:")
            for ext in matching_files:
                print(f'.{ext} Files')
                for files in matching_files[ext]:
                    print(files)
                print()
        else:
            print("No files found with the specified extensions.")
        

    # Keyword Filtering from Text Files.
    image_name = os.path.basename(disk_image)
    image_stem = os.path.splitext(image_name)[0]

    keywords = input("Enter Keywords (comma-separated, e.g.: Lorem, Ipsum, dolor): ").split(",")
    if keywords[0] == '':
        print("No Keywords Chosen")
    else:
        keywords = [kw.strip().lower() for kw in keywords]
        output_dir = input("Enter Output Directory (e.g.: ./output_files/extracted_files): ")
        output_dir = os.path.join(output_dir, image_stem)
        MasterFunc(disk_image, keywords, output_dir, start_sector)

    # Stage 5: Report Generation
    print("\n📝 Generating PDF report...")
    generate_report(disk_image, categorized_output)

if __name__ == "__main__":
    main()