#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from os.path import exists
from time import sleep
import random
import os

current_url = ''
url = ''

# Launch Firefox webdriver and install ublock extension
driver = webdriver.Firefox()
driver.install_addon(r'webdriver\uBlock0@raymondhill.net.xpi', temporary=True)

# Open file with country codes and save it to list for loop
with open('country-code.txt', 'r') as fr:
    countries = fr.readlines()

for country in countries:
    country_path = str(os.getcwd()) + f'\countries-ip\{country}'.strip('\n') + '.txt'

    # Check if file of certain country exist
    if not exists(country_path):

        # Set variables and set to deflaut state
        ip_list = []
        last_page = 0
        current_page = 1
        print(country)
        
        # Create an infinite loop that will create a list from each country in which to save everything
        while True:
                
            url = f'https://www.ipaddress.com/ipv4/country/{country}?page={current_page}'.strip('\n')
            driver.get(url)

            sleep(random.uniform(.5, 2))

            page = driver.page_source
            soup = BS(page, 'lxml')

            # In case if needed to click cookies button
            #cookie_button = driver.find_element(by=By.ID, value='ez-accept-all')
            #cookie_button.click()

            pagination = soup.find(class_='pagination')
            pagination = list(pagination)
            content = soup.find_all('tr')

            # Remove arrows strings
            for p in pagination:
                p_text = p.getText()
                if p_text == '»':
                    pagination.remove(p)
                if p_text == '«':
                    pagination.remove(p)

            # Get last page of current paggination range
            for x in range(0, len(pagination)):
                if x == (len(pagination)-1):
                    print(pagination[x].getText())
                    last_page = int(pagination[x].getText())

            # Get only text from <a> tag and add to ip list
            for c in content:
                td = c.findChildren('td', recursive=False)
                for l in td[0:3]:
                    a = l.findChildren('a', recursive=False)
                    for t in a:
                        text = t.getText()
                        ip_list.append(text)
                        print(text)
            
            # Break loop if page doesn't have next pages
            if len(pagination) == 0:
                break
            # Break loop if current page equals to last page 
            if current_page == last_page:
                break

            current_page += 1
            current_url = driver.current_url.strip('\n')        

        # From LIST OF IP make RANGE OF IP's by adding '-' between them 
        for ip, i in zip(ip_list, range(0, len(ip_list))):
            next_ip = ip_list[i+1]
            ip = ip + '-' + next_ip
            ip_list[i] = ip
            ip_list.remove(next_ip)

        # Check file exist Open/Make txt file in write mode to write range's of ip
        country = country.replace('+', '-').rstrip('\n')
        with open(f'countries-ip\{country}.txt', 'w') as fw:
            for e in ip_list:
                fw.write(e + '\n')
    else:
        continue

sleep(1)
print("Done")
driver.close()
