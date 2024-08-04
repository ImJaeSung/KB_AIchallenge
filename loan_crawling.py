#%%
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

import pandas as pd
#%%
# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the initial URL
url = "https://obank.kbstar.com/quics?page=C103425"
driver.get(url)
wait = WebDriverWait(driver, 10)  # 10 seconds wait time
#%%
# Locate the loan items
loan_items = driver.find_elements(
    By.CSS_SELECTOR, 'li[class^="loan-item"] > a'
)
#%%
loan_data = []

for item in loan_items:
    loan_name = item.text.strip()
    loan_name = re.sub("\n", "", loan_name)
    loan_href = item.get_attribute('href').split('=')[1]
    loan_data.append((loan_name, loan_href))
#%%
codes = []
for loan_name, page_value in tqdm(loan_data, desc="get codes..."):
    driver.get(f'https://obank.kbstar.com/quics?page={page_value}')
    time.sleep(2)  # wait for the page to load
    # for page in range(1, 3):
    for j in range(2, 10):
        elements = driver.find_elements(
            By.CSS_SELECTOR, 'ul.list-product1 > li > div > a'
        )
        
        for i, element in enumerate(elements):
            try:
                onclick_attr = element.get_attribute('onclick')
                details_code = re.search(r"dtlLoan\('([^']*)'", onclick_attr).group(1)
                codes.append((loan_name, details_code))

            except (KeyError, AttributeError) as e:
                print("pass")
                # print(f"An error occurred at index {i}: {e}")
                    # Try to locate the next page button and click it
        try:
            if loan_name == '신용대출':
                path = f'/html/body/div[1]/div[3]/div[2]/div[6]/div[2]/div/div/form[{j}]/span'
            elif loan_name == '담보대출':
                path = f'/html/body/div[1]/div[3]/div[2]/div[5]/div[2]/div/div/form[{j}]/span'
            elif loan_name == '전월세/반환보증':
                path = f'/html/body/div[1]/div[3]/div[2]/div[5]/div[2]/div/div/form[{j}]/span'
            elif loan_name == '자동차대출': 
                path = None
            elif loan_name == '집단중도금/이주비대출':
                path = None
            elif loan_name == '주택도시기금대출':
                path = f'/html/body/div[1]/div[3]/div[2]/div[6]/div[2]/div/div/form[{j}]/span'
            next_page_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, path)
                )
            )
            next_page_button.click()
            time.sleep(2)  # wait for the new page to load
        except Exception as e:
            # print("No more pages or an error occurred:", e)
            print("pass")

#%%
unique_codes = list(set(codes))
assert len(unique_codes) == 172
#%%
loan_products = []
for loan_name, code in tqdm(unique_codes, desc="get explanation..."):
    
    try:
        if loan_name == '신용대출':
            word_address = f'https://obank.kbstar.com/quics?page=C103429&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
            path = '/html/body/div[1]/div[3]/div[2]/div[6]'
        elif loan_name == '담보대출':
            word_address = f'https://obank.kbstar.com/quics?page=C103557&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
            path = '/html/body/div[1]/div[3]/div[2]/div[5]'
        elif loan_name == '전월세/반환보증':
            word_address = f'https://obank.kbstar.com/quics?page=C103507&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
            path = '/html/body/div[1]/div[3]/div[2]/div[5]'
        elif loan_name == '자동차대출': 
            word_address = f'https://obank.kbstar.com/quics?page=C103573&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
            path = '/html/body/div[1]/div[3]/div[2]/div[6]'
        elif loan_name == '집단중도금/이주비대출':
            word_address = f'https://obank.kbstar.com/quics?page=C109229&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
            path = '/html/body/div[1]/div[3]/div[2]/div[5]'
        elif loan_name == '주택도시기금대출':
            word_address = f'https://obank.kbstar.com/quics?page=C103998&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
            path = '/html/body/div[1]/div[3]/div[2]/div[6]'
            
        
        driver.get(word_address)    
        time.sleep(2)  # wait for the page to load

        name = driver.find_element(By.XPATH, f'{path}/div/div[1]/h2/b').text
        
        feature_1 = driver.find_element(By.XPATH, f'{path}/div/div[3]/div/ul/li[1]').text
        feature_1 = re.sub("\n", "", feature_1)
        feature_2 = driver.find_element(By.XPATH, f'{path}/div/div[3]/div/ul/li[2]').text
        feature_2 = re.sub("\n", "", feature_2)
    
        loan_products.append((loan_name, name, feature_1, feature_2))
    except Exception as e:
        print("error")
        # print(f"An error occurred while fetching product details: {e}")
#%%
assert len(loan_products) == 172

columns = ["대출 목적", "상품 이름", "상품 특징", "가입 조건"]
loan_products_df = pd.DataFrame(loan_products, columns=columns)
loan_products_df.to_csv('./assets/loan.csv', index=False)
# Close the WebDriver
driver.quit()
#%%
# Print the extracted loan products
# for loan in loan_products:
#     print(f"Loan Name: {loan[0]}")
#     print(f"Product Name: {loan[1]}")
#     print(f"Product Feature: {loan[2]}\n")
