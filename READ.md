
# Automated File Organizer #

## Overview
This project is a Python program that organizes files into folders according to their file extensions. It was developed as part of the CodeNova Python Programming Internship.

## Features
- Organizes files into Images, Documents, Archives, Media, Code and Others.
- Accepts source and destination directories through command-line arguments.
- Includes a dry-run mode to preview file movements.
- Renames duplicate files to prevent overwriting.
- Skips subdirectories.
- Handles invalid directories and file-operation errors.
- Records operations in a log file.

## Technologies Used
- Python 3
- pathlib
- os
- shutil
- argparse
- datetime

All modules used by the program are included with Python, so no additional packages are required.

## Requirements
Install Python 3 and ensure it is available from the terminal.

## How to Run

Open a terminal in the project directory.

Preview the planned movements:

```bash
python FileOrganizer.py TestFiles organized_files --dry-run
```

Organize the files:

```bash
python FileOrganizer.py TestFiles organized_files
```

Display command-line help:

```bash
python FileOrganizer.py --help
```

On Windows, use `py` instead of `python` if that is the command configured on your computer.

## Category Rules
- Images: JPG, JPEG, PNG, GIF, BMP, WEBP
- Documents: PDF, DOC, DOCX, TXT, PPT, PPTX, XLS, XLSX, CSV
- Archives: ZIP, RAR, 7Z, TAR, GZ
- Media: MP3, WAV, MP4, MKV, AVI, MOV
- Code: PY, HTML, CSS, JS, JAVA, CPP, C, SQL
- Others: Extensions not included in the categories above

## Safety Measures
- Dry-run mode previews changes without moving files.
- Duplicate filenames are renamed instead of overwritten.
- The program skips subdirectories and does not recursively process their contents.
- Testing should be performed on sample files before using important folders.
- File-operation errors are reported and recorded where possible.

## Testing
The program was tested using sample files with different extensions. Dry-run output was compared with actual file movements. Duplicate filenames, invalid source paths and command-line help were also tested.

## Limitations
- The program processes files directly inside the selected source directory, not files inside nested subdirectories.
- Files with unknown extensions are placed in the Others folder.
- Actual movements may fail when files are locked or access permissions are insufficient.
