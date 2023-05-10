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
from services.datalake_connection import write_data_to_datalake
from services.synapse_connection import run_job


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    save a new experiment into the database
    """
    logging.info('Python HTTP trigger function processed a request.')
    response = requires_auth(req.headers)
    if response['code'] == 401:
        return func.HttpResponse(json.dumps(response), status_code=401)
    try:
        req_body = req.get_json()
        write_data_to_datalake(
            json.dumps(req_body['data']), 'Ml_service', 'Input_Final', req_body['id'])
        run_job('Pipeline 1', {
            "fileName": req_body['id']
        })
    except ValueError:
        pass

    # save_list_into_blob("ScopeDirectory/"+req_body["ExperimentId"], scopes)

    return func.HttpResponse(json.dumps({"message": "Success"}), headers={"content-type": "application/json"})
