# Import packages
import pandas as pd
import numpy as np
import pickle
# import category_encoders as ce
# from category_encoders.target_encoder import TargetEncoder
from pycaret.classification import *
from services.filereaders import get_data


# Reading Static Files
CSAT = None  # pd.read_csv('local_files/risk/CSAT.csv')
rest = None  # pd.read_csv('local_files/risk/Other_features.csv')
red = None  # pd.read_csv('local_files/risk/TPID_CP.csv')
region = None  # pd.read_csv('local_files/risk/SubRegion_CP.csv')
ppg = None  # pd.read_csv('local_files/risk/PPG_CP.csv')
seller = None  # pd.read_csv('local_files/risk/Seller_CP.csv')

# List of objects paths to transform X
class_objects = ['Output_1+obj1.pkl', 'Output_2+obj1.pkl',
                 'Output_3+obj1.pkl', 'Output_4+obj1.pkl']
# Load Model in Variable
model = load_model(f"local_files/risk/Risk_RF_Final_29Apr_Final")

# Imputing missing values
df_num_imp = get_data('local_files/risk/df_num_imp.csv', 'csv')


selected_features = ['Deal ID', 'Fee Arrangement',	'Is Public Sector',	'NST Category',	'Total Resource Hours',
                     'Project Manager Mix',	'Standard Offering Type', 'Deal Velocity',	'Is ECIF', 'HAS SOW',
                     'CloudFlag', 'OSEDealsFlag',	'Payment Terms', 'Outlier Type',	'Pricing Cut Off',
                     'Delivery Margin Target', 'Is Misstated', 'Is IP Exchange', 'Derived Primary Domain', 'Domain Count',
                     'PL Requested Type', 'Is Subcon Identified', 'Total SubCon Hours', 'Planned Contract Microsoft IGD Hours',	                                'PPGCategory',	'ORBApproved', 'opportunityaginggroup', 'Is Amendment', 'Area',
                     'IndustrySector', 'IsGlobal', 'CompassOneIndustryName', 'Contract Created Date Fiscal Year',
                     'Is Vaguely Described', 'QA_TQA_Critical', 'QA_TQA_High', 'QA_TQA_Medium', 'QA_TQA_Low',
                     'Output', 'Custom_perc', 'CSAT', 'DeliveryCostServicesUSD',
                     '# Red Projects', 'Cost_Red_Projects', 'Delivery Type', 'Red_Projects_SubRegion',
                     'Red_Count_PPG', 'Red_Cost_PPG', 'Seller_Red_Projects',	'Seller_Red_Cost'
                     ]


# Create list for different types of variables:-
nominal_vars = ['Fee Arrangement', 'Is Public Sector', 'NST Category', 'Standard Offering Type', 'Is ECIF', 'HAS SOW',
                'CloudFlag', 'OSEDealsFlag', 'Payment Terms',  'Outlier Type',
                'Pricing Cut Off', 'Is Misstated', 'Is IP Exchange', 'Derived Primary Domain',  'PL Requested Type',
                'Is Subcon Identified', 'PPGCategory', 'ORBApproved', 'Area', 'IndustrySector', 'IsGlobal',
                'CompassOneIndustryName', 'Delivery Type', 'PPG_Industry']

ordinal_vars = ['opportunityaginggroup',  'Project Manager Mix']

num_vars = ['Total Resource Hours', 'Deal Velocity', 'Delivery Margin Target', 'Domain Count',
            'QA_TQA_Critical', 'QA_TQA_High', 'QA_TQA_Medium', 'QA_TQA_Low', 'CSAT', '# Red Projects', 'Cost_Red_Projects',
            'IGD_Hrs_Over_Resource_Hrs', 'Total_SubCon_Over_Resource_Hrs', 'Red_Projects_SubRegion', 'Custom_perc',
            'Red_Count_PPG', 'Red_Cost_PPG', 'Seller_Red_Projects',	'Seller_Red_Cost', 'DeliveryCostServicesUSD']

