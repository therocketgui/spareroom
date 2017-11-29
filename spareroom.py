
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert


import json
from urllib.parse import urlencode        
from urllib.request import Request, urlopen
import json
import ssl

#from browsermobproxy import Server
#from xlsxlib import Excel
import time
import re
import os
import sys
import json
import random
from random import shuffle

import csv
from datetime import datetime

class Zapier():

    def __init__(self):
        self.webhook = os.environ['SPAREROOM_ZAPIER_WEBHOOK']
        return

    def zapier_post_req(self, prospect):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            url = self.webhook

            post_fields = {'name': prospect['name'],
                            'phone': prospect['phone'],
                            'title': prospect['title'],
                            'url': prospect['uri'],
                            'date': datetime.now()
                            }

            request = Request(url, urlencode(post_fields).encode())
            json = urlopen(request, context=ctx).read().decode()
            #print(json)
            #print('Added to autopilot')
            success = 1
        except Exception as e:
            print(e)
            success = 0

        return success

class Account():

    def __init__(self):
        return

    def get_list(self):
        with open('accounts.json') as data_file: 
            data = json.load(data_file)
        return data

    def store(self, data):
        # write and store the data in the json
        with open('accounts.json', 'w') as f:
            json.dump(data, f, indent=4)
        return

    def add_proxies(self, proxy_list):
        # Add proxy to each account
        accs = self.get_list()
        i = 0
        for acc in accs["accounts"]:
            try:
                acc["proxy"] = str(proxy_list[i]['ip']+':'+proxy_list[i]['port'])
                i = i+1
            except:
                pass
        self.store(accs)
        return

