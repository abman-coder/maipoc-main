"""
    Get data
"""
import datetime
import logging
import json
import base64


def requires_auth(headers):
    # Extract client principal from header
    clientPrincipal = headers.get('X-MS-CLIENT-PRINCIPAL')
    if clientPrincipal is None:
        return {
            "code": 200,
            "name": "name",
            "user name": "user_name",
            "roles": ["o", "r"]
        }
    cp = json.loads(base64.b64decode(clientPrincipal).decode(
        'utf-8'))  # Decode client principal
    # roles = [x['val'] for x in cp['claims'] if x['typ'] ==
    #          'roles']  # Extract claims from client principal
    user_name = ''
    name = ''
    roles = []
    for x in cp['claims']:
        if x['typ'] == 'roles':
            roles.append(x['val'])
        elif x['typ'] == 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn' or "@" in x['val']:
            user_name = x['val']
        elif x['typ'] == 'name':
            name = x['val']

    return {
        "code": 200,
        "name": name,
        "user name": user_name,
        "roles": roles
    }
