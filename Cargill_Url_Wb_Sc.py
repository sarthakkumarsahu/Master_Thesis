from __future__ import print_function
import re
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
import pandas as pd
import json
import os
os.chdir("C:\\Users\\sarth\\PycharmProjects\\Big_Data_Analysis_Project\\Master_Thesis")

input_file = pd.read_csv("final_url_cargill.csv")
input_file['Id'] = ''
input_file['Date'] = ''
input_file['Heading'] = ''
input_file['Text'] = ''

url = input_file.iloc[1,0]
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
urlpage = urlopen(req).read()
bswebpage = BeautifulSoup(urlpage,"html.parser")
date = bswebpage.find("div",{"class":"article-sub-content-header"}).text
print(date)

for i in range(len(input_file)):
    url = input_file.iloc[i,0]
    input_file.iloc[i,2] = i
    print(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    urlpage = urlopen(req).read()
    bswebpage = BeautifulSoup(urlpage,"html.parser")

    try:
        heading = bswebpage.find("h1").text
        #print(heading)
        input_file.iloc[i, 3] = heading
    except Exception as e:
        input_file.iloc[i,3] = ""

    try:
        date = bswebpage.find("div",{"class":"article-sub-content-header"}).text
        #print(date)
        input_file.iloc[i, 2] = date
    except Exception as e:
        input_file.iloc[i, 2] = ""

    try:
        content = bswebpage.find("div",{"class":"padding-default padding-default-sides"}).text
        #print(content)
        input_file.iloc[i, 4] = content
    except Exception as e:
        input_file.iloc[i,4] = ""

input_file.to_excel(r"master_file_cargill.xlsx",index=None, header=True)