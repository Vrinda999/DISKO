import os
import subprocess

def mount_and_extract_text_files(image_path, output_dir, file_types=None):
    if file_types is None:
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
            subprocess.run(['ewfmount', image_path, ewf_mount_point], check=True)
            image_path = os.path.join(ewf_mount_point, 'ewf1')
        
        # Find partition start sector using mmls
        mmls_output = subprocess.check_output(['mmls', image_path]).decode()
        for line in mmls_output.strip().split('\n'):
            if 'Linux' in line or 'NTFS' in line or 'FAT' in line:
                parts = line.split()
                start_sector = parts[2]
                break
        else:
            raise Exception("Couldn't find a valid partition in the image.")

        # Mount the partition using offset
        offset = int(start_sector) * 512
        subprocess.run(['mount', '-o', f'loop,ro,offset={offset}', image_path, mount_dir], check=True)

        # Copy text files
        for root, dirs, files in os.walk(mount_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in file_types):
                    source_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_path, mount_dir)
                    dest_path = os.path.join(output_dir, relative_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    print(f'Copying Files Now. Root: {root}, \nDirs: {dirs}, \nfile: {file}')
                    print(f"src path: {source_path}, \nrel path: {relative_path}, \nDest Path: {dest_path}")
                    try:
                        subprocess.run(['cp', source_path, dest_path], check=True)
                    except subprocess.CalledProcessError:
                        print(f"[!] Failed to copy: {source_path}")

    finally:
        # Cleanup: unmount everything
        subprocess.run(['umount', mount_dir], stderr=subprocess.DEVNULL)
        subprocess.run(['umount', ewf_mount_point], stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    mount_and_extract_text_files(
    image_path='bootcamp.E01',
    output_dir='./output_files/extracted_files',
    file_types=['.txt', '.pdf']
)
