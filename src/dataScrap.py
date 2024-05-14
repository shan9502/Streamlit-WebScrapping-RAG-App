from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from usp.tree import sitemap_tree_for_homepage
from appLog import logger

def get_sitemap(fullDomain):
    rawPagesList = []
    try:       
        # tree = sitemap_tree_for_homepage(fullDomain)
        # for page in tree.all_pages():
        #     rawPagesList.append(page.url)
        print("get_sitemap called!!!!")
        return rawPagesList

    except Exception as e:
        logger.error(e)
        rawPagesList

def get_img_urls(raw_img_list):
    # list_img_list = []
    try:
        img_list = []
        if len(raw_img_list)>0:
            for img in raw_img_list:
                img_list.append(img['src']) 
            # list_img_list.append(img_list)
            return img_list
        else:
            return None
    except Exception as e:
        logger.error(e)
        print(e)
        return None
    
def text_preprocess(web_text):
    current_text = web_text.replace("\n\n","\n").replace("\n"," ")
    while "  " in current_text:
        current_text = current_text.replace("  "," ")
    # print(current_text)
    return current_text
    
def get_scrap_data(pageUrlList,scrap_img=False):
    url_list = []
    text_list = []
    list_img_list = []
    scrap_data_frame = pd.DataFrame()
    
    if len(pageUrlList) == 0:
        return {"hasError":True, "data":scrap_data_frame,"message":"Sitemap Error!"}    
    try:
        for url in pageUrlList:
            req = Request(url, headers={'User-Agent' : "Magic Browser"}) 
            page = urlopen( req )
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")           
            url_list.append(url)
            processed_text = text_preprocess(soup.get_text())
            text_list.append(processed_text)
            if scrap_img == True:
                #get all img urls from soup
                raw_img_list = soup.find_all("img")
                img_list = get_img_urls(raw_img_list)
                list_img_list.append(img_list)
            
        scrap_data_frame['urls'] = url_list
        scrap_data_frame['texts'] = text_list
        scrap_data_frame['image_url_list'] = list_img_list if list_img_list else None
        print("Length of page url length:",len(pageUrlList))
        return {"hasError":False, "data":scrap_data_frame}
    except Exception as e:
        logger.error(e)
        print(e)
        return {"hasError":True, "data":scrap_data_frame,"message":e}
        
    
        