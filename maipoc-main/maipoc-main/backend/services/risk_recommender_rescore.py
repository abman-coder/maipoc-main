import pandas as pd
import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec
import scipy.stats as stats
# import pyspark
# from pyspark.sql import SparkSession
import gower
from services.filereaders import get_data


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 100)

# Loading
# Contracttable_df = pd.read_csv('abfss://maipocaa@maipocaa.dfs.core.windows.net/Risk Recommender/Open_Deals_Resource_Grain_FY22.csv')
# df_signed = pd.read_csv('abfss://maipocaa@maipocaa.dfs.core.windows.net/Risk Recommender/Signed_Completed_Deals_FY20FY21FY22.csv')
# risk_df = pd.read_csv('abfss://maipocaa@maipocaa.dfs.core.windows.net/Risk Recommender/Signed_Completed_Deals_FY20FY21FY22_C1_YAT_risks.csv')

Contracttable_df = get_data(
    'local_files/risk_recommender/Open_Deals_Resource_Grain_FY22.csv', 'csv')
df_signed = get_data(
    'local_files/risk_recommender/Signed_Completed_Deals_FY20FY21FY22.csv', 'csv')
risk_df = get_data(
    'local_files/risk_recommender/Signed_Completed_Deals_FY20FY21FY22_C1_YAT_risks.csv', 'csv')


