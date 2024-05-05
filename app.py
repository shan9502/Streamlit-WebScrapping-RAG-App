import streamlit as st
from src.dataScrap import getScrapData

website_link = st.text_input("Enter any website link and chat with it!")

if website_link:
    st.write("Entered website link is - ",website_link)
    st.write("Process started.........")
    resp = getScrapData(website_link)
    if resp['hasError'] == False:
        scrapDataFrame = resp['data']
        scrapDataFrame.to_csv("scrap_data.csv")
        st.write("/Csv saved successfully./")
    else:
        st.write("Error Occurred!")

