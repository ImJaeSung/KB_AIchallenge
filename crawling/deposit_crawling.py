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
url = "https://obank.kbstar.com/quics?page=C016613&cc=b061496:b061496"
driver.get(url)
wait = WebDriverWait(driver, 10)  # 10 seconds wait time
#%%
# Locate the product items

product_items = [
    ('예금', '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[1]/a'),
    ('적금', '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[2]/a'),
    ('입출금', '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[3]/a'),
    ('주택청약', '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[4]/a')
]

#%%
def deposit_product(class_, code):
    deposit_product = []
    product_url = f'https://obank.kbstar.com/quics?page=C016613&cc=b061496:b061645&isNew=N&prcode={code}'
    driver.get(product_url)
    wait = WebDriverWait(driver, 10)  # 10 seconds wait time
    time.sleep(2)  # wait for the page to load
    try:
        name = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[5]/div/div[1]/h2/b').text
        feature = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[5]/div/div[3]/div/ul/li[1]').text
        feature = re.sub("\n", "", feature)
        name = re.sub("\n", " ", name)
        deposit_product.append((class_, name, feature))
    
    except:
        print("pass")
        
    return deposit_product

#%%
def main():
    #%%
    items_codes = []

    for class_, item in tqdm(product_items, desc="get codes..."):
        element = wait.until(EC.presence_of_element_located((By.XPATH, f"{item}")))
        time.sleep(2)  # wait for the page to load
        element.click()
        time.sleep(2)
        # for page in range(1, 3):

        for j in range(1, 4):
            try:
                page_button = wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                f'/html/body/div[1]/div[3]/div[2]/div[5]/div[3]/div/form[{j}]/span'
                                )
                            )
                        )
                page_button.click()
                time.sleep(2)
                product_list = driver.find_element(By.CSS_SELECTOR, 'ul.list-product1')

                # 모든 'li' 항목 찾기
                lis = product_list.find_elements(By.TAG_NAME, 'li')

                for li in lis:
                    # 고유번호 추출
                    a_tag = li.find_element(By.CSS_SELECTOR, 'a.title')
                    onclick_value = a_tag.get_attribute('onclick')
                    id_match = re.search(r"dtlDeposit\('([^']*)'", onclick_value)
                    id_value = id_match.group(1) if id_match else 'ID 없음'
                    
                    # 이름 추출
                    strong_tag = a_tag.find_element(By.TAG_NAME, 'strong')
                    name = strong_tag.text.strip()
                    
                    items_codes.append((class_, id_value, name))

            except:
                page_button = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                            f'/html/body/div[1]/div[3]/div[2]/div[5]/div[3]/div/form/span'
                            )
                        )
                    )
                page_button.click()
                time.sleep(2)
                product_list = driver.find_element(By.CSS_SELECTOR, 'ul.list-product1')

                # 모든 'li' 항목 찾기
                lis = product_list.find_elements(By.TAG_NAME, 'li')

                for li in lis:
                    # 고유번호 추출
                    a_tag = li.find_element(By.CSS_SELECTOR, 'a.title')
                    onclick_value = a_tag.get_attribute('onclick')
                    id_match = re.search(r"dtlDeposit\('([^']*)'", onclick_value)
                    id_value = id_match.group(1) if id_match else 'ID 없음'
                    # 이름 추출
                    strong_tag = a_tag.find_element(By.TAG_NAME, 'strong')
                    name = strong_tag.text.strip()
                    
                    items_codes.append((class_, id_value, name))
    #%%
    unique_codes = list(set(items_codes))
    
    assert len(unique_codes) == 58
    print("# codes:", len(unique_codes))

    products = []
    for item_code in tqdm(unique_codes, desc="get explanation..."):
        item = item_code[2]
        code = item_code[1]
        class_ = item_code[0]
        product = deposit_product(class_, code)
        products.extend(product)
    driver.quit()

    print("# items:", len(products))

    columns = ["상품분류", "상품이름", "상품특징"]
    products_df = pd.DataFrame(products, columns=columns)

    data_dir = '../assets/crawling'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    products_df.to_csv(f'{data_dir}/deposit.csv', index=False)

    return products

# %%
if __name__ == "__main__":
    main()

