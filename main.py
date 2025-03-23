from stages.stage1_disk_imaging import run_dcfldd
from stages.stage3_extraction import analyze_disk_image

def main():
    print("Disk Forensics Tool - CLI Version")

    # Stage 1: Disk Imaging
    disk_image = run_dcfldd()
    if not disk_image:
        print("Disk imaging failed or cancelled. Exiting...")
        return

    print(f"Disk imaging completed. Output file: {disk_image}")

    # Stage 2: Data Storage and Indexing

    # Stage 3: Analyze Disk Image
    print("\nProceeding to disk image analysis...")
    analyze_disk_image(disk_image)

    # Stage 3.1: Categorization


if __name__ == "__main__":
    main()