dummy_vars = ['Fee Arrangement', 'NST Category', 'Standard Offering Type', 'OSEDealsFlag', 'Outlier Type', 'Pricing Cut Off', 'Derived Primary Domain',
              'PL Requested Type', 'ORBApproved', 'IndustrySector', 'IsGlobal', 'Is Misstated',  'Is Subcon Identified', 'Is Public Sector', 'Is ECIF', 'HAS SOW',
              'Is Amendment', 'Is Vaguely Described', 'Delivery Type']

features = pd.read_csv('local_files/risk/Features.csv')
features = features['Columns'].tolist()


def Target_Encode_Multiclass(X, class_objects):

    X_obj = X.select_dtypes('object')  # separate categorical columns
    X = X.select_dtypes(exclude='object')
    for class_obj in class_objects:

        class_ = class_obj.split('+')[0]
        # class_ = class_obj.name.split('+')[0]
        infile = open(f"local_files/risk/{class_obj}", 'rb')
        enc = pickle.load(infile)
        temp = enc.transform(X_obj)  # columns for class_
        temp.columns = [str(x)+'_'+str(class_) for x in temp.columns]
        X = pd.concat([X, temp], axis=1)  # add to original dataset

    return X


risk_data = get_data(
    'local_files/risk/Risk_Data_Modelling_CP.csv', 'csv')
risk_data = risk_data[risk_data['Agreement Setup Completed Date'] > '2018-07-01']
risk_data = risk_data[~risk_data['Output'].isna()]
inp = risk_data.to_json()

# Defining Function to score


