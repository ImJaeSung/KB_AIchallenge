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

# Open the initial URL
url = "https://obank.kbstar.com/quics?page=C101501"
driver.get(url)
wait = WebDriverWait(driver, 10)  # 10 seconds wait time

#%%
def foreign_deposit_product(class_, code):
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
        foreign_deposit_product.append((class_, name, feature))
    
    except:
        print("pass")
        
    return foreign_deposit_product

#%%
code_dict = [
    ('외화예금', '외화정기예금', 'FD01000952'),
    ('외화예금', 'KB TWO테크 외화정기예금', 'FD01000970'),
    ('외화예금', 'KB 적립식 외화정기예금', 'FD01000953'),
    ('외화적금', 'KB두근두근외화적금', 'FD01000972'),
    ('외화예금', 'KB WISE 외화정기예금', 'FD01000955'),
    ('외화예금', 'KB국민UP 외화정기예금', 'FD01000954')
]

#%%
def main():  
    products = []
    for class_, code_key, code_value in tqdm(code_dict, desc="get explanation..."):
        item = code_key
        code = code_value
        product = foreign_deposit_product(class_, code)
        products.extend(product)
    
    driver.quit()

    columns = ["상품분류", "상품이름", "상품특징"]
    products_df = pd.DataFrame(product, columns=columns)

    data_dir = '../assets/crawling'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    products_df.to_csv(f'{data_dir}/foregin_deposit.csv', index=False)

    return products

#%%
if __name__ == "__main__":
    main()
# %%
