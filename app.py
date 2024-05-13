import solara as sl
import re
from src.data_scraper import get_scrap_data

text = sl.reactive("")

def validate_website(website_url):
    print("validate_website() called!!")
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp://
        r'(?!localhost)'  # Exclude localhost
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Validate the URL using the pattern
    if re.match(url_pattern, website_url):
        return True
    else:
        return False

@sl.component
def Page():
    sl.AppBarTitle("Chat!")
    with sl.Sidebar():
        sl.InputText("Enter the website ", value=text, continuous_update=False)
        if text.value :
            domine_website_url = text.value
            sl.Markdown(f"Entered website is : {domine_website_url}")
            sl.Markdown("Analyzing website .......")
            is_url_validation_success = validate_website(domine_website_url)
            if is_url_validation_success:
                sl.Markdown("Good url")
                response = get_scrap_data(domine_website_url)
                if response['hasError'] == False:
                    scrapDataFrame = response['data']
                    scrapDataFrame.to_csv("scrap_data.csv")
                    sl.Markdown("/Csv saved successfully./",style={"color":"green"})
                else:
                    sl.Markdown("Error Occurred!",style={"color":"red"})
            else:
                sl.Markdown("Please enter a valid website !",style={"color":"red"})
        