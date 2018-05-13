#_*_coding:utf-8_*
import requests
import time
from pprint import pprint
from bs4 import BeautifulSoup
from pymongo import MongoClient
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Host":"zh.58.com"
}
url = "http://zh.58.com/{location}/{type}/pn{number}/?minprice={minPrice}_{maxPrice}"
def get_max_pages(start_url,location="doumen",types="chuzu",minPrice="0",maxPrice="1000"):
    structure_url = start_url.format(location=location,type=types,number=0,minPrice=minPrice,maxPrice=maxPrice)
    try:
        response = requests.get(structure_url,headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(e)
        return -1
    html = BeautifulSoup(response.text,'lxml')
    pages = [int(page.text) for page in html.select("#bottom_ad_li > div.pager > a > span")  ]
    max_page = max(pages)
    if max_page==None and max_page==0:
        print("max_page{0}".format(max_page))
        return 0
    return max_page
def write_zufan_info(start_url,maxPage,location="doumen",types="chuzu",minPrice="0",maxPrice="1000"):
    structure_url_list = [ start_url.format(location=location,type=types,number=page,minPrice=minPrice,maxPrice=maxPrice) for page in range(1,maxPage+1)]
    client = None
    try:
        client = MongoClient('localhost',27017)
        db_58zufangcity = client.db_58zufangcity
        domen_base_info = db_58zufangcity[location+"_base_info"]
        for page in structure_url_list:
            try:
                response = requests.get(page, headers=headers)
                response.raise_for_status()
            except Exception as e:
                print(e)
                return -1
            html = BeautifulSoup(response.text, 'lxml')
            a_tag = html.select("ul.listUl > li > div.des > h2 > a")
            if a_tag == []:
                print("爬取完毕，已经没有数据")
                return 0
            href_list = [href.get("href") for href in a_tag]
            text_list = [href.text for href in a_tag]
            for href, text in zip(href_list, text_list):
                data = {
                    "href": href,
                    "text": text.split()
                }
                domen_base_info.insert(data)
            print("Download:{0}".format(response.url))
            time.sleep(4)
    except Exception as e:
        print('连接数据库失败')
        print(e.args)
    finally:
        if client is not None:
            client.close()
write_zufan_info(url,location='jida',maxPage=get_max_pages(url))