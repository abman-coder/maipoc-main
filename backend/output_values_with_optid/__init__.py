"""
    get experiment by query
"""
from datetime import datetime
import logging
import json
import azure.functions as func
import simplejson
import pandas as pd
from services.common_service import by_query, save_logs
from auth_middleware import requires_auth
from services.datalake_connection import download_file_from_directory
from services.risk_model_rescore import re_score
from services.opt_model_rescore import opt_re_score
from services.nst_model import nst_re_score
from services.risk_recommender_rescore import re_score_recommender
from services.info_logger import write_to_local, save_to_datalake
import time


async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    get experiment by query
    """
    try:
        logging.info('Python HTTP trigger function processed a request.')
        response = requires_auth(req.headers)
        req_body = req.get_json()

        if "type" not in req_body:
            return func.HttpResponse(
                simplejson.dumps(
                    {"error": 'Please pass type in the request body'}),
                status_code=400
            )

        if req_body['type'] == 'NST':
            if "data" not in req_body:
                return func.HttpResponse(
                    simplejson.dumps(
                        {"error": 'Please pass data in the request body'}),
                    status_code=400
                )
            if "NST Type" not in req_body['data'] and "NST Group" not in req_body['data']:
                return func.HttpResponse(
                    simplejson.dumps(
                        {"error": 'Please pass both NST Type and NST Group in the request body'}),
                    status_code=400
                )
            # if 'nst' not in response['roles']:
            #     return func.HttpResponse(json.dumps({"message": "You don't have permission to access this data"}), status_code=401)

            try:
                re_score_otput = nst_re_score(
                    req_body['data'])
                output = simplejson.dumps({
                    "score_output": re_score_otput,
                    "timestamp": str(datetime.now()).split(".")[0],
                    "received": True
                }, indent=4, sort_keys=True, default=str, ignore_nan=True)
            except Exception as error_e:
                return func.HttpResponse(
                    json.dumps({"error": str(error_e)}),
                    status_code=400
                )

            return func.HttpResponse(output,
                                     headers={
                                         "content-type": "application/json",
                                         "Access-Control-Allow-Origin": "*"
                                     })
        elif req_body['type'] == 'Risk Recommender':
            if "deal_id" not in req_body and "opty_id" not in req_body:
                return func.HttpResponse(
                    simplejson.dumps(
                        {"error": 'Please pass deal_id in the request body'}),
                    status_code=400
                )
            deal_id = req_body['deal_id'] if "deal_id" in req_body else req_body['opty_id']
            if "opt_id" not in req_body:
                req_body['opty_id'] = deal_id
            try:
                re_score_otput = re_score_recommender(req_body['data'])
                re_score_otput = re_score_otput if re_score_otput else []
            except Exception as error_e:
                return func.HttpResponse(
                    json.dumps({"error": str(error_e)}),
                    status_code=400
                )
            try:
                await write_to_local(simplejson.dumps({
                    "id": deal_id,
                    "time": int(time.time()),
                    "type": "Deal Assessment",
                    "score": re_score_otput[0]['Score'],
                    "label": re_score_otput[0]['Label'],
                    "user": response['user name'],
                    "modified": req_body['data'],
                }, indent=4, sort_keys=True, default=str, ignore_nan=True))
            except Exception as e:
                logging.info(e)
                pass
            output = simplejson.dumps({
                "score_output": re_score_otput,
                "timestamp": str(datetime.now()).split(".")[0],
                "received": True
            }, indent=4, sort_keys=True, default=str, ignore_nan=True)

            return func.HttpResponse(output,
                                     headers={
                                         "content-type": "application/json",
                                         "Access-Control-Allow-Origin": "*"
                                     })

        if (response['code'] == 401) or ('roles' not in response):
            return func.HttpResponse(json.dumps(response), status_code=401)
        if req_body['type'] == 'Opportunity Propensity':
            if "opty_id" not in req_body:
                return func.HttpResponse(
                    simplejson.dumps(
                        {"error": 'Please pass opty_id in the request body'}),
                    status_code=400
                )
            # data = pd.read_json('local_files/Seller_Narrative_Output_File_ch.json')
            # data = download_file_from_directory(
            #     'Ml_service', 'Output_Final/Output_Final/Seller_Narrative_Output_File.csv', type_of='json')

            # print(data)

            if 'o' not in response['roles']:
                return func.HttpResponse(json.dumps({"message": "You don't have permission to access this data"}), status_code=401)

            try:
                re_score_otput = opt_re_score(
                    req_body['data'], req_body['opty_id'], req_body["source"] if "source" in req_body else None)
            except Exception as error_e:
                return func.HttpResponse(
                    json.dumps({"error": str(error_e)}),
                    status_code=400
                )
            logging.info(re_score_otput)
            if re_score_otput.empty:
                return func.HttpResponse(
                    json.dumps(
                        {"error": "No data found, Please verify Opportunity id and other details"}),
                    status_code=400
                )
            trs_score = re_score_otput['Won'].values[0]
            trs_label = re_score_otput['Prop_Bucket'].values[0]
            re_score_otput_trs = [{
                "Won": trs_score,
                "OpportunityID": req_body['opty_id'],
                "Prop_Bucket": trs_label,
                "Action": list(re_score_otput['Action'])
            }]
            output = simplejson.dumps({
                "score_output": re_score_otput_trs,
                "timestamp": str(datetime.now()).split(".")[0],
                "received": True
            }, indent=4, sort_keys=True, default=str, ignore_nan=True)
            try:
                await save_to_datalake('Ml_service', output, req_body['opty_id'])
                await write_to_local(simplejson.dumps({
                    "type": "Opportunity Propensity",
                    "id": req_body['opty_id'],
                    "time": int(time.time()),
                    "score": trs_score,
                    "label": trs_label,
                    "user": response['user name'],
                    "modified": req_body['data'],
                }, indent=4, sort_keys=True, default=str, ignore_nan=True))
            except Exception as e:
                logging.info(e)
                pass

            # opty_rows = data[data['Opportunity ID'] == req_body['opty_id']]
            # opty_rows = data[data['Action'] != "No Action"]
            # opty_rows = opty_rows.sort_values(['Average'], ascending=False)
            # opty_rows = opty_rows[:5]
            # opty_rows['id'] = range(1, len(opty_rows) + 1)
            # opty_rows = opty_rows.to_dict('records')

            # output = simplejson.dumps({
            #     "opty_rows": opty_rows[0:1000]
            # }, indent=4, sort_keys=True, default=str, ignore_nan=True)
        # elif req_body['type'] == 'NST':
        #     # if 'nst' not in response['roles']:
        #     #     return func.HttpResponse(json.dumps({"message": "You don't have permission to access this data"}), status_code=401)

        #     re_score_otput = nst_re_score(
        #         req_body['data'])
        #     try:
        #         await write_to_local(simplejson.dumps({
        #             "type": "Opportunity Propensity",
        #             "id": req_body['opty_id'],
        #             "time": int(time.time()),
        #             "score": re_score_otput[0]['Won'],
        #             "label": re_score_otput[0]['Prop_Bucket'],
        #             "user": response['user name'],
        #             "modified": req_body['data'],
        #         }, indent=4, sort_keys=True, default=str, ignore_nan=True))
        #     except Exception as e:
        #         logging.info(e)
        #         pass
        #     output = simplejson.dumps({
        #         "score_output": re_score_otput,
        #         "received": True
        #     }, indent=4, sort_keys=True, default=str, ignore_nan=True)
        elif req_body['type'] == 'Risk Assessment':
            if 'r' not in response['roles']:
                return func.HttpResponse(json.dumps({"message": "You don't have permission to access this data"}), status_code=401)
            if "deal_id" not in req_body and "opty_id" not in req_body:
                return func.HttpResponse(
                    simplejson.dumps(
                        {"error": 'Please pass deal_id in the request body'}),
                    status_code=400
                )
            deal_id = req_body['deal_id'] if "deal_id" in req_body else req_body['opty_id']
            if "opt_id" not in req_body:
                req_body['opty_id'] = deal_id
            try:
                re_score_otput = re_score(req_body['data'])
            except Exception as error_e:
                return func.HttpResponse(
                    json.dumps({"error": str(error_e)}),
                    status_code=400
                )
            # simplejson.loads(re_score_otput)
            # re_score_otput = (
            #     re_score_otput[['Score', 'Label']]).to_dict('records')
            re_score_otput = re_score_otput.to_dict('records')
            re_score_otput = re_score_otput if re_score_otput else []
            try:
                await write_to_local(simplejson.dumps({
                    "id": deal_id,
                    "time": int(time.time()),
                    "type": "Deal Assessment",
                    "score": re_score_otput[0]['Score'],
                    "label": re_score_otput[0]['Label'],
                    "user": response['user name'],
                    "modified": req_body['data'],
                }, indent=4, sort_keys=True, default=str, ignore_nan=True))
            except Exception as e:
                logging.info(e)
                pass
            output = simplejson.dumps({
                "score_output": re_score_otput,
                "timestamp": str(datetime.now()).split(".")[0],
                "received": True
            }, indent=4, sort_keys=True, default=str, ignore_nan=True)

        else:
            return func.HttpResponse(
                simplejson.dumps(
                    {"error": 'Please pass a valid type in the body'}),
                status_code=400
            )
        return func.HttpResponse(output,
                                 headers={
                                     "content-type": "application/json",
                                     "Access-Control-Allow-Origin": "*"
                                 })
    except Exception as error_e:
        logging.exception(error_e)
        return func.HttpResponse(
            json.dumps({"error": str(error_e)}),
            status_code=400
        )
