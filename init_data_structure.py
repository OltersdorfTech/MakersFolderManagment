import os

BASE_STRUCTURE = {
    "Personal": {
        "Projects": {"Archive": {}},
        "Documents": {},
        "Photos": {},
        "Media": {},
        "Reference": {},
    },
    "Business": {
        "Projects": {"Archive": {}},
        "Admin": {"Contracts": {}, "Invoices": {}, "HR": {}, "Templates": {}},
        "Marketing": {"Branding": {}, "SocialMedia": {}, "Presentations": {}},
        "Reference": {"Standards": {}, "Research": {}, "Vendor_Info": {}},
    },
}

def create_structure(base_path, structure):
    for name, sub in structure.items():
        folder_path = os.path.join(base_path, name)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(sub, dict):
            create_structure(folder_path, sub)

if __name__ == "__main__":
    root = input("Enter the root directory for your Data folder (default: ./Data): ").strip() or "Data"
    os.makedirs(root, exist_ok=True)
    create_structure(root, BASE_STRUCTURE)
    print(f"\n✅ Folder structure created under: {os.path.abspath(root)}")
