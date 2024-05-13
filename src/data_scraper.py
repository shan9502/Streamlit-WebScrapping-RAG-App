from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from usp.tree import sitemap_tree_for_homepage
from app_logger import logger

def get_pages_from_sitemap(fullDomain):
    try:
        listPagesRaw = []
        tree = sitemap_tree_for_homepage(fullDomain)
        for page in tree.all_pages():
            listPagesRaw.append(page.url)
        return listPagesRaw
    except Exception as e:
        logger.error(e)
        return []
    
def text_preprocess(web_text):
    current_text = web_text.replace("\n\n","\n").replace("\n"," ")
    while "  " in current_text:
        current_text = current_text.replace("  "," ")
    # print(current_text)
    return current_text
    
def get_scrap_data(domain_url):
    url_list = []
    text_list = []
    list_img_list = []
    scrap_data_frame = pd.DataFrame()
    
    listPagesRaw = get_pages_from_sitemap(domain_url)
    if len(listPagesRaw) == 0:
        return {"hasError":True, "data":scrap_data_frame,"message":"Sitemap Error!"}
    pageShortList = listPagesRaw[0:10]
    
    try:
        for url in pageShortList:
            req = Request(url, headers={'User-Agent' : "Magic Browser"}) 
            page = urlopen( req )
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            raw_img_list = soup.find_all("img")
            url_list.append(url)
            processed_text = text_preprocess(soup.get_text())
            text_list.append(processed_text)
            img_list = []
            for img in raw_img_list:
                for img_list_check in list_img_list:
                    if img['src'] not in img_list_check:
                       img_list.append(img['src']) 
            list_img_list.append(img_list)
        scrap_data_frame['urls'] = url_list
        scrap_data_frame['texts'] = text_list
        scrap_data_frame['image_url_list'] = list_img_list
        return {"hasError":False, "data":scrap_data_frame}
    except Exception as e:
        logger.error(e)
        return {"hasError":True, "data":scrap_data_frame,"message":e}
        
    
        