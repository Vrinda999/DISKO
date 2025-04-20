# Disko
## Steps to use
1. Insert pendrive.
2. To check the location at which it's inserted: sudo fdisk -l
3. Go to script folder and run main.py: sudo python3 main.py
4. Currently this setting is working:
    ![image](https://github.com/user-attachments/assets/dda4dbe6-0d3c-4c0d-a2ed-788b66e45d1a)

The image will be generated in the specified folder (e.g.: `./output_files`).

## 🧪 Disk Forensics Tool - CLI Based

A _unified_ command-line tool for performing Disk Forensics, including disk Imaging, Partition Extraction, data categorization, Keyword Filtering and PDF Report generation.

---

### ⚙️ Features
- Perform disk imaging using `dcfldd`
- Analyze partitions using `mmls` and `fsstat`
- Categorize files (deleted, encrypted, current, hidden)
- Filter files from extensions
- Find Keywords from `.txt`, `.pdf`, and `.docx` files
- Generate forensic reports in PDF format

---

### 📁 Project Structure
```
disk-forensics-tool/
├── main.py                         # Entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Helper Document
├── setup.sh                        # Installation script
├── output_files/                   # Disk images, reports
│   ├── extracted_files/            # Files Extracted from the Image
│   ├── mnt/                        # Images are Mounted here for extraction
│   ├── reports/                    # Generated PDF reports
├── stages/                         # Modular scripts
│   ├── stage1_disk_imaging.py
│   ├── stage2_extraction.py
│   ├── stage3_categorization.py
│   ├── stage4_filtering.py
│   ├── stage4.2_keyword.py
│   └── stage5_reporting.py
│   └── template.html
├── utils/                      # Helper functions
│   └── run_command.py          # Run shell commands
└── .venv/                      # Virtual environment
```

---

### 🚀 Quick Start

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/disk-forensics-tool.git
cd disk-forensics-tool
```

#### 2. Run Setup (Installs Tools + Python Packages)
```bash
chmod +x setup.sh
./setup.sh
pip install -r -requirements.txt
```

#### 3. Start the Tool
```bash
source .venv/bin/activate
python main.py
```

---

### 🛠️ Dependencies
#### System Tools (Installed via `setup.sh`)
- `dcfldd`
- `sleuthkit` (for `mmls`, `fls`, `fsstat`)
- `binwalk`
- `grep` and `pdfgrep`

#### Python Packages
- `fpdf`
- `elasticsearch`
- `docx2txt`
- `re`

---

### 📄 Output
- Disk images saved in `./output_files/`
- PDF reports saved in `./output_files/reports/`
- Extracted files saved in `./output_files/<disk_image_name>/`
  - e.g.: for `image.dd`, output directory will be `./output_files/image/`

---

### 📬 Future Work
- [ ] Elasticsearch indexing
- [ ] GUI version with Tkinter or web interface

---

### 👤 Author
Simmi Thapad   
Vrinda Abrol

---

### 🔒 Disclaimer
> [!Important]
> This tool is intended for **educational and lawful forensic analysis** only. Use responsibly.

