# getting all the static part in one cell

# import
from datetime import datetime
import logging
from services.datalake_connection import download_file_from_directory, write_data_to_datalake
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import json
from decimal import *
import numexpr as ne
from services.filereaders import get_data
setcontext(ExtendedContext)
# importing Finance Final

# finance_final = pd.read_csv("abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Finance_Final.csv")

# #importing data_advanalyticslivedata_final
# data_advanalyticslivedata_final = pd.read_csv("abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/data_advanalyticslivedata_final.csv")

# #Importing Pre-processed df
# dataframe1_new = pd.read_csv("abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/df1.csv")

# #importing Oppty amendment
# Oppty_Amendment = pd.read_csv("abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Oppty_Amendment.csv")

# #importing soft_exception
# soft_exception = pd.read_csv("abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/soft_exception.csv")

# #importing model features
# col_model_new = pd.read_csv('abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/model_features.csv')

# #Importing co-eff file
# coeff = pd.read_csv('abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/OpportunityPropensityFeatureCoefficients_v5.csv')

# #Seller Narratives
# Seller_Narratives_new = pd.read_csv("abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Seller_Narratives.csv")

# #feature Contribution
# Feature_Contribution = pd.read_csv('abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Feature_Contribution.csv')

# Inport Resource tier mapping file
# mapping = pd.read_csv(
#     "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Resource_Resource_Tier_Mapping.csv")
mapping = get_data(
    'local_files/opty/Resource_Resource_Tier_Mapping.csv', 'csv')

