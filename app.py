import solara as sl
import re
from src.data_scraper import get_scrap_data,get_sitemap

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
        if sl.Button(label = "Go"):
            if text.value :
                domine_website_url = text.value
                sl.Markdown(f"Entered website is : {domine_website_url}")
                sl.Markdown("Analyzing website .......")
                is_domine_validation_success = validate_website(domine_website_url)
                if is_domine_validation_success:
                    sl.Markdown("Examining Website .......")
                    domine_subpages_list = get_sitemap(domine_website_url)
                    page_list_length = len(domine_subpages_list)
                    if page_list_length > 1:
                        # scrap_limit_range_list = list(range(1,page_list_length+1))
                        if page_list_length < 10:
                            preset_value = page_list_length
                        elif page_list_length > 100:
                            preset_value = 50

                        sl.Markdown(f"The website have {page_list_length} sub pages.")
                        scrap_limit = sl.SliderInt(label="How deep you want to Go..",value=preset_value,
                                                    min=1,max=page_list_length)
                        print("here1")
                    elif page_list_length == 0:
                        print("here2")
                        domine_subpages_list = [domine_website_url]
                        page_list_length = 1
                        scrap_limit = 2
                    else:
                        print("here3")
                        scrap_limit = 2
                    
                    if page_list_length != 0:
                        is_confirm_status = False
                        scrap_img = sl.Checkbox(label="Do you want to analyze the images also!",value=False)
                        sl.Button(label = "Confirm", on_click = is_confirm)
                        if is_confirm_status:
                            print("scrap_limit:",scrap_limit)
                            domine_subpages_list = domine_subpages_list[0:scrap_limit]
                            sl.Markdown("Scraping process started.........")
                            response = get_scrap_data(domine_subpages_list,scrap_img)
                            
                            print("Reached for get_scrap_data()")
                            print("domine_subpages_list:",len(domine_subpages_list),"\nscrap_img:",scrap_img)
                            # sl.Markdown("Good url")
                            # response = get_scrap_data(domine_website_url)
                            if response['hasError'] == False:
                                scrapDataFrame = response['data']
                                scrapDataFrame.to_csv("test/scrap_data.csv")
                                sl.Markdown("/Csv saved successfully./",style={"color":"green"})
                            else:
                                sl.Markdown("Error Occurred!",style={"color":"red"})
                else:
                    sl.Markdown("Please enter a valid website !",style={"color":"red"})

def is_confirm():
    is_confirm_status = True
        