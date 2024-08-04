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
url = "https://obank.kbstar.com/quics?page=C016567&QSL=F#none"
driver.get(url)
wait = WebDriverWait(driver, 10)  # 10 seconds wait time
#%%
# Locate the product items

trust_items = {
    '금전신탁' : '/html/body/div[1]/div[3]/div[2]/div[4]/ul[1]/li[1]/a',
    '상속증여신탁' : '/html/body/div[1]/div[3]/div[2]/div[4]/ul[1]/li[2]/a',
    }

#%%
def trust_product(key, item, code):    
    trust_product = []
    if key == '금전신탁':
        key_code = 'b030198'
    elif key == '상속증여신탁':    
        key_code = 'b061215'
    try:
        product_url = f'https://obank.kbstar.com/quics?page=C016567&cc=b061582:{key_code}&%EB%B8%8C%EB%9E%9C%EB%93%9C%EC%83%81%ED%92%88%EC%BD%94%EB%93%9C={code}'
        driver.get(product_url)
        wait = WebDriverWait(driver, 10)  # 10 seconds wait time
        time.sleep(8)  # wait for the page to load
        feature = driver.find_element(By.XPATH, "//strong[text()='상품특징']/following-sibling::div[@class='infoCont']").text
        name = driver.find_element(By.CSS_SELECTOR, f'#{key_code} > div > div.n_pSummary > div > div.pTit > p').text
        feature = re.sub("\n", "", feature)
        name = re.sub("\n", " ", name)
        trust_product.append((name, feature))
        return trust_product
    
    except:
        driver.quit()
        product_url = f'https://obank.kbstar.com/quics?page=C016567&cc=b061582:{key_code}&%EB%B8%8C%EB%9E%9C%EB%93%9C%EC%83%81%ED%92%88%EC%BD%94%EB%93%9C={code}'
        driver.get(product_url)
        wait = WebDriverWait(driver, 10)  # 10 seconds wait time
        time.sleep(20)
        feature = driver.find_element(By.XPATH, "//strong[text()='상품특징']/following-sibling::div[@class='infoCont']").text
        name = driver.find_element(By.CSS_SELECTOR, f'#{key_code} > div > div.n_pSummary > div > div.pTit > p').text
        feature = re.sub("\n", "", feature)
        name = re.sub("\n", " ", name)
        trust_product.append((name, feature))
        return trust_product

        return trust_product

#%%
items_codes = []

for key, value in tqdm(trust_items.items(), desc='get codes...'):
    element = wait.until(EC.presence_of_element_located((By.XPATH, f"{value}")))
    time.sleep(2)  # wait for the page to load
    element.click()
    time.sleep(2)

    # for page in range(1, 5):
    for j in range(1, 5):
        try:
            overlay = wait.until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "ui-widget-overlay"))
            )

            page_button = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, 
                            f'/html/body/div[1]/div[3]/div[2]/div[4]/div[2]/div/form[{j}]/span'
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
                id_match = re.search(r"dtlTrust\('([^']*)'", onclick_value)
                id_value = id_match.group(1) if id_match else 'ID 없음'
                
                # 이름 추출
                strong_tag = a_tag.find_element(By.TAG_NAME, 'strong')
                name = strong_tag.text.strip()
                
                items_codes.append((id_value, name, key))

        except:
            page_button = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                        f'/html/body/div[1]/div[3]/div[2]/div[4]/div[2]/div/form/span'
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
                id_match = re.search(r"dtlTrust\('([^']*)'", onclick_value)
                id_value = id_match.group(1) if id_match else 'ID 없음'
                
                # 이름 추출
                strong_tag = a_tag.find_element(By.TAG_NAME, 'strong')
                name = strong_tag.text.strip()
                
                items_codes.append((id_value, name, key))


unique_codes = list(set(items_codes))
print(unique_codes)

def main():  
    products = []
    for item_code in tqdm(unique_codes, desc="Get explanation..."):
        key = item_code[2]
        item = item_code[1]
        code = item_code[0]
        product = trust_product(key, item, code)
        products.extend(product)
    return products


#%%
product = main()
columns = ["상품이름", "상품특징"]
products_df = pd.DataFrame(product, columns=columns)
products_df.to_csv('./assets/trust.csv')

driver.quit()