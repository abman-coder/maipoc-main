"""
common service
"""
import logging
from datetime import datetime
import pandas as pd
from services.sqlconnection import connection_auto
from services.table_names import get_tables, get_schema
CONNECTION = None
# for sql connection
tables = get_tables()
schema = get_schema()


def conn(force=False):
    """
    connection to database
    """
    global CONNECTION
    if CONNECTION is None or force:
        CONNECTION = connection_auto()
    return CONNECTION
# to list all rows


def list_all(table, columns="*", second=True):
    """
    list all rows in a table
    """
    try:
        cnx = conn()
        table = tables[table] if table in tables else table
        cursor = cnx.execute(f"SELECT {columns} FROM {schema}.{table}")
        results = [dict(zip([column[0] for column in cursor.description], row))
                   for row in cursor.fetchall()]
        return results
    except Exception as error_e:
        logging.info(error_e)
        if "42S02" in str(error_e):
            return None
        if second:
            conn(True)
            return list_all(table, columns, False)
# to get data on provided condition


def by_query(table, condition, columns="*", second=True):
    """
    rows by condition
    """
    try:
        cnx = conn()
        table = tables[table] if table in tables else table
        cursor = cnx.execute(
            f"SELECT {columns} FROM {schema}.{table} where {condition};")
        results = [dict(zip([column[0] for column in cursor.description], row))
                   for row in cursor.fetchall()]
        return results
    except Exception as error_e:
        logging.info(error_e)
        if "42S02" in str(error_e):
            return None
        if second:
            conn(True)
            return by_query(table, condition, columns, False)


def custom_query(query, table=None, second=True):
    """
    # to get data based on provided entire query
    """
    try:
        cnx = conn()
        if table and second:
            table_d = tables[table] if table in tables else table
            if table != table_d:
                query = query.replace(table, table_d)
        cursor = cnx.execute(query)
        results = [dict(zip([column[0] for column in cursor.description], row))
                   for row in cursor.fetchall()]
        return results
    except Exception as error_e:
        logging.info(error_e)
        if "42S02" in str(error_e):
            return None
        if second:
            conn(True)
            return custom_query(query, table, False)


def add_(table, columns, values, second=True):
    """
    # to insert into a table
    """
    try:
        cnx = conn()
        table = tables[table] if table in tables else table
        cnx.execute(f"insert into {schema}."+table+columns +
                    " values("+",".join("?" for i in range(len(values)))+")", values)
        return {"success": True}
    except Exception as error_e:
        logging.info(error_e)
        if "42S02" in str(error_e):
            return None
        if second:
            conn(True)
            return add_(table, columns, values, False)


def edit_(table, columns, condition, values, second=True):
    """
    # to update a row in provided table
    """
    try:
        cnx = conn()
        table = tables[table] if table in tables else table
        cursor = cnx.execute(
            f"update {schema}.{table} set {columns} where {condition}", values)
        cursor.commit()
        return cursor.rowcount
    except Exception as error_e:
        logging.info(error_e)
        if second:
            conn(True)
            return edit_(table, columns, condition, values, False)


def drop_table(table, second=True):
    """
    to drop a table
    """
    try:
        cnx = conn()
        table = tables[table] if table in tables else table
        cursor = cnx.execute(
            f"Drop table {schema}.{table}")
        cursor.commit()
        return 1
    except Exception as error_e:
        logging.info(error_e)
        if "42S02" in str(error_e):
            return None
        if second:
            conn(True)
            return drop_table(table, False)


def delete_(table, condition, second=True):
    """
    to delete a row in provided table by condition
    """
    try:
        cnx = conn()
        table = tables[table] if table in tables else table
        cursor = cnx.execute(
            f"DELETE FROM {schema}.{table} where {condition}")
        cursor.commit()
        return cursor.rowcount
    except Exception as error_e:
        logging.info(error_e)
        if "42S02" in str(error_e):
            return None
        if second:
            conn(True)
            return delete_(table, condition, False)


def get_a_z(indx):
    """
    convert 0-25 to a-z
    """
    return ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"][indx]


def get_indx_a_z(letter):
    """
    convert a-z to 0-25
    """
    return ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"].index(letter)


def convert_str_to_columns(col_list):
    """
    convert list of columns to string
    """
    return [f"[{x}]" for x in col_list]


