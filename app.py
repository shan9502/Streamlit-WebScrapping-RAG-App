import streamlit as st
from src.dataScrap import get_scrap_data,get_sitemap

with st.sidebar:
    website_link = st.text_input("Enter any website link and chat with it!",placeholder="https://exmaple.com/")
    if website_link:
        st.write("Entered website link is - ",website_link)
        st.write("Checking the website ......")
        if 'sitemap_status' not in st.session_state or st.session_state.sitemap_status == False:
            rawPagesList = get_sitemap(website_link)
            pageListLength = len(rawPagesList)
            st.session_state.sitemap_status = True
        if pageListLength > 1:
            scrapLimitRangeList = list(range(1,pageListLength+1))
            st.write("The website have ",pageListLength," sub pages.")
            scrapLimit = st.select_slider("How deep you want to Go..",
                                        options=scrapLimitRangeList)
            print("here1")
        elif pageListLength == 0:
            print("here2")
            rawPagesList = [website_link]
            pageListLength = 1
            scrapLimit = 2
        else:
            print("here3")
            scrapLimit = 2
        
        if pageListLength != 0:
            scrap_img = st.checkbox("Do you want to analyze the images also!")
            if st.button("Confirm"):
                print("scrapLimit:",scrapLimit)
                rawPagesList = rawPagesList[0:scrapLimit]
                st.write("Scraping process started.........")
                resp = get_scrap_data(rawPagesList,scrap_img)
                
                print("Reached for get_scrap_data()")
                print("rawPagesList:",len(rawPagesList),"\nscrap_img:",scrap_img)
                # resp=0
                
                if resp['hasError'] == False:
                    scrapDataFrame = resp['data']
                    scrapDataFrame.to_csv("scrap_data.csv")
                    st.write("/Csv saved successfully./")
                else:
                    st.write(str(resp['message']))

