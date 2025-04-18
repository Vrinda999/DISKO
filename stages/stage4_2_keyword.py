import os
import subprocess
from stages.stage2_extraction import run_command

def mount_and_extract_text_files(image_path, output_dir, start_sector):
    file_types = ['.txt', '.pdf', '.doc', '.docx']

    image_name = os.path.basename(image_path)
    mount_dir = './output_files/mnt/forensics_mount'
    partition_dir = './output_files/mnt/forensics_partition'
    ewf_mount_point = '/mnt/ewf_mount'

    os.makedirs(mount_dir, exist_ok=True)
    os.makedirs(partition_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    try:
        if image_path.lower().endswith('.e01'):
            os.makedirs(ewf_mount_point, exist_ok=True)
            # Mount the E01
            run_command(f"sudo ewfmount {image_path} {ewf_mount_point}")
            image_path = os.path.join(ewf_mount_point, 'ewf1')
        

        print(f"{"-"*100}\nMMLS START SECTOR!!! = {start_sector}\n\n")

        # Mount the partition using offset
        offset = int(start_sector) * 512
        run_command(f"sudo mount -o loop,ro,offset={offset} {image_path} {mount_dir}")

        # Copy text files
        for root, dirs, files in os.walk(mount_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in file_types):
                    source_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_path, mount_dir)
                    dest_path = os.path.join(output_dir, relative_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    print(f'Copying Files Now. Root: {root}, \nDirs: {dirs}, \nfile: {file}\n\n')
                    print(f"src path: {source_path}, \nrel path: {relative_path}, \nDest Path: {dest_path}\n\n")
                    try:
                        cp_cmd = f'sudo cp "{source_path}" "{dest_path}"'
                        run_command(cp_cmd)
                    except subprocess.CalledProcessError:
                        print(f"[!] Failed to copy: {source_path}")

    finally:
        # Cleanup: unmount everything
        run_command(f'sudo umount "{mount_dir}"')
        run_command(f'sudo umount "{ewf_mount_point}"')


# if __name__ == "__main__":
#     image_path='TEST.E01'
#     output_dir='./output_files/extracted_files'

#     image_name = os.path.basename(image_path)
#     image_stem = os.path.splitext(image_name)[0]
#     output_dir = os.path.join(output_dir, image_stem)

#     start_sector = analyze_disk_image(image_path)

#     mount_and_extract_text_files(image_path, output_dir, start_sector)
