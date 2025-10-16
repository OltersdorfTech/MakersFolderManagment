import os
import re
import csv
import platform
import subprocess
from datetime import datetime

# Folder templates
PERSONAL_PROJECT_TEMPLATE = {
    "CAD": {"Mechanical": {}, "Electrical": {}},
    "Code": {},
    "Docs": {},
    "Images": {},
    "Media": {},
    "Notes": {},
}

BUSINESS_PROJECT_TEMPLATE = {
    "CAD": {"Mechanical": {}, "Electrical": {}},
    "Code": {},
    "Docs": {},
    "Images": {},
    "Reports": {},
    "Finance": {},
    "Deliverables": {},
    "Requirements": {},
    "Schedule": {},
}

def create_structure(base_path, structure):
    """Recursively create folders according to a nested dictionary."""
    for name, sub in structure.items():
        folder_path = os.path.join(base_path, name)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(sub, dict):
            create_structure(folder_path, sub)

def next_project_number(projects_path, identifier):
    """Find next sequential project number for a given customer or category."""
    if not os.path.exists(projects_path):
        return 1
    pattern = re.compile(rf"^{re.escape(identifier)}_(\d{{4}})_", re.IGNORECASE)
    numbers = []
    for entry in os.listdir(projects_path):
        match = pattern.match(entry)
        if match:
            try:
                numbers.append(int(match.group(1)))
            except ValueError:
                pass
    return max(numbers, default=0) + 1

def ensure_csv(csv_path):
    """Create CSV file with headers if missing."""
    if not os.path.exists(csv_path):
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        with open(csv_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "ProjectName", "Path", "Timestamp"])

def update_csv(csv_path, category, project_name, project_path):
    """Add entry and sort CSV alphabetically."""
    ensure_csv(csv_path)
    rows = []

    # Read existing entries
    with open(csv_path, "r", newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            rows.append(row)

    # Add new entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows.append([category.capitalize(), project_name, os.path.abspath(project_path), timestamp])

    # Sort alphabetically by Category then ProjectName
    rows.sort(key=lambda x: (x[0].lower(), x[1].lower()))

    # Write back
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def open_folder(path):
    """Open a folder cross-platform."""
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        print(f"⚠️  Could not open folder: {e}")

def add_project():
    root = input("Enter the base 'Data' folder path (default: ./Data): ").strip() or "Data"

    category = ""
    while category not in ["personal", "business"]:
        category = input("Project category ('personal' or 'business'): ").strip().lower()

    # Handle identifier differently for personal vs business
    if category == "business":
        identifier = input("Enter the customer or client name: ").strip().replace(" ", "_")
        if not identifier:
            print("❌ Customer name cannot be empty.")
            return
    else:
        print("Example categories: Home_Upgrade, Landscape, Repair, Automotive")
        identifier = input("Enter your project category: ").strip().replace(" ", "_")
        if not identifier:
            print("❌ Category cannot be empty.")
            return

    code_name = input("Enter a short project code name or description: ").strip().replace(" ", "_")
    if not code_name:
        print("❌ Code name cannot be empty.")
        return

    projects_root = os.path.join(root, category.capitalize(), "Projects")
    next_num = next_project_number(projects_root, identifier)
    project_name = f"{identifier}_{next_num:04d}_{code_name}"

    template = PERSONAL_PROJECT_TEMPLATE if category == "personal" else BUSINESS_PROJECT_TEMPLATE
    project_path = os.path.join(projects_root, project_name)
    os.makedirs(project_path, exist_ok=True)
    create_structure(project_path, template)

    # Add README.md
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {project_name}\n\n")
        f.write(f"**Category:** {category.capitalize()}\n\n")
        f.write(f"**Path:** {os.path.abspath(project_path)}\n\n")
        f.write("## Notes\n\nDescribe the project purpose, goals, and any relevant context here.\n")

    print(f"\n✅ Created new {category} project:")
    print(f"📁 {os.path.abspath(project_path)}")
    print(f"🗒️  README.md added inside project folder")

    # Update master CSV index
    csv_path = os.path.join(root, "project_index", "projects.csv")
    update_csv(csv_path, category, project_name, project_path)
    print(f"📊 Project added to index: {os.path.abspath(csv_path)}")

    # Prompt to open folder
    open_choice = input("\nOpen this project folder now? (y/n): ").strip().lower()
    if open_choice == "y":
        open_folder(project_path)

def main():
    """Main loop allowing repeated project creation."""
    while True:
        add_project()
        again = input("\nWould you like to create another project? (y/n): ").strip().lower()
        if again != "y":
            print("\n👋 Done. Exiting project setup tool.")
            break

if __name__ == "__main__":
    main()
