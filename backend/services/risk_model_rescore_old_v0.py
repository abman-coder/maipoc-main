# Importing Packages

import pandas as pd
import numpy as np
import pickle
import category_encoders as ce
from category_encoders.target_encoder import TargetEncoder
from pycaret.classification import *
from services.common_service import get_features

# Creating Linked Service

# List of objects paths to transform X
class_objects = ['Output_1+obj.pkl', 'Output_2+obj.pkl',
                 'Output_3+obj.pkl', 'Output_4+obj.pkl']

# Load Model in Variable

model = load_model(f"local_files/Risk_RF_Final")


# List of Selected Features
selected_features = ['Deal ID', 'Is Strategic Opportunity', 'Is Amendment', 'Fee Arrangement', 'Approval Duration',
                     'Contract Revenue Cluster', 'Is Public Sector', 'Has SQA Review', 'Has IP Review', 'Has Finance Review',
                     'Has CN Review', 'Is Contract Reviewed', 'Is Contract Rushed', 'Has ESWO', 'NST Category', 'ESAP',
                     'Total Resource Hours', 'Project Manager Mix', 'Standard Offering Type', 'Deal Velocity', 'Is ECIF',
                     'SQA Review', 'TQA Review', 'HAS SOW', 'Complex Deal Indicator', 'CloudFlag', 'IsAzureandA&IDomainDeal',
                     'VelocityExceedsTarget', 'SolutionExceedsTarget', 'NegotiationsExceedsTarget', 'ApprovalsExceedsTarget',
                     'OSEDealsFlag', 'Is Risk Overridden', 'Payment Terms', 'Domain Involvement', 'Outlier Type',
                     'Planned Contract Riskreserve Required CCUS', 'CM Review', 'Pricing Cut Off', 'Default Delivery Margin Target',
                     'Delivery Margin Target', 'Is Misstated', 'Is IP Exchange', 'Is Vaguely Described', 'Derived Primary Domain',
                     'Domain Count', 'PM Solution Area', 'PL Requested Type', 'Is Subcon Identified',
                     'Planned Contract Microsoft IGD Hours', 'Price To Customer USD', 'commitmentlevel', 'opportunitysize',
                     'PPGCategory', 'ORBApproved', 'exceptiontype', 'opportunityaginggroup', 'isgpo', 'Area_x', 'TimeZone',
                     'TotalRevenueServicesUSD', 'IndustrySector', 'IsGlobal', 'SBDInvolved', 'CompassOneIndustryName',
                     'RevenueServicesUSD', 'DeliveryCostServicesUSD', 'Domain', 'FinalDeliveryValue',	'ApprovalType',
                     'Federal', 'QA_TQA_Critical', 'QA_TQA_High',
                     'QA_TQA_Medium', 'QA_TQA_Low']


# Create list for different types of variables:-

nominal_vars = ['Is Strategic Opportunity', 'Is Amendment', 'Fee Arrangement', 'Is Public Sector', 'Has SQA Review', 'Has IP Review', 'Has Finance Review', 'Has CN Review', 'Is Contract Reviewed', 'Is Contract Rushed', 'Has ESWO', 'NST Category', 'ESAP', 'Standard Offering Type', 'Is ECIF', 'SQA Review', 'TQA Review', 'HAS SOW', 'Complex Deal Indicator', 'CloudFlag',	'IsAzureandA&IDomainDeal',	'VelocityExceedsTarget', 'SolutionExceedsTarget', 'NegotiationsExceedsTarget', 'ApprovalsExceedsTarget',	'OSEDealsFlag', 'Is Risk Overridden', 'Payment Terms', 'Domain Involvement', 'Outlier Type', 'CM Review', 'Pricing Cut Off', 'Is Misstated', 'Is IP Exchange', 'Is Vaguely Described', 'Derived Primary Domain',  'PM Solution Area', 'PL Requested Type', 'Is Subcon Identified', 'PPGCategory', 'ORBApproved', 'exceptiontype', 'isgpo', 'Area_x', 'IndustrySector', 'IsGlobal',
                'SBDInvolved', 'CompassOneIndustryName', 'Domain',  'Federal']

