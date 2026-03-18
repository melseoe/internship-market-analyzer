import time
import random
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def take_post_details(posts_list):
    service = Service(ChromeDriverManager().install()) #to use the web driver, create a service object
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") # headless mode for a quicker workflow

    ua = UserAgent()
    rand_ua = ua.random
    chrome_options.add_argument(f"user-agent={rand_ua}") #set a random user agent
    driver = webdriver.Chrome(service=service, options=chrome_options) #start web driver

    list_of_locations = []
    list_of_post_types = []
    list_of_departments = []
    list_of_sectors = []

    for _, row in posts_list.iterrows():
        post_url = row['URL']
        crawl_delay = random.uniform(1, 3)
        time.sleep(crawl_delay)
        
        post_location = "NotFound"
        post_type = "NotFound"
        post_department = "NotFound"
        post_sector = "NotFound"
        
        try:
            driver.get(post_url)
            WebDriverWait(driver, 18).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #checking if the post is loaded by the body tag of the HTML
            detailed_page = BeautifulSoup(driver.page_source, "html.parser")
            html_parts = detailed_page.find_all("div", class_="c-job_detail_content_list")

            for part in html_parts:
                if part.find("h6"):
                    tag_name = part.find("h6").text.strip()
                else:
                    tag_name = ""

                if part.find("small"):
                    tag_content = part.find("small").text.strip()
                else:
                    tag_content = ""

                if "Departman" in tag_name or "Job function" in tag_name:
                    if tag_content == "-":
                        tag_content = "Çeşitli Departmanlar"
                    post_department = tag_content
                elif "İlan Türü" in tag_name or "Type" in tag_name:
                    post_type = tag_content
                elif "Çalışma Lokasyonları" in tag_name or "Working Locations" in tag_name:
                    tag_content = re.sub(r'\s+', ' ', tag_content).strip() #substitute multiple spaces with a single space
                    tag_content = tag_content.replace(' ,', ',').replace(', ', ',') #replace spaces around commas with no space
                    post_location = tag_content


                post_sector = "NotFound"
                aside_tags = detailed_page.find_all("aside", class_= "l-grid__col l-grid__col--lg-4 l-grid__col--xs-12")
                if aside_tags:
                    aside_element = aside_tags[0] #get the first aside element, there is one for this format

                    sector_div_element = aside_element.find("div", class_= "c-company-card__sector")
                    if sector_div_element:
                        sector_detailed_div = sector_div_element.find('div')
                        if sector_detailed_div:
                            elements = sector_detailed_div.contents #get the elements in the div tag
                            if len(elements) > 1 and isinstance(elements[1], str): #when the elements in the div are 2, it is the second one that contains the sector value
                                post_sector = elements[1].strip()
                            elif len(elements) > 0 and isinstance(elements[0], str): #when there are div tags with only the value
                                post_sector = elements[0].strip()

                    if 'İlan' in post_sector: #the case of there being multiple same postings with the numbering 1, 2, ... at the end
                        post_sector = post_sector.split('İlan')[0].strip()

            list_of_locations.append(post_location)
            list_of_post_types.append(post_type)
            list_of_departments.append(post_department)
            list_of_sectors.append(post_sector)

        except Exception as e:
            print(f"Error found, this post will be skipped", e)
            list_of_locations.append("ERROR")
            list_of_post_types.append("ERROR")
            list_of_departments.append("ERROR")
            list_of_sectors.append("ERROR")
            continue

    driver.quit() #quit the web driver

    # place the found elements of the post into the list
    posts_list["Location"] = list_of_locations
    posts_list["Post Type"] = list_of_post_types
    posts_list["Department"] = list_of_departments
    posts_list["Sector"] = list_of_sectors

    #loop to fix the spacing in the dataframe object
    for col in ["Location", "Post Type", "Department", "Sector"]:
        posts_list[col] = posts_list[col].str.replace('\n', ' ', regex = False)  #replace end lines with a single space
        posts_list[col] = posts_list[col].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip())  #substitute multiple spaces with single space
    return posts_list