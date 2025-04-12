import subprocess
import os

fls_output = ""

def run_command(command):
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        return None


def categorize_data(image_path, start_sector):
    """
    Categorizes deleted, encrypted, current, and hidden data from the disk image.
    """
    if not os.path.exists(image_path):
        print(f"Error: Disk image '{image_path}' not found.")
        return None

    print(f"\nUsing Disk Image: {image_path}")
    print("\n--- Categorizing Data ---")

    results = {}

    # Deleted files
    print("\n--- Deleted Files ---")
    deleted_files = run_command(f"fls -o {start_sector} -r -p {image_path} -d")
    results['deleted'] = deleted_files
    print(deleted_files if deleted_files else "No deleted files found.")

    # Encrypted files
    print("\n--- Encrypted Files ---")
    encrypted_files = run_command(f"binwalk -E -J -N {image_path}")
    results['encrypted'] = encrypted_files
    print(encrypted_files if encrypted_files else "No encrypted data found.")

    # Current files
    print("\n--- Current Files ---")
    current_files = run_command(f"fls -o {start_sector} -r -p {image_path}")
    results['current'] = current_files
    print("-------------/nTYPE: ", type(current_files))
    print(current_files if current_files else "No current files found.")

    # Hidden files
    print("\n--- Hidden Files ---")
    hidden_files = run_command(f"fls -o {start_sector} -r -p {image_path} | grep '\\.'")
    results['hidden'] = hidden_files
    print(hidden_files if hidden_files else "No hidden files found.")
    
    return results


# For testing categorization module independently
if __name__ == "__main__":
    image_path = input("Enter disk image path: ").strip()
    start_sector = input("Enter start sector: ").strip()
    if image_path and start_sector:
        categorize_data(image_path, start_sector)
    else:
        print("Missing image path or start sector. Exiting.")
