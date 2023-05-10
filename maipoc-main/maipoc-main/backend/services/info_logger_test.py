from datetime import datetime, timedelta
import logging
import os
from azure.storage.filedatalake.aio import DataLakeFileClient, FileSystemClient
# import asyncio

account_name = os.environ["accountname"]
accountKey = os.environ["accountkey"]
containerName = os.environ["containername"]
account_url = f"https://{account_name}.dfs.core.windows.net"
SOURCE_FILE = 'local_files/logs.txt'


def write_to_datalake():
    logging.info("Writing to datalake")
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M") + ".json"
    file_client = DataLakeFileClient(account_url=account_url, credential=accountKey,
                                     file_system_name=containerName, file_path='Logs/'+filename)
    with open(SOURCE_FILE, "r") as data:
        parsed_data = "[" + data.read().replace("}\n{", "},{") + "]"
        file_client.upload_data(data=parsed_data, overwrite=True)
        file_client.close()
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


def delete_old_files():
    try:
        logging.info("Deleting old files")
        file_system_client = FileSystemClient(
            account_url=account_url, credential=accountKey, file_system_name=containerName, file_path='Logs/')
        logging.info("Deleting old files1")
        for file in file_system_client.get_paths():
            if file.name.startswith("Logs/") and file.name.endswith(".json"):
                if (datetime.now() - file.last_modified) > timedelta(days=7):
                    logging.info(file.name)
                    logging.info(file.last_modified)
                    fileClient = DataLakeFileClient(account_url=account_url, credential=accountKey,
                                                    file_system_name=containerName, file_path=file.name)
                    fileClient.delete_file()
                    fileClient.close()
                    # file_client = file_system_client.get_file_client(file.name)
                    # file_client.delete_file()
        file_system_client.close()
    except Exception as e:
        print(e)


def write_to_local(data):
    return "Success"
    with open(SOURCE_FILE, "a") as f:
        logging.info("Writing to local")
        f.write(data)
        f.write("\n")
        f.close()
    # print(os.path.getsize(SOURCE_FILE))
    if os.path.getsize(SOURCE_FILE) > 109000:
        # loop = io.get_event_loop()
        # # tsk =
        # loop.create_task(write_to_datalake())
        # loop.create_task(delete_old_files())
        # loop.run_until_complete(tsk)
        write_to_datalake()
        delete_old_files()
        # await write_to_datalake()
