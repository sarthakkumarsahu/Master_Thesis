from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import os
import re

os.chdir("C:\\Users\\sarth\\PycharmProjects\\Big_Data_Analysis_Project\\Master_Thesis")


input_file = pd.read_csv("master_file_agri.csv")
input_file['Political'] = ""
input_file['Political_Terms'] = ""
input_file['Economical'] = ""
input_file['Economical_Terms'] = ""
input_file['Social'] = ""
input_file['Social_Terms'] = ""
input_file['Technological'] = ""
input_file['Technological_Terms'] = ""
input_file['Environment'] = ""
input_file['Environment_Term'] = ""
input_file['Legal'] = ""
input_file['Legal_Term'] = ""

def pre_process(text):

    #lower case
    text = str(text)
    text = text.lower()

    #remove special characters
    text = re.sub("(\\d|\\W)+"," ",text)

    return text

def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

def compare(trigrams1, trigrams2):
    common=[]
    for grams1 in trigrams1:
       if grams1 in trigrams2:
         common.append(grams1)
    return common

stop_words = get_stop_words("resources/stopwords.txt")

Political_list = ['government stability', 'government instability','corruption level', 'tax policies', 'freedom press', 'government regulation deregulation', 'special tariffs', 'political action committees', 'government involvement','trade unions agreements', 'competition regulation', 'voter participation rates', 'amount government protests', 'defense expenditures', 'level government subsidies', 'bilateral relationships', 'import export regulation resctrictions', 'trade control', 'lobbying activities', 'size government budgets']
Economic_list = ['growth rate', 'interest rate', 'inflation rate', 'exchange rate', 'availability credit', 'level disposible income', 'propensity people spend', 'federal government budget deficits', 'gross domestic product trend', 'unemployment trend', 'stock market trends', 'price fluctuations']
Social_list = ['population size growth rate', 'birth rates', 'death rates', 'number mariages', 'number divorces', 'immigration emigration rates', 'life expectancy rates', 'age distribution', 'wealth distribution', 'social classes', 'capita income', 'family size structure', 'lifestyles', 'health consciousness', 'average disposable income', 'attitude government', 'attitude work', 'buying habits', 'ethical concerns', 'cultural norms values', 'sex roles distribution', 'religion beliefs', 'racial equality', 'birth control', 'education level', 'minorities', 'crime levels', 'attitudes saving', 'attitude investing', 'attitudes retirement', 'attitudes leisure time', 'attitudes product quality', 'attitudes customer service', 'attitudes foreign people']
Technology_list = ['technology incentives', 'automation', 'activity', 'technological change', 'access new technology', 'level innovation', 'technological awareness', 'internet infrastructure', 'communication infrastructure', 'life cycle technology']
Environment_list = ['weather', 'climate', 'environmental policies', 'climate change', 'pressures ngo', 'natural disasters', 'air water pollution', 'recycling standards', 'attitudes green products', 'support renewable energy']
Legal_list = ['discrimination laws', 'antitrust laws', 'employment laws', 'consumer protection laws', 'copyright patent laws', 'health safety laws', 'education laws', 'consumer protection laws', 'data protection laws']

for i in range(len(input_file)):
    print(i)
    print(input_file.iloc[i,1])
    clean_text = pre_process(input_file.iloc[i,5])
    clean_text = ' '.join([word for word in clean_text.split() if word not in stop_words])
    bv = CountVectorizer(ngram_range=(2,3))

    try:
        bv_matrix =bv.fit_transform([clean_text])
        vocab = bv.get_feature_names()
    except Exception as e:
        vocab = []

    #For Political
    if(len(compare(vocab,Political_list))>0):
        input_file.iloc[i,6] = 1
        input_file.iloc[i,7] = '|'.join(compare(vocab,Political_list))

    #For Economical
    if(len(compare(vocab,Economic_list))>0):
        input_file.iloc[i,8] = 1
        input_file.iloc[i,9] = '|'.join(compare(vocab,Economic_list))

    # For Social
    if (len(compare(vocab, Social_list)) > 0):
        input_file.iloc[i, 10] = 1
        input_file.iloc[i, 11] = '|'.join(compare(vocab, Social_list))


    # For Technological
    if (len(compare(vocab, Technology_list)) > 0):
        input_file.iloc[i, 12] = 1
        input_file.iloc[i, 13] = '|'.join(compare(vocab, Technology_list))


    # For Environment
    if (len(compare(vocab, Environment_list)) > 0):
        input_file.iloc[i, 14] = 1
        input_file.iloc[i, 15] = '|'.join(compare(vocab, Environment_list))


    # For Legal
    if (len(compare(vocab, Legal_list)) > 0):
        input_file.iloc[i, 16] = 1
        input_file.iloc[i, 17] = '|'.join(compare(vocab, Legal_list))



input_file.to_excel(r"master_PESTEL.xlsx",index=None, header=True)


# list = ['Discrimination laws',
# 'Antitrust laws',
# 'Employment laws',
# 'Consumer protection laws',
# 'Copyright and patent laws',
# 'Health and safety laws',
# 'Education laws',
# 'Consumer protection laws',
# 'Data protection laws']
#
# list_clean = []
#
# for i in list:
#     c_list = pre_process(i)
#     c_list = ' '.join([word for word in c_list.split() if word not in stop_words])
#     list_clean.append(c_list)
#