ordinal_vars = ['Approval Duration', 'Contract Revenue Cluster', 'Project Manager Mix',
                'opportunitysize', 'opportunityaginggroup', 'ApprovalType', 'commitmentlevel']

num_vars = ['Total Resource Hours', 'Deal Velocity', 'Planned Contract Riskreserve Required CCUS', 'Default Delivery Margin Target', 'Delivery Margin Target', 'Domain Count', 'Planned Contract Microsoft IGD Hours',
            'Price To Customer USD', 'TotalRevenueServicesUSD',	'RevenueServicesUSD', 'DeliveryCostServicesUSD', 'FinalDeliveryValue', 'QA_TQA_Critical', 'QA_TQA_High', 'QA_TQA_Medium', 'QA_TQA_Low']  # ,'QA_TQA_Unknown']

dummy_vars = ['Is Amendment', 'IsGlobal', 'Is Misstated', 'Is Vaguely Described', 'Is Subcon Identified',
              'Is Public Sector',
              'Has SQA Review', 'Has IP Review', 'Has Finance Review', 'Has CN Review', 'Is Strategic Opportunity',
              'Is Contract Reviewed', 'Is Contract Rushed', 'Is ECIF', 'IsAzureandA&IDomainDeal', 'VelocityExceedsTarget', 'SolutionExceedsTarget', 'NegotiationsExceedsTarget',
              'ApprovalsExceedsTarget', 'Is Risk Overridden', 'CM Review', 'SBDInvolved', 'HAS SOW']


features = pd.read_csv('local_files/Features.csv')
features = features['Columns'].tolist()


def Target_Encode_Multiclass(X, class_objects):

    X_obj = X.select_dtypes('object')  # separate categorical columns
    X = X.select_dtypes(exclude='object')
    for class_obj in class_objects:

        class_ = class_obj.split('+')[0]
        infile = open(f"local_files/pkl/{class_obj}", 'rb')
        enc = pickle.load(infile)
        temp = enc.transform(X_obj)  # columns for class_
        temp.columns = [str(x)+'_'+str(class_) for x in temp.columns]
        X = pd.concat([X, temp], axis=1)  # add to original dataset

    return X

# Defining Function to score


