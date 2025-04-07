import subprocess
import re
from shutil import disk_usage


def get_files_by_type(image_path, offset, file_types):
    # Run fls command
    fls_command = f"fls -o {offset} {image_path}"
    result = subprocess.run(fls_command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error running fls:", result.stderr)
        return []

    files = result.stdout.splitlines()
    filtered_files = {}
    # Convert file types to lowercase and strip spaces
    file_types = {ft.strip().lower() for ft in file_types}
    for type in file_types:
        extension = type.lower().rsplit('.', 1)[-1] if '.' in type else ''
        filtered_files[extension] = []

    # Regex to extract filenames
    file_pattern = re.compile(r':\t(.+)$')  # Captures everything after the tab

    for line in files:
        match = file_pattern.search(line)
        if match:
            filename = match.group(1)
            extension = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
            print(f'filename: {filename}, \t ext: {extension}')

            if f".{extension}" in file_types:
                list_of_files = filtered_files[extension]
                list_of_files.append(filename)
                filtered_files[extension] = list_of_files

    return filtered_files