class Proxy():
    # CLEAN LIST OF 150 FREE UK PROXY TO FIND THE WORKING ONES
    def __init__(self):
        self.proxies = ["88.211.126.138:8080","46.101.63.28:8118","46.101.90.10:8118","176.253.13.146:8080","91.229.222.163:53281","46.101.88.252:8118","178.62.57.171:8118","46.101.30.203:8118","139.59.169.238:8118","178.239.168.57:80","46.101.37.129:8118","138.68.149.193:8118","163.172.219.142:3128","217.182.76.229:8888","46.101.73.212:8118","88.99.110.166:8080","69.10.49.50:80","46.101.86.183:80","178.62.7.53:8118","145.239.87.247:8080","46.101.92.212:80","46.101.74.237:8080","109.169.1.114:3128","46.101.37.196:8118","194.116.198.211:80","46.101.81.206:8118","138.68.156.224:8118","46.101.56.127:8118","138.68.151.83:8118","145.239.4.43:8080","46.101.75.192:8118","46.101.11.131:3128","46.101.27.174:8118","138.68.150.51:8118","92.27.91.253:53281","46.101.23.10:3128","88.99.246.226:8080","80.87.143.150:80","46.101.77.190:8118","138.68.146.247:8118","51.15.86.160:80","51.15.63.158:53281","51.15.63.158:8080","51.15.63.158:1080","51.15.63.158:65103","51.15.83.8:3128","51.15.199.93:3128","46.101.78.9:8080","163.172.220.221:8888","178.62.112.15:80","194.116.198.210:80","46.101.59.22:8118","46.101.38.246:8118","138.68.158.19:8118","46.101.59.83:8118","46.101.22.252:8118","46.101.36.239:8118","46.101.54.24:8118","46.101.56.151:8118","46.101.73.58:8118","188.166.170.216:8118","46.101.12.39:8118","46.101.35.251:8118","178.62.46.163:8118","178.62.11.5:8118","46.101.27.234:8118","46.101.79.210:8118","46.101.83.147:8118","46.101.7.211:8118","46.101.37.97:8118","78.109.172.231:3128","46.101.76.109:8118","139.59.175.233:8118","178.62.33.147:8118","46.101.87.205:8118","167.98.60.152:8080","178.62.36.50:8118","163.172.211.176:3128","46.101.47.42:8118","82.11.224.237:8080","51.15.63.158:3128","51.15.160.216:80","46.101.91.108:8118","46.101.95.74:8118","178.62.93.62:8118","46.101.55.143:8118","51.15.55.179:3128","88.99.176.193:8080","46.101.83.249:8118","51.15.86.94:3128","46.101.108.112:80","46.101.76.243:8118","178.62.63.231:8118","138.68.154.243:8118","46.101.49.108:8118","46.101.76.197:8118","46.101.61.131:8118","217.174.254.28:80","46.101.9.216:8118","46.101.63.66:8118","178.62.19.5:8118","46.101.79.191:8118","46.101.84.139:8118","46.101.72.28:8118","46.101.56.193:8118","88.99.222.250:8080","51.15.35.158:80","69.10.49.115:80","178.62.116.7:8118","46.101.75.65:8118","46.101.63.111:8118","46.101.30.45:8118","139.59.161.244:8118","46.101.52.98:8118","178.62.118.114:8118","134.213.62.13:3129","178.62.15.246:8118","46.101.55.122:8118","178.62.80.241:8118","46.101.46.174:8118","46.101.48.24:8118","46.101.75.193:8118","178.62.41.33:8118","178.62.102.246:8118","178.62.28.110:8118","46.101.72.31:8118","46.101.55.200:8118","46.101.51.214:8118","104.238.173.60:3128","178.62.68.74:8118","88.99.149.188:31288","46.101.60.15:8118","188.166.175.122:8118","46.101.47.58:8118","134.213.49.60:4444","46.101.72.35:8118","46.101.87.81:8118","46.101.53.211:8118","46.101.80.84:8118","178.62.31.116:8118","188.166.144.158:8118","178.62.91.116:8118","139.59.162.156:8118","46.101.38.116:8118","46.101.86.225:8118","46.101.72.54:8118","139.59.169.231:8118","88.99.185.134:80","46.101.2.115:8118","46.101.62.50:8118","46.101.76.59:8118","46.101.89.168:8118","46.101.74.112:8118","46.101.72.102:8118","46.101.72.53:8118","46.101.26.217:8118","178.62.49.23:8118","46.101.73.138:8118","138.68.151.246:8118","86.19.247.72:80","69.10.49.10:80","46.101.76.125:8118","138.68.150.154:8118","178.62.85.56:8118","46.101.40.241:8118","91.108.212.28:53281","134.213.208.193:4444","134.213.158.212:4444","178.62.22.69:8118","46.101.72.246:8118","46.101.46.36:8118","178.62.43.221:8118","46.101.27.218:8118","81.158.157.27:8080","178.62.16.192:8118","46.101.76.232:8118","46.101.78.122:8118","178.62.93.13:8118","134.213.148.8:3129","46.101.47.118:8118","46.101.10.220:8118","162.13.136.29:3129","185.16.41.130:80","213.41.32.228:8080","86.21.246.83:80","46.101.8.137:80","178.62.75.161:8118","46.101.75.114:8118","46.101.51.238:8118","46.101.77.223:8118","46.101.8.137:8080","46.101.72.25:8118","46.101.46.237:8118","178.62.64.223:8118","162.13.166.149:3129"]
        return

    def order_table(self, source_code):
        proxy_list = []
        soup = BeautifulSoup(source_code, 'lxml')
        for proxy in soup.find_all('tr'):
            try:
                if proxy.find('td', {'class':'status'}).text != 'Dead':
                    ip = proxy.find('td', {'class':'ip'}).text
                    port = proxy.find('td', {'class':'port'}).text
                    typeof = proxy.find('td', {'class':'type'}).text
                    anonymity = proxy.find('td', {'class':'anonymity'}).text
                    country = proxy.find('td', {'class':'country'}).text
                    proxy_list.append({'ip':ip, 'port':port, 'type':typeof, 'anonymity':anonymity, 'country':country})
            except:
                pass
        return proxy_list

    def find_working_proxy(self):
        self.driver = webdriver.Chrome(os.environ['PATH_TO_CHROMIUM'])
        self.driver.get('http://www.checker.freeproxy.ru/checker/')
        textarea = self.driver.find_element_by_css_selector('textarea')
        for proxy in self.proxies[:100]:
            for character in proxy:
                textarea.send_keys(character)
            textarea.send_keys('\n')
        self.driver.find_element_by_class_name('btn-primary').click()
        time.sleep(45)

        source_code = self.driver.page_source
        proxy_list = self.order_table(source_code)

        self.driver.quit()

        return proxy_list


