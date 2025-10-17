import os

def valid_path(path: str) -> str:
    """Ensure the path has no spaces and is not empty."""
    while True:
        if " " in path:
            print("❌ Paths cannot contain spaces. Please enter a valid path.")
            path = input("Enter the root directory (no spaces, default: ./Data): ").strip() or "Data"
        elif path == "":
            path = "Data"
        else:
            return path

def create_structure(base_path, structure):
    """Recursively create folders according to nested dict."""
    for name, sub in structure.items():
        folder_path = os.path.join(base_path, name)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(sub, dict):
            create_structure(folder_path, sub)

if __name__ == "__main__":
    # --- Root folder prompt ---
    root = input("Enter the root directory for your Data folder (default: ./Data): ").strip() or "Data"
    root = valid_path(root)
    os.makedirs(root, exist_ok=True)

    # --- Ask about Business project split ---
    split_choice = input("Split Business Projects into Design and Manufacturing? (y/n, default: n): ").strip().lower()
    split_projects = split_choice == "y"

    BASE_STRUCTURE = {
        "Personal": {
            "Projects": {"Archive": {}},
            "Documents": {},
            "Photos": {},
            "Media": {},
            "Reference": {},
        },
        "Business": {
            "Projects": {"Design": {}, "Manufacturing": {}} if split_projects else {"All_Projects": {}},
            "Admin": {"Contracts": {}, "Invoices": {}, "HR": {}, "Templates": {}, "Notes": {}},
            "Marketing": {"Branding": {}, "SocialMedia": {}, "Presentations": {}, "Sales_and_Service": {}},
            "Reference": {"Standards": {}, "Research": {}, "Vendor_Info": {}},
            "IT": {},
            "Facility": {},
        },
    }

    create_structure(root, BASE_STRUCTURE)
    print(f"\n✅ Folder structure created under: {os.path.abspath(root)}")
