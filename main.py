from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
       "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122" \
       ".30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22" \
       "%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D" \
       "%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value" \
       "%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22" \
       "%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C" \
       "%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C" \
       "%22mapZoom%22%3A12%7D"
PATH = "D:\Python_projects\python_tools\chromedriver.exe"

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdICfQ0zg-5jgJ_yWSzwxcq6Yji8VD-ZS3T9GPX-w-FWHgOEA/viewform?usp=sf_link"
GOOGLE_TABLE_LINK = "https://docs.google.com/spreadsheets/d/1NzkcyKBiANDGnb4Kyyu6KQ0tu5q1zjrDPMApX3nTmfg/edit?usp=sharing"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "ru,ru-RU;q=0.9,en;q=0.8",
}

response = requests.get(LINK, headers=header)
print(response.status_code)
soup = BeautifulSoup(response.text, "html.parser")

all_link_elements = soup.select(".list-card-top a")

link_list = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        link_list.append(f"https://www.zillow.com{href}")
    else:
        link_list.append(href)
print(link_list)

all_address_elements = soup.select(".list-card-info address")
address_list = [address.get_text().split(" | ")[-1] for address in all_address_elements]
print(address_list)

all_price_elements = soup.select(".list-card-price")
prices_list = [price.get_text() for price in all_price_elements]
print(prices_list)



driver = webdriver.Chrome(executable_path=PATH)
driver.get(GOOGLE_FORM_LINK)
time.sleep(5)

for number in range(len(address_list)):
    address_line = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_line.send_keys(address_list[number])
    price_line = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_line.send_keys(prices_list[number])
    link_line = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_line.send_keys(link_list[number])

    accept_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
    accept_button.click()

    time.sleep(2)
    next_form_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_form_button.click()
    time.sleep(2)


