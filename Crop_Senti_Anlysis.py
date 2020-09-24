import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
from statistics import mean
from statistics import variance
import os
import re

os.chdir("C:\\Users\\sarth\\PycharmProjects\\Big_Data_Analysis_Project\\Master_Thesis")

input_file = pd.read_csv("master_file_agri.csv")
SENTENCE_TOKENS_PATTERN = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?|\!)\s'
regex_st = nltk.tokenize.RegexpTokenizer(pattern=SENTENCE_TOKENS_PATTERN,gaps=True)
cachedStopWords = stopwords.words('english')

st = PorterStemmer()

col_names = ['Id','Date','Polarity','Polarity_Variance','Subjectivity','Subjectivity_Variance','Crop_Name']
crop_name_df = pd.DataFrame(columns=col_names)

def senti(x):
    return TextBlob(x).sentiment
crop_names = ["maize","rice","wheat"]

for cname in crop_names:
    for i in range(len(input_file)):
        text_tok = regex_st.tokenize(str(input_file.iloc[i,5]))
        list_senti = []
        list_sub = []
        Id = input_file.iloc[i,0]
        Date = input_file.iloc[i,2]
        for sent in text_tok:
            clean_text = re.sub('[^A-Za-z]+', ' ',sent.lower().replace(u'\xa0',u' '))
            clean_text = ' '.join([word for word in clean_text.split() if word not in cachedStopWords])
            stem_text = ' '.join([st.stem(word) for word in clean_text.split()])
            senti_out = senti(stem_text)
            print(cname in clean_text)
            print(round(senti_out[0],2))
            print(round(senti_out[1],2))
            if (cname in clean_text):
                list_senti.append(round(senti_out[0],2))
                list_sub.append(round(senti_out[1],2))
        try:
            max_val_s = max(list_senti)
            min_val_s = abs(min(list_senti))

            if (max_val_s > min_val_s):
                avg_pol = max(list_senti)
            else:
                avg_pol = min(list_senti)
            #avg_pol = round(max(max_val_s,min_val_s),2)
        except Exception as e:
            avg_pol = None

        try:
            var_pol = round(variance(list_senti),2)
        except Exception as e:
            var_pol = None

        try:
            max_val_o = max(list_sub)
            min_val_o = abs(min(list_sub))

            if (max_val_o > min_val_o):
                avg_sub = max(list_sub)
            else:
                avg_sub = min(list_sub)
            #avg_sub = round(max(max_val_o,min_val_s),2)
        except Exception as e:
            avg_sub = None

        try:
            var_sub = round(variance(list_sub),2)
        except Exception as e:
            var_sub = None

        if (avg_pol is not None and avg_sub is not None):
            temp_dic = {'Id': Id,'Date': Date,'Polarity':avg_pol,'Polarity_Variance':var_pol,'Subjectivity':avg_sub,'Subjectivity_Variance':var_sub,'Crop_Name':cname}
            crop_name_df = crop_name_df.append(temp_dic,ignore_index=True)
    
crop_name_df.to_csv(r"master_senti_crop.csv",index=None, header=True)