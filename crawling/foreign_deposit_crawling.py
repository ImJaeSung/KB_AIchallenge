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

# Open the initial URL
url = "https://obank.kbstar.com/quics?page=C101501"
driver.get(url)
wait = WebDriverWait(driver, 10)  # 10 seconds wait time

#%%
def foreign_deposit_product(item, code):
    foreign_deposit_product = []
    product_url = f'https://obank.kbstar.com/quics?page=C101501&cc=b102293:b103845&QSL&%EB%B8%8C%EB%9E%9C%EB%93%9C%EC%83%81%ED%92%88%EC%BD%94%EB%93%9C={code}'
    driver.get(product_url)
    wait = WebDriverWait(driver, 10)  # 10 seconds wait time
    time.sleep(2)  # wait for the page to load
    try:
        name = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div/form/div[1]/div/div[1]/h2/b').text
        feature = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/div/form/div[1]/div/div[2]/div/ul/li[1]').text
        feature = re.sub("\n", "", feature)
        name = re.sub("\n", " ", name)
        foreign_deposit_product.append((name, feature))
    
    except:
        print("pass")
        
    return foreign_deposit_product

#%%
code_dict = {
    '외화정기예금' : 'FD01000952',
    'KB TWO테크 외화정기예금' : 'FD01000970',
    'KB 적립식 외화정기예금' : 'FD01000953',
    'KB두근두근외화적금' : 'FD01000972',
    'KB WISE 외화정기예금' : 'FD01000955',
    'KB국민UP 외화정기예금' : 'FD01000954'
}

#%%
def main():  
    products = []
    for code_key, code_value in tqdm(code_dict.items(), desc="get explanation..."):
        item = code_key
        code = code_value
        product = foreign_deposit_product(item, code)
        products.extend(product)
    return products

#%%
product = main()
columns = ["상품이름", "상품특징"]
products_df = pd.DataFrame(product, columns=columns)
products_df.to_csv('./assets/foreign_product.csv', index=False)

driver.quit()
# %%
