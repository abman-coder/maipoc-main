# """
# Blob Helpers
# """
# import json
# import os
# import logging
# from tempfile import NamedTemporaryFile
# from azure.storage.blob import BlockBlobService, AppendBlobService
# from azure.storage.blob.baseblobservice import BaseBlobService
# import pandas as pd

# accountName = os.environ["BloBAccountName"]
# accountKey = os.environ["BloBAccountKey"]
# containerName = os.environ["BloBContainerName"]


# """
# # list all blobs in a specified container and directory
# """


# def get_all_files_from_container(dir_prefix):
#     """
#     which directory to list
#     """
#     if dir_prefix:
#         return BaseBlobService(account_name=accountName, account_key=accountKey
#                                ).list_blobs(containerName, prefix=dir_prefix)
#     return None


# def get_list_from_split_blob(url_to=None):
#     """
#     url to get list from
#     """
#     try:
#         if url_to:
#             local_file = NamedTemporaryFile()
#             blob_service_client = BlockBlobService(
#                 account_name=accountName, account_key=accountKey)
#             blob_service_client.get_blob_to_stream(
#                 containerName, url_to, stream=local_file, max_connections=2)
#             local_file.seek(0)
#             d_f = json.loads(local_file.read().decode('utf-8'))
#             return d_f
#         return {}
#     except Exception as erro_e:
#         logging.info(erro_e)
#         return {}


# def del_blob(url):
#     """
#     # delete a blob based on its path
#     """
#     if url:
#         BaseBlobService(account_name=accountName,
#                         account_key=accountKey).delete_blob(containerName, url)


# def save_list_into_blob(url, data):
#     """
#     # save data into blob on provided path
#     """
#     if(url and data):
#         blob_service_client = BlockBlobService(
#             account_name=accountName, account_key=accountKey)
#         try:
#             output = json.dumps(data)
#         except Exception as error_e:
#             logging.info(error_e)
#         try:
#             blob_service_client.create_blob_from_text(
#                 containerName, url, output)
#         except Exception as error_e:
#             logging.info(error_e)


# def get_df_from_split_blob(url=None):
#     """
#     # get data as a dataframe from blob based on provided path
#     """
#     try:
#         if url:
#             local_file = NamedTemporaryFile()
#             blob_service_client = BlockBlobService(
#                 account_name=accountName, account_key=accountKey)
#             blob_service_client.get_blob_to_stream(
#                 containerName, url, stream=local_file, max_connections=2)
#             local_file.seek(0)
#             d_f = pd.read_csv(local_file)
#             return d_f, False
#     except Exception as error_e:
#         logging.info(error_e)
#         return pd.DataFrame([]), error_e


# def save_into_blob(directory, dataframe, filename, container=None):
#     """
#     # save data frame into blob as a csv, on provided path
#     """
#     if filename:
#         file_path = directory+"/"+filename
#         blob_service_client = BlockBlobService(
#             account_name=accountName, account_key=accountKey)
#         try:
#             output = dataframe.to_csv(encoding="utf-8", index=False)
#         except Exception as error_e:
#             logging.info(error_e)
#         try:
#             blob_service_client.create_blob_from_text(
#                 container if container else containerName, file_path, output)
#         except Exception as error_e:
#             logging.info(error_e)


# def append_into_blob(directory, dataframe, filename):
#     """
#     # append data into blob as a csv
#     """
#     if filename:
#         file_path = directory+"/"+filename
#         blob_service_client = AppendBlobService(
#             account_name=accountName, account_key=accountKey)
#         try:
#             output = dataframe.to_csv(
#                 encoding="utf-8", header=False, index=False)
#         except Exception:
#             pass
#         try:
#             blob_service_client.append_blob_from_text(
#                 containerName, file_path, output)
#         except Exception:
#             pass
