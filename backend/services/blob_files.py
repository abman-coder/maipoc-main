# """
# blob file upload and download
# """
# import os
# from tempfile import NamedTemporaryFile
# from datetime import datetime, timedelta
# from azure.storage.blob import BlockBlobService
# from azure.storage.blob.baseblobservice import BaseBlobService

# account_name = os.environ["BloBAccountName"]
# accountKey = os.environ["BloBAccountKey"]
# containerName = os.environ["BloBContainerName"]
# main_container_name = (os.environ["BloBMainContainerName"]
#                        if "BloBMainContainerName" in os.environ else None)


# def generate_sas_with_sdk():
#     """
#     # Writing Data in Blob Storage
#     """
#     ctnr = main_container_name if main_container_name else containerName
#     sas_url = BaseBlobService(account_name=account_name,
#                               account_key=accountKey).generate_container_shared_access_signature(ctnr,
#                                                                                                  permission='rwdl', expiry=datetime.now() +
#                                                                                                  timedelta(hours=10), start=datetime.now() + timedelta(days=-1), protocol='https,http')
#     return {
#         "saas_url": sas_url,
#         "sass_prefix": f"https://{account_name}.blob.core.windows.net/?",
#         "account": account_name,
#         "container": ctnr,
#     }


# def azure_upload_df(container, dataframe, filename):
#     """
#     Upload DataFrame to Azure Blob Storage for given container
#     Keyword arguments:
#     container -- the container name (default None)
#     dataframe -- the dataframe(df) object (default None)
#     filename -- the filename to use for the blob (default None)

#     GroupSplitValidationResults -- it is the name of default folder
#         inside which we need to add new blob file on blob storage.
#     """
#     if filename:
#         file_path = "GroupSplitValidationResults/"+filename
#         blob_service_client = BlockBlobService(
#             account_name=account_name, account_key=accountKey)
#         try:
#             # converting dataframe to csv  which is required to upload file
#             # using create_blob_from_text method
#             output = dataframe.to_csv(index_label="index", encoding="utf-8")
#         except Exception:
#             print(container)
#         try:
#             blob_service_client.create_blob_from_text(
#                 containerName, file_path, output)
#             # Return the full file path of uploaded blob file
#             return "https://" + account_name + \
#                 ".blob.core.windows.net/"+containerName+"/"+file_path
#         except Exception:
#             pass

# # update Data in Blob Storage


# def azure_update_blob(container, dataframe, filename):
#     """
#     Upload DataFrame to Azure Blob Storage for given container
#     Keyword arguments:
#     container -- the container name (default None)
#     dataframe -- the dataframe(df) object (default None)
#     filename -- the filename to use for the blob (default None)

#     GroupSplitValidationResults -- it is the name of default folder inside
#         which we need to add new blob file on blob storage.
#     """
#     if filename:
#         file_path = "GroupSplitValidationResults/"+filename
#         blob_service_client = BlockBlobService(
#             account_name=account_name, account_key=accountKey)
#         try:
#             # converting dataframe to csv  which is required to upload file
#             # using create_blob_from_text method
#             output = dataframe.to_csv(index=False, encoding="utf-8")
#         except Exception:
#             print(container)
#         try:
#             blob_service_client.create_blob_from_text(
#                 containerName, file_path, output)
#             # Return the full file path of uploaded blob file
#             return "https://"+account_name + \
#                 ".blob.core.windows.net/"+containerName+"/"+file_path
#         except Exception:
#             pass

# # Download blob file from Blob Storage


# def azure_download_blob(req_body):
#     """
#     Download dataframe from Azure Blob Storage for given url
#     Keyword arguments:
#     url -- the url of the blob (default None)
#     eg: download_file
#     ("https://<account_name>.blob.core.windows.net/<container_name>/<blob_name>")

#     We are using temporary file name to store download file in cache and
#     delete the file automatically when this function is completed.
#     """
#     url = req_body["TestSplitFileLocation"]
#     if url:
#         download_dir = "GroupSplitValidationResults"
#         blob_name = "experimentDesignResult_ExpId_" + \
#             str(req_body["ExperimentId"])+".txt"
#         local_file = NamedTemporaryFile()
#         block_blob_service = BlockBlobService(
#             account_name=account_name, account_key=accountKey)
#         block_blob_service.get_blob_to_stream(
#             containerName, download_dir+"/"+blob_name, stream=local_file,
#             max_connections=2)
#         local_file.seek(0)
#         return local_file