def save_logs(req):
    """
    save logs to database
    """
    try:
        body = {
            "user_name": req["name"] if "name" in req else "",
            "error_msg": req["msg"][:999] if "msg" in req else "",
            "input_data": req["input"][:999] if "input" in req else "",
            "module": req["module"][:999] if "module" in req else "",
            "time_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        columns = ",".join([column for column, value in body.items()])
        add_("error_logs", "("+columns+")",
             [value for column, value in body.items()])
    except Exception as error_e:
        logging.info(error_e)
        print('error in save_logs')


def get_features():
    return ['Deal ID', 'Is Strategic Opportunity', 'Is Amendment', 'Fee Arrangement', 'Approval Duration', 'Contract Revenue Cluster', 'Is Public Sector', 'Has SQA Review', 'Has IP Review', 'Has Finance Review', 'Has CN Review', 'Is Contract Reviewed', 'Is Contract Rushed', 'Has ESWO', 'NST Category', 'ESAP', 'Total Resource Hours', 'Project Manager Mix', 'Standard Offering Type', 'Deal Velocity', 'Is ECIF', 'SQA Review', 'TQA Review', 'HAS SOW', 'Complex Deal Indicator', 'CloudFlag', 'IsAzureandA&IDomainDeal', 'VelocityExceedsTarget', 'SolutionExceedsTarget', 'NegotiationsExceedsTarget', 'ApprovalsExceedsTarget', 'OSEDealsFlag', 'Is Risk Overridden', 'Payment Terms', 'Domain Involvement', 'Outlier Type', 'Planned Contract Riskreserve Required CCUS', 'CM Review', 'Pricing Cut Off', 'Default Delivery Margin Target', 'Delivery Margin Target', 'Is Misstated', 'Is IP Exchange', 'Is Vaguely Described', 'Derived Primary Domain', 'Domain Count', 'PM Solution Area', 'PL Requested Type', 'Is Subcon Identified', 'Contract Created Date Fiscal Year', 'Planned Contract Microsoft IGD Hours', 'Price To Customer USD', 'commitmentlevel', 'opportunitysize', 'PPGCategory', 'ORBApproved', 'exceptiontype', 'opportunityaginggroup', 'isgpo', 'Area_x', 'TimeZone', 'TotalRevenueServicesUSD', 'IndustrySector', 'IsGlobal', 'SBDInvolved', 'CompassOneIndustryName', 'RevenueServicesUSD', 'DeliveryCostServicesUSD', 'Domain', 'FinalDeliveryValue', 'ApprovalType', 'Federal', 'QA_Critical', 'QA_High', 'QA_Low', 'QA_Medium', 'TQA_Critical', 'TQA_High', 'TQA_Low', 'TQA_Medium']


def get_categorical_features():
    return ['Deal ID', 'Is Strategic Opportunity', 'Is Amendment', 'Fee Arrangement', 'Approval Duration', 'Contract Revenue Cluster', 'Is Public Sector', 'Has SQA Review', 'Has IP Review', 'Has Finance Review', 'Has CN Review', 'Is Contract Reviewed', 'Is Contract Rushed', 'NST Category', 'ESAP', 'Project Manager Mix', 'Standard Offering Type', 'Is ECIF', 'SQA Review', 'TQA Review', 'HAS SOW', 'Complex Deal Indicator', 'CloudFlag', 'IsAzureandA&IDomainDeal', 'VelocityExceedsTarget', 'SolutionExceedsTarget', 'NegotiationsExceedsTarget', 'ApprovalsExceedsTarget', 'OSEDealsFlag', 'Is Risk Overridden', 'Payment Terms', 'Domain Involvement', 'Outlier Type', 'CM Review', 'Pricing Cut Off', 'Is Misstated', 'Is Vaguely Described', 'Derived Primary Domain', 'PM Solution Area', 'PL Requested Type', 'Is Subcon Identified', 'Contract Created Date Fiscal Year',  'opportunitysize', 'PPGCategory', 'ORBApproved', 'exceptiontype', 'opportunityaginggroup', 'isgpo', 'TimeZone', 'IndustrySector', 'IsGlobal', 'SBDInvolved', 'CompassOneIndustryName', 'Domain', 'Federal', 'QA_Critical', 'QA_High', 'QA_Low', 'QA_Medium', 'TQA_Critical', 'TQA_High', 'TQA_Low', 'TQA_Medium']
