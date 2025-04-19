import os
import re
import subprocess
from utils.run_command import run_command

def mount_and_extract_text_files(image_path, output_dir, start_sector, file_types = None):
    if not file_types:
        file_types = ['.txt', '.pdf', '.doc', '.docx']
    
    img_file_type = "dd"

    mount_dir = './output_files/mnt/forensics_mount'
    partition_dir = './output_files/mnt/forensics_partition'
    ewf_mount_point = '/mnt/ewf_mount'

    os.makedirs(mount_dir, exist_ok=True)
    os.makedirs(partition_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    try:
        if image_path.lower().endswith('.e01'):
            img_file_type = "e01"
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
        if img_file_type == "e01":
            run_command(f'sudo umount "{ewf_mount_point}"')



def search_keywords_in_txt_files(txt_files, keywords):
    """Searches for keywords in extracted .txt files"""
    keyword_found = False
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
                        keyword_found = True
                        flag=1
                if flag == 1:
                    results[keyword] = res

        except Exception as e:
            print(f"Error reading {file_path}: {e}")


    if keyword_found:
        # for kw, found_list in results.items():
        #     print(f"\n{"--"*60}\nKeyword: {kw} -->")

        #     if isinstance(found_list, str) or (len(found_list) == 1 and isinstance(found_list[0], str)):
        #         print(f"{found_list[0]}\n")
        #         continue

        #     else:
        #         for file, sent in found_list:
        #             print(f"- {file}: {sent}\n")
        print("Keyword(s) Found!")
        return results

    else:
        print(f"Keyword(s) Not Present.")
        return "Keyword(s) Not Present."


def search_keywords_in_pdf_files(pdf_files, keywords):
    keyword_found = False
    keyword_matches = {kw:['nil'] for kw in keywords}

    for pdf in pdf_files:
        pdf_lower = pdf.lower()
        filename = os.path.basename(pdf)

        for keyword in keywords:
            # if keyword exists in filename
            res = []
            flag = 0
            if keyword in filename.lower():
                res.append((pdf, f"[Filename Match:] {filename}"))
                keyword_found = True
                flag=1
                continue

            try:
                # Run pdfgrep to get lines with matches
                result = run_command(f'sudo pdfgrep -i -n -C 1 "{keyword}" "{pdf}"')
                if result:
                    lines = result.split('\n')
                    for line in lines:
                        # Extract just the sentence part (skip line numbers)
                        match = re.search(r"\d+:.*", line)
                        if match:
                            cleaned_line = re.sub(r'^\s*\d+:\s*', '', line)
                            res.append((pdf, cleaned_line))
                            keyword_found = True
                            flag=1
            except Exception as e:
                if e.endswith("2."):
                    print(f"Error reading {pdf}: {e}")

            if flag == 1:
                keyword_matches[keyword] = res
    
    if keyword_found:
        print("Keyword(s) Found!")
        return keyword_matches
    else:
        print(f"Keyword(s) Not Present.")
        return "Keyword(s) Not Present."


def get_file_paths(folder_path, ext):
    txt_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(ext):
                txt_files.append(os.path.join(root, file))
    return txt_files


def MasterFunc(image_path, keywords, output_dir, start_sector, file_types = None):
    mount_and_extract_text_files(image_path, output_dir, start_sector, file_types)
    txt_paths = get_file_paths(output_dir, ".txt")
    pdf_paths = get_file_paths(output_dir, ".pdf")

    print(f'\nTXT Paths: {txt_paths}, \nPDF Paths: {pdf_paths}\n\n')

    # doc_paths = get_file_paths(output_dir, ".doc")
    # res = get_file_paths(output_dir, ".docx")
    # doc_paths.append(res)

    result = {kw:[] for kw in keywords}
    
    res = search_keywords_in_txt_files(txt_paths, keywords)
    print(f"\n{"-"*120}\nTxt Res: {res}\n\n")
    if res != "Keyword(s) Not Present.":
        for kw in result.keys():
            if res[kw][0] != 'nil':
                result[kw] = res[kw]
    
    res = search_keywords_in_pdf_files(pdf_paths, keywords)
    print(f'\n{"-"*120}\nPDF Res: {res}\n\n')
    if res != "Keyword(s) Not Present.":
        for kw in result.keys():
            print(f'KW: {kw}, \nResult Keys: {result.keys()}, \nres: {res}\n\n')
            if res[kw][0] != 'nil':
                result[kw] += res[kw]
    print(f'Result: {result}')

    # res = search_keywords_in_doc_files(doc_paths, keywords)

    for kw, found_list in result.items():
        if found_list == []:
            result[kw] = ['Keyword Not Found']
    
    print(f'\n\nRsults: {result}')
    return result