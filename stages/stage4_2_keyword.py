import os
import re
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
                    # print(f'Copying Files Now. Root: {root}, \nDirs: {dirs}, \nfile: {file}\n\n')
                    # print(f"src path: {source_path}, \nrel path: {relative_path}, \nDest Path: {dest_path}\n\n")
                    try:
                        cp_cmd = f'sudo cp "{source_path}" "{dest_path}"'
                        run_command(cp_cmd)
                    except subprocess.CalledProcessError:
                        print(f"[!] Failed to copy: {source_path}")

    finally:
        # Cleanup: unmount everything
        run_command(f'sudo umount "{mount_dir}"')
        run_command(f'sudo umount "{ewf_mount_point}"')



def search_keywords_in_txt_files(txt_files, keywords):
    """Searches for keywords in extracted .txt files"""
    keyword_found = 0
    keywords = [kw.strip().lower() for kw in keywords]
    results = {kw:['nil'] for kw in keywords}

    for file_path in txt_files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', content)
            
            for keyword in keywords:
                res = []
                flag=0
                for sentence in sentences:
                    if keyword in sentence.lower():
                        res.append((file_path, sentence.strip()))
                        keyword_found += 1
                        flag=1
                if flag == 1:
                    results[keyword] = res

        except Exception as e:
            print(f"Error reading {file_path}: {e}")


    if keyword_found > 0:
        for kw, found_list in results.items():
            print(f"\n{"--"*60}\nKeyword: {kw} -->")

            if isinstance(found_list, str) or (len(found_list) == 1 and isinstance(found_list[0], str)):
                print(f"{found_list[0]}\n")
                continue

            else:
                for file, sent in found_list:
                    print(f"- {file}: {sent}\n")
        return results

    else:
        print(f"Keyword(s) Not Present.")
        return "Keyword(s) Not Present."


def get_txt_file_paths(folder_path):
    txt_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files



def MasterFunc(image_path, keywords, output_dir, start_sector):
    mount_and_extract_text_files(image_path, output_dir, start_sector)
    txt_paths = get_txt_file_paths(output_dir)
    
    txt_res = search_keywords_in_txt_files(txt_paths, keywords)
    print(txt_res)
    return txt_res



# if __name__ == "__main__":
#     image_path='bootcamp.E01'
#     output_dir='./output_files/extracted_files'

#     image_name = os.path.basename(image_path)
#     image_stem = os.path.splitext(image_name)[0]
#     output_dir = os.path.join(output_dir, image_stem)

#     start_sector = analyze_disk_image(image_path)
#     keywords = ['inDUStry', 'Chomu', 'Infancy']
#     # keywords = input("Enter Keywords (comma-separated, e.g.: Lorem, Ipsum, dolor): ").split(",")
#     MasterFunc(image_path, keywords, output_dir, start_sector)