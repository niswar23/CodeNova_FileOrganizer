import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# File categories
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Media": [".mp3", ".wav", ".mp4", ".mkv", ".avi", ".mov"],
    "Code": [".py", ".html", ".css", ".js", ".java", ".cpp", ".c", ".sql"]
}

LOG_FILE = "organizer.log"


def get_category(file_path):
    extension = file_path.suffix.lower()

    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    if not destination.exists():
        return destination

    folder = destination.parent
    name = destination.stem
    extension = destination.suffix
    number = 1

    while True:
        new_path = folder / f"{name}_{number}{extension}"

        if not new_path.exists():
            return new_path

        number += 1


def write_log(message):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{message}\n"
            )
    except OSError as error:
        print(f"Warning: Could not write log: {error}")


def organized_files(source, target, dry_run):
    source = Path(source).resolve()
    target = Path(target).resolve()

    if not source.is_dir():
        print("Error: The source directory does not exist.")
        return

    if source == target or source in target.parents:
        print("Error: The target must not be the source directory or a folder inside it.")
        return

    if target.exists() and target in source.parents:
        print("Error: The target cannot be a parent of the source directory.")
        return

    if target.exists() and not target.is_dir():
        print("Error: The target path is not a directory.")
        return

    if not dry_run:
        try:
            target.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            print(f"Error creating target directory: {error}")
            return

    print("\nDRY-RUN PREVIEW" if dry_run else "\nORGANIZING FILES")
    print("-" * 45)

    moved = 0
    skipped = 0
    errors = 0

    try:
        for item in source.iterdir():
            if not item.is_file():
                if item.is_dir():
                    print(f"Skipping subdirectory: {item.name}")
                    skipped += 1
                continue

            category = get_category(item)
            category_folder = target / category
            destination = get_unique_path(category_folder / item.name)

            if dry_run:
                print(f"Would move: {item.name}")
                print(f"       To: {category}/{destination.name}")
                write_log(
                    f"DRY-RUN: {item} -> {destination}"
                )
                moved += 1
                continue

            try:
                category_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(destination))

                print(f"Moved: {item.name} -> {category}/{destination.name}")
                write_log(f"MOVED: {item} -> {destination}")
                moved += 1

            except (OSError, shutil.Error) as error:
                print(f"Could not move {item.name}: {error}")
                write_log(f"ERROR moving {item}: {error}")
                errors += 1

    except OSError as error:
        print(f"Could not read the source directory: {error}")
        write_log(f"ERROR reading source directory: {error}")
        return

    print("-" * 45)
    print(f"Files processed: {moved}")
    print(f"Items skipped: {skipped}")
    print(f"Errors: {errors}")
    print("Preview only: no files were moved." if dry_run else "Organization finished.")


def main():
    parser = argparse.ArgumentParser(
        description="Organize files by their extensions."
    )

    parser.add_argument(
        "source",
        help="Path to the folder containing files"
    )

    parser.add_argument(
        "target",
        help="Path to the folder for organized files"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview file movements without changing files"
    )

    args = parser.parse_args()

    organized_files(args.source, args.target, args.dry_run)


if __name__ == "__main__":
    main()

