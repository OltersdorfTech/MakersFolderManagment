import os
import re
import csv
import platform
import subprocess
import sys
from datetime import datetime

# --------------------- Templates ---------------------
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

# --------------------- Helpers ---------------------
def valid_path(path: str) -> str:
    """Ensure the path has no spaces and is not empty."""
    while True:
        if " " in path:
            print("❌ Paths cannot contain spaces.")
            path = input("Enter the base 'Data' folder path (no spaces, default: ./Data): ").strip() or "Data"
        elif path == "":
            path = "Data"
        else:
            return path

def create_structure(base_path, structure):
    """Recursively create folder structure."""
    for name, sub in structure.items():
        folder_path = os.path.join(base_path, name)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(sub, dict):
            create_structure(folder_path, sub)

def next_project_number(projects_path, identifier):
    """Generate next sequential project number."""
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
    """Append to CSV and keep it sorted."""
    ensure_csv(csv_path)
    rows = []
    with open(csv_path, "r", newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            rows.append(row)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows.append([category.capitalize(), project_name, os.path.abspath(project_path), timestamp])
    rows.sort(key=lambda x: (x[0].lower(), x[1].lower()))
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def open_folder(path):
    """Open folder cross-platform."""
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        print(f"⚠️  Could not open folder: {e}")

def get_business_projects_path(root):
    """Return correct Business/Projects path."""
    projects_root = os.path.join(root, "Business", "Projects")
    design_path = os.path.join(projects_root, "Design")
    mfg_path = os.path.join(projects_root, "Manufacturing")

    # Split mode check
    if os.path.exists(design_path) and os.path.exists(mfg_path):
        choice = ""
        while choice not in ["design", "manufacturing"]:
            choice = input("Business projects are split. Choose folder ('Design' or 'Manufacturing'): ").strip().lower()
        return design_path if choice == "design" else mfg_path

    # Otherwise, use the base Projects folder directly
    os.makedirs(projects_root, exist_ok=True)
    return projects_root

# --------------------- Main Logic ---------------------
def add_project():
    root = input("Enter the base 'Data' folder path (default: ./Data): ").strip() or "Data"
    root = valid_path(root)

    category = ""
    while category not in ["personal", "business"]:
        category = input("Project category ('personal' or 'business'): ").strip().lower()

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

    if category == "business":
        projects_root = get_business_projects_path(root)
    else:
        projects_root = os.path.join(root, "Personal", "Projects")

    # Determine next available project number
    next_num = next_project_number(projects_root, identifier)
    project_name = f"{identifier}_{next_num:04d}_{code_name}"

    # Create folders
    template = PERSONAL_PROJECT_TEMPLATE if category == "personal" else BUSINESS_PROJECT_TEMPLATE
    project_path = os.path.join(projects_root, project_name)
    os.makedirs(project_path, exist_ok=True)
    create_structure(project_path, template)

    # Create README.md
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# {project_name}\n\n")
        f.write(f"**Category:** {category.capitalize()}\n\n")
        f.write(f"**Path:** {os.path.abspath(project_path)}\n\n")
        f.write("## Notes\n\nDescribe the project purpose, goals, and relevant context here.\n")

    print(f"\n✅ Created new {category} project:")
    print(f"📁 {os.path.abspath(project_path)}")
    print("🗒️  README.md added inside project folder")

    # Update CSV index
    csv_path = os.path.join(root, "project_index", "projects.csv")
    update_csv(csv_path, category, project_name, project_path)
    print(f"📊 Project added to index: {os.path.abspath(csv_path)}")

    # Offer to open project folder
    open_choice = input("\nOpen this project folder now? (y/n): ").strip().lower()
    if open_choice == "y":
        open_folder(project_path)

def main():
    try:
        while True:
            add_project()
            again = input("\nWould you like to create another project? (y/n): ").strip().lower()
            if again != "y":
                print("\n👋 Done. Exiting project setup tool.")
                break
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        input("\nPress Enter to exit...")  # Keeps window open when double-clicked

if __name__ == "__main__":
    main()