def score(inp, CSAT, rest, red, region, ppg, seller, class_objects, jobId, model, selected_features, nominal_vars, ordinal_vars, num_vars, dummy_vars, features):
    # risk_data = pd.read_json(inp, dtype={'Is Strategic Opportunity': 'object'})
    risk_data_seller = pd.DataFrame(inp)
    # risk_data['Deal ID'] = risk_data['Deal ID'].astype(int)

    # # Step 1
    # CSAT = CSAT.drop_duplicates()
    # CSAT = CSAT.groupby(['ProjectId'])['CSAT'].agg('mean').reset_index()
    # risk_data_CSAT = risk_data.merge(
    #     CSAT, how='left', left_on='Project Id', right_on='ProjectId')

    # rest = rest[['DealId', 'IsRenewal', 'HasSContract']]
    # risk_data_rest = risk_data_CSAT.merge(
    #     rest, how='left', left_on='Deal ID', right_on='DealId')
    # risk_data_rest.drop(['DealId'], axis=1, inplace=True)

    # # For Change Point + SAP Data
    # red['# Red Projects'] = red['# Red Projects'].astype('float')
    # red['Cost_Red_Projects'] = red['Cost_Red_Projects'].astype('float')
    # risk_data_red = risk_data_rest.merge(red, how='left', on='Deal ID')

    # # For Change Point + SAP Data
    # region['Red_Projects_SubRegion'] = region['Red_Projects_SubRegion'].astype(
    #     'float')
    # risk_data_region = risk_data_red.merge(
    #     region, how='left', left_on='SubRegion', right_on='Sub_Region')

    # # For CP + SAP Data
    # ppg.columns = ['PPG', 'Red_Count_PPG', 'Red_Cost_PPG']
    # ppg['Red_Count_PPG'] = ppg['Red_Count_PPG'].astype('float')
    # ppg['Red_Cost_PPG'] = ppg['Red_Cost_PPG'].astype('float')
    # risk_data_ppg = risk_data_region.merge(
    #     ppg, how='left', left_on='PPGCategory', right_on='PPG')
    # risk_data_ppg.drop(['PPG'], axis=1, inplace=True)

    # # For CP + SAP Data
    # seller.columns = ['Deal ID', 'Seller_Red_Projects', 'Seller_Red_Cost']
    # seller['Seller_Red_Projects'] = seller['Seller_Red_Projects'].astype(
    #     'float')
    # seller['Seller_Red_Cost'] = seller['Seller_Red_Cost'].astype('float')
    # risk_data_seller = risk_data_ppg.merge(seller, how='left', on='Deal ID')

    # Step 2
    risk_data_seller['QA_TQA_Critical'] = risk_data_seller['QA_Critical'] + \
        risk_data_seller['TQA_Critical']
    risk_data_seller['QA_TQA_High'] = risk_data_seller['QA_High'] + \
        risk_data_seller['TQA_High']
    risk_data_seller['QA_TQA_Medium'] = risk_data_seller['QA_Medium'] + \
        risk_data_seller['TQA_Medium']
    risk_data_seller['QA_TQA_Low'] = risk_data_seller['QA_Low'] + \
        risk_data_seller['TQA_Low']

    # Fill NA with 0
    risk_data_seller['QA_TQA_Critical'].fillna(value=0, inplace=True)
    risk_data_seller['QA_TQA_High'].fillna(value=0, inplace=True)
    risk_data_seller['QA_TQA_Medium'].fillna(value=0, inplace=True)
    risk_data_seller['QA_TQA_Low'].fillna(value=0, inplace=True)

    # Step 3
    risk_data_selected = risk_data_seller[selected_features]

    # Step 4
    risk_data_selected['IGD_Hrs_Over_Resource_Hrs'] = (
        risk_data_selected['Planned Contract Microsoft IGD Hours']/risk_data_selected['Total Resource Hours']).replace([np.nan, np.Inf], [0, 0])
    risk_data_selected['Total_SubCon_Over_Resource_Hrs'] = (
        risk_data_selected['Total SubCon Hours']/risk_data_selected['Total Resource Hours']).replace([np.nan, np.Inf], [0, 0])

    risk_data_selected.drop(
        ['Planned Contract Microsoft IGD Hours', 'Total SubCon Hours'], axis=1, inplace=True)

    # PPG Industry Feature:-
    risk_data_selected['PPG_Industry'] = risk_data_selected['PPGCategory'].str.cat(
        risk_data_selected['CompassOneIndustryName'])

    # Step 5
    risk_data_oot = risk_data_selected.copy()
    risk_data_oot.drop(
        ['Contract Created Date Fiscal Year'], axis=1, inplace=True)
    risk_data_oot.reset_index(drop=True, inplace=True)

    # Step 6
    df_oot = risk_data_oot.copy()

    # Step 7
    # Missing Value Imputation (Categorical variables with "Unknown")

    # Out Of Time
    for i in nominal_vars:
        if (df_oot.loc[df_oot[i].isnull()].shape[0] != 0):
            df_oot.loc[df_oot[i].isnull(), i] = "Unknown"

    for i in ordinal_vars:
        if (df_oot.loc[df_oot[i].isnull()].shape[0] != 0):
            df_oot.loc[df_oot[i].isnull(), i] = "Unknown"

    # Step 8
    # Club low frequency in Payment Terms into "Others"
    df_oot['Payment Terms_clean'] = df_oot['Payment Terms'].copy()
    df_oot.loc[~df_oot['Payment Terms'].isin(
        ['Net 30', 'Net 60', 'N31', 'Net 45']), 'Payment Terms_clean'] = "Other"
    df_oot.drop(['Payment Terms'], axis=1, inplace=True)

    # Step 9

    # Missing Value Imputation (Numerical variables with -ve values and blank)
    IS = df_oot['CompassOneIndustryName'].unique().tolist()

    for i in IS:
        for col in num_vars:
            if ((df_oot.loc[(df_oot['CompassOneIndustryName'] == i) & (df_oot[col].isnull())].shape[0] != 0)):

                df_oot.loc[(df_oot['CompassOneIndustryName'] == i) & ((df_oot[col].isnull()) | (
                    df_oot[col] <= 0)), col] = df_num_imp[((df_num_imp['CI'] == i) & (df_num_imp['Column'] == col))]['Value']
                #df_train.loc[(df_train['CompassOneIndustryName']==i) & (df_train[col]>0) & (~df_train[col].isna())][col].median()

    # Step 10
    df_oot['opportunityaginggroup'] = np.where(df_oot['opportunityaginggroup'].isin(
        ['UNKNOWN', 'Unknown']), 'Unknown', df_oot['opportunityaginggroup'])

    conditions = [(df_oot['Project Manager Mix'] == 'Unknown'),
                  (df_oot['Project Manager Mix'] == 'No project manager'),
                  (df_oot['Project Manager Mix'] == 'Less than 5%'),
                  (df_oot['Project Manager Mix'] == '5% - 15%'),
                  (df_oot['Project Manager Mix'] == '15% Or More'), ]
    choices = [0, 1, 2, 3, 4]
    df_oot['Project Manager Mix'] = np.select(conditions, choices, default=5)

    conditions = [(df_oot['opportunityaginggroup'] == 'Unknown'),
                  (df_oot['opportunityaginggroup'] == '0-30 days'),
                  (df_oot['opportunityaginggroup'] == '31-60 days'),
                  (df_oot['opportunityaginggroup'] == '61-90 days'),
                  (df_oot['opportunityaginggroup'] == '91-180 days'),
                  (df_oot['opportunityaginggroup'] == 'More than 180 days'), ]
    choices = [0, 1, 2, 3, 4, 5]
    df_oot['opportunityaginggroup'] = np.select(conditions, choices, default=6)

    df_oot_copy = df_oot.copy()

    # Step 11
    # Convert Data Types:-

    df_oot['Project Manager Mix'] = df_oot['Project Manager Mix'].astype(
        'float')
    df_oot['opportunityaginggroup'] = df_oot['opportunityaginggroup'].astype(
        'float')
    df_oot['# Red Projects'] = df_oot['# Red Projects'].astype('float')
    df_oot['Is IP Exchange'] = df_oot['Is IP Exchange'].astype('float')
    df_oot['QA_TQA_High'] = df_oot['QA_TQA_High'].astype('float')
    df_oot['QA_TQA_Medium'] = df_oot['QA_TQA_Medium'].astype('float')

    # Step 12(-)
    # Create dummy variables

    nominal_dummy_oot = pd.get_dummies(data=df_oot, columns=dummy_vars)
    drop_features = list(set(nominal_dummy_oot.columns) - set(features))
    nominal_dummy_oot.drop(columns=drop_features, inplace=True)
    df_oot = nominal_dummy_oot.copy()
    add_features = list(set(features) - set(df_oot.columns))
    for col in add_features:
        df_oot[col] = 0

    # Function to Transform X

    df_oot_cat = Target_Encode_Multiclass(
        df_oot[['CloudFlag', 'Area', 'CompassOneIndustryName', 'Payment Terms_clean', 'PPGCategory', 'PPG_Industry']], class_objects)

    # Step 13
    df_oot.drop(['CloudFlag', 'Area', 'CompassOneIndustryName',
                'Payment Terms_clean', 'PPGCategory', 'PPG_Industry'], axis=1, inplace=True)
    df_oot = pd.concat([df_oot, df_oot_cat], axis=1)

    # step 14
    df_oot = df_oot[df_oot.columns[~df_oot.columns.str.endswith('Output_4')]]

    dataset_oot = df_oot.copy()

    otpt = predict_model(model, dataset_oot)
    return otpt


def re_score(inp):
    # return score(inp, class_objects, "", model, selected_features,
    #              nominal_vars, ordinal_vars, num_vars, dummy_vars, features)
    return score(inp, CSAT, rest, red, region, ppg, seller, class_objects, "", model, selected_features, nominal_vars, ordinal_vars, num_vars, dummy_vars, features)
