import os

def create_structure(base_path, structure):
    for name, sub in structure.items():
        folder_path = os.path.join(base_path, name)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(sub, dict):
            create_structure(folder_path, sub)

if __name__ == "__main__":
    root = input("Enter the root directory for your Data folder (default: ./Data): ").strip() or "Data"
    os.makedirs(root, exist_ok=True)

    # Ask the user whether to split projects
    split_projects_input = input("Do you want to split Business Projects into Design and Manufacturing? (y/n, default: n): ").strip().lower()
    split_projects = split_projects_input == "y"

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
