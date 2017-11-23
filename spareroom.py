
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


class Spareroom():

    def __init__(self):
        # Launch PhantomJS or Chromium
        
        return

    def launch(self):
        # Launch PhantomJS or Chromium
        self.driver = webdriver.Chrome(os.environ['PATH_TO_CHROMIUM'])
        self.driver.implicitly_wait(10)
        
        self.medium_sleep()
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
        r = random.uniform(30, 44)
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
        low_page = 7
        high_page = low_page + page_per_account
        # Rotate accounts
        for account in accounts['accounts']:

            self.launch()
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
                            alert = self.driver.switch_to_alert()
                            alert.dismiss()

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

    #a = Account()
    #data = a.get_list()
    #print(data)
    #print('\n\n')
    #acc= a.get_oldest_account()
    #print(acc)

    #z = Zapier()
    #prospect = {'name':'Test', 'phone':'+44124124214124', 'title':'double room blabla', 'uri':'www.x.com'}
    #z.zapier_post_req(prospect)




