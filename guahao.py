# coding:utf-8
import requests
import selenium
from selenium import webdriver
import time
from lxml import etree
import chardet
from urllib.parse import urlencode
import urllib.request
import urllib.parse

def login(username, passwd):
    url = 'http://wx.ezhuanzhen.com/beida1_wx/userop/login.php'
    browser = webdriver.Chrome(r'/home/hee/Desktop/gitee/aimonitor/utils/chromedriver')
    browser.get(url)
    name_xpath = browser.find_element_by_id('username')

    passwd_xpath = browser.find_element_by_id('password')
    login_xpath = browser.find_element_by_class_name('btn01')
    name_xpath.click()
    name_xpath.send_keys(username)
    passwd_xpath.send_keys(passwd)
    login_xpath.click()
    cookies_list = browser.get_cookies()
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    cookies = [k + "=" + v for k, v in cookies_dict.items()]
    cookies = ';'.join(item for item in cookies)

    # browser.quit()
    return cookies


def get_id():
    url = 'http://wx.ezhuanzhen.com/beida1_wx/hyzslist.php?keid=P9dGq_jG'
    res = requests.get(url)
    html = res.text
    html = html.encode(res.encoding)
    haoid_list = []
    selector = etree.HTML(html)
    for item in selector.xpath('//a'):
        try:
            link = item.xpath('./@href')[0]
        except:
            continue
        try:
            # print(link)
            tmp = item.xpath('.//div[@class="block12d"]/text()')[0]
            tmp = item.xpath('.//div[@class="block12d"]/p/text()')[0]
        except:
            continue
        if 'guahao/guahaoqr.php?' not in link:
            continue
        elif '已约满' in item.xpath('./div/div[1]/text()'):
            # print('不可预约')
            continue
        else:
            p_str = item.xpath('.//div[@class="block12d"]/p/text()')[0]
            # if '杨淑霞' in p_str:
            if '杨淑霞' in p_str:
                # print(link)
                haoid = link.split('=')[-1]
                # break
                # print('---------------')
                # print(haoid)
                haoid_list.append(link)
                # print('----------------')

    return haoid_list


def guahao(        
        cookie,
        haoid_list,
        userid="130425199110177528@leaf@45663930",
        ksid="P9dGq_jqQ[[c]]5c"

    ):
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':'114',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':cookie,
        'Host':'wx.ezhuanzhen.com',
        'Origin':'http://wx.ezhuanzhen.com',
        'Pragma':'no-cache',
        'Referer':'http://wx.ezhuanzhen.com/beida1_wx/guahao/guahaoqr.php?id=IHS,kM[[x]][[(]]',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }
    url = 'http://wx.ezhuanzhen.com/beida1_wx/guahao/confirm.php'

    for haoid in haoid_list:
        form_data = {
            'haoid': haoid,
            'userid': userid,
            'ksid': ksid
        }
        print(form_data)
        # # data = 'haoid=IHS%2CkM%5B%5Bx%5D%5D%5B%5B(%5D%5D&userid=130425199110177528%40leaf%4045663930&ksid=P9dGq_jqQ%5B%5Bc%5D%5D5c'
        # data = urllib.parse.urlencode(form_data)
        # data = data.encode('ascii')
        # req = urllib.request.Request(url, data=data, headers=headers)
        # res = urllib.request.urlopen(req)
        # html  = res.read()
        # print(html)
        print(headers)
        print(urlencode(form_data))
        form_data = urlencode(form_data)
        res = requests.post(url, data=form_data, headers=headers)
        html = res.text
        html = html.encode(res.encoding)
        # print(html)
        print(res.status_code)
        print('-----------------')


def run(username,passwd):
    url = 'http://wx.ezhuanzhen.com/beida1_wx/userop/login.php'
    browser = webdriver.Chrome(r'/home/hee/Desktop/gitee/aimonitor/utils/chromedriver')
    browser.get(url)
    name_xpath = browser.find_element_by_id('username')

    passwd_xpath = browser.find_element_by_id('password')
    login_xpath = browser.find_element_by_class_name('btn01')
    name_xpath.click()
    name_xpath.send_keys(username)
    passwd_xpath.send_keys(passwd)
    login_xpath.click()
    cookies_list = browser.get_cookies()
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    cookies = [k + "=" + v for k, v in cookies_dict.items()]
    cookies = ';'.join(item for item in cookies)
    browser.get('http://wx.ezhuanzhen.com/beida1_wx/hyzslist.php?keid=P9dGq_jG')
    haoid_list = get_id()
    for link in haoid_list:
        link = 'http://wx.ezhuanzhen.com/beida1_wx/{}'.format(link)
        print(link)

        browser.get(link)
        browser.find_element_by_id('button').click()
        time.sleep(0.5)
        # print(dir(browser))
        find = browser.switch_to_alert()
        # print(find.text())
        find.dismiss()
        time.sleep(10000)

if __name__ == '__main__':
    username = '15332177580'
    passwd = 'lirui240713'
    # cookie = login(username, passwd)
    # haoid_list = get_id()
    # guahao(cookie=cookie, haoid_list = haoid_list)
    run(username,passwd)