def score(inp, class_objects, jobId, model, selected_features, nominal_vars, ordinal_vars, num_vars, dummy_vars, features):
    risk_data = pd.DataFrame(inp)

    risk_data['Deal ID'] = risk_data['Deal ID'].astype(int)
    if "Total Resource Hours" in risk_data:
        risk_data['Total Resource Hours'] = risk_data['Total Resource Hours'].astype(
            float)
    if "Deal Velocity" in risk_data:
        risk_data['Deal Velocity'] = risk_data['Deal Velocity'].astype(float)
    if "FinalDeliveryValue" in risk_data:
        risk_data['FinalDeliveryValue'] = risk_data['FinalDeliveryValue'].astype(
            float)

    all_fs = get_features()
    risk_data = risk_data[all_fs]

    risk_data['QA_TQA_Critical'] = risk_data['QA_Critical'] + \
        risk_data['TQA_Critical']
    risk_data['QA_TQA_High'] = risk_data['QA_High'] + risk_data['TQA_High']
    risk_data['QA_TQA_Medium'] = risk_data['QA_Medium'] + \
        risk_data['TQA_Medium']
    risk_data['QA_TQA_Low'] = risk_data['QA_Low'] + risk_data['TQA_Low']

    # Fill NA with 0
    risk_data['QA_TQA_Critical'].fillna(value=0, inplace=True)
    risk_data['QA_TQA_High'].fillna(value=0, inplace=True)
    risk_data['QA_TQA_Medium'].fillna(value=0, inplace=True)
    risk_data['QA_TQA_Low'].fillna(value=0, inplace=True)

    risk_data_selected = risk_data[selected_features]

    risk_data_selected["Output"] = np.NaN
    risk_data_selected["Output"] = risk_data_selected["Output"].astype(
        'object')

    risk_data_train = risk_data_selected.copy()
    risk_data_train.reset_index(drop=True, inplace=True)

    # Create a copy
    df_train = risk_data_train.copy()

    # Missing Value Imputation Categorical Columns

    for i in nominal_vars:
        if (df_train.loc[df_train[i].isnull()].shape[0] != 0):
            df_train.loc[df_train[i].isnull(), i] = "Unknown"

    for i in ordinal_vars:
        if (df_train.loc[df_train[i].isnull()].shape[0] != 0):
            df_train.loc[df_train[i].isnull(), i] = "Unknown"

    # Club low frequency in Payment Terms into "Others"

    df_train['Payment Terms_clean'] = df_train['Payment Terms'].copy()
    df_train.loc[~df_train['Payment Terms'].isin(
        ['Net 30', 'Net 60', 'N31', 'Net 45']), 'Payment Terms_clean'] = "Other"

    # Missing Value Imputation (Numerical variables with -ve values and blank)

    # Reading df that has values to be imputed
    df_num_imp = pd.read_csv('local_files/df_num_imp.csv')

    # Unique CompassOneIndustryName
    IS = df_train['CompassOneIndustryName'].unique().tolist()

    for i in IS:
        for col in num_vars:
            if (df_train.loc[(df_train['CompassOneIndustryName'] == i) & ((df_train[col].isnull()) | (df_train[col] <= 0))].shape[0] != 0):
                df_train.loc[(df_train['CompassOneIndustryName'] == i) & ((df_train[col].isnull()) | (
                    df_train[col] <= 0)), col] = df_num_imp[((df_num_imp['CI'] == i) & (df_num_imp['Column'] == col))]['Value']

    # Replace Unknown with 0 for Commitment Level
    df_train['commitmentlevel'].replace("Unknown", 0, inplace=True)

    # Replacing ['UNKNOWN','Unknown'] with 'Unknown'

    df_train['opportunityaginggroup'] = np.where(df_train['opportunityaginggroup'].isin(
        ['UNKNOWN', 'Unknown']), 'Unknown', df_train['opportunityaginggroup'])

    # Converting categories to number

    conditions = [(df_train['Approval Duration'] == '0-1 days'),
                  (df_train['Approval Duration'] == '2-3 days'),
                  (df_train['Approval Duration'] == '4-5 days'),
                  (df_train['Approval Duration'] == '6-10 days'),
                  (df_train['Approval Duration'] == '11-15 days'),
                  (df_train['Approval Duration'] == '16-30 days'),
                  (df_train['Approval Duration'] == '31-45 days'),
                  (df_train['Approval Duration'] == '46-90 days'), ]
    choices = [0, 1, 2, 3, 4, 5, 6, 7]
    df_train['Approval Duration'] = np.select(
        conditions, choices, default=8)
    conditions = [(df_train['Contract Revenue Cluster'] == 'Less Than 50K'),
                  (df_train['Contract Revenue Cluster'] == '50K - 100K'),
                  (df_train['Contract Revenue Cluster'] == '100K - 300K'),
                  (df_train['Contract Revenue Cluster'] == '300K - 500K'),
                  (df_train['Contract Revenue Cluster'] == '500K - 1M'),
                  (df_train['Contract Revenue Cluster'] == 'Above 1M'), ]
    choices = [0, 1, 2, 3, 4, 5]
    df_train['Contract Revenue Cluster'] = np.select(
        conditions, choices, default=6)
    conditions = [(df_train['Project Manager Mix'] == 'Unknown'),
                  (df_train['Project Manager Mix']
                   == 'No project manager'),
                  (df_train['Project Manager Mix'] == 'Less than 5%'),
                  (df_train['Project Manager Mix'] == '5% - 15%'),
                  (df_train['Project Manager Mix'] == '15% Or More'), ]
    choices = [0, 1, 2, 3, 4]
    df_train['Project Manager Mix'] = np.select(
        conditions, choices, default=5)
    conditions = [(df_train['opportunitysize'] == 'Unknown'),
                  (df_train['opportunitysize'] == '<50K'),
                  (df_train['opportunitysize'] == '50k-100k'),
                  (df_train['opportunitysize'] == '100k-300k'),
                  (df_train['opportunitysize'] == '300k-500k'),
                  (df_train['opportunitysize'] == '500k-1M'),
                  (df_train['opportunitysize'] == '>1M'), ]
    choices = [0, 1, 2, 3, 4, 5, 6]
    df_train['opportunitysize'] = np.select(conditions, choices, default=7)
    conditions = [(df_train['opportunityaginggroup'] == 'Unknown'),
                  (df_train['opportunityaginggroup'] == '0-30 days'),
                  (df_train['opportunityaginggroup'] == '31-60 days'),
                  (df_train['opportunityaginggroup'] == '61-90 days'),
                  (df_train['opportunityaginggroup'] == '91-180 days'),
                  (df_train['opportunityaginggroup'] == 'More than 180 days'), ]
    choices = [0, 1, 2, 3, 4, 5]
    df_train['opportunityaginggroup'] = np.select(
        conditions, choices, default=6)
    conditions = [(df_train['ApprovalType'] == 'T1'),
                  (df_train['ApprovalType'] == 'T2'),
                  (df_train['ApprovalType'] == 'T3'),
                  (df_train['ApprovalType'] == 'T4'),
                  (df_train['ApprovalType'] == 'T5'), ]
    choices = [0, 1, 2, 3, 4]
    df_train['ApprovalType'] = np.select(conditions, choices, default=5)
    conditions = [(df_train['commitmentlevel'] == 0),
                  (df_train['commitmentlevel'] == 1),
                  (df_train['commitmentlevel'] == 2),
                  (df_train['commitmentlevel'] == 3),
                  (df_train['commitmentlevel'] == 4), ]
    choices = [0, 1, 2, 3, 4]
    df_train['commitmentlevel'] = np.select(conditions, choices, default=5)

    # Creating copy of df_train
    df_train_copy = df_train.copy()

    # Converting to float

    df_train['Approval Duration'] = df_train['Approval Duration'].astype(
        'float')
    df_train['Contract Revenue Cluster'] = df_train['Contract Revenue Cluster'].astype(
        'float')
    df_train['Project Manager Mix'] = df_train['Project Manager Mix'].astype(
        'float')
    df_train['opportunitysize'] = df_train['opportunitysize'].astype(
        'float')
    df_train['opportunityaginggroup'] = df_train['opportunityaginggroup'].astype(
        'float')
    df_train['ApprovalType'] = df_train['ApprovalType'].astype('float')
    df_train['commitmentlevel'] = df_train['commitmentlevel'].astype(
        'float')

    # Create dummy variables

    nominal_dummy_train = pd.get_dummies(data=df_train, columns=dummy_vars)
    drop_features = list(set(nominal_dummy_train.columns) - set(features))
    nominal_dummy_train.drop(columns=drop_features, inplace=True)
    df_train = nominal_dummy_train.copy()
    add_features = list(set(features) - set(df_train.columns))
    for col in add_features:
        df_train[col] = 0

    # Function to Transform X

    df_train = Target_Encode_Multiclass(df_train, class_objects)

    # Dropping unnecessary columns

    df_train = df_train[df_train.columns[~df_train.columns.str.endswith(
        'Output_4')]]
    df_train.drop(['Output_Output_1', 'Output_Output_2',
                   'Output_Output_3'], axis=1, inplace=True)
    df_train['Output'] = df_train_copy['Output']

    # Transforming Numerical Variables to Log:-

    df_train['Log_Deal Velocity'] = np.log1p(df_train['Deal Velocity'])
    df_train['Log_DeliveryCostServicesUSD'] = np.log1p(
        df_train['DeliveryCostServicesUSD'])
    df_train['Log_Planned Contract_Microsoft_IGD_Hours'] = np.log1p(
        df_train['Planned Contract Microsoft IGD Hours'])
    df_train['Log_FinalDeliveryValue'] = np.log1p(
        df_train['FinalDeliveryValue'])
    df_train['Log_RevenueServicesUSD'] = np.log1p(
        df_train['RevenueServicesUSD'])
    df_train['Log_Price_To_Customer_USD'] = np.log1p(
        df_train['Price To Customer USD'])

    dataset_train = df_train.copy()
    return predict_model(model, dataset_train).to_json()


def re_score(inp):
    return score(inp, class_objects, "", model, selected_features,
                 nominal_vars, ordinal_vars, num_vars, dummy_vars, features)
