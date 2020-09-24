from __future__ import print_function
import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import json

url_cargill_final = pd.DataFrame(columns=["URL_name"])

for i in range(1,100000):

    url = "https://www.cargill.com/cs/ContentServer?d=&pagename=CCOM/AjaxHandlers/FilterListPaginationHandler&query_asset=CGL_SpecialModule_C%3A1432079769596&module_asset=CGL_ContentModule_C%3A1432079809064&sort_by_attr=CCOM_PublishDate&sort_by_order=descending&selected_filters=CCOM_Topic%253AAny%253A%253ACCOM_Region%253AAny%253A%253ACCOM_PublishYear%253AAny&display_attrs=assetId%2CassetType%2Curl%2CCCOM_Topic%2CCCOM_Region%2CCCOM_PublishYear&result_start_index="+str(i)+"&view_type=Content+Preview+Accent+Rules&results_per_page=12&site=CCOM&sitepfx=CCOM&max_results_count=200"
    print("Reading : " + url)
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        urlpage = urlopen(req).read()
    except Exception as e:
        break
    bswebpage = BeautifulSoup(urlpage,"html.parser")
    #print(bswebpage)
    results = bswebpage.find_all("h3")
    if len(results)==0:
        break
    url_list = []
    for h in results:
        url = str(h.find('a',href=True)['href'])
        url_list.append(url)
    url_cargill_final = url_cargill_final.append(pd.DataFrame(url_list, columns=['URL_name']), ignore_index=True)

url_cargill_final.to_csv(r"final_url_cargill.csv",index=None, header=True)
