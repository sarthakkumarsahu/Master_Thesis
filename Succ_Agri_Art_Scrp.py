from __future__ import print_function
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import json
import os
#os.chdir("C:\\Users\\sarth\\PycharmProjects\\Big_Data_Analysis_Project\\Master_Thesis")

input_file = pd.read_csv("final_url_succ_agri.csv")
input_file['Date'] = ''
input_file['Heading'] = ''
input_file['subtitle'] = ''
input_file['Text'] = ''

for i in range(len(input_file)):
    url = input_file.iloc[i,0]
    print(url)
    urlpage = urlopen(url).read()
    bswebpage = BeautifulSoup(urlpage,"html.parser")

    try:
        heading = bswebpage.find("h1").text
        input_file.iloc[i, 2] = heading
    except Exception as e:
        input_file.iloc[i,2] = ""

    try:
        subtitle = bswebpage.find("div",{"class":"field-subheading"}).text
        input_file.iloc[i, 3] = subtitle
    except Exception as e:
        input_file.iloc[i,3] = ""

    try:
        date = bswebpage.find("div",{"class":"byline-date"}).text
        input_file.iloc[i, 1] = date
    except Exception as e:
        input_file.iloc[i, 1] = ""

    try:
        content = bswebpage.find("div",{"class":"field-body"}).text
        new_string = ""
        for lines in content.split("\n"):
            input_str = lines.strip()
            #print(input_str)
            rep_param_1 = input_str.find("READ MORE:")
            rep_param_2 = input_str.find("Want more agriculture, technology, and investment news?")
            rep_param_3 = len(input_str)
            #print(rep_param_1,rep_param_2,rep_param_3)

            if (rep_param_1 !=0 and rep_param_2!=0 and rep_param_3>1):
                new_string = new_string + input_str
                new_string = new_string.replace(u'\xa0', u' ')
                #print(new_string)
        #print(new_string)
        print("------------------end-----------------")
        input_file.iloc[i,4] = str(new_string)
    except Exception as e:
        input_file.iloc[i,4] = ""

input_file.to_csv(r"master_file_agri.csv",index=None, header=True)

