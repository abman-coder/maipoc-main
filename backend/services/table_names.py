"""
# table names mapping
"""
import os
current_env = os.environ["TOOL_ENV"]
current_schema = os.environ["DB_SCHEMA"] if "DB_SCHEMA" in os.environ else None

tables = {
    "DEV": {

    },
    "UAT": {

    },
    "PROD": {

    }
}


def get_schema():
    return current_schema


def get_tables():
    """
    all env tables
    """
    return tables[current_env] if current_env in tables else tables["DEV"]
