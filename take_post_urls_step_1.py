import time
import random
import requests
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests import RequestException


BASE_URL = "https://www.youthall.com/tr/jobs/"
MAX_PAGES = 5
CLASS_MAIN_CARD = 'l-grid__col l-grid__col--lg-4 l-grid__col--md-4 l-grid__col--xs-12 u-gap-bottom-25'

def take_posts():
    #agent header to seem like a user
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random #get a random user agent
    }
    posts = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE_URL}?page={page}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            post_cards = soup.find_all('div', class_=CLASS_MAIN_CARD)

            if not post_cards:
                break
            for card in post_cards:
                link_tag = card.find('a')
                if link_tag:
                    try:
                        post_url = link_tag['href']

                        company_tag_name = link_tag.find('label', class_='jobs-content-company')
                        if company_tag_name:
                            company = company_tag_name.text.strip()
                        else:
                            company = "company name not found"

                        post_name_tag = link_tag.find('div', class_='jobs-content-title')
                        if post_name_tag:
                            post = post_name_tag.text.strip()
                        else:
                            post = "no post name found"

                        posts.append({
                            "Post Name": post,
                            "Company Name": company,
                            "Post URL": post_url
                        })
                    except Exception as e:
                        print(f"Error found this post will be skipped:", e)
                        continue
        except RequestException as e:
            print("Error found while connecting:", e)
            break

        crawl_delay = random.uniform(1, 3)
        time.sleep(crawl_delay)

    posts_list = pd.DataFrame(posts)
    if posts_list.empty:
        exit()
    return posts_list

