
import json
import requests


token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"


def get_token():
    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": "client id",
            "client_secret": "client secret",
            "scope": "https://dev.azuresynapse.net/.default"
        },
        # headers=headers
    )
    return response.json()['access_token']


def run_job(pipeline_name, body={}):
    token = get_token()
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.post(
        f"https://maipocaa.dev.azuresynapse.net/pipelines/{pipeline_name}/createRun?api-version=2020-12-01",
        data=json.dumps(body),
        headers=headers
    )
    return response.json()
