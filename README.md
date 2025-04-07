# Steps to use
1. Insert pendrive.
2. To check the location at which it's inserted: sudo fdisk -l
3. Go to script folder and run main.py: sudo python3 main.py
4. Currently this setting is working:
    ![image](https://github.com/user-attachments/assets/dda4dbe6-0d3c-4c0d-a2ed-788b66e45d1a)

The image will be gerated in a folder.

# 🧪 Disk Forensics Tool - CLI Based

A command-line tool for performing disk forensics, including disk imaging, partition extraction, data categorization, and PDF report generation.

---

## ⚙️ Features
- Perform disk imaging using `dcfldd`
- Analyze partitions using `mmls` and `fsstat`
- Categorize files (deleted, encrypted, current, hidden)
- Generate forensic reports in PDF format

---

## 📁 Project Structure
```
disk-forensics-tool/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── setup.sh                     # Installation script
├── output_files/               # Disk images, reports
│   ├── reports/                # Generated PDF reports
├── stages/                      # Modular scripts
│   ├── stage1_disk_imaging.py
│   ├── stage2_extraction.py
│   ├── stage2.1_categorization.py
│   ├── stage4_indexing.py       # (on hold)
│   └── stage5_reporting.py
├── utils/                      # Helper functions (optional)
└── .venv/                      # Virtual environment
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/disk-forensics-tool.git
cd disk-forensics-tool
```

### 2. Run Setup (Installs Tools + Python Packages)
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Start the Tool
```bash
source .venv/bin/activate
python main.py
```

---

## 🛠️ Dependencies
### System Tools (Installed via `setup.sh`)
- `dcfldd`
- `sleuthkit` (for `mmls`, `fls`, `fsstat`)
- `binwalk`

### Python Packages
- `fpdf`
- `elasticsearch`

---

## 📄 Output
- Disk images saved in `output_files/`
- PDF reports saved in `output_files/reports/`

---

## 📬 Future Work
- Elasticsearch indexing in Stage 4 (currently on hold)
- GUI version with Tkinter or web interface

---

## 👤 Author
Simmi Thapad   
Vrinda Abrol

---

## 🔒 Disclaimer
This tool is intended for **educational and lawful forensic analysis** only. Use responsibly.

