import asyncio
import aiohttp
from alive_progress import alive_bar
import json
import requests
import time

"""
Todo

-change the get_hash() file_path to api from game
"""
def get_hash():
    file_path = "/workspaces/ag-data/assethash.bytes"

    with open(file_path, "r") as file:
        data = json.load(file)

    asset_hash_list = []
    for item in data["assetHashList"]:
        asset_hash = item.split("|")[1]
        asset_hash_list.append(asset_hash)

    return asset_hash_list

async def download_file(session, file_url, file_path):
    async with session.get(file_url) as response:
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            while True:
                chunk = await response.content.read(8192)
                if not chunk:
                    break
                file.write(chunk)
    return file_path

async def download_hash(hashes):
    download_directory = '/workspaces/ag-data/resource'
    base_url = 'https://static.aethergazer.com/android/resources/'

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        tasks = []
        for hash in hashes:
            file_url = base_url + hash + '.ys'
            file_name = hash + '.ys'
            file_path = download_directory + '/' + file_name
            tasks.append(download_file(session, file_url, file_path))

        with alive_bar(len(hashes), bar='smooth', spinner='twirls') as bar:
            print("Downloading hashes")
            i = 1
            for task in asyncio.as_completed(tasks):
                file_path = await task

                if i == len(hashes):
                    print(f"Download finished")
                    # break
                else:
                    # print(f"Downloaded: {file_path}")
                    i += 1

                bar()

def get_hash_2():

    url = input("Input URL: ")

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        versions = []
        for item in data['data']:
            version = item['version']
            versions.append(version)

        combined_versions = '_'.join(reversed(versions))
        url = f'https://static.aethergazer.com/android/resources/assethash_{combined_versions}.bytes'
        save_path = "/workspaces/ag-data/assethash.bytes"

        response = requests.get(url)

        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            print("File downloaded and saved successfully.")
        
            with open("version.txt", "w") as file:
                file.write(combined_versions)
                
        else:
            print("Failed to download the file.")

    else:
        print("Request failed with status code:", response.status_code)

    return

get_hash_2()
hashes = get_hash()
asyncio.run(download_hash(hashes))