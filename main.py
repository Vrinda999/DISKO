from stages.stage1_disk_imaging import run_dcfldd

def main():
    print("Disk Forensics Tool - CLI Version")

    # stage 1: Disk Imaging
    disk_image = run_dcfldd()
    if not disk_image:
        print("Disk imaging failed or cancelled. Exiting...")
        return

    # stage 2: Data Storage and Indexing