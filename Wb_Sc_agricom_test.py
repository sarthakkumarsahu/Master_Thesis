from __future__ import print_function
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import json

url_succ_farm_final = pd.DataFrame(columns=["URL_name"])

for i in range(1,10000):

    url = "https://www.agriculture.com/news?page="+ str(i)
    print("Reading : " + url)
    try:
        urlpage = urlopen(url).read()
    except Exception as e:
        break
    bswebpage = BeautifulSoup(urlpage,"html.parser")
    results = bswebpage.find("script",{'type':"application/ld+json"})
    #print(results)

    url_list = []
    #for result in results:
    json_content = json.loads(results.text)
    #print(len(json_content["itemListElement"]))
    if len(json_content["itemListElement"]) == 0:
        break
    for url in json_content["itemListElement"]:
        print("---------------end------------------")
        url_val = str(url['url'])
        rep_param_1 = url_val.find("/video")
        rep_param_2 = url_val.find("/podcast")
        print(url_val)
        print(rep_param_1,rep_param_2)
        if (rep_param_1<0 and rep_param_2<0):
            url_list.append(url['url'])
        #print(url['url'])
    url_succ_farm_final = url_succ_farm_final.append(pd.DataFrame(url_list, columns=['URL_name']), ignore_index= True)

url_succ_farm_final.to_csv(r"final_url_succ_agri.csv",index=None, header=True)
