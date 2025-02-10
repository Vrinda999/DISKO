import subprocess

def run_command(command):
    """Helper function to execute a command and return its output"""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        return None


def analyze_disk_image(image_path):
    """Extracts partition info and file metadata using The Sleuth Kit"""

    print("\n--- Partition Table Information ---")
    mmls_output = run_command(f"mmls {image_path}")
    if mmls_output:
        print(mmls_output)
        print(f"Type of Output = {type(mmls_output)}")

    print("\n--- File System Information ---")
    fsstat_output = run_command(f"fsstat -o 0000000032 {image_path}")
    if fsstat_output:
        print(fsstat_output)

    print("\n--- Listing Root Directory Files ---")
    fls_output = run_command(f"fls -r -o 0000000032 {image_path}")
    if fls_output:
        print(fls_output)



def extract_file(image_path, inode, output_file):
    """Extracts a file from a disk image using icat"""
    command = f"icat {image_path} {inode} > {output_file}"
    run_command(command)
    print(f"Extracted file saved as {output_file}")


# Example usage:
img = input("Enter Image Source Path (/home/vrinda/Desktop/TEST/TEST.E01): ")
analyze_disk_image(img)
# extract_file(img, 5, "recovered_file.txt")