import os
import UnityPy
import json
import asyncio

async def process_asset(file_path, destination_folder):
    env = UnityPy.load(file_path)
    for path, obj in env.container.items():
        for obj in env.objects:
            try:
                if obj.type.name == "TextAsset":
                    data = obj.read()
                    dest = os.path.join(destination_folder, *path.split("/"))
                    dest, ext = os.path.splitext(dest)
                    if "/assets/luabuilds/luajit2.0/x64/game/config/story" in dest:
                        continue
                    if "/assets/luabuilds/luajit2.0/x64/game/config" in dest:
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        print(dest)
                        with open(dest, "wb") as f:
                            f.write(bytes(data.script))
                        if obj.serialized_type.nodes:
                            tree = obj.read_typetree()
                            fp = os.path.join(dest, f"{tree['m_Name']}.json")
                            with open(fp, "wt", encoding="utf8") as f:
                                json.dump(tree, f, ensure_ascii=False, indent=4)
                        else:
                            data = obj.read()
                            fp = os.path.join(dest, f"{data.name}.bin")
                            with open(fp, "wb") as f:
                                f.write(data.raw_data)
            except:
                continue

async def unpack_all_assets(source_folder: str, destination_folder: str):
    tasks = []
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            task = process_asset(file_path, destination_folder)
            tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(unpack_all_assets('/workspaces/ag-data/resource', '/workspaces/ag-data/extract'))
