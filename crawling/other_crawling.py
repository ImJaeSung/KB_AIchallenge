#%%
import os
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

product_items = [
    ('기타', 'ISA', 'https://obank.kbstar.com/quics?page=C041164'),
    ('기타', '방카슈랑스', 'https://obank.kbstar.com/quics?page=C019237'),
    ('기타', '골드뱅킹', 'https://obank.kbstar.com/quics?page=C016622')
]

#%%
def main(): 
    items = []

    for class_, key, value in tqdm(product_items, desc="get crawling other item..."):
        item_name = key
        url = value
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # 10 seconds wait time
        time.sleep(2)
        
        if item_name == 'ISA':
            feature = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[1]/img')  
            feature = feature.get_attribute('alt')
            items.append((class_, key, feature))
        elif item_name == '방카슈랑스':
            feature = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[1]/img')
            feature = feature.get_attribute('alt')
            items.append((class_, key, feature))
        elif item_name == '골드뱅킹':
            name = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[1]/h2/b').text
            feature = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div[2]/div/ul/li[1]').text
            feature = re.sub("\n", "", feature)
            name = re.sub("\n", " ", name)
            items.append((class_, name, feature))

    driver.quit()
    print("# items:", len(items))
    
    columns = ["상품분류", "상품이름", "상품특징"]
    products_df = pd.DataFrame(items, columns=columns)
    data_dir = '../assets/crawling'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    products_df.to_csv(f'{data_dir}/other_product.csv', index=False)
    
    return items

#%%
if __name__ == "__main__":
    main()

# %%
