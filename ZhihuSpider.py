#_*_coding:utf-8_*
import configparser
from  pprint import pprint
import time
import json
import base64
import requests

url = "https://www.zhihu.com/api/v3/oauth/sign_in"

headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        "authorization":'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'

            }
post_data={
        'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
        'grant_type':'password',
        'timestamp':'1525618945556',
        'source':'com.zhihu.web',
        'signature':'beeab4ca13a4a4d55c774d12dd75e542ed2a1e71',
        'username':"",
        'password':"7",
        'captcha':None,
        'lang':'en',
        'ref_source':'homepage',
        'utm_source':''
    }

session = requests.Session()
response = session.post(url,headers = headers,data = post_data)
response1 = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=headers,verify= False)
response2 = session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=headers,verify=False)
print(response.content.decode("utf-8"))
print(response1.content.decode("utf-8"))
img = json.loads(response2.content)['img_base64']
img = img.encode('utf-8')
img_data = base64.b64decode(img)
with open('zhihu_captcha.GIF','wb') as f:
        f.write(img_data)

