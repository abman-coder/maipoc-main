"""
sql connection
"""
import os
# import pyodbc

server = os.environ["DataBase_Server"]
username = os.environ["DataBase_UserName"]
password = os.environ["DataBase_Password"]
database = os.environ['DataBase_Name'] if 'DataBase_Name' in os.environ else 'BrewlabDWH'
DRIVER_TYPE = '{ODBC Driver 17 for SQL Server}'

AUTH_METHOD = ""
if username and "@" in username:
    AUTH_METHOD = "Authentication=ActiveDirectoryPassword"


def connection():
    """
    sql connection
    """
    return ""
    # return pyodbc.connect('DRIVER=' + DRIVER_TYPE + ';SERVER=' +
    #                       server + ';PORT=1433;DATABASE=' +
    #                       database + ';UID=' +
    #                       username + ';PWD=' +
    #                       password + ';'+AUTH_METHOD)


def connection_auto():
    """
    sql connection with autocommit
    """
    return ""
    # return pyodbc.connect('DRIVER=' + DRIVER_TYPE + ';SERVER=' +
    #                       server + ';PORT=1433;DATABASE=' +
    #                       database + ';UID=' +
    #                       username + ';PWD=' +
    #                       password + ';'+AUTH_METHOD,
    #                       autocommit=True)
