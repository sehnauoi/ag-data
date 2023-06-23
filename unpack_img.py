import os
import UnityPy
from tqdm import tqdm
import asyncio
import shutil

version_file = 'version.txt'

with open(version_file, 'r') as file:
    version = file.read().strip()

#######################

keywords = [
    "assets/abresources/textures/activity/banner",
    "assets/abresources/textures/announcements/activity",
    "assets/abresources/textures/character/icon",
    "assets/abresources/textures/character/portrait",
    "assets/abresources/textures/equip/portrait",
    # "assets/abresources/textures/item",
    "assets/abresources/textures/loading",
    "assets/abresources/textures/weaponservant",
    "assets/abresources/textures/weaponui/btn"
]

async def process_file(file_path, destination_folder):
    try:
        env = UnityPy.load(file_path)
        for path,obj in env.container.items():
            if any(keyword in path for keyword in keywords):
                if obj.type.name in ["Texture2D", "Sprite"]:
                    data = obj.read()
                    dest = os.path.join(destination_folder, *path.split("/"))
                    dest = dest.replace("assets/abresources/textures/", "")
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    dest, ext = os.path.splitext(dest)
                    dest = dest + ".png"

                    if "@jp" in dest or "@fr" in dest or "@de" in dest:
                        continue

                    print(f"{dest.replace('/workspaces/ag-data/extract/', '')}")
                    data.image.save(dest)

    except:
        pass

async def process_files(source_folder, destination_folder):
    for root, dirs, files in os.walk(source_folder):
        tasks = []
        for file_name in files:
            file_path = os.path.join(root, file_name)
            task = asyncio.create_task(process_file(file_path, destination_folder))
            tasks.append(task)
        await asyncio.gather(*tasks)

def unpack_img_assets(source_folder: str, destination_folder: str):
    asyncio.run(process_files(source_folder, destination_folder))

source = '/workspaces/ag-data/resource'
destination_img = f'/workspaces/ag-data/extract/{version}'
# unpack_img_assets(source, destination_img)

def move_folder(source, destination):
    updated_path = source.replace("/banner", "").replace("/portrait", "")

    shutil.rmtree(updated_path)


# Move the "activity/banner" folder
move_folder(f"/workspaces/ag-data/extract/{version}/activity/banner", f"/workspaces/ag-data/extract/{version}/event_banner")

# Move the "equip/portrait" folder
move_folder(f"/workspaces/ag-data/extract/{version}/equip/portrait", f"/workspaces/ag-data/extract/{version}/sigil")

def rename_folders(old_names, new_names):
    if len(old_names) != len(new_names):
        print("Error: Number of old names and new names should be the same.")
        return
    
    for old_name, new_name in zip(old_names, new_names):
        try:
            os.rename(old_name, new_name)
            print(f"Folder '{old_name}' renamed to '{new_name}' successfully!")
        except OSError:
            print(f"Folder renaming failed for '{old_name}' to '{new_name}'.")

# Example usage
old_folder_names = ["/workspaces/ag-data/extract/279_88/weaponservant", "/workspaces/ag-data/extract/279_88/weaponui", "/workspaces/ag-data/extract/279_88/character"]
new_folder_names = ["/workspaces/ag-data/extract/279_88/functor", "/workspaces/ag-data/extract/279_88/functor_scan", "/workspaces/ag-data/extract/279_88/modifier"]
rename_folders(old_folder_names, new_folder_names)