# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 23:58:00 2022

@author: ndasadhikari
"""

import string
import re
import pandas as pd
import numpy as np
import pickle
# from services.filereaders import get_data
from services.datalake_connection import download_file_from_directory


def main_fun(name, inp1=None, inp2=None, inp3=None, inp4=None):
    try:
        df_recommended1 = pd.read_csv(
            'local_files/nst/temp_NST_Recommendation_SubRegion_Translated_Text_corrected.csv', encoding='latin-1')
    except:
        # return "error"
        df_recommended1 = download_file_from_directory(
            'NST', 'NST_Recommendation_SubRegion_Translated_Text_corrected.csv', encoding='latin-1')

    df_recommend_approval = df_recommended1['NST Translater'].value_counts(
    ).rename_axis('Approval NST Comments').to_frame('Users Used')

    xgb_model = pickle.load(open(
        "local_files/nst/xgb_model.pkl", "rb"))
    vectorizer = pickle.load(open(
        "local_files/nst/Xvec.pkl", "rb"))

    NST_types = list(df_recommended1['NST Type'].value_counts().keys())
    # NST_types.append(None)
    NST_groups = list(df_recommended1['NST Group'].value_counts().keys())
    # NST_groups.append(None)
    SubRegion = list(df_recommended1['SubRegion'].value_counts().keys())

    # API: 1. To get the options for nst type, group and subregion

    if name == 'get_defaults':
        # def get_defaults():
        return {
            'NST_types': NST_types,
            'NST_groups': NST_groups,
            'SubRegion': SubRegion,
        }
    # Cleaning Text phase
    #from nltk.corpus import stopwords
    #stop = stopwords.words('english')
    stop = ['i',
            'me',
            'my',
            'myself',
            'we',
            'our',
            'ours',
            'ourselves',
            'you',
            "you're",
            "you've",
            "you'll",
            "you'd",
            'your',
            'yours',
            'yourself',
            'yourselves',
            'he',
            'him',
            'his',
            'himself',
            'she',
            "she's",
            'her',
            'hers',
            'herself',
            'it',
            "it's",
            'its',
            'itself',
            'they',
            'them',
            'their',
            'theirs',
            'themselves',
            'what',
            'which',
            'who',
            'whom',
            'this',
            'that',
            "that'll",
            'these',
            'those',
            'am',
            'is',
            'are',
            'was',
            'were',
            'be',
            'been',
            'being',
            'have',
            'has',
            'had',
            'having',
            'do',
            'does',
            'did',
            'doing',
            'a',
            'an',
            'the',
            'and',
            'but',
            'if',
            'or',
            'because',
            'as',
            'until',
            'while',
            'of',
            'at',
            'by',
            'for',
            'with',
            'about',
            'against',
            'between',
            'into',
            'through',
            'during',
            'before',
            'after',
            'above',
            'below',
            'to',
            'from',
            'up',
            'down',
            'in',
            'out',
            'on',
            'off',
            'over',
            'under',
            'again',
            'further',
            'then',
            'once',
            'here',
            'there',
            'when',
            'where',
            'why',
            'how',
            'all',
            'any',
            'both',
            'each',
            'few',
            'more',
            'most',
            'other',
            'some',
            'such',
            'no',
            'nor',
            'not',
            'only',
            'own',
            'same',
            'so',
            'than',
            'too',
            'very',
            's',
            't',
            'can',
            'will',
            'just',
            'don',
            "don't",
            'should',
            "should've",
            'now',
            'd',
            'll',
            'm',
            'o',
            're',
            've',
            'y',
            'ain',
            'aren',
            "aren't",
            'couldn',
            "couldn't",
            'didn',
            "didn't",
            'doesn',
            "doesn't",
            'hadn',
            "hadn't",
            'hasn',
            "hasn't",
            'haven',
            "haven't",
            'isn',
            "isn't",
            'ma',
            'mightn',
            "mightn't",
            'mustn',
            "mustn't",
            'needn',
            "needn't",
            'shan',
            "shan't",
            'shouldn',
            "shouldn't",
            'wasn',
            "wasn't",
            'weren',
            "weren't",
            'won',
            "won't",
            'wouldn',
            "wouldn't",
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            'aa',
            'ab',
            'bf',
            'bb',
            'abb',
            'ac',
            'ae',
            'af',
            'ba',
            'bb',
            'bd',
            'af',
            'ef',
            'bc']

    def clean_text(text):
        '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
        and remove words containing numbers.'''
        text = str(text).lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    new_alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'ab', 'bf', 'bb', 'abb', 'ac', 'ae', 'af', 'ba', 'bb', 'bd', 'af', 'ef', 'bc']
    for num in new_alpha:
        stop.append(num)
    df_recommended1['cleaned_text'] = df_recommended1['NST Translater'].apply(
        lambda x: clean_text(x))
    df_recommended1['NST_clean_translated_Comment'] = df_recommended1['cleaned_text'].apply(
        lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    def evaluate_approval(approved, df_unique_NST_comments, vectorizer, xgb_model):
        #approved = 'Microsoft will be paid for work performed but not any additional hours of the fee. Approved by the SPL.'
        d = {'NST_clean_translated_Comment': [[approved]]}
        df_recommend_approval = pd.DataFrame(d)
        df_training = df_recommend_approval
        df_training['NST_clean_translated_Comment'] = df_training['NST_clean_translated_Comment'].apply(
            str)
        df_training['length'] = df_training['NST_clean_translated_Comment'].map(
            lambda text: len(text))
        df_training['NST_clean_translated_Comment'] = df_training['NST_clean_translated_Comment'].apply(
            lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

        # tfnew = TfidfVectorizer(max_features=50000, ngram_range=(2, 3), vocabulary = tfidf_tokens)#Xvec.vocabulary_)
        corpus = df_training['NST_clean_translated_Comment'].values
        Xvec1 = vectorizer.transform(corpus)
        cols_when_model_builds = xgb_model.get_booster().feature_names
        X = pd.DataFrame(data=Xvec1.toarray(), columns=cols_when_model_builds)
        zpred = xgb_model.predict_proba(X)

        """
        The code for Recommendation
        """
        #d1 = {'NST_clean_translated_Comment': d}
        #df_recommend_approval = pd.DataFrame(d1)
        #df_training = df_recommend_approval
        #df_training['NST_clean_translated_Comment'] = df_training['NST_clean_translated_Comment'].apply(str)
        #df_training['length'] = df_training['NST_clean_translated_Comment'].map(lambda text: len(text))
        #df_training['NST_clean_translated_Comment'] = df_training['NST_clean_translated_Comment'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

        df_unique_NST_comments['unique_NST_comments'] = df_unique_NST_comments['unique_NST_comments'].apply(
            str)
        df_unique_NST_comments['documents_cleaned'] = df_unique_NST_comments['unique_NST_comments'].apply(lambda x: " ".join(
            re.sub(r'[^a-zA-Z]', ' ', w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]', ' ', w).lower() not in stop))
        #vectorizer123 = TfidfVectorizer()
        tfidf_vectors = vectorizer.transform(
            df_unique_NST_comments.documents_cleaned)

        tfidf_test_vectors = vectorizer.transform(
            df_training.NST_clean_translated_Comment)
        pairwise_similarities = np.dot(
            tfidf_vectors, tfidf_test_vectors.T).toarray()

        df_unique_NST_comments['similarity'] = pairwise_similarities

        final_df = df_unique_NST_comments.sort_values(
            by=['similarity'], ascending=False)

        if final_df.head(1).tail(1)['similarity'].values <= 0.0:
            print('zpred: ', [1, 0])
            print('NOT APPROVED')
        else:
            print('zpred: ', zpred)

        return zpred

    # API: 2. To get default comments for the NST options selected

    def get_default_comments(nst_type, nst_group, sub_region=None, from_server=False):
        df_training1 = df_recommended1
        df_approved = df_training1[df_training1['New Review Recommendation'] == 1]

        df_approved1 = df_approved[df_approved['NST Type'] == nst_type]
        df_approved12 = df_approved1[df_approved1['NST Group'] == nst_group]
        if sub_region:
            df_approved13 = df_approved12[df_approved12['SubRegion']
                                          == sub_region]
        else:
            df_approved13 = df_approved12

        if df_approved13.shape[0] == 0:
            if df_approved12.shape[0] == 0:
                if df_approved1.shape[0] == 0:
                    df_approval_reco = df_approved
                else:
                    df_approval_reco = df_approved1
            else:
                df_approval_reco = df_approved12
        else:
            df_approval_reco = df_approved13

        df_approval_reco['NST_clean_translated_Comment'] = df_approval_reco['NST_clean_translated_Comment'].apply(
            str)
        df_approval_reco['length'] = df_approval_reco['NST_clean_translated_Comment'].map(
            lambda text: len(text))
        df_approval_reco['NST_clean_translated_Comment'] = df_approval_reco['NST_clean_translated_Comment'].apply(
            lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

        value_counts = df_approval_reco['NST_clean_translated_Comment'].value_counts(
            dropna=True, sort=True)

        df_NST_counts = pd.DataFrame(value_counts)
        df_unique_NST_comments = df_NST_counts.reset_index()
        df_unique_NST_comments.columns = ['unique_NST_comments', 'counts']
        if from_server:
            return df_unique_NST_comments
        return df_unique_NST_comments.to_dict('records')

    # API: 3. To get the score output

    def nst_re_score(data):
        approved = data["approved"]
        if not data["df_unique_NST_comments"]:
            df_unique_NST_comments = get_default_comments(
                data['NST Type'], data['NST Group'], data['SubRegion'] if "SubRegion" in data else None, from_server=True)
        else:
            df_unique_NST_comments = pd.DataFrame(
                data["df_unique_NST_comments"])
        zpred = evaluate_approval(
            approved, df_unique_NST_comments, vectorizer, xgb_model)
        if zpred[0, 1] > 0.90:
            text = 'Approval Chances More'
        elif zpred[0, 1] > 0.6 and zpred[0, 1] <= 0.9:
            text = 'Not Sure'
        else:
            text = 'Approval Denail More!!'
        return {
            "label": text,
            "score": zpred
        }

    if name == 'get_default_comments':
        return get_default_comments(inp1, inp2, inp3, inp4)
    elif name == 'nst_re_score':
        return nst_re_score(inp1)


def get_defaults():
    return main_fun(name='get_defaults', inp1=None, inp2=None, inp3=None, inp4=None)


def get_default_comments(nst_type, nst_group, sub_region=None):
    return main_fun(name='get_default_comments', inp1=nst_type, inp2=nst_group, inp3=sub_region, inp4=None)


def nst_re_score(data):
    return main_fun(name='nst_re_score', inp1=data)

# # %% Stream Lit

# # Display Images

# # import Image from pillow to open images
# img = Image.open(
#     "C:\\Users\\ndasadhikari\\OneDrive - Microsoft\\Documents\\Python Scripts\\mslogo.png")

# # display image using streamlit
# # width is used to set the width of an image
# st.sidebar.image(img, width=305)

# st.title("NST Analysis")

# selectbox = st.sidebar.selectbox(
#     "Manually Write the NST Comments?",
#     ["Yes", "No"]
# )

# checkbox_two = st.sidebar.selectbox("NST Group", NST_groups)
# checkbox_one = st.sidebar.selectbox("NST Type", NST_types)
# checkbox_three = st.sidebar.selectbox("SubRegion", SubRegion)

# value1 = checkbox_one
# value2 = checkbox_two
# value3 = checkbox_three

# # %% Df Approved for the Recommendation
# df_training1 = df_recommended1
# # print('aa',df_training1.columns)
# df_approved = df_training1[df_training1['New Review Recommendation'] == 1]

# df_approved1 = df_approved[df_approved['NST Type'] == value1]
# print(df_approved1.shape)
# df_approved12 = df_approved1[df_approved1['NST Group'] == value2]
# print(df_approved1.shape)
# df_approved13 = df_approved12[df_approved12['SubRegion'] == value3]
# print(df_approved13.shape)
# # df_approved1.head()

# if df_approved13.shape[0] == 0:
#     if df_approved12.shape[0] == 0:
#         if df_approved1.shape[0] == 0:
#             df_approval_reco = df_approved
#         else:
#             df_approval_reco = df_approved1
#     else:
#         df_approval_reco = df_approved12
# else:
#     df_approval_reco = df_approved13

# df_approval_reco['NST_clean_translated_Comment'] = df_approval_reco['NST_clean_translated_Comment'].apply(
#     str)
# df_approval_reco['length'] = df_approval_reco['NST_clean_translated_Comment'].map(
#     lambda text: len(text))
# df_approval_reco['NST_clean_translated_Comment'] = df_approval_reco['NST_clean_translated_Comment'].apply(
#     lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

# value_counts = df_approval_reco['NST_clean_translated_Comment'].value_counts(
#     dropna=True, sort=True)

# # solution here
# df_NST_counts = pd.DataFrame(value_counts)
# df_unique_NST_comments = df_NST_counts.reset_index()
# df_unique_NST_comments.columns = ['unique_NST_comments', 'counts']


# # %%

# if selectbox == 'Yes':
#     comment_type = st.text_input("Enter NST Comment", "Type Here ...")
#     approved = comment_type.title()

# else:
#     approved = 'Please Enter the Comments here.....'

#     if value1 == None and value2 == None:
#         selected_comments = list(df_recommended1['NST Translater'].values)
#         approved = st.selectbox("NST Comment Selection",
#                                 selected_comments[:10])
#     elif value1 != None and value2 != None:
#         data = df_recommended1[df_recommended1['NST Type'] == value1]
#         data1 = data[data['NST Group'] == value2]
#         df_recommend_approval_nst = list(data1['NST Translater'].values)
#         approved = st.selectbox("NST Comment Selection",
#                                 df_recommend_approval_nst[:10])
#     elif value1 != None and value2 == None:
#         data = df_recommended1[df_recommended1['NST Type'] == value1]
#         data1 = data
#         df_recommend_approval_nst = list(data1['NST Translater'].values)
#         approved = st.selectbox("NST Comment Selection",
#                                 df_recommend_approval_nst[:10])
#     elif value1 == None and value2 != None:
#         data = df_recommended1[df_recommended1['NST Group'] == value2]
#         data1 = data
#         df_recommend_approval_nst = list(data1['NST Translater'].values)
#         approved = st.selectbox("NST Comment Selection",
#                                 df_recommend_approval_nst[:10])
#     else:
#         comment_type = st.text_input("Enter NST Comment", "Type Here ...")
#         approved = comment_type.title()

# st.write("NST Comment:")
# st.write(approved)

# if(st.button('Evaluate Approval Process')):
#     zpred = evaluate_approval(
#         approved, df_unique_NST_comments, vectorizer, xgb_model)
#     if zpred[0, 1] > 0.90:
#         st.success('Approval Chances More')
#         if(st.button('Submit')):
#             st.success(
#                 'NST Comment Submitted Successfully. Id generated xx0003edf')

#     elif zpred[0, 1] > 0.6 and zpred[0, 1] <= 0.9:
#         st.warning('Not Sure')
#         selectbox = st.selectbox(
#             "Wish to Change the NST Comments?",
#             ["Yes", "No"]
#         )
#         if selectbox == 'Yes':
#             st.info(
#                 'Navigate to the Left Side and Select the proper NST Group and NST Type')
#         elif selectbox == 'No':
#             if(st.button('Submit')):
#                 st.success(
#                     'NST Comment Submitted Successfully. Id generated xx0003edf')
#     else:
#         st.error('Approval Denail More!!')
#         selectbox = st.selectbox(
#             "Wish to Change the NST Comments?",
#             ["Yes", "No"]
#         )
#         if selectbox == 'No':
#             if(st.button('Submit')):
#                 st.success(
#                     'NST Comment Submitted Successfully. Id generated xx0003edf')
#         else:
#             st.info(
#                 'Navigate to the Left Side and Select the proper NST Group and NST Type')