def scoring(Contracttable_df, df_signed, risk_df, input_json):
    # Step 1
    Contracttable_df = pd.DataFrame(input_json)
    # Contracttable_df[Contracttable_df['DealId'] == deal_id].reset_index(drop=True)
    Contracttable_df[['EstimatedStartDate', 'EstimatedEndDate']] = Contracttable_df[[
        'EstimatedStartDate', 'EstimatedEndDate']].apply(pd.to_datetime)
    Contracttable_df['Project Duration'] = (
        Contracttable_df['EstimatedEndDate'] - Contracttable_df['EstimatedStartDate']).dt.days
    Contracttable_df.loc[:, 'StandardOfferingType'] = np.where(
        Contracttable_df['StandardOfferingType'].isin(['SO', 'MSO', 'ESO']), 'SO', 'Custom')
    Contracttable_df.loc[:, 'FeeType'] = np.where(Contracttable_df['FeeType'].isin(
        ['Time & Materials', 'T & M Cap']), 'Time & Materials', 'Fixed Fee')
    Contracttable_df.loc[:, 'Domain'] = np.where(Contracttable_df['Domain'].isin(['Business Applications', 'Apps', 'Business Productivity']), 'Business Applications', np.where(
        Contracttable_df['Domain'].isin(['Azure Cloud & AI', 'Data and AI']), 'Azure Cloud & AI', 'Modern Work'))
    Contracttable_df[['PlannedPackageRevenueLOC', 'PlannedPackageRevenueCCUS', 'PlannedPackageDeliveryCostCCUS', 'EstimatedDeliveryValueLOC', 'EstimatedDeliveryValueCCUS', 'SoldMarginCCUS', 'PlannedPackageDiscountCCUS', 'ECIF', 'ResourceHours']] = Contracttable_df[[
        'PlannedPackageRevenueLOC', 'PlannedPackageRevenueCCUS', 'PlannedPackageDeliveryCostCCUS', 'EstimatedDeliveryValueLOC', 'EstimatedDeliveryValueCCUS', 'SoldMarginCCUS', 'PlannedPackageDiscountCCUS', 'ECIF', 'ResourceHours']].astype('float')
    # print(Contracttable_df.columns.values)
    df = Contracttable_df[['DealId', 'PackageId']].drop_duplicates().groupby(
        'DealId')['PackageId'].count().reset_index()
    df.rename(columns={'PackageId': 'No_of_Packages'}, inplace=True)
    # EstimatedDeliveryValueCCUS < 0 what should we do? Replace with PackageRevenue?
    Contracttable_df['Package_Flag'] = 1
    df_offering = Contracttable_df[['DealId', 'StandardOfferingType', 'EstimatedDeliveryValueCCUS']].drop_duplicates(
    ).pivot_table(index=['DealId'], columns=['StandardOfferingType'], values=['EstimatedDeliveryValueCCUS'])
    df_offering.reset_index(inplace=True)
    # print(df_offering.columns)
    df_offering.columns = df_offering.columns.droplevel()
    df_offering.columns.values[0] = 'DealId'
    missing_cols = list(set(['DealId', 'Custom', 'SO']
                            ).difference(set(df_offering.columns)))
    df_offering[missing_cols] = 0
    df_offering.loc[:, 'Custom'] = np.where(
        df_offering['Custom'] < 0, 0, df_offering['Custom'])
    df_offering.loc[:, 'SO'] = np.where(
        df_offering['SO'] < 0, 0, df_offering['SO'])
    df_offering.fillna(0, inplace=True)
    df_offering['PercentCustom'] = df_offering['Custom'] * \
        100/(df_offering['Custom']+df_offering['SO'])
    df_offering['PercentSO'] = df_offering['SO'] * \
        100/(df_offering['Custom']+df_offering['SO'])
    df_offering.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_offering.fillna(0, inplace=True)
    # print(df_offering.shape)
    # df_offering.head()
    df_fee = Contracttable_df[['DealId', 'FeeType', 'EstimatedDeliveryValueCCUS']].drop_duplicates(
    ).pivot_table(index=['DealId'], columns=['FeeType'], values=['EstimatedDeliveryValueCCUS'])
    df_fee.reset_index(inplace=True)
    # print(df_fee.columns)
    df_fee.columns = df_fee.columns.droplevel()
    df_fee.columns.values[0] = 'DealId'
    missing_cols1 = list(
        set(['DealId', 'Fixed Fee', 'Time & Materials']).difference(set(df_fee.columns)))
    df_fee[missing_cols1] = 0
    df_fee.loc[:, 'Fixed Fee'] = np.where(
        df_fee['Fixed Fee'] < 0, 0, df_fee['Fixed Fee'])
    df_fee.loc[:, 'Time & Materials'] = np.where(
        df_fee['Time & Materials'] < 0, 0, df_fee['Time & Materials'])
    df_fee.fillna(0, inplace=True)
    df_fee['PercentFixedFee'] = df_fee['Fixed Fee']*100 / \
        (df_fee['Fixed Fee']+df_fee['Time & Materials'])
    df_fee['PercentTM'] = df_fee['Time & Materials']*100 / \
        (df_fee['Fixed Fee']+df_fee['Time & Materials'])
    df_fee.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_fee.fillna(0, inplace=True)
    # print(df_fee.head())
    df_domain = Contracttable_df[['DealId', 'Domain', 'EstimatedDeliveryValueCCUS']].drop_duplicates(
    ).pivot_table(index=['DealId'], columns=['Domain'], values=['EstimatedDeliveryValueCCUS'])
    df_domain.reset_index(inplace=True)
    # print(df_domain.columns)
    df_domain.columns = df_domain.columns.droplevel()
    df_domain.columns.values[0] = 'DealId'
    missing_cols2 = list(set(['DealId', 'Azure Cloud & AI', 'Business Applications',
                         'Modern Work']).difference(set(df_domain.columns)))
    df_domain[missing_cols2] = 0
    df_domain.loc[:, 'Azure Cloud & AI'] = np.where(
        df_domain['Azure Cloud & AI'] < 0, 0, df_domain['Azure Cloud & AI'])
    df_domain.loc[:, 'Business Applications'] = np.where(
        df_domain['Business Applications'] < 0, 0, df_domain['Business Applications'])
    df_domain.loc[:, 'Modern Work'] = np.where(
        df_domain['Modern Work'] < 0, 0, df_domain['Modern Work'])
    df_domain.fillna(0, inplace=True)
    df_domain['PercentACAI'] = df_domain['Azure Cloud & AI']*100 / \
        (df_domain['Azure Cloud & AI'] +
         df_domain['Business Applications']+df_domain['Modern Work'])
    df_domain['PercentBA'] = df_domain['Business Applications']*100 / \
        (df_domain['Azure Cloud & AI'] +
         df_domain['Business Applications']+df_domain['Modern Work'])
    df_domain['PercentMW'] = df_domain['Modern Work']*100 / \
        (df_domain['Azure Cloud & AI'] +
         df_domain['Business Applications']+df_domain['Modern Work'])
    df_domain.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_domain.fillna(0, inplace=True)
    # df_domain.head()
    Contracttable_df['Resource Type Updated'] = np.where(Contracttable_df['Resource'].isin(['Domain Solution Architect', 'Senior Domain Solution Architect', 'Digital Architect', 'Area Solution Architect', 'Senior Area Solution Architect', 'Senior Digital Architect', 'GD Offshore Domain Solution Architect', 'GD Onsite Domain Solution Architect', 'Offshore Architect (Blended)', 'Offshore Domain Solution Architect', 'Onsite Domain Solution Architect', 'GitHub Senior Solution Architect', 'Associate Architect', 'Principal Enterprise Architect', 'Associate Enterprise Architect', 'Managing Architect', 'Domain Solution Architect - CL', 'WECP Architect', 'WECP Associate Architect', 'Architect (Dynamics Blended)', 'Architect (GP Blended)', 'Program Architect']), 'Architect', np.where(Contracttable_df['Resource'].isin(['Project Manager', 'Account Delivery Executive', 'Senior Account Delivery Executive', 'Engagement Manager', 'Senior Engagement Manager', 'Senior Project Manager', 'GD Offshore Project Manager', 'GD Onsite Project Manager', 'GD Offshore Delivery Data Scientist', 'Offshore Infosec', 'Offshore Project Manager (Blended)', 'Offshore Engagement Manager (Blended)', 'Offshore Project Manager', 'US Delivery Center Project Manager', 'Onsite Project Manager', 'US Delivery Center Project Manager - CL', 'GitHub Project Manager',
                                                         'Project Manager (Dynamics Blended)', 'GitHub Senior Project Manager', 'Offshore Project Manager (Blended)', 'Project Manager - CL', 'Engagement Manager - CL', 'Engagement Manager', 'Senior Engagement Manager', 'Principal Engagement Manager', 'Offshore Engagement Manager (Blended)', 'Delivery Data Scientist', 'Senior Delivery Data Scientist', 'GD Offshore Delivery Data Scientist', 'Program Director', 'Delivery Management Executive']), 'Oversight', np.where(Contracttable_df['Resource'].isin(['Senior Consultant', 'Consultant', 'GD Offshore Consultant', 'GD Onsite Consultant', 'Offshore Consultant', 'Offshore Consultant (Blended)', 'Nearshore Consultant', 'Onsite Consultant', 'WECP Associate Consultant', 'US Delivery Center Consultant - CL', 'WECP Consultant', 'WECP Senior Consultant', 'Consultant - CL', 'US Delivery Center Sr Consultant', 'Associate Consultant - CL', 'Consultant (Dynamics Blended)', 'Senior Consultant - CL', 'Consultant (GP Blended)', 'WECP Principal Consultant', 'Associate Consultant', 'Principal Consultant', 'US Delivery Center Consultant', 'Azure for Operators Consultant']), 'Consultant',                                                                                              np.where(Contracttable_df['Resource'].isin(['GD Offshore', 'GD Onsite']), 'IGD', 'SubcontractorOther'))))
    Contracttable_df['ResourceHours'] = pd.to_numeric(
        Contracttable_df['ResourceHours'])
    Contracttable_df.head()
    resource_hrs = Contracttable_df[['DealId', 'Resource Type Updated', 'ResourceHours']].groupby(
        ['DealId', 'Resource Type Updated']).agg('sum')
    # print(resource_hrs.shape)
    resource_hrs.head()
    resource_df3 = resource_hrs.pivot_table(
        index=['DealId'], columns=['Resource Type Updated'], values='ResourceHours')
    resource_df3.reset_index(inplace=True)
    missing_cols3 = list(set(['DealId', 'Oversight', 'Architect', 'Consultant',
                         'SubcontractorOther']).difference(set(resource_df3.columns)))
    resource_df3[missing_cols3] = 0
    resource_df3.fillna(0, inplace=True)
    resource_df3.head()
    resource_df3['ResourceHours'] = resource_df3[['Oversight',
                                                  'Architect', 'Consultant', 'SubcontractorOther']].sum(axis=1)
    resource_df3.head()
    resource_category = Contracttable_df[['DealId', 'ResourceCategory', 'ResourceHours']].groupby(
        ['DealId', 'ResourceCategory']).agg('sum')
    # print(resource_category.shape)
    resource_category.head()
    resource_category2 = resource_category.pivot_table(
        index=['DealId'], columns=['ResourceCategory'], values='ResourceHours')
    resource_category2.reset_index(inplace=True)
    missing_cols4 = list(set(['DealId', 'IGD', 'Subcon', 'TZ FTE']).difference(
        set(resource_category2.columns)))
    resource_category2[missing_cols4] = 0
    resource_category2.fillna(0, inplace=True)
    # resource_df3.head()

    # Step 2
    df = df.merge(df_offering, how='left', left_on='DealId', right_on='DealId')
    df = df.merge(df_fee, how='left', left_on='DealId', right_on='DealId')
    df = df.merge(df_domain, how='left', left_on='DealId', right_on='DealId')
    df = df.merge(resource_df3, how='left',
                  left_on='DealId', right_on='DealId')
    df = df.merge(resource_category2, how='left',
                  left_on='DealId', right_on='DealId')
    # print(df.shape)
    # print(df[(df['Oversight']<0)|(df['Architect']<0)|(df['Consultant']<0)|(df['SubcontractorOther']<0)].shape) #381
    # impute resource hours with 0 where it is less than 0 total resource hours will also change accordingly
    df.loc[:, 'Oversight'] = np.where(df['Oversight'] < 0, 0, df['Oversight'])
    df.loc[:, 'Architect'] = np.where(df['Architect'] < 0, 0, df['Architect'])
    df.loc[:, 'Consultant'] = np.where(
        df['Consultant'] < 0, 0, df['Consultant'])
    #print(df[(df['IGD']<0)|(df['Subcon']<0)|(df['TZ FTE']<0)].shape)
    df.loc[:, 'IGD'] = np.where(df['IGD'] < 0, 0, df['IGD'])
    df.loc[:, 'Subcon'] = np.where(df['Subcon'] < 0, 0, df['Subcon'])
    df.loc[:, 'TZ FTE'] = np.where(df['TZ FTE'] < 0, 0, df['TZ FTE'])
    df['Resource Hrs Updated'] = df[['Oversight', 'Architect',
                                     'Consultant', 'SubcontractorOther']].sum(axis=1)
    # print(df[(df['Oversight']<0)|(df['Architect']<0)|(df['Consultant']<0)|(df['SubcontractorOther']<0)].shape) #381
    df['PercentOversight'] = df['Oversight']*100/df['Resource Hrs Updated']
    df['PercentArchitect'] = df['Architect']*100/df['Resource Hrs Updated']
    df['PercentConsultant'] = df['Consultant']*100/df['Resource Hrs Updated']
    df['PercentIGD'] = df['IGD']*100/(df['IGD']+df['Subcon']+df['TZ FTE'])
    df['PercentSubcon'] = df['Subcon']*100 / \
        (df['IGD']+df['Subcon']+df['TZ FTE'])
    df['PercentTZFTE'] = df['TZ FTE']*100/(df['IGD']+df['Subcon']+df['TZ FTE'])
    df.fillna(0, inplace=True)
    # df.head()

    # Step 3
    df2 = Contracttable_df[['DealId', 'ContractID', 'PlannedPackageRevenueCCUS', 'PlannedPackageDeliveryCostCCUS', 'PlannedPackageRevenueLOC', 'SoldMarginCCUS',
                            'ECIF', 'EstimatedDeliveryValueCCUS', 'PlannedPackageDiscountCCUS']].drop_duplicates().groupby(['DealId', 'ContractID']).sum().reset_index()
    df2['ECIF_Percent'] = np.where(
        df2['ECIF'] > 0, df2['ECIF'].div(df2['PlannedPackageRevenueCCUS']), 0)
    #df2 = df2[(df2['EstimatedDeliveryValueCCUS']>0) & (df2['PlannedPackageRevenueCCUS']>0)].reset_index(drop=True)
    df2.drop('ContractID', axis=1, inplace=True)
    Contracttable_df = Contracttable_df[Contracttable_df['DealId'].isin(
        df2['DealId'])].reset_index(drop=True)
    Contracttable_df['PPG'] = np.where(Contracttable_df['PPG'].isin(
        [None]), 'Unknown', Contracttable_df['PPG'])
    Contracttable_df['PrimaryProductName'] = np.where(Contracttable_df['PrimaryProductName'].isin(
        [None]), 'Unknown', Contracttable_df['PrimaryProductName'])
    final_df = Contracttable_df[['DealId', 'PrimaryProductName', 'PPG', 'PlannedPackageRevenueCCUS']].groupby(
        ['DealId', 'PrimaryProductName', 'PPG'])['PlannedPackageRevenueCCUS'].sum().reset_index()
    final_df['Rev_Rank'] = final_df.groupby(
        ['DealId'])['PlannedPackageRevenueCCUS'].rank(ascending=False, method='min')
    final_df = final_df[final_df['Rev_Rank'] == 1].reset_index(drop=True)
    # print(final_df.shape,final_df['DealId'].nunique())
    final_df['PPG_Rank'] = final_df.groupby(['DealId']).cumcount()+1
    final_df = final_df[final_df['PPG_Rank'] == 1].reset_index(drop=True)
    final_df.drop(
        ['Rev_Rank', 'PPG_Rank', 'PlannedPackageRevenueCCUS'], axis=1, inplace=True)
    # print(final_df.shape,final_df['DealId'].nunique())
    # final_df.groupby('DealId')['DealId'].count().sort_values(ascending=False)

    # Step 4
    final_df = final_df.merge(Contracttable_df[['DealId', 'ContractID', 'Area', 'AccountIndustryName', 'AccountSegmentName', 'IsGlobal', 'PrimaryProductName', 'PPG', 'NSTCategory', 'CloudFlag', 'Overall Risk Rating Original', 'Project Duration',
                              'Contract Status Group', 'Agreement Setup Completed Date Fiscal Year', 'Estimated Start Date Fiscal Year']].drop_duplicates(), how='left', left_on=['DealId', 'PrimaryProductName', 'PPG'], right_on=['DealId', 'PrimaryProductName', 'PPG'])
    # print(final_df.shape)
    final_df = final_df.merge(
        df, how='left', left_on='DealId', right_on='DealId')
    # print(final_df.shape)
    final_df = final_df.merge(
        df2, how='left', left_on='DealId', right_on='DealId')
    # print(final_df.shape)
    # final_df.head()
    final_df['D8'] = np.where(final_df['Area'].isin(
        ['ANZ', 'Canada', 'Western Europe', 'France', 'Germany', 'Japan', 'UK', 'United States']), 'D8', 'Rest')
    df_signed['D8'] = np.where(df_signed['Area'].isin(
        ['ANZ', 'Canada', 'Western Europe', 'France', 'Germany', 'Japan', 'UK', 'United States']), 'D8', 'Rest')

    scopefinriskcols = ['Area', 'AccountIndustryName', 'AccountSegmentName', 'IsGlobal', 'No_of_Packages', 'PercentCustom', 'PercentSO', 'PrimaryProductName', 'PPG', 'PercentACAI', 'PercentBA', 'PercentMW', 'PercentFixedFee', 'PercentTM', 'PlannedPackageRevenueCCUS',
                        'PlannedPackageDeliveryCostCCUS', 'EstimatedDeliveryValueCCUS', 'SoldMarginCCUS', 'PlannedPackageDiscountCCUS', 'ECIF_Percent', 'PercentOversight', 'PercentArchitect', 'PercentConsultant', 'PercentIGD', 'PercentSubcon', 'PercentTZFTE', 'NSTCategory', 'CloudFlag', 'Project Duration']
    final_df[scopefinriskcols].head()  # take only base contracts
    w = [1]*28
    w.insert(0, 2)
    # print(w)
    wt = np.asarray(w)
    # print(wt)
    df_signed_D8 = df_signed[df_signed['D8'] == 'D8'].reset_index(drop=True)
    df_signed_Rest = df_signed[df_signed['D8']
                               == 'Rest'].reset_index(drop=True)
    df_open_D8 = final_df[final_df['D8'] == 'D8'].reset_index(drop=True)
    df_open_Rest = final_df[final_df['D8'] == 'Rest'].reset_index(drop=True)
    df3_1 = df_signed_D8.iloc[0:3000, :]
    df3_2 = df_signed_D8.iloc[3000:, :].reset_index(drop=True)
    # print(df3_1.shape,df3_2.shape)

    # step 5
    final_sim_df = pd.DataFrame(data=None, columns=df_signed.columns)
    final_sim_df['DealType'] = None
    final_sim_df['Distance'] = None
    final_sim_df['Base DealId'] = None
    final_sim_df['Base ContractID'] = None
    for i in range(0, df_open_D8.shape[0]):
        gwr_dist = gower.gower_topn(df_open_D8[scopefinriskcols].iloc[[
                                    i]], df3_1[scopefinriskcols], n=5, weight=wt)
        index = gwr_dist['index']
        values = gwr_dist['values']
        gwr_dist1 = gower.gower_topn(df_open_D8[scopefinriskcols].iloc[[
                                     i]], df3_2[scopefinriskcols], n=5, weight=wt)
        index1 = gwr_dist1['index']
        values1 = gwr_dist1['values']
        base_df = df_open_D8.iloc[[i]]
        base_df['DealType'] = 'BaseDeal'
        base_df['Distance'] = 0
        base_df['Base DealId'] = base_df['DealId'].values[0]
        base_df['Base ContractID'] = base_df['ContractID'].values[0]
        sim_df = df3_1.iloc[index]
        sim_df['DealType'] = 'SimilarDeal'
        sim_df['Distance'] = values
        sim_df['Base DealId'] = base_df['DealId'].values[0]
        sim_df['Base ContractID'] = base_df['ContractID'].values[0]
        final_sim_df = pd.concat([final_sim_df, base_df])
        final_sim_df = pd.concat([final_sim_df, sim_df])
        sim_df = df3_2.iloc[index1]
        sim_df['DealType'] = 'SimilarDeal'
        sim_df['Distance'] = values1
        sim_df['Base DealId'] = base_df['DealId'].values[0]
        sim_df['Base ContractID'] = base_df['ContractID'].values[0]
        final_sim_df = pd.concat([final_sim_df, sim_df])

    for i in range(0, df_open_Rest.shape[0]):
        gwr_dist = gower.gower_topn(df_open_Rest[scopefinriskcols].iloc[[
                                    i]], df_signed_Rest[scopefinriskcols], n=5, weight=wt)
        index2 = gwr_dist['index']
        values2 = gwr_dist['values']
        base_df = df_open_Rest.iloc[[i]]
        base_df['DealType'] = 'BaseDeal'
        base_df['Distance'] = 0
        base_df['Base DealId'] = base_df['DealId'].values[0]
        base_df['Base ContractID'] = base_df['ContractID'].values[0]
        sim_df = df_signed_Rest.iloc[index2]
        sim_df['DealType'] = 'SimilarDeal'
        sim_df['Distance'] = values2
        sim_df['Base DealId'] = base_df['DealId'].values[0]
        sim_df['Base ContractID'] = base_df['ContractID'].values[0]
        final_sim_df = pd.concat([final_sim_df, sim_df])

    final_sim_df = final_sim_df[~((final_sim_df['DealType'] == 'SimilarDeal') & (
        final_sim_df['DealId'] == final_sim_df['Base DealId']))]
    final_sim_df['Distance'] = final_sim_df['Distance'].astype('float')
    final_sim_df = final_sim_df[final_sim_df['Distance'] < 0.2]
    final_sim_df = final_sim_df.sort_values(
        ['Base DealId', 'Distance']).reset_index(drop=True)
    final_sim_df['Rank'] = final_sim_df.groupby(
        ['Base DealId', 'DealType'])['Distance'].rank()
    final_sim_df = final_sim_df[final_sim_df['Rank']
                                <= 4].reset_index(drop=True)
    print(final_sim_df.shape, final_sim_df['Base DealId'].nunique())
    # print(final_sim_df['Area'].unique())
    #final_sim_df[['DealId','Base DealId','Area','DealType','Distance','Rank']].head(10)
    #final_sim_df.to_csv("abfss://maidatalake@maidevadls.dfs.core.windows.net/data/ML Models/L2O/Deal Similarity Score/Model Output/Data/ScoringData/Snapshot/RegularAppend/Deal_Similarity_open_deals_overall_risk_output_top4_with_weights(2_1)_05112022.csv",sep=',',index=False)

    # Step 6
    risk_assoc = risk_df.copy(deep=True)
    risk_assoc = risk_assoc[['DealId', 'ContractID', 'GRRUID', 'Category', 'SubCategory', 'Name',
                             'Risk Rating', 'Severity', 'Source', 'Answer Is Required']].drop_duplicates().reset_index(drop=True)
    final_resultArea2 = final_sim_df[final_sim_df['DealType']
                                     == 'SimilarDeal'].reset_index(drop=True)
    final_resultArea3 = final_resultArea2[[
        'DealId', 'ContractID', 'Base DealId', 'Base ContractID', 'DealType', 'Overall Risk Rating Original']]
    final_resultArea3 = final_resultArea3.merge(risk_assoc, how='left', left_on=[
                                                'DealId', 'ContractID'], right_on=['DealId', 'ContractID'])
    Risk_mapping = {"Low": 1,
                    "Medium": 2,
                    "High": 3,
                    "Critical": 4}
    Severity_mapping = {"Low": 1,
                        "Medium": 2,
                        "High": 3,
                        "Critical": 4}
    final_resultArea3['Risk Rating Rank'] = final_resultArea3['Risk Rating'].map(
        Risk_mapping)
    final_resultArea3['Severity Rank'] = final_resultArea3['Severity'].map(
        Severity_mapping)
    final_resultArea3.head()
    rec_risks = final_resultArea3.groupby(['Base DealId', 'Base ContractID', 'GRRUID', 'Category', 'SubCategory', 'Name', 'Risk Rating', 'Risk Rating Rank', 'Severity Rank']).size().reset_index(
        name='No_of_deals').sort_values(['Base DealId', 'Base ContractID', 'Risk Rating Rank', 'No_of_deals', 'Severity Rank'], ascending=False).reset_index(drop=True)  # what should be order for recommendation?
    rec_risks = rec_risks[['Base DealId', 'Base ContractID', 'GRRUID', 'Category',
                           'SubCategory', 'Name', 'Risk Rating', 'Risk Rating Rank', 'Severity Rank', 'No_of_deals']]
    Severity_mapping = {1: "Low",
                        2: "Medium",
                        3: "High",
                        4: "Critical"}
    rec_risks['Severity'] = rec_risks['Severity Rank'].map(Severity_mapping)
    rec_risks.drop(['Severity Rank', 'Risk Rating Rank'], axis=1, inplace=True)
    rec_risks = rec_risks[rec_risks['Risk Rating'].notna()
                          ].reset_index(drop=True)
    # print(rec_risks.shape,rec_risks['Base DealId'].nunique()) #166023
    rec_risks2 = rec_risks[(rec_risks['Risk Rating'].isin(['Critical', 'High'])) | (
        rec_risks['Severity'].isin(['Critical', 'High']))].reset_index(drop=True)
    # print(rec_risks2.shape,rec_risks2['Base DealId'].nunique()) #33083 3328
    # rec_risks2.head()

    return rec_risks.to_dict('records')


def re_score_recommender(input_json):
    return scoring(Contracttable_df, df_signed, risk_df, input_json)
