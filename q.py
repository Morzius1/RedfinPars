from seleniumbase import Driver, BaseCase
import time
import itertools
from seleniumbase import BaseCase,SB
from db import get_urls,select_urls,vstavka1
import lxml
import random
from selenium.common.exceptions import  StaleElementReferenceException as Stale_Exception
from datetime import datetime,timedelta

lst=['Yqnhp8:8Fh2Bq@147.45.122.60:9576',
    'vyagHY:JSb6Tr@5.8.12.244:9248']



def take_url_in_db():
    with SB( sjw=True,pls='none',uc=True) as sb:
        # sb.open('https://www.redfin.com/')
        # sb.load_cookies(name='test_case.txt')
        for z in range(1,4):
            sb.open(f"https://www.redfin.com/city/11458/FL/Miami/filter/sort=lo-days/page-{z}")
            time.sleep(30)
            sb.click('span[data-text="Table"]')
            time.sleep(20)
            addresses=sb.find_elements('a[class="address"]')
            links=[i.get_attribute('href') for i in addresses]
            date=sb.find_elements('td[class="column column_8 col_days"]')
            date_res=[i.text for i in date] 
            for k,v in itertools.zip_longest(links,date_res,fillvalue='Отсутствует'):
                if k!='Отсутствует':
                    if 'hrs' in v:
                        date_res1=datetime.date(datetime.now())-timedelta(hours=int(v.split(' ')[0]))
                        get_urls(k,date_res1)
                        print('Данные успешно вставлены, переход на следующую страницу.')
                    elif 'day' in v:
                        date_res1=datetime.date(datetime.now())-timedelta(days=int(v.split(' ')[0]))
                        get_urls(k,date_res1)
                        print('Данные успешно вставлены, переход на следующую страницу.')
                    elif 'days' in v:
                        date_res1=datetime.date(datetime.now())-timedelta(days=int(v.split(' ')[0]))
                        get_urls(k,date_res1)
                        print('Данные успешно вставлены, переход на следующую страницу.')
                else:
                    continue 
            print(z)       

def take_info_about_flats():
    with SB( sjw=True,pls='none',uc=True,headless=True) as sb:
        # sb.open('https://www.redfin.com/')
        # sb.load_cookies(name='test_case.txt')
        for i in select_urls():
            try:
                sb.open(f"{i[1]}")
                time.sleep(7)
                status=sb.find_element('span[class="bp-DefinitionFlyout bp-DefinitionFlyout__underline"]')
                price=sb.find_element('div[class="statsValue"]').text[1:]
                price=price.replace(',','')
                descr=sb.find_element('div[id="marketing-remarks-scroll"]')  
                date=sb.find_element('div[class="inline-block"]')  
                year=sb.find_elements('div[class="keyDetails-value"]')
                if 'hours' in date.text or 'hour' in date.text:
                    date_res=datetime.date(datetime.now())-timedelta(hours=int(date.text.split(' ')[0]))
                elif 'day' in date.text or 'days' in date.text:
                    date_res=datetime.date(datetime.now())-timedelta(days=int(date.text.split(' ')[0]))
                print(str(i[1]),
                    str(status.text),
                    str(price),
                    str(date_res),
                    str(descr.text),
                    str(year[2].text.split(' ')[-1]))
                vstavka1(str(i[1]),str(status.text),int(price),date_res,str(descr.text),str(year[2].text.split(' ')[-1]))
                time.sleep(7)
            except Stale_Exception as s:
                print('Произошла ошибка',s)
                continue
            except Exception as ex:
                print('warn',ex)

take_info_about_flats()

def take_info_about_select_url(url):
    with SB( sjw=True,pls='none',uc=True,headless=True) as sb:
        # sb.open('https://www.redfin.com/')
        # sb.load_cookies(name='test_case.txt')
        # try:
        sb.open(url)
        time.sleep(5)
        status=sb.find_element('span[class="bp-DefinitionFlyout bp-DefinitionFlyout__underline"]')
        price=sb.find_element('div[class="statsValue"]').text[1:]
        price=price.replace(',','')
        descr=sb.find_element('div[id="marketing-remarks-scroll"]')  
        date=sb.find_element('div[class="inline-block"]')  
        year=sb.find_elements('div[class="keyDetails-value"]')
        date_res=datetime.date(datetime.now())-timedelta(days=int(date.text.split(' ')[0]))
        print(str(url),
            str(status.text),
            str(price),
            str(date_res),
            str(descr.text),
            str(year[2].text.split(' ')[-1]))
        get_urls(str(url),date_res)
        time.sleep(2)
        vstavka1(str(url),str(status.text),int(price),date_res,str(descr.text),str(year[2].text.split(' ')[-1]))
        # except Stale_Exception() as ex:
        #     print("Произошла ошибочка, сайт испуган",ex)
            

# for i in select_urls():
#     print(i)