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
url = "https://obank.kbstar.com/quics?page=C103425"
driver.get(url)
wait = WebDriverWait(driver, 10)  # 10 seconds wait time
#%%
# Locate the loan items
loan_items = driver.find_elements(By.CSS_SELECTOR, 'li[class^="loan-item"] > a')
#%%
loan_data = []

for item in loan_items:
    loan_name = item.text.strip()
    loan_name = re.sub("\n", "", loan_name)
    loan_href = item.get_attribute('href').split('=')[1]
    loan_data.append((loan_name, loan_href))
#%%
codes = []
for loan_name, page_value in loan_data:
    driver.get(f'https://obank.kbstar.com/quics?page={page_value}')
    time.sleep(2)  # wait for the page to load
    # for page in range(1, 3):
    for j in range(2, 8):
        elements = driver.find_elements(
            By.CSS_SELECTOR, 'ul.list-product1 > li > div > a'
        )
        
        for i, element in enumerate(elements):
            try:
                onclick_attr = element.get_attribute('onclick')
                details_code = re.search(r"dtlLoan\('([^']*)'", onclick_attr).group(1)
                codes.append((loan_name, details_code))

            except (KeyError, AttributeError) as e:
                print(f"An error occurred at index {i}: {e}")
                    # Try to locate the next page button and click it
        try:
            next_page_button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, 
                    f'/html/body/div[1]/div[3]/div[2]/div[6]/div[2]/div/div/form[j]/span'
                    )
                )
            )
            next_page_button.click()
            time.sleep(2)  # wait for the new page to load
        except Exception as e:
            print("No more pages or an error occurred:", e)
    

    #%%
loan_products = []
for loan_name, code in codes:
    word_address = f'https://obank.kbstar.com/quics?page=C103429&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
    driver.get(word_address)
    time.sleep(2)  # wait for the page to load

    try:
        name = driver.find_element(By.CSS_SELECTOR, 'h1[style="display: none;"]').text
        feature = driver.find_element(By.XPATH, "//strong[text()='상품특징']/following-sibling::div[@class='infoCont']").text
        feature = re.sub("\n", "", feature)
        loan_products.append((loan_name, name, feature))
    except Exception as e:
        print(f"An error occurred while fetching product details: {e}")
#%%
# Close the WebDriver
driver.quit()
#%%
# Print the extracted loan products
for loan in loan_products:
    print(f"Loan Name: {loan[0]}")
    print(f"Product Name: {loan[1]}")
    print(f"Product Feature: {loan[2]}\n")
