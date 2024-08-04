#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

from tqdm import tqdm
import pandas as pd
#%%
# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


#%%
# Locate the other items

product_items = {
    'ISA' : 'https://obank.kbstar.com/quics?page=C041164',
    '방카슈랑스' : 'https://obank.kbstar.com/quics?page=C019237',
    '골드뱅킹' : 'https://obank.kbstar.com/quics?page=C016622'
    }

#%%
def main(): 
    items = []

    for key, value in tqdm(product_items.items(), desc="get crawling other item..."):
        item_name = key
        url = value
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # 10 seconds wait time
        time.sleep(2)
        
        if item_name == 'ISA':
            feature = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[1]/img')  
            feature = feature.get_attribute('alt')
            items.append((key, feature))
        elif item_name == '방카슈랑스':
            feature = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[1]/img')
            feature = feature.get_attribute('alt')
            items.append((key, feature))
        elif item_name == '골드뱅킹':
            name = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[1]/h2/b').text
            feature = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/ul/li[1]').text
            feature = re.sub("\n", "", feature)
            name = re.sub("\n", " ", name)
            items.append((name, feature))

    return items

#%%
product = main()
columns = ["상품이름", "상품특징"]
products_df = pd.DataFrame(product, columns=columns)
products_df.to_csv('./assets/other_product.csv', index=False)

driver.quit()
# %%
