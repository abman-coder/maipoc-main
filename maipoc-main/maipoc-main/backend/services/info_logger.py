from datetime import datetime, timedelta
import logging
import os
from azure.storage.filedatalake.aio import DataLakeFileClient, FileSystemClient
import asyncio
from io import StringIO
import pathlib
import json
import pandas as pd

account_name = os.environ["accountname"]
accountKey = os.environ["accountkey"]
containerName = os.environ["containername"]
account_url = f"https://{account_name}.dfs.core.windows.net"
SOURCE_FILE = 'local_files/logs.txt'


async def write_to_datalake():
    logging.info("Writing to datalake")
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M") + ".json"
    file_client = DataLakeFileClient(account_url=account_url, credential=accountKey,
                                     file_system_name=containerName, file_path='Logs/'+filename)
    with open(SOURCE_FILE, "r") as data:
        parsed_data = "[" + data.read().replace("}\n{", "},{") + "]"
        await file_client.upload_data(data=parsed_data, overwrite=True)
        await file_client.close()
        data.close()
        try:
            os.remove(SOURCE_FILE)
        except Exception as e:
            print(e)
            pass
    # file_client = file_system_client.get_file_client("myfile")
    # await file_client.create_file()
    # with open(SOURCE_FILE, "rb") as data:
    #     length = data.tell()
    #     await file_client.append_data(data, 0)
    #     await file_client.flush_data(length)


async def delete_old_files():
    try:
        logging.info("Deleting old files")
        file_system_client = FileSystemClient(
            account_url=account_url, credential=accountKey, file_system_name=containerName, file_path='Logs/')
        logging.info("Deleting old files1")
        async for file in file_system_client.get_paths():
            if file.name.startswith("Logs/") and file.name.endswith(".json"):
                if (datetime.now() - file.last_modified) > timedelta(days=7):
                    logging.info(file.name)
                    logging.info(file.last_modified)
                    fileClient = DataLakeFileClient(account_url=account_url, credential=accountKey,
                                                    file_system_name=containerName, file_path=file.name)
                    await fileClient.delete_file()
                    await fileClient.close()
                    # file_client = file_system_client.get_file_client(file.name)
                    # file_client.delete_file()
        await file_system_client.close()
    except Exception as e:
        print(e)


async def write_to_local(data):
    with open(SOURCE_FILE, "a") as f:
        logging.info("Writing to local")
        f.write(data)
        f.write("\n")
        f.close()
    # print(os.path.getsize(SOURCE_FILE))
    if os.path.getsize(SOURCE_FILE) > 109000:
        loop = asyncio.get_event_loop()
        # tsk =
        loop.create_task(write_to_datalake())
        loop.create_task(delete_old_files())
        # loop.run_until_complete(tsk)
        # await write_to_datalake()


async def write_data_to_datalake(dir, data, id):
    logging.info("Writing to datalake")
    filename = f"{id}_output.json"
    file_client = DataLakeFileClient(account_url=account_url, credential=accountKey,
                                     file_system_name=containerName, file_path=dir+"/"+filename)
    await file_client.upload_data(data=data, overwrite=True)
    await file_client.close()
    data.close()
    try:
        os.remove(SOURCE_FILE)
    except Exception as e:
        print(e)
        pass


async def save_to_datalake(dir, data, id):
    loop = asyncio.get_event_loop()
    loop.create_task(write_data_to_datalake(dir, data, id))


async def download_from_datalake(dir, file_name, type_of='csv', download_path=None, encoding=None):
    logging.info("downloading from datalake")
    file_client = DataLakeFileClient(account_url=account_url, credential=accountKey,
                                     file_system_name=containerName, file_path=dir+"/"+file_name)
    download = await file_client.download_file()
    downloaded_bytes = await download.readall()
    if download_path:
        pathlib.Path("/".join(download_path.split("/")
                     [:-1])).mkdir(parents=True, exist_ok=True)

        local_file = open(download_path, 'wb')
        local_file.write(downloaded_bytes)
        local_file.close()
        await file_client.close()
        return "success"

    s = str(downloaded_bytes, 'utf-8')

    data = StringIO(s)
    await file_client.close()

    if type_of == 'csv':
        if encoding:
            return pd.read_csv(data, encoding=encoding)
        return pd.read_csv(data)
    elif type_of == 'json':
        return pd.read_json(data)
    elif type_of == 'dict':
        return json.loads(s)

    return pd.read_csv(data)


async def download_from_datalake_async(dir, file_name, type_of='csv', download_path=None, encoding=None):
    # loop = asyncio.get_event_loop()
    # loop.create_task(download_from_datalake(
    #     dir, file_name, type_of=type_of, download_path=download_path, encoding=encoding))

    data = await download_from_datalake(
        dir, file_name, type_of=type_of, download_path=download_path, encoding=encoding)
    return data
