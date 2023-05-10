"""
    save a new experiment into the database
"""
import datetime
import logging
import json
import azure.functions as func
from auth_middleware import requires_auth
from services.common_service import add_, by_query
# from services.blob_helpers import save_list_into_blob
from services.datalake_connection import download_file_from_directory
from services.synapse_connection import run_job


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    save a new experiment into the database
    """
    logging.info('Python HTTP trigger function processed a request.')
    response = requires_auth(req.headers)
    if (response['code'] == 401) or ('roles' not in response):
        return func.HttpResponse(json.dumps(response), status_code=401)
    access = {"data": response}
    try:
        # type = req.params.get('type')
        # file_data = download_file_from_directory(
        #     'Service', 'users.json', 'dict')
        access = response['roles'] if 'roles' in response else []
        # file_data[response['user name']
        #                    ] if response['user name'] in file_data else []
        # print(file_data)
    except Exception as e:
        return func.HttpResponse(json.dumps({
            "error": str(e),
        }), status_code=400)

    # save_list_into_blob("ScopeDirectory/"+req_body["ExperimentId"], scopes)

    return func.HttpResponse(json.dumps({"message": "Success", "access": access}), headers={"content-type": "application/json"})