class Spareroom():

    def __init__(self):
        # Launch PhantomJS or Chromium
        # Retrieve proxy list
        proxies = Proxy()
        proxy_list = proxies.find_working_proxy()
        accounts = Account()
        accounts.add_proxies(proxy_list)
        print(proxy_list)
        
        return

    def launch(self, proxy):
        # Launch PhantomJS or Chromium
        self.driver = webdriver.Chrome(os.environ['PATH_TO_CHROMIUM'])
        #capabilities = dict(DesiredCapabilities.CHROME)
        #capabilities['proxy'] = {'proxyType': 'MANUAL',
        #                         'httpProxy': proxy,
        #                         'ftpProxy': proxy,
        #                         'sslProxy': proxy,
        #                         'noProxy': '',
        #                         'class': "org.openqa.selenium.Proxy",
        #                         'autodetect': False}

        #self.driver = webdriver.Chrome(executable_path=os.environ['PATH_TO_CHROMIUM'], desired_capabilities=capabilities)
        self.driver.implicitly_wait(10)

        self.driver.get("http://whatismyipaddress.com")
        #print(bcolors.FAIL + 'Proxy: ' + str(proxy) + bcolors.ENDC)


        self.large_sleep()
        
        #self.medium_sleep()
        return

    def quit(self):
        print('Quit Driver')
        self.driver.quit()
        self.short_sleep()
        return  

    def get(self, url):
        self.driver.get(url)
        self.medium_sleep()
        return

    def very_short_sleep(self):
        # Random short sleep time
        r = random.uniform(0.08, 0.13)
        time.sleep(r)
        return

    def short_sleep(self):
        # Random short sleep time
        r = random.uniform(0.6, 1.2)
        time.sleep(r)
        return

    def medium_sleep(self):
        # Random medium sleep time
        r = random.uniform(1.6, 2.2)
        time.sleep(r)
        return

    def large_sleep(self):
        # Random medium sleep time
        r = random.uniform(3, 6)
        time.sleep(r)
        return

    def very_large_sleep(self):
        # Random medium sleep time
        r = random.uniform(59, 90)
        time.sleep(r)
        print('Sleeping for '+str(r)+ ' seconds...')
        return r

    def scroll_bottom(self):
        # Scroll to bottom of a page
        print('Scrolling...')
        for scroll in range(0,15):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.short_sleep()

        self.medium_sleep()
        self.driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        return

    def get_data(self):
        with open('prospects.json') as data_file: 
            data = json.load(data_file)
        return data

    def get_uri_list(self):
        data = self.get_data()
        uri_list=[]
        for prospect in data['prospects']:
            if 'search_id' in prospect['uri']:
                uri_list.append(self.reformate_uri(prospect['uri']))
            else:
                uri_list.append(prospect['uri'])

        return uri_list

    def store(self, prospects):

        data = self.get_data()
        phone_list=[]
        for d in data['prospects']:
            phone_list.append(d['phone'])

        # Insert and avoid duplicates
        for prospect in prospects:
            if prospect['phone'] not in phone_list:
                data['prospects'].append(prospect)

        # write and store the data in the json
        with open('prospects.json', 'w') as f:
            json.dump(data, f, indent=4)

        return

    def get_phone_list(self):

        data = self.get_data()
        phone_list=[]
        for d in data['prospects']:
            phone_list.append(d['phone'])

        return phone_list

    def login(self, login_username, login_password):
        self.get('https://m.spareroom.co.uk/flatshare/logon.pl')

        div_login = self.driver.find_element_by_class_name("logon")
        email = div_login.find_element_by_name("email")
        password = div_login.find_element_by_name("password")

        email_address = login_username
        for character in email_address:
            email.send_keys(character)
            self.very_short_sleep()
        self.medium_sleep()

        password_text = login_password
        for character in password_text:
            password.send_keys(character)
            self.very_short_sleep()
        self.medium_sleep()  

        div_login.find_element_by_name("submit").click()  
        self.large_sleep()
        return

    def get_uri_gen(self,page):
        uri = 'https://www.spareroom.co.uk/flatshare/london/page'+str(page)
        self.get(uri)
        return

    def get_uri(self,page):
        uri = 'https://www.spareroom.co.uk/flatshare/london'
        self.get(uri)
        # Need to click the "private ads" button and push the search update at it's generating a custom search ID that we can only use once.
        self.medium_sleep()
        self.driver.find_element_by_id("privateAds").click()
        self.medium_sleep()
        self.driver.find_element_by_class_name("aside-form_foot_btn").click()
        self.medium_sleep() 
        if page > 1:
            # if it's not page 1: perform a search to get the search ID and add offset=page*10 (10 ads per page)
            page_url = self.driver.current_url + 'offset=' + str(page*10) + '&sort_by=age&mode=list'
            self.get(page_url)

        return

    def get_page_list(self, page):
        # BS4
        uri_list =[]
        self.get_uri(page)
        self.medium_sleep()
        source_code = self.driver.page_source
        soup = BeautifulSoup(source_code, 'lxml')
        for flat in soup.find_all('li', {'class':'listing-result'}):
            link = flat.find('header', {'class':'desktop'}).a['href']
            uri = 'https://www.spareroom.co.uk'+link
            uri_list.append(uri)
            #print(uri)
        return uri_list

    def is_phone_available(self, uri):
        self.get(uri)
        source_code = self.driver.page_source
        soup = BeautifulSoup(source_code, 'lxml')

        result = soup.find('li', {'class':'phoneadvertiser'})
        if result is not None:
            return True
        else:
            return False

    def get_infos(self):
        source_code = self.driver.page_source
        soup = BeautifulSoup(source_code, 'lxml')

        title = soup.h1.text

        return title

    def click_phone(self):
        self.driver.find_element_by_class_name("secondary-standard").click()
        return

    def find_contact(self):
        source_code = self.driver.page_source
        soup = BeautifulSoup(source_code, 'lxml')
        try:
            result = soup.find('fieldset', {'id':'contact_advertiser_form'}).text
            details,sep,tail = result.partition('Mark as contacted')

            name,sep,tail = details.partition('(')
            head,sep,phone = details.partition('):')
        except:
            name = ""
            phone = ""

        #print(contact)
        return name.strip(), phone.replace('+','').strip()

    def reformate_uri(self, uri):
        ref_uri, sep, tail = uri.partition('&search_id=')
        return ref_uri

    def scrape(self):
        # TODO
        
        accs = Account()
        accounts = accs.get_list()
        page_per_account = 1
        low_page = 1
        high_page = low_page + page_per_account
        # Rotate accounts
        for account in accounts['accounts']:

            self.launch(account['proxy'])
            print(bcolors.OKBLUE + 'Account: '+ account['fname'] + ' - ' + account['email'] + ' - page '+str(low_page)+' to '+str(high_page-1)+ bcolors.ENDC)
            # Login account
            self.login(account['email'], account['password'])
            self.large_sleep()
            past_uri_list = self.get_uri_list()

            for i in range(low_page, high_page):
                uri_list = self.get_page_list(i)
                prospects = []

                for uri in uri_list:
                    # Never scrap same ad twice
                    if self.reformate_uri(uri) not in past_uri_list:
                        try:
                            # Verify if phone is available
                            self.large_sleep()
                            if self.is_phone_available(uri) is True:
                                title = self.get_infos()
                                self.medium_sleep()
                                self.click_phone()
                                self.medium_sleep()
                                name, phone = self.find_contact()
                                prospect = {'name':name, 'phone':phone, 'title':title.strip(), 'uri':self.reformate_uri(uri)}
                                prospects.append(prospect)
                                print(bcolors.OKGREEN + 'Adding: '+ prospect['name'] + ' - ' + prospect['phone'] + bcolors.ENDC)
                                self.large_sleep()

                        except Exception as e:
                            print(e)
                            # if popup, dimiss
                            #alert = self.driver.switch_to_alert()
                            #alert.dismiss()

                # push to Zapier
                try:
                    print('Post to Zapier start...')
                    zap = Zapier()

                    phone_list = self.get_phone_list()
                    for prospect in prospects:
                        if prospect['phone'] not in phone_list:
                            zap.zapier_post_req(prospect)
                            print(bcolors.OKBLUE + prospect['phone'] + ' added to Spreadsheet' + bcolors.ENDC)
                    print('Post to Zapier end...')
                except Exception as e:
                    print(e)

                self.store(prospects)

            self.quit()
            low_page = high_page
            high_page = high_page + page_per_account
            print(bcolors.FAIL + '\nSleeping for 30 seconds, you may want to change IP now (or quit the scraper)\n'+ bcolors.ENDC)
            sleep_time = self.very_large_sleep()

        return

class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

if __name__ == "__main__":
    s = Spareroom()
    s.scrape()





