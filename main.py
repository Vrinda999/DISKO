# import os

# from stages.stage1_disk_imaging import run_dcfldd
# from stages.stage2_extraction import analyze_disk_image
# from stages.stage3_categorization import categorize_data
# from stages.stage4_filtering import get_files_by_type
# from stages.stage4_2_keyword import MasterFunc
# from stages.stage4_2_keyword import mount_and_extract_files
# from stages.stage5_reporting import generate_report


# def main():
#     print("🔍 DISKO: Disk Operation Tool for Data Categorization and Keyword Filtering - CLI Version")

#     # Stage 1: Disk Imaging or Use Existing Image
#     disk_image = run_dcfldd()
#     if not disk_image:
#         print("❌ Disk imaging failed or cancelled. Exiting...")
#         return

#     print(f"\n✅ Using Disk Image: {disk_image}")

#     # Stage 2: Partition Analysis (Get start sector)
#     print("\n📊 Analyzing disk image to identify partition...")
#     start_sector = analyze_disk_image(disk_image)
#     if not start_sector:
#         print("❌ Disk image analysis failed. Exiting...")
#         return

#     # Stage 3: Data Categorization
#     print("\n📂 Proceeding to data categorization...")
#     categorized_output = categorize_data(disk_image, start_sector)
#     if not categorized_output:
#         print("❌ Categorization failed. Exiting...")
#         return

#     # Stage 4
#     print("\n📂 Proceeding to Filtering...")
    
#     # File type filtering
#     file_types = input("Enter file types (comma-separated, e.g., .pdf, .png): ").split(", ")
#     matching_files = "No Extension Selected"
#     if file_types[0] == '':
#         print("No File Type Selected")
#     else:
#         matching_files = get_files_by_type(disk_image, categorized_output['current'], file_types)
#         if matching_files:
#             print("\nMatching files:")
#             for ext in matching_files:
#                 print(f'.{ext} Files')
#                 for files in matching_files[ext]:
#                     print(files)
#                 print()
#         else:
#             print("No files found with the specified extensions.")
        

#     # Keyword Filtering from Text Files.
#     image_name = os.path.basename(disk_image)
#     image_stem = os.path.splitext(image_name)[0]

#     keywords = input("Enter Keywords (comma-separated, e.g.: Lorem, Ipsum, dolor): ").split(",")
#     kw_res = "No Keyword Selected"
#     if keywords[0] == '':
#         print("No Keywords Chosen")
#     else:
#         keywords = [kw.strip().lower() for kw in keywords]
#         output_dir = input("Enter Output Directory (e.g.: ./output_files/extracted_files): ")
#         output_dir = os.path.join(output_dir, image_stem)
#         kw_res = MasterFunc(disk_image, keywords, output_dir, start_sector)
    
#     # Stage 4.2: Extracting Images, Videos and Audios.
#     ans = input("Do You Want to Exract Media (like images, videos, audios etc.)?: (y/n): ")
#     media_file_types = "Not Selected"
#     if ans.lower() == 'y':
#         output_dir = input("Enter Output Directory (e.g.: ./output_files/extracted_files): ")
#         output_dir = os.path.join(output_dir, image_stem)
#         media_file_types = input("Enter File Types (comma-separated, e.g.: .png, .mp4, .mp3): ").split(", ")
#         if media_file_types[0] == '':
#             media_file_types = ['.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mp3']
#         mount_and_extract_files(disk_image, output_dir, start_sector, file_types)

#     # Stage 5: Report Generation
#     print("\n📝 Generating PDF report...")
#     generate_report(disk_image, categorized_output)
#     '''
#                     file_types, matching_files = matching_files, 
#                     keywords = keywords, kw_res = kw_res,
#                     ans = ans, media_file_types = media_file_types)
#     '''

# if __name__ == "__main__":
#     main()

import os

from stages.stage1_disk_imaging import run_dcfldd
from stages.stage2_extraction import analyze_disk_image
from stages.stage3_categorization import categorize_data
from stages.stage4_filtering import get_files_by_type
from stages.stage4_2_keyword import MasterFunc
from stages.stage4_2_keyword import mount_and_extract_files
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

    # Stage 4: File type filtering
    print("\n📂 Proceeding to Filtering...")
    file_types_input = input("Enter file types (comma-separated, e.g., .pdf, .png): ").strip()
    file_types = [ft.strip() for ft in file_types_input.split(",") if ft.strip()]
    matching_files = {}

    if not file_types:
        print("No file types selected.")
    else:
        matching_files = get_files_by_type(disk_image, categorized_output['current'], file_types)
        if matching_files:
            print("\n📁 Matching files found:")
            for ext, files in matching_files.items():
                print(f'.{ext} Files')
                for f in files:
                    print(f)
                print()
        else:
            print("No files found with the specified extensions.")

    # Stage 4.2: Keyword Filtering from Text Files
    keywords_input = input("Enter Keywords (comma-separated, e.g.: Lorem, Ipsum, dolor): ").strip()
    keywords = [kw.strip().lower() for kw in keywords_input.split(",") if kw.strip()]
    keyword_results = {}

    if not keywords:
        print("No keywords selected.")
    else:
        image_name = os.path.basename(disk_image)
        image_stem = os.path.splitext(image_name)[0]
        output_dir = input("Enter Output Directory (e.g.: ./output_files/extracted_files): ").strip()
        output_dir = os.path.join(output_dir, image_stem)
        keyword_results = MasterFunc(disk_image, keywords, output_dir, start_sector)

    # Stage 4.3: Media Extraction
    extract_media = input("Do you want to extract media (images, videos, audios)? (y/n): ").strip().lower()
    if extract_media == 'y':
        media_output_dir = input("Enter Output Directory (e.g.: ./output_files/extracted_files): ").strip()
        media_output_dir = os.path.join(media_output_dir, os.path.splitext(os.path.basename(disk_image))[0])
        media_types_input = input("Enter File Types (comma-separated, e.g.: .png, .mp4, .mp3): ").strip()
        media_types = [ft.strip() for ft in media_types_input.split(",") if ft.strip()]
        if not media_types:
            media_types = ['.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mp3']
        mount_and_extract_files(disk_image, media_output_dir, start_sector, media_types)

    # Stage 5: Report Generation
    print("\n📝 Generating PDF report...")
    filtered_only = input("Do you want to include only filtered data in the report? (y/n): ").strip().lower() == 'y'

    generate_report(
        disk_image_path=disk_image,
        categorized_output=categorized_output,
        filtered_output=matching_files if filtered_only else None,
        keyword_hits=keyword_results if filtered_only else None,
        filtered_only=filtered_only,
        include_metadata=True
    )


if __name__ == "__main__":
    main()
