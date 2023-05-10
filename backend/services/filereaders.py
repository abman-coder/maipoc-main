import logging
import pandas as pd


cache_files = {}
removable_files = ["opty/Feature_Contribution.csv", "opty/model_features.csv", "opty/Oppty_Amendment.csv", "opty/Resource_Resource_Tier_Mapping.csv",
                   "opty/soft_exception.csv", "risk_recommender/Signed_Completed_Deals_FY20FY21FY22_C1_YAT_risks.csv", "risk_recommender/Open_Deals_Resource_Grain_FY22.csv"]


def get_data(file_name, file_type, file_encoding=None):
    if file_name in cache_files:
        return cache_files[file_name]
    else:
        logging.info(f"read again {file_name}")
        if len(cache_files) > 10:
            all_keys = list(cache_files.keys())
            for name in all_keys:
                if not "opty" in name:
                    cache_files.pop(f"{name}", None)

            # for name in removable_files:
            #     cache_files.pop(f"local_files/{name}", None)
        file_path = (file_name)
        if file_type == 'csv':
            if file_encoding:
                data = pd.read_csv(file_path, encoding=file_encoding)
            else:
                data = pd.read_csv(file_path)
        elif file_type == 'json':
            data = pd.read_json(file_path)
        elif file_type == 'pkl':
            return file_path
        cache_files[file_name] = data
        return data


def update_data(key, value):
    cache_files[key] = value
