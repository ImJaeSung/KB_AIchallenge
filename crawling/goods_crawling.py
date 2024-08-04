#%%
import re
import requests
from bs4 import BeautifulSoup
#%%

#%%
"""예금"""
requested = requests.get('https://obank.kbstar.com/quics?page=C016613', 'html.parser')
soup = BeautifulSoup(requested.content, 'html.parser')

codes = []
elements = soup.select('ul.list-product1 > li > div > a')

for i, element in enumerate(elements):
    try:
        onclick_attr = element['onclick']
        details_code = re.search(r"dtlDeposit\('([^']*)'", onclick_attr).group(1)
        codes.append(details_code)
    except (KeyError, AttributeError) as e:
        print(f"An error occurred at index {i}: {e}")

#%%
products = []

for code in codes:
  word_address = f'https://obank.kbstar.com/quics?page=C016613&cc=b061496:b061645&isNew=N&prcode={code}'
  requested = requests.get(word_address, 'html.parser')
  soup = BeautifulSoup(requested.content, 'html.parser')

  name = soup.find('h1', style='display: none;').text
  feature = soup.find('strong', text='상품특징').find_next('div', class_='infoCont').text

  products.append((name, feature))
# %%
"""대출"""
requested = requests.get('https://obank.kbstar.com/quics?page=C103425', 'html.parser')
soup = BeautifulSoup(requested.content, 'html.parser')
loan_items = soup.select('li[class^="loan-item"] > a')

loan_data = []

for item in loan_items:
    loan_name = item.text.strip()
    loan_href = item['href'].split('=')[1]
    loan_data.append((loan_name, loan_href))

codes = []
for loan_name, page_value in loan_data:
  request = requests.get(f'https://obank.kbstar.com/quics?page={page_value}', 'html.parser')
  soup = BeautifulSoup(request.content, 'html.parser')
  elements = soup.select('ul.list-product1 > li > div > a')

  for i, element in enumerate(elements):
    try:
        onclick_attr = element['onclick']
        details_code = re.search(r"dtlLoan\('([^']*)'", onclick_attr).group(1)
        codes.append((loan_name, details_code))
    except (KeyError, AttributeError) as e:
        print(f"An error occurred at index {i}: {e}")

loan_products = []
for loan_name, code in codes:
  word_address = f'https://obank.kbstar.com/quics?page=C103429&cc=b104363:b104516&isNew=N&prcode={code}&QSL=F'
  requested = requests.get(word_address, 'html.parser')
  soup = BeautifulSoup(requested.content, 'html.parser')

  name = soup.find('h1', style='display: none;').text
  feature = soup.find('strong', text='상품특징').find_next('div', class_='infoCont').text
  feature = re.sub("\n", "", feature)
  loan_products.append((loan_name, name, feature))  

#%%
"""신탁"""
requested = requests.get('https://obank.kbstar.com/quics?page=C016567', 'html.parser')
soup = BeautifulSoup(requested.content, 'html.parser')
trust_items = soup.select('ul.list-product1 > li > div > a')
#%%
codes = []
for i, element in enumerate(trust_items):
    try:
        onclick_attr = element['onclick']
        details_code = re.search(r"dtlTrust\('([^']*)'", onclick_attr).group(1)
        codes.append(details_code)
    except (KeyError, AttributeError) as e:
        print(f"An error occurred at index {i}: {e}")
#%%
trust_products = []

for code in codes:
  word_address = f'https://obank.kbstar.com/quics?page=C016567&cc=b061582:b030198&%EB%B8%8C%EB%9E%9C%EB%93%9C%EC%83%81%ED%92%88%EC%BD%94%EB%93%9C={code}'
  requested = requests.get(word_address, 'html.parser')
  soup = BeautifulSoup(requested.content, 'html.parser')

  name = soup.find('h1', style='display: none;').text
  feature = soup.find('strong', text='상품특징').find_next('div', class_='infoCont').text

  trust_products.append((name, feature))


print(products)
print(loan_products)
print(trust_products)