#%%
import os
import sys

import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.utils import TextProcessor
#%%
class WebResearch:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.text_processor = TextProcessor()

    def get_blog_links(self, query, num_results=3):
        naver_engine = f'https://search.naver.com/search.naver?ssc=tab.blog.all&query={query}&sm=tab_opt&nso=so%3Ar%2Cp%3A6m'
        
        response = requests.get(naver_engine, headers=self.headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        blog_list = soup.find_all('div', attrs={"class": "title_area"})

        titles = []
        links = []

        idx = 0  # numbering

        for blog in blog_list:
            title_tag = blog.find("a", attrs={"class": "title_link"})
            if title_tag:
                title = title_tag.get_text()
                link = title_tag['href']

                # 링크가 'cafe'를 포함하지 않는 경우만 추가
                if 'cafe' not in link:
                    titles.append(title)
                    links.append(link)
                    idx += 1

                    if idx >= num_results:
                        break

        return titles, links

    def get_blog_contents(self, links):
        contents = []

        for link in links:
            response = requests.get(link, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # extract real blog url
            real_engine = "https://blog.naver.com" + soup.find('iframe').get('src')
            response_new = requests.get(real_engine, headers=self.headers)
            soup_new = BeautifulSoup(response_new.content, 'html.parser')

            bodys = soup_new.find_all('div', attrs={"class": "se-module se-module-text"})
            content = ''

            for body in bodys:
                text = body.get_text()
                cleaning_text = self.text_processor.clean_text(text)
                content += cleaning_text

            content = content.replace('\u200b', '')
            contents.append(content)

        return contents

    def get_dict_links(self, query, num_results=3):
        word = self.text_processor.extract_first_noun_phrase(query)

        naver_dic_engine = f'https://terms.naver.com/search.naver?query={word}&searchType=text&dicType=&subject='
        
        response = requests.get(naver_dic_engine, headers=self.headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        word_list = soup.find_all('div', attrs={'class': 'search_result_area'})

        titles = []
        links = []

        idx = 0  # numbering

        for word in word_list:
            if idx >= num_results:
                break
            strong_tag = word.find('strong', class_='title')
            title = strong_tag.get_text(strip=True)
            titles.append(title)

            a_tag = strong_tag.find('a')
            if a_tag:
                link = a_tag.get('href')
                full_link = f"https://terms.naver.com{link}" if link else None
                links.append(full_link)

            idx += 1

        return titles, links

    def get_dict_contents(self, links):
        contents = []

        for link in links:
            response = requests.get(link, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            bodys = soup.find_all('p', attrs={'class': 'txt'})
            content = ''

            for body in bodys:
                text = body.get_text()
                cleaning_text = self.text_processor.clean_text(text)
                content += cleaning_text

            contents.append(content)

        return contents
#%%