"""
caching module
"""
import logging
from time import time
from services.blob_helpers import get_list_from_split_blob, save_list_into_blob
from services.blob_helpers import get_all_files_from_container, del_blob
from services.common_service import custom_query


def get_data(name, query, cache_expiry_required=False):
    """
    # get the data from cache directory
    """
    try:
        data = get_list_from_split_blob("CacheDirectory/"+name)
        if "expiry" in data and data["expiry"] > + \
           time() and data["query"] == query:
            logging.info("From Cache: " + name)
            if cache_expiry_required:
                return data
            return data["data"]
        return None
    except Exception as error_e:
        logging.info(error_e)
        return None


def put_data(name, query, data):
    """
    # insert into cahce directory
    """
    if not data:
        data = []
    tmp = {}
    tmp["data"] = data
    tmp["query"] = query
    tmp["expiry"] = time() + 86400
    tmp["cached_at"] = time()
    logging.info("To Cache: " + name)
    save_list_into_blob("CacheDirectory/"+name, tmp)


def update_cache(i_d=None):
    """
    # update the cache, based on query provided
    """
    # list all cache files
    files = get_all_files_from_container("CacheDirectory")
    for fil in list(files):
        if i_d and i_d not in fil.name:
            continue
        logging.info(fil.name)
        try:
            # get the blob based on it's name
            data = get_list_from_split_blob(fil.name)
            query = str(data["query"])
            # get the updated data based on query provided
            updated_data = custom_query(query)
            tmp = {}
            tmp["data"] = updated_data
            tmp["query"] = query
            tmp["expiry"] = time() + 86400
            tmp["cached_at"] = time()
            # update into blob
            save_list_into_blob(fil.name, tmp)
        except Exception as erroe_e:
            # delete the blob, if any errors
            # this may occur when table referred in the table has been dropped
            logging.info(erroe_e)
            del_blob(fil.name)
