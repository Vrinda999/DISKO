from stages.stage1_disk_imaging import run_dcfldd

def main():
    print("Disk Forensics Tool - CLI Version")

    # Stage 1: Disk Imaging
    disk_image = run_dcfldd()
    if not disk_image:
        print("Disk imaging failed or cancelled. Exiting...")
        return

    print(f"Disk imaging completed. Output file: {disk_image}")

    # stage 2: Data Storage and Indexing


if __name__ == "__main__":
    main()