from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep

country = 'cn-china'
page = 1
url = f'https://www.ipaddress.com/ipv4/country/{country}?page={page}'
path_chrome = ".\chromedriver.exe"

ip_list = []
i = 0

driver = webdriver.Firefox()
driver.install_addon('uBlock0@raymondhill.net.xpi', temporary=True)
driver.get(url)

page = driver.page_source
soup = BS(page, 'lxml')

sleep(.2)

#cookie_button = driver.find_element(by=By.ID, value='ez-accept-all')
#cookie_button.click()

content = soup.find_all('tr')

# Get only text from <a> tag and add to ip list
for c in content:
    td = c.findChildren('td', recursive=False)
    for l in td:
        a = l.findChildren('a', recursive=False)
        for t in a:
            text = t.getText()
            ip_list.append(text)

# Remove single ip
for ip in ip_list:
    if ip_list.count(ip) >= 2:
        ip_list = [ele for ele in ip_list if ele != ip]

# Remove SAMPLE IP row by deleting every third element
del ip_list[3 - 1::3]

# From LIST OF IP make RANGE OF IP's by adding between '-' them 
for ip in ip_list:
    ip_list[i] = ip_list[i] + '-' + ip_list[i+1]
    ip_list.remove(ip_list[i+1])
    if i <= len(ip_list):
        i += 1
print(ip_list)

sleep(.5)
            
sleep(10)

driver.close()