finance_final = get_data('local_files/opty/Finance_Final.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'Finance_Final.csv')
# pd.read_csv(
# "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Finance_Final.csv")

# importing data_advanalyticslivedata_final
data_advanalyticslivedata_final = get_data(
    'local_files/opty/data_advanalyticslivedata_final.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'data_advanalyticslivedata_final.csv')
#             pd.read_csv(
# "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/data_advanalyticslivedata_final.csv")

# Importing Pre-processed df
dataframe1_new = get_data('local_files/opty/df1.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'df1.csv')
# pd.read_csv(
#     "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/df1.csv")

# importing Oppty amendment
Oppty_Amendment = get_data('local_files/opty/Oppty_Amendment.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'Oppty_Amendment.csv')
#             pd.read_csv(
# "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Oppty_Amendment.csv")

# importing soft_exception
soft_exception = get_data('local_files/opty/soft_exception.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'soft_exception.csv')
#             pd.read_csv(
# "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/soft_exception.csv")

# importing model features
col_model_new = get_data('local_files/opty/model_features.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'model_features.csv')
#             pd.read_csv(
# 'abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/model_features.csv')

# Importing co-eff file
coeff = get_data(
    'local_files/opty/OpportunityPropensityFeatureCoefficients.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'OpportunityPropensityFeatureCoefficients_v5.csv')
#             pd.read_csv(
# 'abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/OpportunityPropensityFeatureCoefficients_v5.csv')


Seller_Narratives_new = get_data(
    'local_files/opty/seller_narratives.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'Seller_Narratives.csv')
# pd.read_csv(
#     "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Seller_Narratives.csv")

Feature_Contribution = get_data(
    'local_files/opty/Feature_Contribution.csv', 'csv')
# download_file_from_directory(
#     'Ml_service', 'Feature_Contribution.csv')
# pd.read_csv(
#     'abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Feature_Contribution.csv')

# ne.set_vml_num_threads(8)

Seller_Narratives = Seller_Narratives_new.copy()

Seller_Narratives['Odds_Ratio'] = pd.to_numeric(
    Seller_Narratives['Odds_Ratio'], errors='coerce')
Seller_Narratives['MaxOdds_Ratio'] = pd.to_numeric(
    Seller_Narratives['MaxOdds_Ratio'], errors='coerce')
Feature_Contribution_small = Feature_Contribution[["feature", "max"]]
Feature_Contribution_star = Feature_Contribution[["feature", "Feature_Star"]]


def opt_re_score(inp, opt_id, source=None):

    # #Step - 1
    global finance_final
    global data_advanalyticslivedata_final
    global dataframe1_new
    global Oppty_Amendment
    global soft_exception
    global col_model_new
    global coeff
    global Seller_Narratives_new
    global Feature_Contribution

    logging.info(datetime.now())

    # finance_final = pd.read_csv('local_files/Finance_Final.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'Finance_Final.csv')
    # # pd.read_csv(
    # # "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Finance_Final.csv")

    # # importing data_advanalyticslivedata_final
    # data_advanalyticslivedata_final = pd.read_csv(
    #     'local_files/data_advanalyticslivedata_final.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'data_advanalyticslivedata_final.csv')
    # #             pd.read_csv(
    # # "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/data_advanalyticslivedata_final.csv")

    # # Importing Pre-processed df
    # dataframe1_new = pd.read_csv('local_files/df1.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'df1.csv')
    # # pd.read_csv(
    # #     "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/df1.csv")

    # # importing Oppty amendment
    # Oppty_Amendment = pd.read_csv('local_files/Oppty_Amendment.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'Oppty_Amendment.csv')
    # #             pd.read_csv(
    # # "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Oppty_Amendment.csv")

    # # importing soft_exception
    # soft_exception = pd.read_csv('local_files/soft_exception.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'soft_exception.csv')
    # #             pd.read_csv(
    # # "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/soft_exception.csv")

    # # importing model features
    # col_model_new = pd.read_csv('local_files/model_features.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'model_features.csv')
    # #             pd.read_csv(
    # # 'abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/model_features.csv')

    # # Importing co-eff file
    # coeff = pd.read_csv(
    #     'local_files/OpportunityPropensityFeatureCoefficients_v5.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'OpportunityPropensityFeatureCoefficients_v5.csv')
    # #             pd.read_csv(
    # # 'abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/OpportunityPropensityFeatureCoefficients_v5.csv')

    # Seller_Narratives_new = pd.read_csv('local_files/Seller_Narratives.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'Seller_Narratives.csv')
    # # pd.read_csv(
    # #     "abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Seller_Narratives.csv")

    # Feature_Contribution = pd.read_csv('local_files/Feature_Contribution.csv')
    # # download_file_from_directory(
    # #     'Ml_service', 'Feature_Contribution.csv')
    # # pd.read_csv(
    # #     'abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Feature_Contribution.csv')

    # Assigning input to the dataframe
    # Assigning input to the dataframe
    if source and source == 'uitool':
        #Step - 1
        finance_final_input = pd.DataFrame(inp)
        finance_final_input.drop(columns=['id'], inplace=True)
        finance_final_package = finance_final_input.groupby(by=['opty_id', 'pkg_id', 'ItemLevel']).agg({'Discount CCUS': 'sum', 'Revenue CCUS': 'sum', 'ECIFCommitted': 'max', 'Risk Reserve CCUS': 'max', 'Total Resource Hours': 'sum',
                                                                                                        'ACRPotentialRevenue': 'min', 'BIF Amount CCUS': 'max', 'opportunitycreateddatefiscalyear': 'min', 'ResourceTier': 'min', 'opportunitystatus': 'min', 'contract id': 'min', 'FeeType': 'min', 'is S500 Flag': 'min'}).reset_index()
        finance_final_package['ItemLevel'] = 'Package'
        finance_final_package['Revenue CCUS'] = finance_final_package['Revenue CCUS'] + \
            finance_final_package['Risk Reserve CCUS']
        finance_final_temp = finance_final_input.append(
            finance_final_package, ignore_index=True)
        finance_final_1 = finance_final_temp.copy()
    else:
        # Convert
        #import input
        # df1 = pd.read_json('abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Sample_Quote_check.json')
        try:
            # df1 = pd.DataFrame(inp)
            # a = df1.to_json()
            # df = json.loads(a)
            df = inp[0]
            oppty_id = df['CpqHeaderInfo']['CRMOpportunityId']
        except Exception as e:
            logging.info(e)
            df1 = download_file_from_directory(
                'Ml_service', 'Sample_Quote_check.json', 'json')
            a = df1.to_json()
            df = json.loads(a)
            oppty_id = df['CpqHeaderInfo']['CRMOpportunityId']

        # Extracting Oppty_id & Contract id
        # oppty_id = df['CpqHeaderInfo']['CRMOpportunityId']
        contract_id = df['CpqHeaderInfo']['QuoteId']

        # Fetching revenue and discount
        d1 = pd.DataFrame(columns=['oppty_id', 'contract_id', 'package_id', 'revenue', 'discount',
                          'FeeArrangementType', 'PrimaryProductName', 'BusinessScenarioName', 'CatalogName'])
        temp = pd.DataFrame.from_records(df['CpqQuoteDetails']['CpqPackages'])
        for i in range(len(df['CpqQuoteDetails']['CpqPackages'])):
            id = temp['Id'][i]
            revenue = temp['Revenue'][i]
            discount = temp['Discount'][i]
            FeeArrangementType = temp['FeeArrangementType'][i]
            PrimaryProductName = temp['PrimaryProductName'][i]
            BusinessScenarioName = temp['BusinessScenarioName'][i]
            CatalogName = temp['CatalogName'][i]
            d1 = d1.append({'oppty_id': oppty_id, 'contract_id': contract_id, 'package_id': id, 'revenue': revenue, 'discount': discount, 'FeeArrangementType': FeeArrangementType,
                           'PrimaryProductName': PrimaryProductName, 'BusinessScenarioName': BusinessScenarioName, 'CatalogName': CatalogName}, ignore_index=True)

        # Fetching Risk reserve
        d2 = pd.DataFrame()
        for i in range(len(temp['Adjustments'])):
            k = pd.DataFrame(json_normalize(temp["Adjustments"][i]))
            if k.empty == True:
                pass
            else:
                k = k[['PackageId', 'Revenue', 'Type']]
                d2 = pd.concat([d2, k])
        d2['oppty_id'] = oppty_id
        # Filtering only for Risk Reserve
        d2 = d2[d2['Type'] == 'Risk Reserve']
        d2.rename(columns={'Revenue': 'Risk_Reserve'}, inplace=True)

        # Fetching ECIF
        d3 = pd.DataFrame()
        for i in range(len(temp['Fundings'])):
            p = pd.DataFrame(json_normalize(temp['Fundings'][i]))
            if p.empty == True:
                pass
            else:
                p = p[['PackageId', 'Revenue', 'Type']]
                d3 = pd.concat([d3, p])
        d3['oppty_id'] = oppty_id
        # Filtering only for ECIF
        d3 = d3[d3['Type'] == 'End-Customer Investment Funds (ECIF)']
        #d3['BIF Amount CCUS'] = d3['Revenue']
        d3.rename(columns={'Revenue': 'ECIF_Revenue'}, inplace=True)

        # Fetching Resource Name and hours
        d4 = pd.DataFrame(columns=[
                          'oppty_id', 'package_id', 'ParentItemId', 'Resource_Name', 'Resource_Hours'])
        for i in range(len(temp['Services'])):
            temp1 = pd.DataFrame(json_normalize(temp['Services'][i]))
            package_id = temp1['ParentItemId'][0]
            for i in range(len(temp1)):
                temp2 = pd.DataFrame(json_normalize(temp1['Resources'][i]))
                ParentItemId = temp2['ParentItemId'][0]
                CatalogItemName = temp2['CatalogItemName'][0]
                Quantity = temp2['Quantity'][0]
                d4 = d4.append({'oppty_id': oppty_id, 'package_id': package_id, 'ParentItemId': ParentItemId,
                               'Resource_Name': CatalogItemName, 'Resource_Hours': Quantity}, ignore_index=True)

        # Fetching Tags
        d5 = pd.DataFrame(columns=['oppty_id', 'package_id', 'Tags'])
        for i in range(len(temp['AdditionalAttributes'])):
            package_id = temp['Id'][i]
            temp2 = pd.DataFrame(json_normalize(
                temp['AdditionalAttributes'][i]))
            Tags = temp2['Tags'][0][0]
            d5 = d5.append(
                {'oppty_id': oppty_id, 'package_id': package_id, 'Tags': Tags}, ignore_index=True)

        # joining the extracted dataframes
        f1 = d1.merge(d2[['PackageId', 'Risk_Reserve']], left_on=['package_id'], right_on=[
                      'PackageId'], how='left').drop(columns=['PackageId'])
        f2 = f1.merge(d3[['PackageId', 'ECIF_Revenue']], left_on=['package_id'], right_on=[
                      'PackageId'], how='left').drop(columns=['PackageId'])
        f3 = f2.merge(d4[['package_id', 'Resource_Name', 'Resource_Hours']], left_on=[
                      'package_id'], right_on=['package_id'], how='left')
        f4 = f3.merge(d5[['package_id', 'Tags']], left_on=[
                      'package_id'], right_on=['package_id'], how='left')

        # Assiging BIF & Item Level
        f4['BIF Amount CCUS'] = f4['ECIF_Revenue']
        f4['Item Level'] = 'Resource'

        # creating package level data
        f4_pkge = f4.groupby(by=['oppty_id', 'package_id']).agg({'contract_id': 'min', 'revenue': 'max', 'discount': 'max', 'FeeArrangementType': 'min', 'PrimaryProductName': 'min',
                                                                'BusinessScenarioName': 'min', 'CatalogName': 'min', 'Risk_Reserve': 'min', 'ECIF_Revenue': 'min', 'Resource_Name': 'min',
                                                                 'Resource_Name': 'min', 'Resource_Hours': 'sum', 'Tags': 'min', 'BIF Amount CCUS': 'max'}).reset_index()
        f4_pkge['Item Level'] = 'Package'
        final_f4 = pd.concat((f4, f4_pkge), axis=0, ignore_index=True)
        new_final_f4 = final_f4.merge(
            mapping, left_on='Resource_Name', right_on='Resource').drop(columns=['Resource'])
        if new_final_f4.empty:
            # final_f4.rename(
            #     columns={'Resource': 'Resource_Name'}, inplace=True)
            final_f4['ResourceTier'] = final_f4['Resource_Name']
        else:
            final_f4 = new_final_f4

        finance_final = finance_final[finance_final['ItemLevel'] == 'Package']
        # Extracting few features
        final = final_f4.merge(finance_final[['opty_id', 'pkg_id', 'opportunitycreateddatefiscalyear', 'opportunitystatus',
                               'ACRPotentialRevenue', 'is S500 Flag']], left_on=['oppty_id', 'package_id'], right_on=['opty_id', 'pkg_id'], how='inner')
        final.drop(columns=['opty_id', 'pkg_id'], inplace=True)

        # Renaming
        final.columns = ['opty_id', 'contract id', 'pkg_id', 'Revenue CCUS', 'Discount CCUS', 'FeeType', 'PrimaryProductName', 'BusinessScenarioName', 'CatalogName',
                         'Risk Reserve CCUS', 'ECIFCommitted', 'Resource_Name', 'Total Resource Hours', 'Tags', 'BIF Amount CCUS', 'ItemLevel', 'ResourceTier',
                         'opportunitycreateddatefiscalyear', 'opportunitystatus', 'ACRPotentialRevenue', 'is S500 Flag']

        # Name Correction
        final['FeeType'] = final['FeeType'].map(
            {'Fixed Fee': 'Fixed Fee', 'Time & Materials': 'Time & Materials', 'T & M Cap': 'T & M Cap', 'FixedFee': 'Fixed Fee', 'Time&Materials': 'Time & Materials', 'T&MCap': 'T & M Cap'})

        final = final[['opty_id', 'contract id', 'pkg_id', 'Revenue CCUS', 'Discount CCUS', 'FeeType',
                       'Risk Reserve CCUS', 'ECIFCommitted', 'Total Resource Hours', 'BIF Amount CCUS', 'ItemLevel', 'ResourceTier',
                       'opportunitycreateddatefiscalyear', 'opportunitystatus', 'ACRPotentialRevenue', 'is S500 Flag']]

        # final['contract id'] = final['contract id'].astype(int)
        # final['pkg_id'] = final['pkg_id'].astype(int)
        finance_final_1 = final.copy()
        finance_final_input = final
    #Step - 1
    # finance_final_temp = finance_final.copy()

    # logging.info(datetime.now())

    # # #Reading Financial Input file - Dynamic file
    # finance_final_input = pd.DataFrame(inp)

    # Replacing values
    # finance_final_temp.loc[((finance_final_temp['opty_id'].isin(finance_final_input['opty_id'])) &
    #                         (finance_final_temp['contract id'].isin(finance_final_input['contract id'])) &
    #                         (finance_final_temp['pkg_id'].isin(finance_final_input['pkg_id'])) &
    #                         (finance_final_temp['ItemLevel'].isin(finance_final_input['ItemLevel']) &
    #                          finance_final_temp['ResourceTier'].isin(finance_final_input['ResourceTier']))),
    #                        ['Revenue CCUS', 'Discount CCUS', 'Risk Reserve CCUS', 'ECIFCommitted', 'FeeType', 'Total Resource Hours']] = finance_final_input[['Revenue CCUS', 'Discount CCUS', 'Risk Reserve CCUS', 'ECIFCommitted', 'FeeType', 'Total Resource Hours']]

    # finance_final_temp = finance_final_temp[finance_final_temp['opty_id']
    #                                         == finance_final_input['opty_id'].values[0]]

    # wk = finance_final_temp.loc[(
    #     finance_final_temp['opty_id'] == finance_final_input['opty_id'].values[0])]
    # wk.drop(columns=['Revenue CCUS', 'Discount CCUS', 'Risk Reserve CCUS',
    #         'ECIFCommitted', 'FeeType', 'Total Resource Hours'], inplace=True)
    # wk = wk.reset_index().merge(finance_final_input, on=[
    #     'opty_id', 'contract id', 'pkg_id', 'ItemLevel', 'ResourceTier'], how='inner')
    # finance_final_temp.loc[wk['index'], ['Revenue CCUS', 'Discount CCUS', 'Risk Reserve CCUS', 'ECIFCommitted', 'FeeType', 'Total Resource Hours']] = wk[[
    #     'Revenue CCUS', 'Discount CCUS', 'Risk Reserve CCUS', 'ECIFCommitted', 'FeeType', 'Total Resource Hours']].values

    # # Assigning a copy
    # finance_final_1 = finance_final_temp.copy()

    #Step - 2

    #Step - 2
    data_final = finance_final_1.copy()

    data_final_srvc = data_final.loc[data_final['ItemLevel'] == 'Resource']
    data_final_pkg = data_final.loc[data_final['ItemLevel'] == 'Package']

    data_final_srvc['Revenue_CCUS_agg'] = data_final_srvc.groupby(['opty_id', 'opportunitycreateddatefiscalyear', 'opportunitystatus'])[
        'Revenue CCUS'].transform(np.sum).astype(np.float64)
    data_final_srvc['Discount_CCUS_agg'] = data_final_srvc.groupby(['opty_id', 'opportunitycreateddatefiscalyear', 'opportunitystatus'])[
        'Discount CCUS'].transform(np.sum).astype(np.float64)
    data_final_srvc['BIF_agg'] = data_final_srvc.groupby(['opty_id', 'opportunitycreateddatefiscalyear', 'opportunitystatus'])[
        'BIF Amount CCUS'].transform(np.sum).astype(np.float64)
    data_final_srvc['ECIFCommitted_agg'] = data_final_srvc.groupby(['opty_id', 'opportunitycreateddatefiscalyear', 'opportunitystatus'])[
        'ECIFCommitted'].transform(np.sum).astype(np.float64)

    data_final_srvc1 = data_final_srvc[['opty_id', 'opportunitycreateddatefiscalyear', 'opportunitystatus', 'ACRPotentialRevenue',
                                        'is S500 Flag', 'Revenue_CCUS_agg', 'Discount_CCUS_agg', 'BIF_agg', 'ECIFCommitted_agg']].drop_duplicates()

    data_final_pkg['Risk_Reserve_CCUS_agg'] = data_final_pkg.groupby(
        ['opty_id', 'opportunitycreateddatefiscalyear', 'opportunitystatus'])['Risk Reserve CCUS'].transform(np.sum)

    data_final_pkg1 = data_final_pkg[[
        'opty_id', 'Risk_Reserve_CCUS_agg']].drop_duplicates()

    data_final_pkg2 = pd.merge(data_final_pkg1, data_final_pkg[['opty_id', 'ACRPotentialRevenue', 'opportunitystatus']], how='left', left_on=[
                               'opty_id'], right_on=['opty_id']).drop_duplicates()

    data_merged = pd.merge(data_final_pkg2, data_final_srvc1, how='left', left_on=[
                           'opty_id'], right_on=['opty_id'])

    data_merged.rename(columns={'ACRPotentialRevenue_x': 'ACRPotentialRevenue',
                       'opportunitystatus_x': 'opportunitystatus'}, inplace=True)

    data_merged_selected = data_merged[['opty_id', 'opportunitystatus', 'ACRPotentialRevenue', 'is S500 Flag',
                                        'Revenue_CCUS_agg', 'Discount_CCUS_agg', 'BIF_agg', 'ECIFCommitted_agg', 'Risk_Reserve_CCUS_agg']]

    data_merged_selected_unique = data_merged_selected.drop_duplicates()

    data_merged_selected_unique['Revenue_CCUS_agg'][data_merged_selected_unique['Revenue_CCUS_agg'] < 0] = 0
    data_merged_selected_unique['Discount_CCUS_agg'][data_merged_selected_unique['Discount_CCUS_agg'] < 0] = 0
    data_merged_selected_unique['Risk_Reserve_CCUS_agg'][data_merged_selected_unique['Risk_Reserve_CCUS_agg'] < 0] = 0
    data_merged_selected_unique['ECIFCommitted_agg'][data_merged_selected_unique['ECIFCommitted_agg'] < 0] = 0

    # #Step - 3
    df_aal_data_features = pd.merge(data_merged_selected_unique, data_advanalyticslivedata_final, how='left', left_on=[
                                    'opty_id'], right_on=['OpportunityID'])

    # step-4

    fee_type = data_final_srvc[['opty_id', 'pkg_id',
                                'FeeType']].drop_duplicates().reset_index(drop=True)
    fee_type["feetypecount"] = fee_type.groupby(['opty_id', 'FeeType'])[
        'FeeType'].transform("count")
    fee_type["optycount"] = fee_type.groupby(
        ['opty_id'])['opty_id'].transform("count")
    fee_type["FeeTypePresent"] = fee_type['feetypecount']/fee_type['optycount']
    fee_type.drop(['pkg_id', 'feetypecount', 'optycount'],
                  axis=1, inplace=True)
    fee_type = fee_type.drop_duplicates().reset_index(drop=True)
    fee_type_pivot = pd.pivot_table(fee_type, values='FeeTypePresent', index=['opty_id'],
                                    columns=['FeeType'], aggfunc=np.sum, fill_value=0).reset_index('opty_id')
    # fee_type_pivot['Time & Materials'] = fee_type_pivot['Time & Materials'] + fee_type_pivot['T & M Cap']
    # fee_type_pivot.drop(['T & M Cap'], axis=1, inplace=True)

    if('T & M Cap' in (fee_type_pivot.columns)):
        fee_type_pivot['Time & Materials'] = fee_type_pivot['Time & Materials'] + \
            fee_type_pivot['T & M Cap']
        fee_type_pivot.drop(['T & M Cap'], axis=1, inplace=True)
    elif('Time & Materials' in (fee_type_pivot.columns)):
        fee_type_pivot['Time & Materials'] = fee_type_pivot['Time & Materials']

    else:
        fee_type_pivot['Fixed Fee'] = fee_type_pivot['Fixed Fee']

    # #Step-5

    resource_mix = data_final_srvc[['opty_id', 'ResourceTier',
                                    'Total Resource Hours']].drop_duplicates().reset_index(drop=True)
    resource_mix['Total Resource Hours'] = resource_mix.groupby(['opty_id', 'ResourceTier'])[
        'Total Resource Hours'].transform(np.sum).astype(np.float64)
    resource_mix = resource_mix.drop_duplicates().reset_index(drop=True)
    resource_mix['Opty Resource Hours'] = resource_mix.groupby(
        ['opty_id'])['Total Resource Hours'].transform(np.sum).astype(np.float64)
    resource_mix['Opty Resource Percent'] = resource_mix['Total Resource Hours'] / \
        resource_mix['Opty Resource Hours']
    resource_mix.drop(
        ['Total Resource Hours', 'Opty Resource Hours'], axis=1, inplace=True)
    resource_mix_pivot = pd.pivot_table(resource_mix, values='Opty Resource Percent', index=['opty_id'],
                                        columns=['ResourceTier'], aggfunc=np.sum, fill_value=0).reset_index('opty_id')
    # resource_mix_pivot.drop(['Other'], axis=1, inplace=True)
    if ('Other' in resource_mix_pivot.columns):
        resource_mix_pivot.drop(['Other'], axis=1, inplace=True)
    else:
        pass

    # Step-6
    df_aal_data_features_feetype_resourcemix = pd.merge(
        df_aal_data_features, fee_type_pivot, how='left', left_on=['opty_id'], right_on=['opty_id'])
    df_aal_data_features_feetype_resourcemix = pd.merge(
        df_aal_data_features_feetype_resourcemix, resource_mix_pivot, how='left', left_on=['opty_id'], right_on=['opty_id'])

    # #Step-7
    df_aal_data_features_feetype_resourcemix['Discount_CCUS_agg%'] = (df_aal_data_features_feetype_resourcemix['Discount_CCUS_agg'] / (
        df_aal_data_features_feetype_resourcemix['Discount_CCUS_agg'] + df_aal_data_features_feetype_resourcemix['Revenue_CCUS_agg']))*100
    df_aal_data_features_feetype_resourcemix['BIF_agg%'] = (df_aal_data_features_feetype_resourcemix['BIF_agg'] / (
        df_aal_data_features_feetype_resourcemix['BIF_agg'] + df_aal_data_features_feetype_resourcemix['Revenue_CCUS_agg']))*100
    df_aal_data_features_feetype_resourcemix['ECIFCommitted_agg%'] = (df_aal_data_features_feetype_resourcemix['ECIFCommitted_agg'] / (
        df_aal_data_features_feetype_resourcemix['ECIFCommitted_agg'] + df_aal_data_features_feetype_resourcemix['Revenue_CCUS_agg']))*100

    # Imputation
    # Imputation
    df_aal_data_features_feetype_resourcemix['Discount_CCUS_agg%'] = df_aal_data_features_feetype_resourcemix['Discount_CCUS_agg%'].fillna(
        0)
    df_aal_data_features_feetype_resourcemix['BIF_agg%'] = df_aal_data_features_feetype_resourcemix['BIF_agg%'].fillna(
        0)
    df_aal_data_features_feetype_resourcemix['ECIFCommitted_agg%'] = df_aal_data_features_feetype_resourcemix['ECIFCommitted_agg%'].fillna(
        0)
    df_aal_data_features_feetype_resourcemix['Risk_Reserve_CCUS_agg'] = df_aal_data_features_feetype_resourcemix['Risk_Reserve_CCUS_agg'].fillna(
        0)
    df_aal_data_features_feetype_resourcemix['is S500 Flag'][df_aal_data_features_feetype_resourcemix['is S500 Flag'].isna(
    )] = 'No'
    df_aal_data_features_feetype_resourcemix['ACRPotentialRevenue'][
        df_aal_data_features_feetype_resourcemix['ACRPotentialRevenue'].isna()] = 0

    if ('Time & Materials' in df_aal_data_features_feetype_resourcemix.columns):
        df_aal_data_features_feetype_resourcemix['Time & Materials'][
            df_aal_data_features_feetype_resourcemix['Time & Materials'].isna()] = 0
    if ('Fixed Fee' in df_aal_data_features_feetype_resourcemix.columns):
        df_aal_data_features_feetype_resourcemix['Fixed Fee'][df_aal_data_features_feetype_resourcemix['Fixed Fee'].isna(
        )] = 0
    if ('Tier 1: Sr Architect' in df_aal_data_features_feetype_resourcemix.columns):
        df_aal_data_features_feetype_resourcemix['Tier 1: Sr Architect'][
            df_aal_data_features_feetype_resourcemix['Tier 1: Sr Architect'].isna()] = 0
    if ('Tier 2: Architect' in df_aal_data_features_feetype_resourcemix.columns):
        df_aal_data_features_feetype_resourcemix['Tier 2: Architect'][
            df_aal_data_features_feetype_resourcemix['Tier 2: Architect'].isna()] = 0
    if ('Tier 3: Sr PjM/Cons/ADE' in df_aal_data_features_feetype_resourcemix.columns):
        df_aal_data_features_feetype_resourcemix['Tier 3: Sr PjM/Cons/ADE'][
            df_aal_data_features_feetype_resourcemix['Tier 3: Sr PjM/Cons/ADE'].isna()] = 0
    if ('Tier 4: PjM/Cons/ADE' in df_aal_data_features_feetype_resourcemix.columns):
        df_aal_data_features_feetype_resourcemix['Tier 4: PjM/Cons/ADE'][
            df_aal_data_features_feetype_resourcemix['Tier 4: PjM/Cons/ADE'].isna()] = 0
    if ('Tier 5: GD/Subcon' in df_aal_data_features_feetype_resourcemix.columns):
        df_aal_data_features_feetype_resourcemix['Tier 5: GD/Subcon'][
            df_aal_data_features_feetype_resourcemix['Tier 5: GD/Subcon'].isna()] = 0

    if (df_aal_data_features['RiskRating'].value_counts().index.size == 0):
        df_aal_data_features['RiskRating'] = 3
        df_aal_data_features_feetype_resourcemix['RiskRating'][df_aal_data_features_feetype_resourcemix['RiskRating'].isna(
        )] = df_aal_data_features['RiskRating'].value_counts().index[0]
    else:
        df_aal_data_features_feetype_resourcemix['RiskRating'][df_aal_data_features_feetype_resourcemix['RiskRating'].isna(
        )] = df_aal_data_features['RiskRating'].value_counts().index[0]

    if (df_aal_data_features['RiskRating'].value_counts().index.size == 0):
        df_aal_data_features['RiskRating'] = 3
        df_aal_data_features_feetype_resourcemix['RiskRating'][df_aal_data_features_feetype_resourcemix['RiskRating']
                                                               == 'NA'] = df_aal_data_features['RiskRating'].value_counts().index[0]
    else:
        df_aal_data_features_feetype_resourcemix['RiskRating'][df_aal_data_features_feetype_resourcemix['RiskRating']
                                                               == 'NA'] = df_aal_data_features['RiskRating'].value_counts().index[0]

    if (df_aal_data_features['FeeType'].value_counts().index.size == 0):
        df_aal_data_features['FeeType'] = 'T&M'
        df_aal_data_features_feetype_resourcemix['FeeType'][df_aal_data_features_feetype_resourcemix['FeeType'].isna(
        )] = df_aal_data_features['FeeType'].value_counts().index[0]
    else:
        df_aal_data_features_feetype_resourcemix['FeeType'][df_aal_data_features_feetype_resourcemix['FeeType'].isna(
        )] = df_aal_data_features['FeeType'].value_counts().index[0]

    if (df_aal_data_features['FeeType'].value_counts().index.size == 0):
        df_aal_data_features['FeeType'] = 'T&M'
        df_aal_data_features_feetype_resourcemix['FeeType'][df_aal_data_features_feetype_resourcemix['FeeType']
                                                            == ""] = df_aal_data_features['FeeType'].value_counts().index[0]
    else:
        df_aal_data_features_feetype_resourcemix['FeeType'][df_aal_data_features_feetype_resourcemix['FeeType']
                                                            == ""] = df_aal_data_features['FeeType'].value_counts().index[0]

    # step-8
    disc_bins = [-1, 0, 3, 10, 18, 100]
    df_aal_data_features_feetype_resourcemix['binned_disc'] = pd.cut(df_aal_data_features_feetype_resourcemix['Discount_CCUS_agg%'], disc_bins, labels=[
                                                                     '0% Discount', '0%-3% Discount', '3%-10% Discount', '10%-18% Discount', '18%-100% Discount'])

    risk_reserve_bins = [-1, 0, 7618.41, 18500, 49814.16, 22836934.63]
    df_aal_data_features_feetype_resourcemix['binned_riskreserve'] = pd.cut(df_aal_data_features_feetype_resourcemix['Risk_Reserve_CCUS_agg'], risk_reserve_bins, labels=[
                                                                            '0 RR', '0-7618 RR', '7618-18500 RR', '18500-49814 RR', '49814-22836934 RR'])

    ecifcommitted_bins = [-1, 0, 100]
    df_aal_data_features_feetype_resourcemix['binned_ecifcommitted'] = pd.cut(
        df_aal_data_features_feetype_resourcemix['ECIFCommitted_agg%'], ecifcommitted_bins, labels=['0% ecif', '0-100% ecif'])

    # if (df_aal_data_features_feetype_resourcemix['RiskRating'].value_counts().index.size != 0):
    RiskRating_groups = [-1, 0, 1, 3, 5]
    df_aal_data_features_feetype_resourcemix['RiskRating_levels'] = pd.cut(
        df_aal_data_features_feetype_resourcemix['RiskRating'].astype(int), RiskRating_groups, labels=['NULL', 'High', 'Medium', 'Low'])

    df_aal_data_features_feetype_resourcemix['FeeType1'] = df_aal_data_features_feetype_resourcemix['FeeType'].replace({
                                                                                                                       'Mixed': 'T&M', 'T&M Cap': 'T&M'})

    ecif_bins = [-1, 0, 45, 60, 75, 100]
    df_aal_data_features_feetype_resourcemix['binned_ecif'] = pd.cut(
        df_aal_data_features_feetype_resourcemix['ECIFCommitted_agg%'], ecif_bins)

    if ('Time & Materials' in df_aal_data_features_feetype_resourcemix.columns):
        TandM_bins = [-1, 0, 0.43, 0.99, 1]
        df_aal_data_features_feetype_resourcemix['binned_TandM'] = pd.cut(
            df_aal_data_features_feetype_resourcemix['Time & Materials'], TandM_bins)

    if ('Tier 1: Sr Architect' in df_aal_data_features_feetype_resourcemix.columns):
        tier1_bins = [-1, 0, 0.08, 0.16, 0.4, 1]
        df_aal_data_features_feetype_resourcemix['binned_Tier 1: Sr Architect'] = pd.cut(
            df_aal_data_features_feetype_resourcemix['Tier 1: Sr Architect'], tier1_bins)

    if ('Tier 2: Architect' in df_aal_data_features_feetype_resourcemix.columns):
        tier2_bins = [-1, 0, 0.05, 0.09, 0.13, 0.18, 0.27, 0.5, 1]
        df_aal_data_features_feetype_resourcemix['binned_Tier 2: Architect'] = pd.cut(
            df_aal_data_features_feetype_resourcemix['Tier 2: Architect'], tier2_bins)

    if ('Tier 3: Sr PjM/Cons/ADE' in df_aal_data_features_feetype_resourcemix.columns):
        tier3_bins = [-1, 0, 0.03, 0.1, 0.19, 0.3, 0.43, 0.6, 0.82, 1]
        df_aal_data_features_feetype_resourcemix['binned_Tier 3: Sr PjM/Cons/ADE'] = pd.cut(
            df_aal_data_features_feetype_resourcemix['Tier 3: Sr PjM/Cons/ADE'], tier3_bins)

    if ('Tier 4: PjM/Cons/ADE' in df_aal_data_features_feetype_resourcemix.columns):
        tier4_bins = [-1, 0, 0.01, 0.03, 0.06, 0.11, 0.17, 0.26, 0.41, 0.67, 1]
        df_aal_data_features_feetype_resourcemix['binned_Tier 4: PjM/Cons/ADE'] = pd.cut(
            df_aal_data_features_feetype_resourcemix['Tier 4: PjM/Cons/ADE'], tier4_bins)

    if ('Tier 5: GD/Subcon' in df_aal_data_features_feetype_resourcemix.columns):
        tier5_bins = [-1, 0, 0.08, 0.28, 0.48, 0.63, 0.81, 1]
        df_aal_data_features_feetype_resourcemix['binned_Tier 5: GD/Subcon'] = pd.cut(
            df_aal_data_features_feetype_resourcemix['Tier 5: GD/Subcon'], tier5_bins)

    #Step - 9
    df_aal_data_features_feetype_resourcemix_grouped = df_aal_data_features_feetype_resourcemix.groupby(
        ['opty_id', 'RiskRating_levels', 'FeeType1'])['Risk_Reserve_CCUS_agg'].sum().reset_index()
    df_aal_data_features_feetype_resourcemix_grouped_merged = pd.merge(df_aal_data_features_feetype_resourcemix, df_aal_data_features_feetype_resourcemix_grouped, how='left',
                                                                       left_on=['opty_id', 'RiskRating_levels', 'FeeType1'], right_on=['opty_id', 'RiskRating_levels', 'FeeType1'])

    #Step - 10

    column_list = ['opty_id', 'opportunitystatus', 'binned_ecif', 'ACRPotentialRevenue', 'is S500 Flag', 'binned_disc', 'binned_riskreserve', 'RiskRating_levels',
                   'FeeType1', 'binned_TandM', 'binned_Tier 1: Sr Architect', 'binned_Tier 2: Architect', 'binned_Tier 3: Sr PjM/Cons/ADE',
                   'binned_Tier 4: PjM/Cons/ADE', 'binned_Tier 5: GD/Subcon']

    Present_columns = [
        i for i in column_list if i in df_aal_data_features_feetype_resourcemix_grouped_merged.columns]
    Not_present = [
        i for i in column_list if i not in df_aal_data_features_feetype_resourcemix_grouped_merged.columns]

    final_df_op = df_aal_data_features_feetype_resourcemix_grouped_merged[Present_columns]

    for i in Not_present:
        final_df_op[i] = np.nan

    final_df_op = final_df_op.drop_duplicates()

    # # #Step - 11
    final_df_op['binned_ecif is S500 Flag ACRPotentialRevenue'] = final_df_op['binned_ecif'].astype(
        str) + '&' + final_df_op['is S500 Flag'].astype(str) + '&' + final_df_op['ACRPotentialRevenue'].astype(str)
    final_df_op['binned_riskreserve_RiskRating_levels_FeeType1'] = final_df_op['binned_riskreserve'].astype(
        str) + '&' + final_df_op['RiskRating_levels'].astype(str) + '&' + final_df_op['FeeType1'].astype(str)
    final_df_op['binned_disc is S500 Flag ACRPotentialRevenue'] = final_df_op['binned_disc'].astype(
        str) + '&' + final_df_op['is S500 Flag'].astype(str) + '&' + final_df_op['ACRPotentialRevenue'].astype(str)

    #Step - 1.1
    Fin_features = final_df_op.copy()
    Fin_features = Fin_features.rename(columns={'binned_ecif is S500 Flag ACRPotentialRevenue': 'binned_ecif_is_S500_Flag_ACRPotentialRevenue', 'binned_disc is S500 Flag ACRPotentialRevenue': 'binned_disc_is_S500_Flag_ACRPotentialRevenue', 'binned_Tier 1: Sr Architect': 'binned_Tier_1__Sr_Architect',
                                       'binned_Tier 2: Architect': 'binned_Tier_2__Architect', 'binned_Tier 3: Sr PjM/Cons/ADE': 'binned_Tier_3__Sr_PjM_Cons_ADE', 'binned_Tier 4: PjM/Cons/ADE': 'binned_Tier_4__PjM_Cons_ADE', 'binned_Tier 5: GD/Subcon': 'binned_Tier_5__GD_Subcon'})

    Fin_features_small = Fin_features[["opty_id", "binned_ecif_is_S500_Flag_ACRPotentialRevenue", "binned_disc_is_S500_Flag_ACRPotentialRevenue", "binned_riskreserve_RiskRating_levels_FeeType1",
                                       "binned_ecif", "binned_TandM", "binned_Tier_1__Sr_Architect", "binned_Tier_2__Architect", "binned_Tier_3__Sr_PjM_Cons_ADE", "binned_Tier_4__PjM_Cons_ADE", "binned_Tier_5__GD_Subcon"]]
    Fin_features_small = Fin_features_small.rename(columns={'binned_ecif_is_S500_Flag_ACRPotentialRevenue': 'binned_ecif.is.S500.Flag.ACRPotentialRevenue', 'binned_disc_is_S500_Flag_ACRPotentialRevenue': 'binned_disc.is.S500.Flag.ACRPotentialRevenue', 'binned_Tier_1__Sr_Architect': 'binned_Tier.1..Sr.Architect',
                                                   'binned_Tier_2__Architect': 'binned_Tier.2..Architect', 'binned_Tier_3__Sr_PjM_Cons_ADE': 'binned_Tier.3..Sr.PjM.Cons.ADE', 'binned_Tier_4__PjM_Cons_ADE': 'binned_Tier.4..PjM.Cons.ADE', 'binned_Tier_5__GD_Subcon': 'binned_Tier.5..GD.Subcon'})

    # filtering only one oppty
    dataframe1_filtered = dataframe1_new[dataframe1_new['Opportunity ID'].isin(
        finance_final_input['opty_id'])]
    dataframe1 = dataframe1_filtered.copy()

    #dataframe1 = dataframe1_new.copy()

    dataframe1 = pd.merge(dataframe1, Fin_features_small,
                          left_on="Opportunity ID", right_on="opty_id", how='left')
    dataframe1 = pd.merge(dataframe1, Oppty_Amendment, left_on="Opportunity ID",
                          right_on="Package_Opportunity_Id", how='left')
    dataframe1.drop(
        columns=['opty_id', 'Package_Opportunity_Id'], axis=1, inplace=True)

    # Step-1.2
    # Python changes
    dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] = np.where(dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'].isnull(
    ), "0% Discount&No&0", dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_riskreserve_RiskRating_levels_FeeType1'] = np.where(dataframe1['binned_riskreserve_RiskRating_levels_FeeType1'].isnull(
    ), "0 RR&Low&FF", dataframe1['binned_riskreserve_RiskRating_levels_FeeType1'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'].isnull(
    ), "(-1, 0]&No&0", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_TandM'] = np.where(
        dataframe1['binned_TandM'].isnull(), "(-1.0, 0.0]", dataframe1['binned_TandM'])

    dataframe1['binned_Tier.1..Sr.Architect'] = np.where(dataframe1['binned_Tier.1..Sr.Architect'].isnull(
    ), "(-1.0, 0.0]", dataframe1['binned_Tier.1..Sr.Architect'])
    dataframe1['binned_Tier.2..Architect'] = np.where(dataframe1['binned_Tier.2..Architect'].isnull(
    ), "(-1.0, 0.0]", dataframe1['binned_Tier.2..Architect'])
    dataframe1['binned_Tier.3..Sr.PjM.Cons.ADE'] = np.where(dataframe1['binned_Tier.3..Sr.PjM.Cons.ADE'].isnull(
    ), "(-1.0, 0.0]", dataframe1['binned_Tier.3..Sr.PjM.Cons.ADE'])
    dataframe1['binned_Tier.5..GD.Subcon'] = np.where(dataframe1['binned_Tier.5..GD.Subcon'].isnull(
    ), "(-1.0, 0.0]", dataframe1['binned_Tier.5..GD.Subcon'])
    dataframe1['binned_Tier.4..PjM.Cons.ADE'] = np.where(dataframe1['binned_Tier.4..PjM.Cons.ADE'].isnull(
    ), "(-1.0, 0.0]", dataframe1['binned_Tier.4..PjM.Cons.ADE'])

    dataframe1['Amendment_Opportunity_Flag'] = np.where(
        dataframe1['Amendment_Opportunity_Flag'].isnull(), 0, dataframe1['Amendment_Opportunity_Flag'])
    dataframe1['Amendment_Opportunity_Flag'] = dataframe1['Amendment_Opportunity_Flag'].astype(
        'int').astype('object')

    dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] == "0%-3% Discount&No&1500000", "0%-3% Discount&No&1000000", dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] == "18%-100% Discount&No&1500000", "18%-100% Discount&No&1000000", dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'])

    dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] = dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'].str.replace(
        "18%-100% Discount", "18%+ Discount")
    dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] = dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'].str.replace(
        "3%-10% Discount", "[3%-10%] Discount")

    # check lines
    dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'] = np.where(dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'].str.startswith(
        "0% Discount"), '0% Discount', dataframe1['binned_disc.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'].str.startswith(
        "(-1, 0]"), '0% ECIF', dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])

    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(0, 45]&No&1000000", "(0, 45]&No&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(0, 45]&Yes&1500000", "(0, 45]&Yes&1000000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(45, 60]&Yes&1000000", "(45, 60]&Yes&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(45, 60]&Yes&1500000", "(45, 60]&Yes&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(60, 75]&Yes&1000000", "(60, 75]&Yes&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])

    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(60, 75]&Yes&1500000", "(60, 75]&Yes&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(60, 75]&Yes&1500000", "(60, 75]&Yes&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(75, 100]&Yes&250000", "(75, 100]&Yes&0", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(60, 75]&No&1000000", "(60, 75]&No&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(75, 100]&No&1500000", "(75, 100]&No&1000000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(45, 60]&Yes&250000", "(45, 60]&Yes&0", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])
    dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] = np.where(
        dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'] == "(75, 100]&No&1000000", "(75, 100]&No&250000", dataframe1['binned_ecif.is.S500.Flag.ACRPotentialRevenue'])

    dataframe1 = pd.merge(dataframe1, soft_exception,
                          left_on="Opportunity ID", right_on="OpportunityId")
    dataframe1.drop(columns=['OpportunityId'], axis=1, inplace=True)

    #Step - 1.3
    dataframe1.rename(columns={'Commercial_Active_Oppty_Count_Bucketted': 'Commercial.Active.Oppty.Count_Bucketted', 'Owner_Win_Rate_Bucketted': 'Owner.Win.Rate_Bucketted',
                      'Tpid_Win_Rate_Bucketted': 'Tpid.Win.Rate_Bucketted', 'AvgCSATScore_Binned': 'AvgCSATScore.Binned', 'Consulting_Action': 'Consulting.Action'}, inplace=True)
    dataframe1 = dataframe1[~dataframe1['PPG_FeeType'].isin(
        ['App Dev _ null', 'Azure Security _ null', 'Biz Apps _ null', '', 'Data & AI _ null', 'Infra _ null', 'MW _ null', 'MW Security _ null', 'null _ null'])]

    #Step - 1.4
    cols = ['Has SSSP', 'SSSP Ownership', 'Is Global', 'Digital Advisory Curr Flag', 'Is Tpid Active Support Contract',
            'PrimarySponsorBDM', 'ExternalStallingFlag', 'POC', 'Accountplankey', 'Consulting.Action']

    for col in cols:
        dataframe1[col] = dataframe1[col].astype('object')

    # Amendment_Opportunity_Flag has float values instead of int - so converting to int then astyping to str to remove after decmial places
    dataframe1['Amendment_Opportunity_Flag'] = dataframe1['Amendment_Opportunity_Flag'].astype(
        'int').astype('object')

    #Step - 1.5
    col_model = col_model_new.copy()
    col_model = col_model['features'].tolist()

    df_model = dataframe1[col_model]
    df_model = pd.get_dummies(df_model, prefix_sep='')

    # Step 1.6
    # dropping features that are in dataset but not in coeff file -  baseline features
    drop_f = list(set(df_model.columns) - set(coeff['Coefficient_name']))
    df_model.drop(columns=drop_f, inplace=True)

    # Adding features to dataset that are in coeff file but not in dataset, assigning value 0
    add_f = set(coeff['Coefficient_name']) - set(df_model.columns)

    for col in add_f:
        df_model[col] = 0

    # Changing value for intercept column to 1
    df_model['Intercept'] = 1

    # Step 1.7
    # CHanging order of columns as we have in coeff dataframe
    df_model = df_model[coeff['Coefficient_name'].tolist()]

    #Step- 1.8
    score = np.dot(df_model, coeff[['Beta_values_ln']]).reshape(
        df_model.shape[0])
    z = 1/(1 + np.exp(-score))

    #Step- 1.9
    dataframe1['Won'] = z
    dataframe1['Lost'] = 1-z

    #step - 1.10
    FinalData_to_upload = dataframe1.copy()

    # Python Change
    Seller_Narratives = Seller_Narratives_new.copy()

    Seller_Narratives['Odds_Ratio'] = pd.to_numeric(
        Seller_Narratives['Odds_Ratio'], errors='coerce')
    Seller_Narratives['MaxOdds_Ratio'] = pd.to_numeric(
        Seller_Narratives['MaxOdds_Ratio'], errors='coerce')
    Feature_Contribution_small = Feature_Contribution[["feature", "max"]]
    Feature_Contribution_star = Feature_Contribution[[
        "feature", "Feature_Star"]]

    dataframe1['Cloud_Partner'] = np.where(
        dataframe1['Cloud_Partner'] == "Other", "AA", dataframe1['Cloud_Partner'])
    dataframe1['ClosePlanExists'] = np.where(
        dataframe1['ClosePlanExists'] == 'Yes', 1, 0)
    dataframe1['ExternalStallingFlag'] = np.where(
        dataframe1['ExternalStallingFlag'] == 1, "TRUE", "FALSE")
    dataframe1['Cloud_Partner'] = np.where(
        dataframe1['Cloud_Partner'] == "AA", "Other", "Cloud_1")
    dataframe1['Total Resources'] = dataframe1['Total Resources'].astype('str')

    Seller_Narratives.loc[Seller_Narratives['Feature_Name'] == 'Intercept',
                          'MaxOdds_Ratio'] = Seller_Narratives.loc[Seller_Narratives['Feature_Name'] == 'Intercept', 'Average']
    Oppty_Narratives = dataframe1[["Opportunity ID", "Has SSSP", "SSSP Ownership", "Total Resources", "Is Global", "PreviousDAcountBucket", "CombinationIteration", "incidentBucket", "Avg_Resource_Experience_Bucket", "GrossNWSBucket", "approvedHoursBucket",
                                   "GrowthLicensingSpendBucket", "AvgResourceWinRateBucket", "Digital Advisory Curr Flag", "PPG_FeeType", "Commercial.Active.Oppty.Count_Bucketted", "MonthsSlipped_Bucketted", "Owner.Win.Rate_Bucketted", "Tpid.Win.Rate_Bucketted", "Is Tpid Active Support Contract", "PrimarySponsorBDM", "ExternalStallingFlag",
                                   "ClosePlanExists", "Domain PreSales Indicator", "POC", "StandardOfferingType", "Accountplankey", "MACC_binned", "Cloud_SE", "Cloud_Partner", "Consulting.Action", "AvgCSATScore.Binned", "DBScore_Binned", "Amendment_Opportunity_Flag", "binned_disc.is.S500.Flag.ACRPotentialRevenue", "binned_ecif.is.S500.Flag.ACRPotentialRevenue",
                                   "binned_riskreserve_RiskRating_levels_FeeType1", "binned_TandM",
                                   "binned_Tier.1..Sr.Architect", "binned_Tier.2..Architect", "binned_Tier.3..Sr.PjM.Cons.ADE", "binned_Tier.4..PjM.Cons.ADE", "binned_Tier.5..GD.Subcon"]].copy()

    Oppty_Narratives = Oppty_Narratives.drop_duplicates()
    Oppty_Narratives_long = pd.melt(Oppty_Narratives, id_vars='Opportunity ID')

    Oppty_Narratives_long.columns = [
        "Opportunity ID", "Feature_Name", "Feature_Value"]
    Oppty_Narratives_long['Feature_Name'] = Oppty_Narratives_long['Feature_Name'].str.lstrip()
    Oppty_Narratives_long['Feature_Name'] = Oppty_Narratives_long['Feature_Name'].str.rstrip()
    Oppty_Narratives_long['Feature_Value'] = Oppty_Narratives_long['Feature_Value'].astype(
        str).str.lstrip()
    Oppty_Narratives_long['Feature_Value'] = Oppty_Narratives_long['Feature_Value'].astype(
        str).str.rstrip()
    Oppty_Narratives_long['Coefficient_name'] = Oppty_Narratives_long['Feature_Name'] + \
        Oppty_Narratives_long['Feature_Value']
    Oppty_Narratives_long.loc[Oppty_Narratives_long['Feature_Name']
                              == 'Total Resources', 'Coefficient_name'] = 'Total Resources'
    Oppty_Narratives_long['Coefficient_name'] = Oppty_Narratives_long['Coefficient_name'].str.strip()

    Seller_Narratives = Seller_Narratives.rename(
        columns={'Seller_Narratives': 'Seller.Narratives', 'Seller_Narratives_Other': 'Seller.Narratives.Other'})
    Seller_Narratives_small = Seller_Narratives[["Feature_Name", "Actionable_Flag", "Odds_Ratio", "MaxOdds_Ratio", "Seller.Narratives", "Coefficient_name",
                                                 "Feature_Direction", "Seller.Narratives.Other", "Average", "Rank_Feature", "Action", "Feature_Show_Hide", "Business_Feature_Name", "Level_Name"]]
    Seller_Narratives_small = Seller_Narratives_small.drop_duplicates()
    Seller_Narratives_small['Coefficient_name'] = Seller_Narratives_small['Coefficient_name'].str.lstrip()
    Seller_Narratives_small['Coefficient_name'] = Seller_Narratives_small['Coefficient_name'].str.rstrip()

    Seller_Narratives_small_intercept = Seller_Narratives_small.loc[
        Seller_Narratives_small['Feature_Name'] == 'Intercept', :]

    Oppty_Narratives_long = pd.merge(Oppty_Narratives_long, Seller_Narratives_small, left_on=[
                                     "Feature_Name", "Coefficient_name"], right_on=["Feature_Name", "Coefficient_name"], how='left')
    Oppty_Narratives_long = pd.merge(Oppty_Narratives_long, Feature_Contribution_small, left_on=[
                                     "Feature_Name"], right_on=["feature"], how='left')
    Oppty_Narratives_long.drop(columns=['feature'], axis=1, inplace=True)
    Seller_Narratives_small_intercept['Feature_Value'] = 1
    Seller_Narratives_small_intercept['max'] = 0
    Seller_Narratives_small_intercept['merge_col'] = 1
    open_oppty = dataframe1[["Opportunity ID", "Opportunity Status"]]
    open_oppty['merge_col'] = 1
    Oppty_narrative_intercept = pd.merge(
        open_oppty, Seller_Narratives_small_intercept, on='merge_col', how='left')
    Oppty_narrative_intercept.drop(
        columns=["merge_col", "Opportunity Status"], axis=1, inplace=True)

    Oppty_Narratives_long = pd.concat(
        [Oppty_Narratives_long, Oppty_narrative_intercept], axis=0)

    Oppty_Narratives_long_TR = Oppty_Narratives_long.loc[
        Oppty_Narratives_long['Feature_Name'] == 'Total Resources', :]
    Oppty_Narratives_long_TR['Odds_Ratio'] = pd.to_numeric(
        Oppty_Narratives_long_TR['Odds_Ratio'], errors='coerce')
    Oppty_Narratives_long_TR['MaxOdds_Ratio'] = pd.to_numeric(
        Oppty_Narratives_long_TR['MaxOdds_Ratio'], errors='coerce')
    Oppty_Narratives_long_TR['Feature_Value'] = pd.to_numeric(
        Oppty_Narratives_long_TR['Feature_Value'], errors='coerce')
    Oppty_Narratives_long_TR['Odds_Ratio'] = np.where(Oppty_Narratives_long_TR['Coefficient_name'] == 'Total Resources',
                                                      Oppty_Narratives_long_TR['Odds_Ratio']*Oppty_Narratives_long_TR['Feature_Value'], Oppty_Narratives_long_TR['Odds_Ratio'])
    Oppty_Narratives_long_TR['MaxOdds_Ratio'] = np.where(Oppty_Narratives_long_TR['Coefficient_name'] == 'Total Resources',
                                                         Oppty_Narratives_long_TR['MaxOdds_Ratio']*Oppty_Narratives_long_TR['Feature_Value'], Oppty_Narratives_long_TR['MaxOdds_Ratio'])

    Oppty_Narratives_long_NTR = Oppty_Narratives_long.loc[
        Oppty_Narratives_long['Feature_Name'] != "Total Resources", :]
    Oppty_Narratives_long = pd.concat(
        [Oppty_Narratives_long_TR, Oppty_Narratives_long_NTR], axis=0)
    Oppty_Narratives_long_imp = Oppty_Narratives_long.copy()
    Oppty_Narratives_long_imp['completed_task'] = np.where(Oppty_Narratives_long_imp['Actionable_Flag'] == "Non-Actionable", "NA", np.where(
        Oppty_Narratives_long_imp['MaxOdds_Ratio'] == Oppty_Narratives_long_imp['Odds_Ratio'], "completed", "pending"))
    Oppty_Narratives_long_imp = Oppty_Narratives_long_imp.drop_duplicates()

    Prop_score = FinalData_to_upload[["Opportunity ID", "Won"]]
    Prop_score['Prop_Bucket'] = np.where(Prop_score['Won'] < 0.2, "Low", np.where(
        Prop_score['Won'] < 0.374, "Medium-Low", np.where(Prop_score['Won'] < 0.8, "Medium-High", "High")))
    Oppty_Narratives_long_imp = pd.merge(
        Oppty_Narratives_long_imp, Prop_score, on='Opportunity ID', how='left')

    OpptySalesStage = dataframe1[["Opportunity ID", "SalesStage"]]
    Oppty_Narratives_long_imp_Small = Oppty_Narratives_long_imp[[
        "Opportunity ID", "Feature_Name"]]
    Oppty_Narratives_long_imp_Small = Oppty_Narratives_long_imp_Small.drop_duplicates()
    Oppty_Narratives_long_imp_SS = pd.merge(
        Oppty_Narratives_long_imp_Small, OpptySalesStage, on="Opportunity ID")
    Seller_Narrative_Sales_stage = Seller_Narratives[[
        "Feature_Name", "Earliest_Sales_Stage", "Latest_Sales_Stage"]]
    Oppty_Narratives_long_imp_SS = pd.merge(
        Oppty_Narratives_long_imp_SS, Seller_Narrative_Sales_stage, on="Feature_Name")

    Oppty_Narratives_long_imp_SS_select = Oppty_Narratives_long_imp_SS.loc[(Oppty_Narratives_long_imp_SS['SalesStage'] >= Oppty_Narratives_long_imp_SS['Earliest_Sales_Stage']) & (
        Oppty_Narratives_long_imp_SS['SalesStage'] <= Oppty_Narratives_long_imp_SS['Latest_Sales_Stage']), :]
    Oppty_Narratives_long_imp_SS_select = Oppty_Narratives_long_imp_SS_select.drop_duplicates()
    Oppty_Narratives_long_imp_SS_small = Oppty_Narratives_long_imp_SS_select[[
        "Opportunity ID", "Feature_Name"]]
    Oppty_Narratives_long_imp_SS_final = pd.merge(
        Oppty_Narratives_long_imp, Oppty_Narratives_long_imp_SS_small, on=["Opportunity ID", "Feature_Name"])

    Oppty_Narratives_long_imp_outsideSS = Oppty_Narratives_long_imp_SS.copy()
    Oppty_Narratives_long_imp_outsideSS_small = Oppty_Narratives_long_imp_outsideSS[[
        "Opportunity ID", "Feature_Name"]]
    Oppty_Narratives_long_imp_outsideSS = pd.merge(
        Oppty_Narratives_long_imp, Oppty_Narratives_long_imp_outsideSS_small, on=["Opportunity ID", "Feature_Name"])
    Oppty_Narratives_long_imp_outsideSS = Oppty_Narratives_long_imp_outsideSS.drop_duplicates()

    #Step - 1.11
    Oppty_Narratives_long_imp_test = Oppty_Narratives_long_imp.loc[
        Oppty_Narratives_long_imp['Feature_Show_Hide'] == 'Show', :]
    opty_rows = Oppty_Narratives_long_imp_test[
        Oppty_Narratives_long_imp_test['Opportunity ID'] == opt_id]

    opty_rows = opty_rows[opty_rows['Action'] != "No Action"]
    opty_rows = opty_rows.sort_values(['Average'], ascending=False)
    opty_rows = opty_rows[['Won', 'Prop_Bucket', 'Action']]
    opty_rows['id'] = range(1, len(opty_rows) + 1)

    json_output = opty_rows

    logging.info(datetime.now())

    # 'abfss://maipocaa@maipocaa.dfs.core.windows.net/Ml_service/Output_Final/Seller_Narrative_Output_File_new.json')
    # write_data_to_datalake(
    #     json.dumps(Oppty_Narratives_long_imp_test.to_dict('records')), 'Ml_service', 'Output_Final', 'Seller_Narrative_Output_File_new.json')
    return json_output
