"""
    get experiment by query
"""
import logging
import json
import simplejson
import azure.functions as func
import pandas as pd
import numpy as np
from services.common_service import by_query, save_logs, get_categorical_features
from auth_middleware import requires_auth
from services.datalake_connection import download_file_from_directory
from services.filereaders import get_data
from services.nst_model import get_defaults


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    get experiment by query
    """
    try:
        logging.info('Python HTTP trigger function processed a request.')
        response = requires_auth(req.headers)

        if response['code'] == 401:
            return func.HttpResponse(json.dumps(response), status_code=401)
        type = req.params.get('type')
        query_text = req.params.get('q')
        limit_num = req.params.get('limit')
        page = req.params.get('p')
        others = {}
        if not type:
            return func.HttpResponse(
                simplejson.dumps(
                    {"error": 'Please pass type in the query parameters'}),
                status_code=400
            )

        if type == 'Opportunity Propensity':
            # data = download_file_from_directory(
            #     'Ml_service', 'Finance_Final.csv')
            # data_1 = pd.read_csv('local_files/Finance_Final.csv')
            # data_2 = pd.read_json(
            #     'local_files/Seller_Narrative_Output_File_Original.json')
            # # data = pd.merge(data_1, data_2, left_on='opty_id',
            # #                 right_on='Opportunity ID')
            # data = pd.DataFrame({"opty_id": np.intersect1d(
            #     data_1['opty_id'], data_2['Opportunity ID'])})
            # data['opty_id'] = data['opty_id'].astype(str)
            data = get_data(
                'local_files/opty/Seller_Narrative_Output_File_Original.json', 'json')
            data['opty_id'] = data['Opportunity ID'].astype(str)
            if query_text:
                # data['opty_id'] = data['Opportunity ID'].astype(str)
                # opty_ids = list(data[
                #                 data['opty_id'].str.contains(f"{query_text}")])
                opty_ids = list(data[data['opty_id'].str.contains(
                    f"{query_text}")]['opty_id'].unique())
                # opty_ids = opty_ids[:int(limit_num) if limit_num else 20]
            else:
                opty_ids = list(data['opty_id'].unique())
        elif type == 'NST':
            data = get_defaults()
            return func.HttpResponse(simplejson.dumps(data, indent=4, sort_keys=True, default=str, ignore_nan=True),
                                     headers={
                                         "content-type": "application/json",
                                         "Access-Control-Allow-Origin": "*"
            })
        elif type == 'Risk Recommender':
            data = get_data(
                'local_files/risk_recommender/Open_Deals_Resource_Grain_FY22.csv', 'csv')
            data['Deal ID'] = data['DealId']
            data = data[~data['Deal ID'].isna()]
            if query_text:
                data['Deal ID'] = data['Deal ID'].astype(str)
                opty_ids = list(data[data['Deal ID'].str.contains(
                    f"{query_text}")]['Deal ID'].unique())
            else:
                opty_ids = list(data['Deal ID'].unique())
                # df_ = data.select_dtypes(include=['object'])
                # if req.params.get('drop_down'):
                #     drop_down = {}
                #     for col in df_.columns:
                #         try:
                #             drop_down[col] = list(
                #                 data[data[col].notna()][col].unique()
                #             )
                #         except Exception as e:
                #             logging.info(e)
                #             pass
                #     others['drop_down'] = drop_down

        elif type == 'Risk Assessment':
            data = get_data('local_files/risk/Risk_Data_Modelling_CP.csv', 'csv')
            # data = download_file_from_directory(
            #     'RiskAssessment', 'Risk_Data_Modelling.csv')
            data = data[~data['Deal ID'].isna()]
            data = data[data['Agreement Setup Completed Date'] > '2018-07-01']
            data = data[~data['Output'].isna()]
            if query_text:
                data['Deal ID'] = data['Deal ID'].astype(str)
                opty_ids = list(data[data['Deal ID'].str.contains(
                    f"{query_text}")]['Deal ID'].unique())
                # opty_ids = opty_ids[:int(limit_num) if limit_num else 20]
            else:
                opty_ids = list(data['Deal ID'].unique())
                all_features_cols = get_categorical_features()
                data = data[all_features_cols]
                df_ = data.select_dtypes(include=['object'])
                if req.params.get('drop_down'):
                    drop_down = {}
                    for col in df_.columns:
                        try:
                            drop_down[col] = list(
                                data[data[col].notna()][col].unique()
                            )
                        except Exception as e:
                            logging.info(e)
                            pass
                    others['drop_down'] = drop_down
        else:
            return func.HttpResponse(
                simplejson.dumps(
                    {"error": 'Please pass a valid type in the query parameters'}),
                status_code=400
            )


        if page:
            opty_ids = opty_ids[int(page) * 50:int(page) * 50 + 50]
        else:
            opty_ids = opty_ids[0: 50]

        output = simplejson.dumps({
            "opty_ids": opty_ids, **others
        }, indent=4, sort_keys=True, default=str, ignore_nan=True)

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
