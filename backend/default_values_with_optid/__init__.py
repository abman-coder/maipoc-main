"""
    get experiment by query
"""
import logging
import json
import azure.functions as func
import simplejson
import pandas as pd
# from services.common_service import by_query, save_logs
from auth_middleware import requires_auth
# from services.datalake_connection import download_file_from_directory
from services.filereaders import get_data
from services.nst_model import get_default_comments


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    get experiment by query
    """
    try:
        logging.info('Python HTTP trigger function processed a request.')
        response = requires_auth(req.headers)
        if response['code'] == 401:
            return func.HttpResponse(json.dumps(response), status_code=401)
        req_body = req.get_json()
        others = {}

        if "type" not in req_body:
            return func.HttpResponse(
                simplejson.dumps(
                    {"error": 'Please pass type in the request body'}),
                status_code=400
            )

        if req_body['type'] == 'Opportunity Propensity':
            if "opty_id" not in req_body:
                return func.HttpResponse(
                    simplejson.dumps(
                        {"error": 'Please pass opty_id in the request body'}),
                    status_code=400
                )
            data = get_data('local_files/opty/RiskReserveAddition.csv', 'csv')
            # data = download_file_from_directory('Ml_service', 'Finance_Final.csv')
            old_input = get_data(
                'local_files/opty/Seller_Narrative_Output_File_Original.json', 'json')
            # pd.read_json(
            #     'local_files/Seller_Narrative_Output_File_Original.json')
            # download_file_from_directory(
            #     'Ml_service', 'Output_Final/Seller_Narrative_Output_File_ch.json', type_of='json')
            if (not old_input.empty) and ('Prop_Bucket' in old_input) and old_input['Prop_Bucket'].values.any():
                old_input = old_input[old_input['Opportunity ID']
                                      == req_body['opty_id']]
                if not old_input.empty:
                    old_input_score = {
                        "Label": old_input['Prop_Bucket'].values[0],
                        "Score": old_input['Won'].values[0],
                    }
                    others["old_input_score"] = old_input_score
            opty_rows = data[(data['opty_id'] ==
                              req_body['opty_id']) & (data['ItemLevel'] == "Resource")]
            opty_rows = opty_rows.sort_values(
                ['pkg_id', 'ResourceTier'], ascending=True)
            if not opty_rows.empty and not ("source" in req_body and req_body["source"] == 'uitool'):
                opty_rows_dict = opty_rows.to_dict('records')
                opty_rows_output = {
                    "CpqHeaderInfo": {
                        "CRMOpportunityId": req_body['opty_id'],
                        "QuoteId": opty_rows_dict[0]['contract id'],
                        "IsGlobalDeal": False
                    },
                    "CpqQuoteDetails": {
                        "CpqPackages": []
                    }
                }
                CpqPackages = {}
                vals = ["A310 - Azure AD Application Integration",
                        "Dynamics 365 Standard Migration Assessment"]
                vals1 = ["Digi Security&Compl_Azure_Sec",
                         "Finance & Operations_D365_BA"]
                vals2 = ["SecA_Identity & Access", "BA_Assessments"]
                for value in opty_rows_dict:
                    if value['pkg_id'] not in CpqPackages:
                        CpqPackages[value['pkg_id']] = {
                            "Id": value['pkg_id'],
                            "CatalogName": vals.pop() if vals else "",
                            "Revenue": value['Revenue CCUS'],
                            "Discount": value['Discount CCUS'],
                            "PrimaryProductName": vals1.pop() if vals1 else "",
                            "BusinessScenarioName": vals2.pop() if vals2 else "",
                            "FeeArrangementType": value["FeeType"],
                            "Services": [
                                {
                                    "ParentItemId": value['pkg_id'],
                                    "Resources": [
                                        {
                                            "ParentItemId": value['pkg_id'],
                                            "CatalogItemName": value['ResourceTier'],
                                            "Quantity": 1
                                        }
                                    ]
                                }
                            ],
                            "Fundings": [
                                {
                                    "PackageId": value['pkg_id'],
                                    "Type": "End-Customer Investment Funds (ECIF)",
                                    "Revenue": value['ECIFCommitted']
                                },
                            ],
                            "Adjustments": [
                                {
                                    "PackageId": value['pkg_id'],
                                    "Type": "Risk Reserve",
                                    "Revenue": value['Risk Reserve CCUS']
                                },
                            ],
                            "AdditionalAttributes": {
                                "Tags": [
                                    "MSO"
                                ]
                            }
                        }
                    else:
                        CpqPackages[value['pkg_id']
                                    ]["Revenue"] += value['Revenue CCUS']
                        CpqPackages[value['pkg_id']
                                    ]["Discount"] += value['Discount CCUS']
                        CpqPackages[value['pkg_id']]["Services"].append(
                            {
                                "ParentItemId": value['pkg_id'],
                                "Resources": [
                                    {
                                        "ParentItemId": value['pkg_id'],
                                        "CatalogItemName": value['ResourceTier'],
                                        "Quantity": 1
                                    }
                                ]
                            }
                        )
                opty_rows_output["CpqQuoteDetails"]["CpqPackages"] = list(
                    CpqPackages.values())
                output = simplejson.dumps({
                    "opty_rows": [opty_rows_output], **others
                }, indent=4, sort_keys=True, default=str, ignore_nan=True)
                return func.HttpResponse(output,
                                         headers={
                                             "content-type": "application/json",
                                             "Access-Control-Allow-Origin": "*"
                                         })
        elif req_body['type'] == 'NST':
            if "NST Type" not in req_body or "NST Group" not in req_body:
                return func.HttpResponse(
                    json.dumps({"error": "NST Type and NST Group are required"}), status_code=400)
            data = get_default_comments(
                req_body['NST Type'], req_body['NST Group'], req_body['SubRegion'] if "SubRegion" in req_body else None)
            json_data = simplejson.dumps(
                data, indent=4, sort_keys=True, default=str, ignore_nan=True)
            return func.HttpResponse(json_data,
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
            data = get_data(
                'local_files/risk_recommender/Open_Deals_Resource_Grain_FY22.csv', 'csv')
            data['Deal ID'] = data['DealId'].astype(str)
            opty_rows = data[(data['Deal ID'] ==
                              deal_id)]
        elif req_body['type'] == 'Risk Assessment':
            if "deal_id" not in req_body and "opty_id" not in req_body:
                return func.HttpResponse(
                    simplejson.dumps(
                        {"error": 'Please pass deal_id in the request body'}),
                    status_code=400
                )
            deal_id = req_body['deal_id'] if "deal_id" in req_body else req_body['opty_id']
            data = get_data(
                'local_files/risk/Risk_Data_Modelling_CP.csv', 'csv')
            data['Deal ID'] = data['Deal ID'].astype(str)
            # data = download_file_from_directory(
            #     'RiskAssessment', 'Risk_Data_Modelling.csv')
            opty_rows = data[(data['Deal ID'] ==
                              deal_id)]

        # opty_rows = opty_rows.round(decimals=3)
        # print(data)

        else:
            return func.HttpResponse(
                simplejson.dumps(
                    {"error": 'Please pass a valid type in the body'}),
                status_code=400
            )

        if not opty_rows.empty:
            opty_rows['id'] = range(1, len(opty_rows) + 1)
            opty_rows = opty_rows.to_dict('records')
        else:
            opty_rows = []
            others["error"] = "No data found"

        output = simplejson.dumps({
            "opty_rows": opty_rows[0:1000], **others
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
