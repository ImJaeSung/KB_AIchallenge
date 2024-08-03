#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
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

product_items = {
    '예금' : '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[1]/a',
    '적금' : '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[2]/a',
    '입출금' : '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[3]/a',
    '주택청약' : '/html/body/div[1]/div[3]/div[2]/div[5]/ul[1]/li[4]/a'
    }

#%%
def deposit_product(item, code):
    deposit_product = []
    product_url = f'https://obank.kbstar.com/quics?page=C016613&cc=b061496:b061645&isNew=N&prcode={code}'
    driver.get(product_url)
    wait = WebDriverWait(driver, 10)  # 10 seconds wait time
    time.sleep(2)  # wait for the page to load
    try:
        feature = driver.find_element(By.XPATH, "//strong[text()='상품특징']/following-sibling::div[@class='infoCont']").text
        name = driver.find_element(By.CSS_SELECTOR, '#b061645 > div.product-basic > h2').text
        feature = re.sub("\n", "", feature)
        name = re.sub("\n", " ", name)
        deposit_product.append((name, feature))
        return deposit_product
    
    except Exception as e:
        print(f"An error occurred while fetching product details: {e}")
        feature = driver.find_element(By.XPATH, "//strong[text()='상품유형']/following-sibling::div[@class='infoCont']").text
        name = driver.find_element(By.CSS_SELECTOR, '#b061645 > div.product-basic > h2').text
        feature = re.sub("\n", "", feature)
        name = re.sub("\n", " ", name)
        deposit_product.append((name, feature))
        return deposit_product

#%%
items_codes = []

for item in list(product_items.values()):
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
                
                items_codes.append((id_value, name))

        except Exception as e:
            print("No more pages or an error occurred:", e)

print(items_codes)


def main():  
    products = []
    for item_code in items_codes:
        item = item_code[1]
        code = item_code[0]
        product = deposit_product(item, code)
        products.extend(product)
    return products

#%%
main()
driver.quit()