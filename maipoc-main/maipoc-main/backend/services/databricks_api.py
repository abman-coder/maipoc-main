# from adal import AuthenticationContext
# import requests

# authority_host_url = "https://login.microsoftonline.com/"
# azure_databricks_resource_id = ""
# base_url = 'https://abc.azuredatabricks.net/api/2.0/'

# # Required user input
# user_parameters = {
#     "tenant": "",
#     "client_id": "",
#     "username": "",
#     "password": "",
# }

# # configure AuthenticationContext
# # authority URL and tenant ID are used
# authority_url = authority_host_url + user_parameters['tenant']
# context = AuthenticationContext(authority_url)

# # API call to get the token
# token_response = context.acquire_token_with_username_password(
#     azure_databricks_resource_id,
#     user_parameters['username'],
#     user_parameters['password'],
#     user_parameters['client_id']
# )

# access_token = token_response['accessToken']
# refresh_token = token_response['refreshToken']
# # print(token_response)

# # supply the refresh_token
# # (whose default lifetime is 90 days or longer [token lifetime])


# def refresh_access_token(rfs_tkn):
#     context = AuthenticationContext(authority_url)
#     # function link
#     token_response = context.acquire_token_with_refresh_token(
#         rfs_tkn,
#         user_parameters['client_id'],
#         azure_databricks_resource_id)
#     # print all the fields in the token_response
#     for key in token_response.keys():
#         print(str(key) + ': ' + str(token_response[key]))

#     global access_token, refresh_token
#     access_token = token_response['accessToken']
#     refresh_token = token_response['refreshToken']
#     return 1

# # (refresh_token, access_token) =  get_refresh_and_access_token()


# def list_cluster_with_aad_token():
#     token = access_token

#     # request header
#     headers = {
#         'Authorization': 'Bearer ' + token
#     }

#     response = requests.get(
#         base_url+"clusters/list",
#         headers=headers
#     )

#     try:
#         res_json = response.json()

#         for cluster in res_json['clusters']:
#             print(cluster["cluster_id"], cluster["cluster_name"])
#     except Exception as e:
#         refresh_access_token()
#         print('Response cannot be parsed as JSON:')
#         print('\t: ' + str(response))
#         print('The exception is: %s' % str(e))


# def start_cluster_with_aad_token(id):
#     token = access_token

#     # request header
#     headers = {
#         'Authorization': 'Bearer ' + token
#     }

#     response = requests.post(
#         base_url+"clusters/start",
#         data={"cluster_id": id},
#         headers=headers
#     )

#     try:
#         res_json = response.json()
#         print(res_json)
#     except Exception as e:
#         refresh_access_token()
#         # start_cluster_with_aad_token(id)
#         print('Response cannot be parsed as JSON:')
#         print('\t: ' + str(response))
#         print('The exception is: %s' % str(e))


# def start_job_with_aad_token(id):
#     token = access_token

#     # request header
#     headers = {
#         'Authorization': 'Bearer ' + token
#     }

#     response = requests.post(
#         base_url+"jobs/run-now",
#         data={"job_id": id},
#         headers=headers
#     )

#     try:
#         res_json = response.json()
#         print(res_json)
#     except Exception as e:
#         refresh_access_token()
#         # start_job_with_aad_token(id)
#         print('Response cannot be parsed as JSON:')
#         print('\t: ' + str(response))
#         print('The exception is: %s' % str(e))

# # list_cluster_with_aad_token()
# # start_cluster_with_aad_token()
# # start_job_with_aad_token()
