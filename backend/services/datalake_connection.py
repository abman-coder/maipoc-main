import os
from tempfile import NamedTemporaryFile
from io import StringIO
import json
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient

account_name = os.environ["accountname"]
accountKey = os.environ["accountkey"]
containerName = os.environ["containername"]


def initialize_storage_account(storage_account_name, storage_account_key):

    try:
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
        # return service_client
        print('done 1')

    except Exception as e:
        print(e)


initialize_storage_account(account_name, accountKey)


def write_data_to_datalake(data, filesystem_name, dir_name, filename):

    file_path = f'{dir_name}/{filename}'

    file_system_client = service_client.get_file_system_client(
        file_system=containerName)

    directory_client = file_system_client.get_directory_client(
        filesystem_name)

    # local_file = open("C:/MSFT/mas/code/backend/services/test.csv", 'wb')

    # file_client = directory_client.get_file_client("Fin_features.csv")

    file_client = directory_client.get_file_client(file_path)

    # processed_df = df.to_parquet(index=False)

    file_client.upload_data(data=data, overwrite=True)

    file_client.close()

    return True


def download_file_from_directory(dir_name, file_name, type_of='csv', encoding=None, download_path=None):
    try:
        file_system_client = service_client.get_file_system_client(
            file_system=containerName)

        directory_client = file_system_client.get_directory_client(
            dir_name)

        # open("C:/MSFT/mas/code/backend/services/test.csv", 'wb')
        # local_file = NamedTemporaryFile()

        file_client = directory_client.get_file_client(file_name)

        download = file_client.download_file()

        downloaded_bytes = download.readall()

        if download_path:
            local_file = open(download_path, 'wb')
            local_file.write(downloaded_bytes)
            local_file.close()
            return ""

        s = str(downloaded_bytes, 'utf-8')

        data = StringIO(s)

        if type_of == 'csv':
            if encoding:
                return pd.read_csv(data, encoding=encoding)
            return pd.read_csv(data)
        elif type_of == 'json':
            return pd.read_json(data)
        elif type_of == 'dict':
            return json.loads(s)

        return pd.read_csv(data)

        # return pd.read_csv(downloaded_bytes)

        # local_file.close()
        # print('done 2')

    except Exception as e:
        print(e)
        return pd.DataFrame([])


# download_file_from_directory()
