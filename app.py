# Description: Main file for the web app
# Author: Yarne Gooris (WebPrograme)

# Importing modules
# Standard modules
import datetime
import json
import logging
import os
import random
from argparse import ArgumentParser
from base64 import b64decode, b64encode

# Third party modules
import requests
from bs4 import BeautifulSoup
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
from flask_cors import CORS, cross_origin
from PIL import Image
from rich.console import Console
from werkzeug.middleware.proxy_fix import ProxyFix

# Import the model file
import model

# Initialize the Flask app
app = Flask('Fashion recommender', template_folder='template')
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
dev_status = False

# Initialize the log and error console
console = Console()
error_console = Console(stderr=True, style="bold red")

# Initialize needed variables
temp_list = []
ready2go_results_list = []
last_index = 0

# Get the ready2go results and parse them
ready2go_results = requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/data/ready2go_results.txt').content
ready2go_results = ready2go_results.decode('utf-8')

for count, i in enumerate(ready2go_results):
    if i == ']':
        temp_list.append(ready2go_results[last_index:count])
        last_index = count

for i in temp_list:
    a = i.split(', ')
    if ']\n' in a[0]:
        a[0] = a[0].replace(']\n', '')
    elif '] \n' in a[0]:
        a[0] = a[0].replace('] \n', '')
    ready2go_results_list.append(a)

# Get the express color list
express_color_list_file = requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/data/express_color_list.json').content
express_color_list = json.loads(express_color_list_file)['colors']

# Initialize the standard headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 
           "Upgrade-Insecure-Requests": "1", 
           "DNT": "1",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5",
           "Accept-Encoding": "gzip, deflate"}

# Initialize all the available Ready2Go items
forselectedItems = ['fashion_bershka//women\\0581666603.webp',
                    'fashion_bershka//women\\0847810920.webp',
                    'fashion_bershka//women\\1305354615.webp',
                    'fashion_bershka//women\\1618200400.webp',
                    'fashion_bershka//women\\1619200806.webp',
                    'fashion_bershka//women\\2562033807.webp',
                    'fashion_bershka//women\\2569492800.webp',
                    'fashion_bershka//women\\3315187800.webp',
                    'fashion_bershka//women\\4048694800.webp',
                    'fashion_bershka//women\\7603777514.webp',
                    'fashion_bershka//women\\2317381800.webp',
                    'fashion_bershka//women\\0045969428.webp',
                    'fashion_bershka//women\\0054969433.webp',
                    'fashion_bershka//women\\0035352400.webp',
                    'fashion_hm//women\\0940771016.webp',
                    'fashion_hm//women\\0981815007.webp',
                    'fashion_hm//women\\0982361008.webp',
                    'fashion_hm//women\\0994907004.webp',
                    'fashion_hm//women\\1018158008.webp',
                    'fashion_hm//women\\1021205001.webp',
                    'fashion_hm//women\\1026309002.webp',
                    'fashion_hm//women\\1028353003.webp',
                    'fashion_hm//women\\1031889003.webp',
                    'fashion_hm//women\\1042266001.webp',
                    'fashion_hm//women\\1042286003.webp',
                    'fashion_hm//women\\1048732001.webp',
                    'fashion_mango//women\\2701826099.webp',
                    'fashion_mango//women\\2702252679.webp',
                    'fashion_mango//women\\2705576191.webp',
                    'fashion_mango//women\\2708476650.webp',
                    'fashion_mango//women\\2708288382.webp',
                    'fashion_mango//women\\2709712743.webp',
                    'fashion_mango//women\\2707475849.webp',
                    'fashion_mango//women\\27022512TC.webp',
                    'fashion_mango//women\\27021097TC.webp',
                    'fashion_pullbear//women\\4245361603.webp',
                    'fashion_pullbear//women\\4240362424.webp',
                    'fashion_pullbear//women\\4245317751.webp',
                    'fashion_pullbear//women\\4245386445.webp',
                    'fashion_pullbear//women\\4245388800.webp',
                    'fashion_pullbear//women\\4245458615.webp',
                    'fashion_pullbear//women\\4245461800.webp',
                    'fashion_pullbear//women\\4246373800.webp',
                    'fashion_pullbear//women\\4247364513.webp',
                    'fashion_pullbear//women\\4390364021.webp',
                    'fashion_pullbear//women\\4474328707.webp',
                    'fashion_pullbear//women\\4555305400.webp',
                    'fashion_pullbear//women\\4556303420.webp',
                    'fashion_pullbear//women\\4590383602.webp',
                    'fashion_pullbear//women\\4674322529.webp',
                    'fashion_pullbear//women\\4684322427.webp',
                    'fashion_pullbear//women\\4694317802.webp',
                    'fashion_pullbear//women\\4711323800.webp',
                    'fashion_pullbear//women\\8681320406.webp',
                    'fashion_pullbear//women\\8696321407.webp',
                    'fashion_pullbear//women\\9553316800.webp',
                    'fashion_pullbear//women\\8245312022.webp',
                    'fashion_pullbear//women\\8241350433.webp',
                    'fashion_pullbear//women\\8245336420.webp',
                    'fashion_pullbear//women\\4593409719.webp',
                    'fashion_pullbear//women\\4573301527.webp',
                    'fashion_pullbear//women\\4474359500.webp',
                    'fashion_pullbear//women\\4474374400.webp',
                    'fashion_pullbear//women\\4474371505.webp',
                    'fashion_pullbear//women\\4549309430.webp',
                    'fashion_pullbear//women\\4390360800.webp',
                    'fashion_pullbear//women\\4246332515.webp',
                    'fashion_pullbear//women\\4245376500.webp',
                    'fashion_stradivarius//women\\0709203042.webp',
                    'fashion_stradivarius//women\\0927029552.webp',
                    'fashion_stradivarius//women\\2051876001.webp',
                    'fashion_stradivarius//women\\2120225145.webp',
                    'fashion_stradivarius//women\\2110419001.webp',
                    'fashion_stradivarius//women\\2386228001.webp',
                    'fashion_stradivarius//women\\2616512340.webp',
                    'fashion_stradivarius//women\\2619836250.webp',
                    'fashion_stradivarius//women\\5918583145.webp',
                    'fashion_stradivarius//women\\7006820341.webp',
                    'fashion_stradivarius//women\\7010186010.webp',
                    'fashion_stradivarius//women\\7168120045.webp',
                    'fashion_stradivarius//women\\7341168700.webp',
                    'fashion_stradivarius//women\\7346216700.webp',
                    'fashion_stradivarius//women\\8828132001.webp',
                    'fashion_stradivarius//women\\8817155411.webp',
                    'fashion_stradivarius//women\\7100184400.webp',
                    'fashion_stradivarius//women\\7093130422.webp',
                    'fashion_stradivarius//women\\2663663001.webp',
                    'fashion_stradivarius//women\\2504571400.webp',
                    'fashion_stradivarius//women\\0861026144.webp',
                    'fashion_stradivarius//women\\0894063004.webp',
                    'fashion_stradivarius//women\\1362768702.webp',
                    'fashion_zara//women\\3067418.webp',
                    'fashion_zara//women\\3253320.webp',
                    'fashion_zara//women\\4387312.webp',
                    'ready2go//women\\1.webp',
                    'ready2go//women\\2.webp',
                    'ready2go//women\\3.webp',
                    'ready2go//women\\4.webp',
                    'ready2go//women\\5.webp',
                    'ready2go//women\\6.webp',
                    'ready2go//women\\7.webp',
                    'ready2go//women\\8.webp',
                    'ready2go//women\\9.webp',
                    'ready2go//women\\10.webp',
                    'ready2go//women\\11.webp',
                    'ready2go//women\\12.webp',
                    'ready2go//women\\13.webp',
                    'ready2go//women\\14.webp',
                    'ready2go//women\\15.webp',
                    'ready2go//women\\16.webp',
                    'ready2go//women\\17.webp',
                    'ready2go//women\\18.webp',
                    'ready2go//women\\19.webp',
                    'ready2go//women\\20.webp',
                    'ready2go//women\\21.webp',
                    'ready2go//women\\22.webp',
                    'ready2go//women\\23.webp',
                    'ready2go//women\\24.webp',
                    'ready2go//women\\25.webp',
                    'ready2go//women\\26.webp',
                    'ready2go//women\\27.webp',
                    'ready2go//women\\28.webp',
                    'ready2go//women\\29.webp',
                    'ready2go//women\\30.webp',
                    'ready2go//women\\31.webp',
                    'ready2go//women\\32.webp',
                    'ready2go//women\\33.webp',
                    'ready2go//women\\34.webp',
                    'ready2go//women\\35.webp',
                    'ready2go//women\\36.webp',
                    'ready2go//women\\37.webp',
                    'ready2go//women\\38.webp',
                    'ready2go//women\\39.webp',
                    'ready2go//women\\40.webp',
                    'ready2go//women\\41.webp',
                    'ready2go//women\\42.webp',
                    'ready2go//women\\43.webp',
                    'ready2go//women\\44.webp',
                    'ready2go//women\\45.webp',
                    'ready2go//women\\46.webp',
                    'ready2go//women\\47.webp',
                    'ready2go//women\\48.webp',
                    'ready2go//women\\49.webp',
                    'ready2go//women\\50.webp',
                    'ready2go//women\\51.webp',
                    'ready2go//women\\52.webp',
                    'ready2go//women\\53.webp',
                    'ready2go//women\\54.webp',
                    'ready2go//women\\55.webp',
                    'ready2go//women\\56.webp',
                    'ready2go//women\\57.webp',
                    'ready2go//women\\58.webp',
                    'ready2go//women\\59.webp',
                    'ready2go//women\\60.webp',
                    'ready2go//women\\61.webp',
                    'ready2go//women\\65.webp',
                    'ready2go//women\\66.webp',
                    'ready2go//women\\67.webp',
                    'ready2go//women\\68.webp',
                    'ready2go//women\\69.webp',
                    'ready2go//women\\70.webp',
                    'ready2go//women\\71.webp',
                    'ready2go//women\\72.webp']

@app.route('/', defaults={'page': 'index'})
@app.route('/')
# This function is called when the user visits the home page
def home():
    picked_items =  random.sample(range(len(forselectedItems)), 20)
    results = [forselectedItems[i] for i in picked_items]
    product_img = []
    product_links = []
    product_numbers = []
    stores = []
    count = 1
    for result in results:
        if 'fashion_hm' in result:
            storeName = 'H&M'
            store_path = 'fashion_hm'
        elif 'fashion_pullbear' in result:
            storeName = 'Pull&Bear'
            store_path = 'fashion_pullbear'
        elif 'fashion_bershka' in result:
            storeName = 'Bershka'
            store_path = 'fashion_bershka'
        elif 'fashion_mango' in result:
            storeName = 'Mango'
            store_path = 'fashion_mango'
        elif 'fashion_newyorker' in result:
            storeName = 'New Yorker'
            store_path = 'fashion_newyorker'
        elif 'fashion_zalando' in result:
            storeName = 'Zalando'
            store_path = 'fashion_zalando'
        elif 'fashion_zara' in result:
            storeName = 'Zara'
            store_path = 'fashion_zara'
        elif 'fashion_mostwanted' in result:
            storeName = 'Most Wanted'
            store_path = 'fashion_mostwanted'
        elif 'fashion_we' in result:
            storeName = 'WE'
            store_path = 'fashion_we'
        elif 'fashion_stradivarius' in result:
            storeName = 'Stradivarius'
            store_path = 'fashion_stradivarius'
        elif 'ready2go' in result:
            storeName = 'Ready2Go'
            store_path = 'ready2go'
        
        path = result
        start = os.path.splitext(path)[0].find('\\')
        file_name = os.path.splitext(path)[0][start+1:] + os.path.splitext(path)[1]
        link = ''
        product_links.append(f'href={link}')
    
        if storeName != 'Most Wanted':
            stores.append(storeName)
        else:
            stores.append('WM')
        product_numbers.append(file_name[:-5])        
        product_img.append(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{file_name[:-5]}.webp')
            
        count += 1
    
    return render_template('index.html',len=len(product_img), product_img=product_img, product_number=product_numbers, product_store=stores, product_link=product_links)          

# Used to handle errors
class errorhandler(Exception):
    # This function is called when a 400 error occurs
    @app.errorhandler(400)
    def page_not_found(e):
        return render_template('error/400.html'), 400
    
    # This function is called when a 404 error occurs
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    # This function is called when a 500 error occurs
    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('error/500.html'), 500

# Used to handle the terminal
class terminal():
    # Used to log a event/message
    def log(message):
        try:
            console.log(message)
        except Exception as e:
            terminal.error(e)
        
    # Used to log a error
    def error(message):
        error_console.log(message)

# Used to extract the image from given input
class extract_img():
    def __init__(self, userID, headers):
        self.headers = headers
        self.userID = userID
    
    # Used to extract the image from a given number and store
    def extract_img_from_number(number, store, userID, gender):
        global headers
        
        if store == 'H&M':
            page = requests.get(f"https://www2.hm.com/nl_be/productpage.{number}.html", headers=headers).content
            soup = BeautifulSoup(page, 'html.parser')

            try:
                soup = soup.find_all('a', {"class": "active"})
                img_urls = []
                for i in soup:
                    img_urls.append(i.find_all('img')[0]['src'])
                
                for img in img_urls:
                    if 'DESCRIPTIVESTILLLIFE' in img:
                        img_url = img
                        img_url = img_url.replace('miniature', 'main')
                        break

                return 'https:' + img_url, headers
            except:
                pass
        elif store == 'Bershka':
            number_backup = number
            data = requests.post(f'https://2kv2lbqg6e-dsn.algolia.net/1/indexes/pro_SEARCH_NL/query?x-algolia-agent=Algolia for JavaScript (3.35.1); Browser&x-algolia-application-id=2KV2LBQG6E&x-algolia-api-key=MGY4YzYzZWI2ZmRlYmYwOTM1ZGU2NGI3MjVjZjViMjgyMDIyYWM3NWEzZTM5ZjZiOWYwMzAyYThmNTkxMDUwMGF0dHJpYnV0ZXNUb0hpZ2hsaWdodD0lNUIlNUQmYXR0cmlidXRlc1RvU25pcHBldD0lNUIlNUQmZW5hYmxlUGVyc29uYWxpemF0aW9uPWZhbHNlJmVuYWJsZVJ1bGVzPXRydWUmZmFjZXRpbmdBZnRlckRpc3RpbmN0PXRydWUmZ2V0UmFua2luZ0luZm89dHJ1ZSZzbmlwcGV0RWxsaXBzaXNUZXh0PSVFMiU4MCVBNiZzdW1PckZpbHRlcnNTY29yZXM9dHJ1ZQ==', headers=headers, json={"params":f"query={number}&analytics=true&analyticsTags=%5B%22dweb%22%2C%22country_nl%22%2C%22lang_nl%22%2C%22wmen%22%2C%22no_teen%22%2C%22season%22%2C%22store%22%5D&clickAnalytics=false&hitsPerPage=36&ruleContexts=%5B%22dweb%22%2C%22country_nl%22%2C%22lang_nl%22%2C%22wmen%22%2C%22wmen_nl%22%5D&attributesToRetrieve=%5B%22pElement%22%5D&facets=%5B%22mainCategory%22%5D&filters=&page=0"}).content
            
            number = json.loads(data)['hits'][0]['pElement']
                
            data = requests.get(f'https://www.bershka.com/itxrest/3/catalog/store/44009503/40259546/productsArray?productIds={number}%2C106465680%2C106185120%2C103578123%2C103646838&languageId=100', headers=headers).content
            data = json.loads(data)
            try:
                img_path = data['products'][0]['bundleProductSummaries'][0]['detail']['xmedia'][0]['path']
                if str(data['products'][0]['bundleProductSummaries'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-2][-1]) == '_':
                    img_id = data['products'][0]['bundleProductSummaries'][0]['detail'][
                        'xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-2] + '4_3'
                    img_ts = data['products'][0]['bundleProductSummaries'][0]['detail'][
                        'xmedia'][0]['xmediaItems'][0]['medias'][0]['timestamp']
                elif str(data['products'][0]['bundleProductSummaries'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-3][-1]) == '_':
                    img_id = data['products'][0]['bundleProductSummaries'][0]['detail'][
                        'xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-3] + '4_3'
                    img_ts = data['products'][0]['bundleProductSummaries'][0]['detail'][
                        'xmedia'][0]['xmediaItems'][0]['medias'][0]['timestamp']
            except:
                img_path = data['products'][0]['detail']['xmedia'][0]['path']
                if str(data['products'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-2][-1]) == '_':
                    img_id = data['products'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-2] + '4_3'
                    img_ts = data['products'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['timestamp']
                elif str(data['products'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-3][-1]) == '_':
                    img_id = data['products'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['idMedia'][:-3] + '4_3'
                    img_ts = data['products'][0]['detail']['xmedia'][0]['xmediaItems'][0]['medias'][0]['timestamp']
            end = img_id.find('_')
            img_id = str(img_id[:end][:-3]) + str(number_backup)[-3:] + str(img_id[end:])
            img_path = str(img_path[:-3]) + str(number_backup)[-3:]
            return f'https://static.bershka.net/4/photos2{img_path}/{img_id}.jpg?t={img_ts}', headers
        elif store == 'C&A':
            return f'https://www.c-and-a.com/productimages/b_rgb:EBEBEB,c_scale,h_790,q_70,e_sharpen:70/v1646044533/{number}-1-08.jpg', headers
        elif store == 'Mango':
            data = requests.get(f'https://shop.mango.com/services/garments/{number}', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "stock-id": "017.NL.0.false.false.v3"}).content
            data = json.loads(data)['colors']['colors'][0]
            id_color = data['id']
            return f'https://st.mngbcn.com/rcs/pics/static/T3/fotos/S20/{number}_{id_color}_B.jpg', headers
        elif store == 'New Yorker':
            data = requests.get(f'https://api.newyorker.de/csp/products/public/product/{number}?country=nl', headers=headers).content
            data = json.loads(data)
            try:
                images = data['variants'][0]['images']
            except:
                images = data['images']
            for imageFile in images:
                if imageFile['type'] == 'CUTOUT' and imageFile['angle'] == 'FRONT':
                    return f'https://nyblobstoreprod.blob.core.windows.net/product-images-public/{imageFile["key"]}', headers
        elif store == 'Guess':
            data = requests.get(f'https://www.guess.eu/en-sk/guess/women/clothing/{number}.html', headers=headers)
            number = data.url
            end_url = ''.join(number).rindex('/')
            number = number[end_url+1:-5]
            return f'https://res.cloudinary.com/guess-img/image/upload/f_auto,q_auto,fl_strip_profile,e_sharpen:50,w_640,c_scale,dpr_auto/v1/EU/Style/ECOMM/{number}-ALTGHOST', headers
        elif store == 'Zara':
            number = number.replace('/', '')
            data = requests.get(f'https://www.zara.com/be/nl/-p0{number}.html', headers=headers).content
            data = str(data)
            img_find = data.find('6_1_1.jpg')
            end = data[img_find:].find('"')
            reverse = data[:end+img_find][::-1]
            start = reverse.find('"')
            img_url = reverse[:start][::-1]
            return img_url, headers
        elif store == 'Reserved':
            return f'https://www.reserved.com/media/catalog/product/{number[0]}/{number[1]}/{number.upper()}-010-1_1.jpg', headers
        elif store == 'Weekday':
            product_data = requests.get(f'https://www.weekday.com/en_eur/search.html?q={number}', headers=headers).content

            soup = BeautifulSoup(product_data, 'html.parser')
            product = soup.find_all('div', {'class': 'o-product'})[0]
            product_img_url = product.find_all('img', {'class': 'a-image'})[0]['data-resolvechain']
            return 'https://lp.weekday.com/app003prod?set=key[resolve.pixelRatio],value[1]&set=key[resolve.width],value[450]&set=key[resolve.height],value[10000]&set=key[resolve.imageFit],value[containerwidth]&set=key[resolve.allowImageUpscaling],value[0]&set=key[resolve.format],value[webp]&set=key[resolve.quality],value[90]&:' + product_img_url, headers
        elif store == 'Pull&Bear':
            data = requests.get('https://api.empathybroker.com/search/v1/query/pullbear/searchv2?scope=desktop&lang=en&catalogue=20309426&store=24009502&warehouse=22109425&section=' + "woman" +'&q=' + number +'&start=0&rows=48&origin=linked&filter={!tag=hierarchical_category_facet}hierarchical_category_20309426_24009502:"' + "woman" + '"', headers=headers).content
            
            number = json.loads(data)['content']['docs'][0]['mocacoReference'].replace('/', '')
            
            possible_urls = [f"https://static.pullandbear.net/2/photos//2023/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?",
                            f"https://static.pullandbear.net/2/photos//2023/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?",
                            f"https://static.pullandbear.net/2/photos//2022/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?",
                            f"https://static.pullandbear.net/2/photos//2022/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?",
                            f"https://static.pullandbear.net/2/photos//2021/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?",
                            f"https://static.pullandbear.net/2/photos//2021/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_6_8.jpg?"]
            
            for url in possible_urls:
                req = requests.get(url, headers=headers)
                if req.status_code == 200:
                    return url, headers
        elif store == 'Aerie':
            product_data = requests.get(f'https://www.ae.com/us/en/s/{number}', headers=headers).content
            
            soup = BeautifulSoup(product_data, 'html.parser')
            product_url = soup.find_all('a', {'class': 'tile-link'})[0]['href']
            number_reverse = product_url[::-1]
            start = number_reverse.find('/')
            product_id = number_reverse[:start][::-1][:13]
                
            return f'https://s7d2.scene7.com/is/image/aeo/{product_id}_f?$pdp-mdg-opt$&fmt=jpeg', headers
        elif store == 'American Eagle':
            product_data = requests.get(f'https://www.ae.com/us/en/s/{number}', headers=headers).content
            
            soup = BeautifulSoup(product_data, 'html.parser')
            product_url = soup.find_all('a', {'class': 'tile-link'})[0]['href']
            number_reverse = product_url[::-1]
            start = number_reverse.find('/')
            product_id = number_reverse[:start][::-1][:13]
                
            return f'https://s7d2.scene7.com/is/image/aeo/{product_id}_f?$pdp-mdg-opt$&fmt=jpeg', headers
        elif store == 'River Island':
            return f'https://images.riverisland.com/is/image/RiverIsland/_{number}_alt2?$ProductImagePortraitLarge$', headers
        elif store == 'Hollister (+ Social Tourist)':
            product_data = requests.get(f'https://www.hollisterco.com/api/search/h-eu/search/department/NDC_12552-HOL?catalogId=11558&expandedFacet=true&requestType=search&rows=240&searchTerm={number}&start=0&storeId=19158&version=1.2', headers=headers).content

            product_img_id = json.loads(product_data)['products'][0]['imageId']

            return f'https://img.hollisterco.com/is/image/anf/{product_img_id}_prod1?policy=product-large', headers
        
    # Used to extract the image from a given link and store
    def extract_img_from_link(number, store):
        global headers
        if not 'https://' in number:
            number = f'https://{number}'
        
        if store == 'H&M':
            page = requests.get(number, headers=headers).content
            soup = BeautifulSoup(page, 'html.parser')

            try:
                soup = soup.find_all('a', {"class": "active"})
                img_urls = []
                for i in soup:
                    img_urls.append(i.find_all('img')[0]['src'])
                
                for img in img_urls:
                    if 'DESCRIPTIVESTILLLIFE' in img:
                        img_url = img
                        img_url = img_url.replace('miniature', 'main')
                        break

                return 'https:' + img_url, headers
            except:
                pass
        elif store == 'Bershka':
            base_url = number.find('c0p')
            end_url = number.find('.html')
            if 'colorid=' in number:
                startColor = number.find('colorid=')
            else:
                startColor = number.find('colorId=')                
            colorId = number[startColor+8:startColor+11]
            number = number[base_url+3:end_url]
            data = requests.get(f'https://www.bershka.com/itxrest/3/catalog/store/44009503/40259546/productsArray?productIds={number}%2C106465680%2C106185120%2C103578123%2C103646838&languageId=100', headers=headers).content
            data = json.loads(data)
            if not data['products'][0]['bundleProductSummaries']:
                for color in data['products'][0]['detail']['colors']:
                    if color['id'] == str(colorId):
                        img_path = color['image']['url'] + '_2_4_3'
                        img_ts = color['image']['timestamp']
                        break
            else:
                for color in data['products'][0]['bundleProductSummaries'][0]['detail']['colors']:
                    if color['id'] == str(colorId):
                        img_path = color['image']['url'] + '_2_4_3'
                        img_ts = color['image']['timestamp']
                        break
            return f'https://static.bershka.net/4/photos2{img_path}.jpg?t={img_ts}', headers
        elif store == 'Stradivarius':            
            start = number.find('colorId=') + 8
            colorId = number[start:start+3]
            page = requests.get(number, headers=headers).content
            page = page.decode('utf-8')
            start = page.find('inditex.iProductId = ') + 21
            number = page[start:start+9]
            
            data = requests.get(f'https://www.stradivarius.com/itxrest/2/catalog/store/54009552/50331084/category/0/product/{number}/detail?languageId=100&appId=1', headers=headers).content
            data = json.loads(data)
            img_path = data['detail']['xmedia'][0]['path']
            if not data['bundleProductSummaries']:
                for color in data['detail']['colors']:
                    if color['id'] == str(colorId):
                        img_path = color['image']['url'] + '_2_4_3'
                        img_ts = color['image']['timestamp']
                        break
            else:
                for color in data['bundleProductSummaries'][0]['detail']['colors']:
                    if color['bundleProductSummaries'][0]['id'] == str(colorId):
                        img_path = color['bundleProductSummaries'][0]['image']['url'] + '_2_4_3'
                        img_ts = color['bundleProductSummaries'][0]['image']['timestamp']
                        break
            return f'https://static.e-stradivarius.net/5/photos3{img_path}.jpg?t={img_ts}', headers
        elif store == 'C&A':
            end_url = ''.join(number).rindex('/')
            number = number[end_url-7:end_url]
            return f'https://www.c-and-a.com/productimages/b_rgb:EBEBEB,c_scale,h_790,q_70,e_sharpen:70/v1646044533/{number}-1-08.jpg', headers
        elif store == 'Mango':
            backup_url = number
            end_url = number.find('.html')
            number = number[end_url-8:end_url]
            data = requests.get(f'https://shop.mango.com/services/garments/{number}', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "stock-id": "017.NL.0.false.false.v3"}).content
            data = json.loads(data)['colors']['colors'][0]
            id_color = data['id']
            return f'https://st.mngbcn.com/rcs/pics/static/T3/fotos/S20/{number}_{id_color}_B.jpg', headers
        elif store == 'New Yorker':
            backup_url = number
            base_url = number.find('detail/')
            end_url = ''.join(backup_url).rindex('/')
            number = number[base_url+7:end_url]
            data = requests.get(f'https://api.newyorker.de/csp/products/public/product/{number}?country=nl', headers=headers).content
            data = json.loads(data)
            try:
                images = data['variants'][0]['images']
            except:
                images = data['images']
            for imageFile in images:
                if imageFile['type'] == 'CUTOUT' and imageFile['angle'] == 'FRONT':
                    return f'https://nyblobstoreprod.blob.core.windows.net/product-images-public/{imageFile["key"]}', headers
        elif store == 'Guess':
            end_url = ''.join(number).rindex('/')
            number = number[end_url:-5]
            return f'https://res.cloudinary.com/guess-img/image/upload/f_auto,q_auto,fl_strip_profile,e_sharpen:50,w_640,c_scale,dpr_auto/v1/EU/Style/ECOMM/{number}-ALTGHOST', headers
        elif store == 'Zara':
            data = requests.get(number, headers=headers).content
            data = str(data)
            img_find = data.find('6_1_1.jpg')
            end = data[img_find:].find('"')
            reverse = data[:end+img_find][::-1]
            start = reverse.find('"')
            img_url = reverse[:start][::-1]
            return img_url, headers
        elif store == 'Pull&Bear':
            start = number.find('-l0')+3
            end = number.find('cS=')
            if end == -1:
                number_1 = number[start:start+4]
                number_2 = number[start+4:start+7]
                number_3 = number[start:start+7]
                
                data = requests.get(number, headers=headers).content
                
                data = str(data)
                start = data.find('iProductId = ') + 13
                end = data[start:].find(';')
                number2 = data[start:start+end]
                
                data = requests.get(f'https://www.pullandbear.com/itxrest/2/catalog/store/24009502/20309426/category/0/product/{number2}/detail?languageId=-1&appId=1', headers=headers).content
                
                data = str(data)
                start = data.find('colors":[{"id":"') + 16
                colorId = data[start:start+3]
                
                possible_urls = [f"https://static.pullandbear.net/2/photos//2023/V/0/1/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/1/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2023/V/0/2/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/2/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2022/V/0/1/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/1/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2022/V/0/2/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/2/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2021/V/0/1/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/1/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2021/V/0/2/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/2/p/{number_1}/{number_2}/{colorId}/{number_3}{colorId}_2_6_8.jpg?"]
                
                for url in possible_urls:
                    req = requests.get(url, headers=headers)
                    if req.status_code == 200:
                        return url, headers
                
            else:
                possible_urls = [f"https://static.pullandbear.net/2/photos//2023/V/0/1/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/1/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2023/V/0/2/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/2/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2022/V/0/1/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/1/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2022/V/0/2/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/2/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2021/V/0/1/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/1/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?",
                                f"https://static.pullandbear.net/2/photos//2021/V/0/2/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/2/p/{number[start:start+4]}/{number[start+4:start+7]}/{number[end+3:end+6]}/{number[start:start+7]}{number[end+3:end+6]}_2_6_8.jpg?"]

                for url in possible_urls:
                    req = requests.get(url, headers=headers)
                    if req.status_code == 200:
                        return url, headers
        elif store == 'Reserved':
            number = number[-9:]
            return f'https://www.reserved.com/media/catalog/product/{number[0]}/{number[1]}/{number.upper()}-010-1_1.jpg', headers
        elif store == 'Weekday':
            number = number[:-5]
            number_reverse = number[::-1]
            start = number_reverse.find('.')
            number = number_reverse[:start][::-1]
            product_data = requests.get(f'https://www.weekday.com/en_eur/search.html?q={number}', headers=headers).content
            
            soup = BeautifulSoup(product_data, 'html.parser')
            product = soup.find_all('div', {'class': 'o-product'})[0]
            product_img_url = product.find_all('img', {'class': 'a-image'})[0]['data-resolvechain']
            return 'https://lp.weekday.com/app003prod?set=key[resolve.pixelRatio],value[1]&set=key[resolve.width],value[450]&set=key[resolve.height],value[10000]&set=key[resolve.imageFit],value[containerwidth]&set=key[resolve.allowImageUpscaling],value[0]&set=key[resolve.format],value[webp]&set=key[resolve.quality],value[90]&:' + product_img_url, headers
        elif store == 'American Eagle':
            number_reverse = number[::-1]
            start = number_reverse.find('/')
            number = number_reverse[:start][::-1][:13]
            
            return f'https://s7d2.scene7.com/is/image/aeo/{number}_f?$pdp-mdg-opt$&fmt=jpeg', headers
        elif store == 'Aerie':
            number_reverse = number[::-1]
            start = number_reverse.find('/')
            number = number_reverse[:start][::-1][:13]
            
            return f'https://s7d2.scene7.com/is/image/aeo/{number}_f?$pdp-mdg-opt$&fmt=jpeg', headers
        elif store == 'River Island':
            number_reverse = number[::-1]
            start = number_reverse.find('-')
            number = number_reverse[:start][::-1][:6]
            
            return f'https://images.riverisland.com/is/image/RiverIsland/_{number}_alt2?$ProductImagePortraitLarge$', headers
        elif store == 'Abercrombie & Fitch':
            headers = headers
            img_data = requests.get(number, headers=headers).content
            
            soup = BeautifulSoup(img_data, 'html.parser')
            page = soup.find('div', {'class': 'product-page__info'})
            data = page.find('script')
            data = data.text
            start = data.find('"image": "') + len('"image": "')
            end = data.find('"', start)
            product_img_url = data[start:end]     
                
            return product_img_url, headers
        elif store == 'Express':
            number = number[:-1]
            number_reverse = number[::-1]
            start = number_reverse.find('/')
            color = number_reverse[:start][::-1]
            if '%20' in color:
                color = color.replace('%20', ' ')
            number = number[:-(9+len(color))]
            number = number[-8:]
            for i in express_color_list:
                if i['color'] == color:
                    color_id = i['ipColorCode']
                    if len(color_id) == 1:
                        color_id = '000' + color_id
                    elif len(color_id) == 2:
                        color_id = '00' + color_id
                    elif len(color_id) == 3:
                        color_id = '0' + color_id
                    break
                
            return f'https://images.express.com/is/image/expressfashion/0086_{number}_{color_id}_a001?cache=on&wid=960&fmt=jpeg&qlt=85,1&resmode=sharp2&op_usm=1,1,5,0&defaultImage=Photo-Coming-Soon$', headers
        elif store == 'Everlane':
            number = number.split('?')[0]

            number_reverse = number[::-1]
            start = number_reverse.find('/')
            number = number_reverse[::-1][-start:]

            img_data = requests.get(f'https://www.everlane.com/_next/data/zneatQD7T9oUcG1RTcBBG/products/{number}.json', headers=headers).content

            products = json.loads(img_data)['pageProps']['fallbackData']['products']

            for product in products:
                if product['permalink'] == number:
                    img_url = product['flatImage']
                    break

            return img_url, {"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "x-algolia-agen": "Algolia for JavaScript (3.35.1); Browser"}
        elif store == 'Hollister (+ Social Tourist)':
            data = requests.get(number, headers=headers).content
            soup = BeautifulSoup(data, 'html.parser')
            divs = soup.find_all('div')
            
            for div in divs:
                try:
                    product_id = div['data-bv-product-id']
                except:
                    continue

            product_data = requests.get(f'https://api.bazaarvoice.com/data/products.json?passkey=caw88B42LYsvvz6PM0ilR4nuwhBK0laeUlr9EtkOKbjZI&locale=en_US&allowMissing=true&apiVersion=5.4&filter=id:{product_id}', headers=headers).content
            product_img_url = json.loads(product_data)['Results'][0]['ImageUrl']
            return product_img_url, headers
        elif store == 'About You':
            data = requests.get(number).content
            data = str(data)
                
            imgStart = data.find('data-testid="productImage"')
            start = data[imgStart:].find('src="') + imgStart + 5
            end = data[start:].find('"') + start
            imgSrc = data[start:end]
            
            return imgSrc, headers
        elif store == 'Link of an image':
            image_formats = ("image/png", "image/jpeg", "image/jpg")
            r = requests.get(number, headers=headers)
            if r.headers["content-type"] in image_formats:
                return number, headers
            return None, None
                 
# Used to get the model image of a product (only contains functions for available stores)
class get_model_image():
    def hm(number):
        page = requests.get(f"https://www2.hm.com/nl_be/productpage.{number}.html", headers=headers).content
        soup = BeautifulSoup(page, 'html.parser')

        try:
            img_url = soup.find_all('img')[1].get('src')

            return 'https:' + img_url
        except:
            pass

    def mango(number):
        img_data = requests.get(f"https://st.mngbcn.com/rcs/pics/static/T3/fotos/S20/{number[:-2]}_{number[-2:]}.jpg", headers=headers)
        if img_data.status_code != 200:
            img_data = requests.get(f"https://st.mngbcn.com/rcs/pics/static/T3/fotos/S20/{number[:-2]}_{number[-2:]}_D1.jpg", headers=headers)
            return f"https://st.mngbcn.com/rcs/pics/static/T3/fotos/S20/{number[:-2]}_{number[-2:]}_D1.jpg"
        return f"https://st.mngbcn.com/rcs/pics/static/T3/fotos/S20/{number[:-2]}_{number[-2:]}.jpg"

    def newyorker(number):
        data = requests.get(f'https://api.newyorker.de/csp/products/public/product/{number}?country=nl', headers=headers).content
        data = json.loads(data)

        try:
            images = data['variants'][0]['images']
        except:
            images = data['images']

        for imageFile in images:
            if imageFile['type'] == 'OUTFIT_IMAGE' and imageFile['angle'] == 'FRONT':
                return f'https://nyblobstoreprod.blob.core.windows.net/product-images-public/{imageFile["key"]}'

    def zara(number):
        productId = number
        try:
            data = requests.get(f'https://www.zara.com/be/nl/-p0{productId}.html', headers=headers).content
            data = str(data)

            img_find = data.find('_1_1.jpg')
            end = data[img_find:].find('"')
            reverse = data[:end+img_find][::-1]
            start = reverse.find('"')
            img_url = reverse[:start][::-1]

            return img_url
        except Exception as e:
            print(e)
            pass

    def pullbear(number):
        possible_urls = [f"https://static.pullandbear.net/2/photos//2023/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?",
                         f"https://static.pullandbear.net/2/photos//2023/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?", f"https://static.pullandbear.net/2/photos//2023/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?",
                         f"https://static.pullandbear.net/2/photos//2022/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?",
                         f"https://static.pullandbear.net/2/photos//2022/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?", f"https://static.pullandbear.net/2/photos//2022/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?",
                         f"https://static.pullandbear.net/2/photos//2021/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?",
                         f"https://static.pullandbear.net/2/photos//2021/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?", f"https://static.pullandbear.net/2/photos//2021/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_2_1_1.jpg?"]
        
        for url in possible_urls:
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                return url 

    def stradivarius(number):
        return f"https://static.e-stradivarius.net/5/photos3/2022/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?"
        
    def bershka(number):
        possible_urls = [f"https://static.bershka.net/4/photos2/2023/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?", f"https://static.bershka.net/4/photos2/2023/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?",
                         f"https://static.bershka.net/4/photos2/2023/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?", f"https://static.bershka.net/4/photos2/2023/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?",
                         f"https://static.bershka.net/4/photos2/2022/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?", f"https://static.bershka.net/4/photos2/2022/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?",
                         f"https://static.bershka.net/4/photos2/2022/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?", f"https://static.bershka.net/4/photos2/2022/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?",
                         f"https://static.bershka.net/4/photos2/2021/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?", f"https://static.bershka.net/4/photos2/2021/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?",
                         f"https://static.bershka.net/4/photos2/2021/V/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?", f"https://static.bershka.net/4/photos2/2021/I/0/2/p/{number[:4]}/{number[4:7]}/{number[7:]}/{number}_1_1_1.jpg?"]
        
        for url in possible_urls:
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                return url
            
    def we(number):
        return f"https://www.wefashion.be/dw/image/v2/AANH_PRD/on/demandware.static/-/Sites-master-catalog/default/images/hi-res/{number}_2.jpg"

    def weekday(number):
        product_data = requests.get(f"https://www.weekday.com/en_eur/search.html?q={number}", headers=headers).content
        
        try:
            soup = BeautifulSoup(product_data, 'html.parser')
            product_url = soup.find_all('a', {'class': 'search-link-track'})[0]['href']
            product_data = requests.get(product_url, headers=headers).content
            
            soup = BeautifulSoup(product_data, 'html.parser')
            product_img_url = soup.find_all('img', {'class': 'default-image'})[0]['data-large-src']
                
            return 'https://lp.weekday.com/app003prod?set=key[resolve.pixelRatio],value[1]&set=key[resolve.width],value[450]&set=key[resolve.height],value[10000]&set=key[resolve.imageFit],value[containerwidth]&set=key[resolve.allowImageUpscaling],value[0]&set=key[resolve.format],value[webp]&set=key[resolve.quality],value[90]&:' + product_img_url
        except:
            return None

    def zalando(number):
        img_data = requests.get(f'https://www.zalando.be/dames/?q={number}', headers=headers).content
        data = str(img_data)
            
        start = data.find('"Image","uri":"')
        end = data.find('"', start + len('"Image","uri":"'))
        product_img_url = data[start + len('"Image","uri":"'):end]
        product_img_url = product_img_url[:product_img_url.find('?imwidth=')]
        return product_img_url

    def riverisland(number):
        return f'https://images.riverisland.com/is/image/RiverIsland/_{number}_main?$ProductImagePortraitLarge$'

# Used to switch between pages
class switch_page():
    # Used to switch to the first page (THIS IS NOT USED ANYMORE, ALERNATIVE IS USED INSTEAD)
    @app.route('/predict/1', methods=['POST', 'GET'])
    def prev_page():
        process_with_image = False
        start_time = datetime.datetime.now()
        terminal.log(f'User changed page to page number 1')
        url = request.form['id']
        used_headers = request.form['headers']
        
        share_store = request.form['share-store']
        share_content = request.form['share-content']
        share_method = request.form['share-method']
        
        if 'data:;base64,' in url:
            url_b64 = url.replace('data:;base64,', '')
            url_b64 = b64decode(url_b64)
            process_with_image = True
        
        try:
            if share_method == 'ready2go':
                if 'H&M' in share_store:
                    store_path = 'fashion_hm'
                elif 'Pull&Bear' in share_store:
                    store_path = 'fashion_pullbear'
                elif 'Bershka' in share_store:
                    store_path = 'fashion_bershka'
                elif 'Mango' in share_store:
                    store_path = 'fashion_mango'
                elif 'Zalando' in share_store:
                    store_path = 'fashion_zalando'
                elif 'Zara' in share_store:
                    storeName = 'Zara'
                    store_path = 'fashion_zara'
                elif 'Stradivarius' in share_store:
                    store_path = 'fashion_stradivarius'
                elif 'Ready2Go' in share_store:
                    store_path = 'ready2go'
                    
                used_file = f'{store_path}//women\\{share_content}.webp'
                file_index = forselectedItems.index(used_file)
                results = list(ready2go_results_list)[file_index][:10]
            else:
                if process_with_image:
                    results = model.process_file(url_b64, 1)
                else:
                    results = model.process(url, used_headers, 1)
            uploaded_img_path = url
            terminal.log(f'10 results found with input type: IMAGE and with gender: WOMEN')
            dev_mode(f'Results: {results}')
            model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, 'WOMEN', '')
            terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
            return render_template(f'pages/predict_page_1.html', share_method=share_method, share_store=share_store, share_content=share_content, recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID='', gender='WOMEN', uploaded_img=uploaded_img_path, headers=used_headers, display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])          
        except Exception as e:
            flash('Something went wrong, please try again!')
            return redirect('/')
        
    # Used to switch to the second page of the prediction
    @app.route('/predict/2', methods=['POST', 'GET'])
    def next_page():
        process_with_image = False
        start_time = datetime.datetime.now()
        terminal.log(f'User changed page to page number 2')
        url = request.form['id']
        used_headers = request.form['headers']
        
        if 'data:;base64,' in url:
            url_b64 = url.replace('data:;base64,', '')
            url_b64 = b64decode(url_b64)
            process_with_image = True
        
        share_store = request.form['share-store']
        share_content = request.form['share-content']
        share_method = request.form['share-method']
        try:
            if share_method == 'ready2go':
                if 'H&M' in share_store:
                    store_path = 'fashion_hm'
                elif 'Pull&Bear' in share_store:
                    store_path = 'fashion_pullbear'
                elif 'Bershka' in share_store:
                    store_path = 'fashion_bershka'
                elif 'Mango' in share_store:
                    store_path = 'fashion_mango'
                elif 'Zalando' in share_store:
                    store_path = 'fashion_zalando'
                elif 'Zara' in share_store:
                    storeName = 'Zara'
                    store_path = 'fashion_zara'
                elif 'Stradivarius' in share_store:
                    store_path = 'fashion_stradivarius'
                elif 'Ready2Go' in share_store:
                    store_path = 'ready2go'
                    
                used_file = f'{store_path}//women\\{share_content}.webp'
                file_index = forselectedItems.index(used_file)
                results = list(ready2go_results_list)[file_index][10:]
            else:
                if process_with_image:
                    results = model.process_file(url_b64, 2)
                else:
                    results = model.process(url, used_headers, 2)
            uploaded_img_path = url
            terminal.log(f'10 results found with input type: IMAGE and with gender: WOMEN')
            dev_mode(f'Results: {results}')
            model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, 'WOMEN', '')
            terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
            return render_template(f'pages/predict_page_2.html', share_method=share_method, share_store=share_store, share_content=share_content, recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID='', gender='WOMEN', uploaded_img=uploaded_img_path, headers=used_headers, display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])          
        except Exception as e:
            flash('Something went wrong, please try again!')
            return redirect('/')

# Used for the extension
class extension():
    # Used to show the results from the extension input
    @app.route('/extension', methods=['POST', 'GET'])
    @cross_origin(origin='*',headers=['Content- Type','Authorization'])
    def open_extension():
        if request.method == 'POST':
            start_time = datetime.datetime.now()
            url = request.form['url']
            used_headers = request.form['headers']
            userID = ' '
            gender = 'WOMEN'
            
            try:
                terminal.log(f'Programm started with input type: EXT')
                results = model.process(url, used_headers, 1)
                terminal.log(f'10 results found with input type: EXTENSION and with gender: {gender.upper()}')
                dev_mode(f'Results: {results}')
                uploaded_img_path = url
                model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, gender, userID)
                terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
                return render_template(f'pages/predict_page_1.html', recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID=userID, gender=gender.capitalize(), uploaded_img=uploaded_img_path, headers=headers, display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])          
            except Exception as e:
                flash('Something went wrong, please try again!')
                return redirect('/')
            
    # Used to extract the image from the extension input and return the image
    @app.route('/extensioninput', methods=['POST', 'GET'])
    @cross_origin(origin='*',headers=['Content- Type','Authorization'])
    def input_extension():
        link = request.form['link']
        userID = request.form['id']
        store = request.form['store']
        try:
            url, used_headers = extract_img.extract_img_from_link(link, store)
            img_data = {'url': url, 'headers': used_headers}
        except Exception as e:
            return 'Error'
        return img_data

# Used for the recommendation system
class recommend():
    # Used to get the recommended products with the given product number and return the images and links
    @app.route('/recommend', methods=['GET'])
    def recommend_products():
        data = request.args['number'].split(' ')
        number = data[0]
        store = data[1]
        imgs = []
        links = []
        terminal.log(f'Get the look with {number} from {store}')
        
        if store == 'Stradivarius':
            data = requests.get(f'https://api.empathybroker.com/search/v1/query/stradivarius/skusearch?q={number}&lang=nl&start=0&store=54009552&catalogue=50331084&warehouse=52110059&session=e5705e12-5521-5d65-5912-ff9e86d99a4f&user=4e3f7b10-53a4-b1c4-52ab-4c6855368d6a&scope=desktop&rows=5', headers=headers).content
            
            id = json.loads(data)['content']['docs'][0]['internal_id']
                
            data = requests.post('https://pro.api-mirror.wide-eyes.it/v2/RecommendById', data={"uid":f"{id}","country":"be"}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate", "apikey": "8379c292fcc467de39b5a2fe0c63bcb9feff0bdd"}).content
            colorId = number[-3:]
            data = json.loads(data)['results']
            for i in range(len(data)):
                imgs.append(data[i]['images'][0]['imageUrl'].replace('6_1_4', '1_1_1'))
                links.append(data[i]['productUrl'].replace('https://www.stradivarius.com/share/', 'https://www.stradivarius.com/be/'))
        elif store == 'Mango':
            product_data = requests.get(f'https://shop.mango.com/services/garments/{number[:-2]}/looktotal?color={number[-2:]}', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "stock-id": "017.NL.0.true.false.v4"}).content
            
            data = json.loads(product_data)['lookTotal']
            for i in range(len(data)):
                imgs.append(f"https://st.mngbcn.com/rcs/pics/static{data[i]['img']}")
                links.append(f"https://shop.mango.com{data[i]['url']}")
        elif store == 'River':
            product_data = requests.post(f'https://api.riverisland.com/graphql', json={"operationName":"styleWith","variables":{"productId":number,"countryCode":"BE","currencyCode":"EUR","crossSellType":"StyleWith","slotCount":4},"query":"fragment CollectionFields on Collection {\n  id\n  products {\n    displayName\n    productId\n    productPageUrl\n    images {\n      url\n      type\n      __typename\n    }\n    priceInfo {\n      currency\n      currencyCode\n      prices {\n        name\n        formattedValue\n        value\n        __typename\n      }\n      __typename\n    }\n    swatchInfo {\n      hasSwatches\n      swatchCount\n      swatchItems {\n        imgSrc\n        webColour\n        swatchColour\n        productPageUrl\n        productId\n        __typename\n      }\n      __typename\n    }\n    trackingCategoriesInfo {\n      categories\n      __typename\n    }\n    attributes {\n      colour\n      __typename\n    }\n    hasPriceRange\n    trackingCategoriesInfo {\n      categories\n      __typename\n    }\n    variants {\n      inventoryQuantity\n      __typename\n    }\n    attributes {\n      colour\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CrossSellsFields on CrossSells {\n  slots {\n    collection\n    __typename\n  }\n  __typename\n}\n\nquery styleWith($productId: String!, $countryCode: String!, $currencyCode: String!, $crossSellType: String!, $slotCount: Int!) {\n  styleWith(\n    productId: $productId\n    countryCode: $countryCode\n    currencyCode: $currencyCode\n    crossSellType: $crossSellType\n    slotCount: $slotCount\n  ) {\n    ... on StyleWith {\n      id\n      crossSells {\n        ...CrossSellsFields\n        __typename\n      }\n      collections {\n        ...CollectionFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}).content
            
            
            data = json.loads(product_data)['data']
            slots = data['styleWith']['crossSells'][0]['slots']
            collection_numbers = []
                
            for slot in slots:
                collection_numbers.append(slot['collection'])
                
            for number in collection_numbers:
                products = data['styleWith']['collections'][number-1]['products']
                product = random.choice(products)
                imgs.append(product['images'][1]['url'])
                links.append(f"https://www.riverisland.com{product['productPageUrl']}")
        elif store == 'Bershka':
            data = requests.post(f'https://2kv2lbqg6e-dsn.algolia.net/1/indexes/pro_SEARCH_NL/query?', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "x-algolia-agen": "Algolia for JavaScript (3.35.1); Browser", "x-algolia-application-id": "2KV2LBQG6E", "x-algolia-api-key": "MGY4YzYzZWI2ZmRlYmYwOTM1ZGU2NGI3MjVjZjViMjgyMDIyYWM3NWEzZTM5ZjZiOWYwMzAyYThmNTkxMDUwMGF0dHJpYnV0ZXNUb0hpZ2hsaWdodD0lNUIlNUQmYXR0cmlidXRlc1RvU25pcHBldD0lNUIlNUQmZW5hYmxlUGVyc29uYWxpemF0aW9uPWZhbHNlJmVuYWJsZVJ1bGVzPXRydWUmZmFjZXRpbmdBZnRlckRpc3RpbmN0PXRydWUmZ2V0UmFua2luZ0luZm89dHJ1ZSZzbmlwcGV0RWxsaXBzaXNUZXh0PSVFMiU4MCVBNiZzdW1PckZpbHRlcnNTY29yZXM9dHJ1ZQ=="}, json={"query": number, "analyticsTags": ["dweb","country_nl","lang_nl","wmen","no_teen","season","store"], "clickAnalytics": "false", "hitsPerPage": "36", "ruleContexts": ["dweb","country_nl","lang_nl","wmen","wmen_nl"], "attributesToRetrieve": ["pElement"], "facets": ["mainCategory"], "filter":"", "page": "0"}).content

            product_id = json.loads(data)['hits'][0]['pElement']    
            
            product_data = requests.get(f'https://www.bershka.com/itxrest/3/catalog/store/44009503/40259546/productsArray?productIds={product_id}&languageId=100', headers=headers).content

            product_id = json.loads(product_data)['products'][0]['bundleProductSummaries'][0]['id']    
                
            product_data = requests.get(f'https://www.bershka.com/itxrest/2/catalog/store/44009503/40259546/category/0/product/{product_id}/relatedProducts?languageId=100', headers=headers).content
            
            products = json.loads(product_data)['relatedProducts']
                
            for product in products:
                path = product['xmedia'][0]['path']
                start = path.find('p/')
                number = path[start+2:].replace('/', '')
                imgs.append(f"https://static.bershka.net/4/photos2/{path}/{number}_1_1_1.jpg?")
                        
                links.append(f"https://www.bershka.com/nl/{product['productUrl']}")
            
        if len(imgs) == 0:
            response = {'result': 'No results found'}
            response = json.dumps(response, indent = 4) 
            return response
        elif len(imgs) == 1:
            response = {'result': {'img':[imgs[0]], 'link':[links[0]]}}
            response = json.dumps(response, indent = 4) 
            return response
        elif len(imgs) == 2:
            response = {'result': {'img':[imgs[0], imgs[1]], 'link':[links[0], links[1]]}}
            response = json.dumps(response, indent = 4) 
            return response
        elif len(imgs) == 3:
            response = {'result': {'img':[imgs[0], imgs[1], imgs[2]], 'link':[links[0], links[1], links[2]]}}
            response = json.dumps(response, indent = 4) 
            return response
        
        response = {'result': {'img':[imgs[0], imgs[1], imgs[2], imgs[3]], 'link':[links[0], links[1], links[2], links[3]]}}
        response = json.dumps(response, indent = 4) 
        return response
    
    # Used to check if there are recommended products available for a specific product
    def recommend_check(userID, number, store):        
        if store == 'Stradivarius':
            data = requests.get(f'https://api.empathybroker.com/search/v1/query/stradivarius/skusearch?q={number}&lang=nl&start=0&store=54009552&catalogue=50331084&warehouse=52110059&session=e5705e12-5521-5d65-5912-ff9e86d99a4f&user=4e3f7b10-53a4-b1c4-52ab-4c6855368d6a&scope=desktop&rows=5', headers=headers).content

            try:
                id = json.loads(data)['content']['docs'][0]['internal_id']
            except:
                return False
                
            data = requests.post('https://pro.api-mirror.wide-eyes.it/v2/RecommendById', data={"uid":f"{id}","country":"be"}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate", "apikey": "8379c292fcc467de39b5a2fe0c63bcb9feff0bdd"}).content
            
            colorId = number[-3:]
            try:
                data = json.loads(data)['results']     
                return True
            except:
                return False        
        elif store == 'Mango':
            product_data = requests.get(f'https://shop.mango.com/services/garments/{number[:-2]}/looktotal?color={number[-2:]}', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "stock-id": "017.NL.0.true.false.v4"}).content
            
            try:
                data = json.loads(product_data)['lookTotal']
            except:
                return False
            if len(data) == 0:
                return False
            return True
        elif store == 'River Island':
            product_data = requests.post(f'https://api.riverisland.com/graphql', json={"operationName":"styleWith","variables":{"productId":number,"countryCode":"BE","currencyCode":"EUR","crossSellType":"StyleWith","slotCount":4},"query":"fragment CollectionFields on Collection {\n  id\n  products {\n    displayName\n    productId\n    productPageUrl\n    images {\n      url\n      type\n      __typename\n    }\n    priceInfo {\n      currency\n      currencyCode\n      prices {\n        name\n        formattedValue\n        value\n        __typename\n      }\n      __typename\n    }\n    swatchInfo {\n      hasSwatches\n      swatchCount\n      swatchItems {\n        imgSrc\n        webColour\n        swatchColour\n        productPageUrl\n        productId\n        __typename\n      }\n      __typename\n    }\n    trackingCategoriesInfo {\n      categories\n      __typename\n    }\n    attributes {\n      colour\n      __typename\n    }\n    hasPriceRange\n    trackingCategoriesInfo {\n      categories\n      __typename\n    }\n    variants {\n      inventoryQuantity\n      __typename\n    }\n    attributes {\n      colour\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CrossSellsFields on CrossSells {\n  slots {\n    collection\n    __typename\n  }\n  __typename\n}\n\nquery styleWith($productId: String!, $countryCode: String!, $currencyCode: String!, $crossSellType: String!, $slotCount: Int!) {\n  styleWith(\n    productId: $productId\n    countryCode: $countryCode\n    currencyCode: $currencyCode\n    crossSellType: $crossSellType\n    slotCount: $slotCount\n  ) {\n    ... on StyleWith {\n      id\n      crossSells {\n        ...CrossSellsFields\n        __typename\n      }\n      collections {\n        ...CollectionFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}).content
            
            try:
                data = json.loads(product_data)['data']
                slots = data['styleWith']['crossSells'][0]['slots']
            except:
                return False
            if len(data) == 0:
                return False
            return True
        elif store == 'Bershka':
            data = requests.post(f'https://2kv2lbqg6e-dsn.algolia.net/1/indexes/pro_SEARCH_NL/query?', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "x-algolia-agen": "Algolia for JavaScript (3.35.1); Browser", "x-algolia-application-id": "2KV2LBQG6E", "x-algolia-api-key": "MGY4YzYzZWI2ZmRlYmYwOTM1ZGU2NGI3MjVjZjViMjgyMDIyYWM3NWEzZTM5ZjZiOWYwMzAyYThmNTkxMDUwMGF0dHJpYnV0ZXNUb0hpZ2hsaWdodD0lNUIlNUQmYXR0cmlidXRlc1RvU25pcHBldD0lNUIlNUQmZW5hYmxlUGVyc29uYWxpemF0aW9uPWZhbHNlJmVuYWJsZVJ1bGVzPXRydWUmZmFjZXRpbmdBZnRlckRpc3RpbmN0PXRydWUmZ2V0UmFua2luZ0luZm89dHJ1ZSZzbmlwcGV0RWxsaXBzaXNUZXh0PSVFMiU4MCVBNiZzdW1PckZpbHRlcnNTY29yZXM9dHJ1ZQ=="}, json={"query": number, "analyticsTags": ["dweb","country_nl","lang_nl","wmen","no_teen","season","store"], "clickAnalytics": "false", "hitsPerPage": "36", "ruleContexts": ["dweb","country_nl","lang_nl","wmen","wmen_nl"], "attributesToRetrieve": ["pElement"], "facets": ["mainCategory"], "filter":"", "page": "0"}).content

            try:
                product_id = json.loads(data)['hits'][0]['pElement']    
            except:
                return False
            
            product_data = requests.get(f'https://www.bershka.com/itxrest/3/catalog/store/44009503/40259546/productsArray?productIds={product_id}&languageId=100', headers=headers).content

            try:
                product_id = json.loads(product_data)['products'][0]['bundleProductSummaries'][0]['id']    
            except:
                return False
                
            product_data = requests.get(f'https://www.bershka.com/itxrest/2/catalog/store/44009503/40259546/category/0/product/{product_id}/relatedProducts?languageId=100', headers=headers).content
            
            try:
                products = json.loads(product_data)['relatedProducts']
            except:
                return False
            if len(products) == 0:
                return False
            return True

# Used when dev_mode is enabled
def dev_mode(mess):
    if dev_status:
        terminal.log(f'{mess}')        

# Used to get the random images for the Ready2Go feature
def get_ramdom_img():
    picked_items =  random.sample(range(len(forselectedItems)), 20)
    results = [forselectedItems[i] for i in picked_items]
    product_img = []
    product_links = []
    product_numbers = []
    stores = []
    count = 1
    for result in results:
        if 'fashion_hm' in result:
            storeName = 'H&M'
            store_path = 'fashion_hm'
        elif 'fashion_pullbear' in result:
            storeName = 'Pull&Bear'
            store_path = 'fashion_pullbear'
        elif 'fashion_bershka' in result:
            storeName = 'Bershka'
            store_path = 'fashion_bershka'
        elif 'fashion_mango' in result:
            storeName = 'Mango'
            store_path = 'fashion_mango'
        elif 'fashion_newyorker' in result:
            storeName = 'New Yorker'
            store_path = 'fashion_newyorker'
        elif 'fashion_zalando' in result:
            storeName = 'Zalando'
            store_path = 'fashion_zalando'
        elif 'fashion_zara' in result:
            storeName = 'Zara'
            store_path = 'fashion_zara'
        elif 'fashion_mostwanted' in result:
            storeName = 'Most Wanted'
            store_path = 'fashion_mostwanted'
        elif 'fashion_we' in result:
            storeName = 'WE'
            store_path = 'fashion_we'
        elif 'fashion_stradivarius' in result:
            storeName = 'Stradivarius'
            store_path = 'fashion_stradivarius'
        elif 'ready2go' in result:
            storeName = 'Ready2Go'
            store_path = 'ready2go'
        path = result
        start = os.path.splitext(path)[0].find('\\')
        file_name = os.path.splitext(
            path)[0][start+1:] + os.path.splitext(path)[1]
        link = ''
        product_links.append(f'href={link}')
    
        if storeName != 'Most Wanted':
            stores.append(storeName)
        else:
            stores.append('WM')
        product_numbers.append(file_name[:-5])
        product_img.append(f'{store_path}/women/{file_name}')
        count += 1

    return product_links, product_numbers, stores, product_img

# Used to get the link of the product
def get_link(number, storeName, zara_model_img_status):
    if storeName == 'H&M':
        return f'https://www.hm.com/productpage.{number}.html'
    elif storeName == 'Pull&Bear':
        return f'https://www.pullandbear.com/be/en/-l0{number[:-3]}?cS={number[-3:]}'
    elif storeName == 'Bershka':
        product_data = requests.post(f'https://2kv2lbqg6e-dsn.algolia.net/1/indexes/pro_SEARCH_NL/query?', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "x-algolia-agen": "Algolia for JavaScript (3.35.1); Browser", "x-algolia-application-id": "2KV2LBQG6E", "x-algolia-api-key": "MGY4YzYzZWI2ZmRlYmYwOTM1ZGU2NGI3MjVjZjViMjgyMDIyYWM3NWEzZTM5ZjZiOWYwMzAyYThmNTkxMDUwMGF0dHJpYnV0ZXNUb0hpZ2hsaWdodD0lNUIlNUQmYXR0cmlidXRlc1RvU25pcHBldD0lNUIlNUQmZW5hYmxlUGVyc29uYWxpemF0aW9uPWZhbHNlJmVuYWJsZVJ1bGVzPXRydWUmZmFjZXRpbmdBZnRlckRpc3RpbmN0PXRydWUmZ2V0UmFua2luZ0luZm89dHJ1ZSZzbmlwcGV0RWxsaXBzaXNUZXh0PSVFMiU4MCVBNiZzdW1PckZpbHRlcnNTY29yZXM9dHJ1ZQ=="}, json={"query": number, "analyticsTags": ["dweb","country_nl","lang_nl","wmen","no_teen","season","store"], "clickAnalytics": "false", "hitsPerPage": "36", "ruleContexts": ["dweb","country_nl","lang_nl","wmen","wmen_nl"], "attributesToRetrieve": ["pElement"], "facets": ["mainCategory"], "filter":"", "page": "0"}).content
                    
        try:
            product_id = json.loads(product_data)['hits'][0]['pElement']
            data = requests.get(f'https://www.bershka.com/itxrest/3/catalog/store/44009503/40259546/productsArray?productIds={product_id}%2C106465680%2C106185120%2C103578123%2C103646838&languageId=100', headers=headers).content

            product_url = json.loads(data)['products'][0]['name'].replace(' ', '-')
        except Exception as e:
            return f'https://www.bershka.com/nl/q/{number}'
        return f'https://www.bershka.com/nl/{product_url}-c0p{product_id}.html?colorId={number[-3:]}'
    elif storeName == 'New Yorker':
        return f'https://www.newyorker.de/nl/products/#/detail/{number}/001'
    elif storeName == 'Mango':
        product_data = requests.get(f'https://shop.mango.com/services/garments/{number}', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "stock-id": "017.NL.0.true.false.v4"}).content

        product_data = json.loads(product_data)
        canonicalUrl = 'canonicalUrl'
        
        try:
            temp = product_data[canonicalUrl]
            return f'https://shop.mango.com{product_data[canonicalUrl]}?c={number[-2:]}'
        except:       
            return f'https://www.google.be/search?q={storeName}+{number}'
    elif storeName == 'Zara':
        if zara_model_img_status:
            return f'https://www.zara.com/be/nl/-p0{number}.html'
        else:
            return f'https://www.zara.com/be/nl/search?searchTerm={number}'
    elif storeName == 'Most Wanted':
        return f'https://www.mostwantednl.nl/catalogsearch/result/?q={number}'
    elif storeName == 'WE':
        end = number.find('_')
        return f'https://www.wefashion.be/nl_BE/-{number[:end]}.html?dwvar_{number[:end]}_color={number[end+1:]}'
    elif storeName == 'Stradivarius':
        search_data = requests.get(f'https://api.empathybroker.com/search/v1/query/stradivarius/skusearch?q={number[:-3]}&lang=nl&start=0&store=54009552&catalogue=50331084&warehouse=52110059', headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "stock-id": "017.NL.0.true.false.v4"}).content
        
        search_data = json.loads(search_data)
            
        try:
            link = f'https://www.stradivarius.com/be/-c0p{search_data["content"]["docs"][0]["productId"]}.html?colorId={number[-3:]}'
        except:
            link = f'https://www.google.be/search?q={storeName}+{number}'
            
        return link
    elif storeName == 'Zalando':
        return f'https://www.zalando.be/dames/?q={number}'
    elif storeName == 'Weekday':
        product_data = requests.get(f"https://photorankapi-a.akamaihd.net/customers/219461/streams/bytag/{number}?auth_token=36250991614184b2b35282b4efc7de904d5f0fbf01936e8a65006fc56dd969c4&wrap_responses=1&version=v2.2", headers=headers).content
        
        product_data = json.loads(product_data)
            
        try: 
            return product_data['data']['product_url']
        except:
            return f'https://www.weekday.com/en_eur/search.html?q={number}'
    elif storeName == 'River Island':
        return f'https://www.riverisland.com/p/-{number}'
    else:
        return ''
                
# Used to get the the store name and use it in the get_model_image class
def get_model_store(storeName, number):
    if storeName == 'H&M':
        url = get_model_image.hm(number)
    elif storeName == 'Mango':
        url = get_model_image.mango(number)
    elif storeName == 'New Yorker':
        url = get_model_image.newyorker(number)
    elif storeName == 'Zara':
        url = get_model_image.zara(number)
    elif storeName == 'Pull&Bear':
        url = get_model_image.pullbear(number)
    elif storeName == 'Stradivarius':
        url = get_model_image.stradivarius(number)
    elif storeName == 'Bershka':
        url = get_model_image.bershka(number)
    elif storeName == 'WE':
        url = get_model_image.we(number)
    elif storeName == 'Weekday':
        url = get_model_image.weekday(number)
    elif storeName == 'Zalando':
        url = get_model_image.zalando(number)
    elif storeName == 'River Island':
        url = get_model_image.riverisland(number)
    return url

# Used to process the results (get the product image, product link, product number, store name, recommended avaible)
def process_output(results, gender, userID):
    model_img = []
    product_img = []
    product_links = []
    product_numbers = []
    stores = []
    recommended_avaible = []
    count = 1
    for result in results:
        result = result.replace('.jpg', '.webp')
        if 'fashion_hm' in result:
            storeName = 'H&M'
            store_path = 'fashion_hm'
        elif 'fashion_pullbear' in result:
            storeName = 'Pull&Bear'
            store_path = 'fashion_pullbear'
        elif 'fashion_bershka' in result:
            storeName = 'Bershka'
            store_path = 'fashion_bershka'
        elif 'fashion_mango' in result:
            storeName = 'Mango'
            store_path = 'fashion_mango'
        elif 'fashion_newyorker' in result:
            storeName = 'New Yorker'
            store_path = 'fashion_newyorker'
        elif 'fashion_zalando' in result:
            storeName = 'Zalando'
            store_path = 'fashion_zalando'
        elif 'fashion_zara' in result:
            storeName = 'Zara'
            store_path = 'fashion_zara'
        elif 'fashion_mostwanted' in result:
            storeName = 'Most Wanted'
            store_path = 'fashion_mostwanted'
        elif 'fashion_weekday' in result:
            storeName = 'Weekday'
            store_path = 'fashion_weekday'
        elif 'fashion_we' in result:
            storeName = 'WE'
            store_path = 'fashion_we'
        elif 'fashion_stradivarius' in result:
            storeName = 'Stradivarius'
            store_path = 'fashion_stradivarius'
        elif 'fashion_riverisland' in result:
            storeName = 'River Island'
            store_path = 'fashion_riverisland'
        
        zara_model_img_status = True
        path = result
        start = os.path.splitext(path)[0].find('\\')
        file_name = os.path.splitext(path)[0][start+1:] + os.path.splitext(path)[1]
        if storeName != 'Most Wanted' and storeName != 'New Yorker' and storeName != 'Stradivarius':
            modelUrl = get_model_store(storeName, file_name[:-5])
            try:
                reqstatus = requests.get(modelUrl, headers=headers).status_code
                if reqstatus == 200:
                    model_img.append(modelUrl)
                elif storeName == 'Zara':
                    zara_model_img_status = False
                    model_img.append(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{file_name[:-5]}.webp')
                else:
                    model_img.append(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{file_name[:-5]}.webp')
            except Exception as e:
                model_img.append(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{file_name[:-5]}.webp')
        else:
            if storeName == 'Stradivarius':
                    
                number = file_name[:-5]
                req = requests.get(f'https://static.e-stradivarius.net/5/photos3/2022/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:10]}/{number}_1_1_2.jpg', headers=headers)
                req_2023 = requests.get(f'https://static.e-stradivarius.net/5/photos3/2023/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:10]}/{number}_1_1_2.jpg', headers=headers)
                
                if req.status_code == 200:
                    model_img.append(f'https://static.e-stradivarius.net/5/photos3/2022/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:10]}/{number}_1_1_2.jpg')
                elif req_2023.status_code == 200:
                    model_img.append(f'https://static.e-stradivarius.net/5/photos3/2023/I/0/1/p/{number[:4]}/{number[4:7]}/{number[7:10]}/{number}_1_1_2.jpg')
                else:
                    model_img.append(f'https://static.e-stradivarius.net/5/photos3/2022/V/0/1/p/{number[:4]}/{number[4:7]}/{number[7:10]}/{number}_1_1_2.jpg')
            else:
                model_img.append(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{file_name[:-5]}.webp')
        
        if storeName == 'Stradivarius' or storeName == 'Mango' or storeName == 'River Island' or storeName == 'Bershka':
            recommended_avaible.append(recommend.recommend_check(userID, file_name[:-5], storeName))
        else:
            recommended_avaible.append(False)
        
        link = get_link(file_name[:-5], storeName, zara_model_img_status)
        product_links.append(f'href={link}')
    
        if storeName != 'Most Wanted':
            stores.append(storeName)
        else:
            stores.append('WM')

        product_numbers.append(file_name[:-5])
        product_img.append(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{file_name[:-5]}.webp')
        
        count += 1
    
    try:
        os.remove(f'bin\\{userID}.json')
    except:
        pass
    try:
        os.remove(f'bin\\{userID}.html')
    except:
        pass
    return model_img, product_img, product_links, stores, product_numbers, recommended_avaible

# This function is the main function of the app, it processes the input and returns the output
@app.route('/predict/', methods=['POST', 'GET'])
def predict():
    start_time = datetime.datetime.now()
    
    if request.method == 'POST':
        if request.form['UserID'] == '':
            flash('Please agree to the terms and conditions.')
            terminal.error(f'The user did\'t agree to the terms')
            product_links, product_numbers, stores, product_img = get_ramdom_img()    
            return redirect('/')
        if 'file' not in request.files:
            userID = request.form['UserID']
            if 'forselected-input' in request.form:
                request_content = request.form['forselected-input'].split(' ')
                store = request_content[0]
                number = request_content[1]
                if 'H&M' in store:
                    store_path = 'fashion_hm'
                elif 'Pull&Bear' in store:
                    store_path = 'fashion_pullbear'
                elif 'Bershka' in store:
                    store_path = 'fashion_bershka'
                elif 'Mango' in store:
                    store_path = 'fashion_mango'
                elif 'Zalando' in store:
                    store_path = 'fashion_zalando'
                elif 'Zara' in store:
                    storeName = 'Zara'
                    store_path = 'fashion_zara'
                elif 'Stradivarius' in store:
                    store_path = 'fashion_stradivarius'
                elif 'Ready2Go' in store:
                    store_path = 'ready2go'
                    
                share_method = 'ready2go'
                share_store = store
                share_content = number
                
                used_file = f'{store_path}//women\\{number}.webp'
                file_index = forselectedItems.index(used_file)
                results = list(ready2go_results_list)[file_index][:10]
                
                url = f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{number}.webp'
                terminal.log(f'Programm started with given input')
                terminal.log(f'10 results found with input type: Ready2Go images')
                dev_mode(f'Results: {results}')
                uploaded_img_path = url
                model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, 'WOMEN', userID)
                terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
                return render_template('pages/predict_page_1.html', share_method=share_method, share_store=share_store, share_content=share_content, recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID=userID, gender='Women', uploaded_img=uploaded_img_path, headers='', display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])
            else:
                gender = 'Women'
                inputType = 'Ready2Go images'
                pass
            if 'link' in request.form:
                request_content_link = request.form['link']
                terminal.log(f'Extracting image with link ({request_content_link}) and store ({request.form["store"]})')
                inputType = 'LINK'
                share_content = request_content_link
                share_store = request.form['store']
                share_method = 'link'
                try:
                    url, used_headers = extract_img.extract_img_from_link(request_content_link, request.form['store'])
                except Exception as e:         
                    product_links, product_numbers, stores, product_img = get_ramdom_img()
                    flash('Product not found. Try with another link or store.')
                    terminal.error(f'An error accured when extracting image with as input type {inputType}: {e}')
                    return redirect('/')   
                if url == None:
                    product_links, product_numbers, stores, product_img = get_ramdom_img()
                    flash('Link doesn\'t contain an image. Try with another link.')
                    terminal.error(f'An error accured when extracting image with as input type {inputType}')
                    return redirect('/') 
            else:
                terminal.log(f'Extracting image with number ({request.form["number"]}) and store ({request.form["store"]})')
                inputType = 'NUMBER'
                try:
                    gender = 'woman'
                    url, used_headers = extract_img.extract_img_from_number(request.form['number'], request.form['store'] , userID, gender)
                    share_content = request.form['number']
                    share_store = request.form['store']
                    share_method = 'number'
                except Exception as e:
                    product_links, product_numbers, stores, product_img = get_ramdom_img()    
                    flash('Product not found. Try with another number or store.')
                    terminal.error(f'An error accured when extracting image with as input type {inputType}: {e}')
                    return redirect('/') 
            try:
                gender = 'WOMEN'
                terminal.log(f'Programm started with given input')
                results = model.process(url, used_headers, 1)
                terminal.log(f'10 results found with input type: {inputType} and with gender: {gender.upper()}')
                dev_mode(f'Results: {results}')
                uploaded_img_path = url
                model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, gender, userID)
                terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
                return render_template('pages/predict_page_1.html', share_method=share_method, share_store=share_store, share_content=share_content, recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID=userID, gender=gender.capitalize(), uploaded_img=uploaded_img_path, headers=used_headers, display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])
            except Exception as e:    
                product_links, product_numbers, stores, product_img = get_ramdom_img()    
                flash('Product not found. Try with another input type.')
                terminal.error(f'An error accured when using input type {inputType}: {e}')
                return redirect('/')  
        else:
            terminal.log(f'Extracting uploaded image')
            try:
                userID = request.form['UserID']
                file = request.files['file'].read()
                uploaded_img_path = f"data:;base64,{b64encode(file).decode('utf-8')}"
                gender = 'WOMEN'
                terminal.log(f'Programm started with given input')
                results = model.process_file(file, 1)
                terminal.log(f'10 results found with input type: IMAGE and with gender: {gender.upper()}')
                dev_mode(f'Results: {results}')
                model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, gender, userID)
                terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
                return render_template('pages/predict_page_1.html', share_method='', share_store='', share_content='', recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID=userID, gender=gender.capitalize(), uploaded_img=uploaded_img_path, display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])          
            except Exception as e:
                flash('An error occurred: one result could not be found')
                terminal.error(f'An error accured: {e}')
                product_links, product_numbers, stores, product_img = get_ramdom_img()    
                return redirect('/') 
    else:      
        userID = request.args['UserID']
        if 'forselected-input' in request.args:
            request_content = request.args['forselected-input'].split(' ')
            store = request_content[0]
            number = request_content[1]
            if 'H&M' in store:
                store_path = 'fashion_hm'
            elif 'Pull&Bear' in store:
                store_path = 'fashion_pullbear'
            elif 'Bershka' in store:
                store_path = 'fashion_bershka'
            elif 'Mango' in store:
                store_path = 'fashion_mango'
            elif 'Zalando' in store:
                store_path = 'fashion_zalando'
            elif 'Zara' in store:
                storeName = 'Zara'
                store_path = 'fashion_zara'
            elif 'Stradivarius' in store:
                store_path = 'fashion_stradivarius'
            elif 'Ready2Go' in store:
                store_path = 'ready2go'
                
            share_method = 'ready2go'
            share_store = store
            share_content = number
                
            used_file = f'{store_path}//women\\{number}.webp'
            file_index = forselectedItems.index(used_file)
            results = list(ready2go_results_list)[file_index][:10]
            
            url = f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/{store_path}/women/{number}.webp'
            terminal.log(f'Programm started with given input')
            terminal.log(f'10 results found with input type: Ready2Go images')
            dev_mode(f'Results: {results}')
            uploaded_img_path = url
            model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, 'WOMEN', userID)
            terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
            return render_template('pages/predict_page_1.html', share_method=share_method, share_store=share_store, share_content=share_content, recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID=userID, gender='Women', uploaded_img=uploaded_img_path, headers=used_headers, display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])
        else:
            gender = 'Women'
            inputType = 'Ready2Go images'
            pass
        if 'link' in request.args:
            request_content_link = request.args['link']
            terminal.log(f'Extracting image with link ({request_content_link}) and store ({request.args["store"]})')
            inputType = 'LINK'
            share_content = request_content_link
            share_store = request.args['store']
            share_method = 'link'
            try:
                url, used_headers = extract_img.extract_img_from_link(request_content_link, request.args['store'])
            except Exception as e:         
                product_links, product_numbers, stores, product_img = get_ramdom_img()
                flash('Product not found. Try with another link or store.')
                terminal.error(f'An error accured when extracting image with as input type {inputType}: {e}')
                return redirect('/')    
        else:
            terminal.log(f'Extracting image with number ({request.args["number"]}) and store ({request.args["store"]})')
            inputType = 'NUMBER'
            try:
                gender = 'woman'
                url, used_headers = extract_img.extract_img_from_number(request.args['number'], request.args['store'] , userID, gender)
                share_content = request.args['number']
                share_store = request.args['store']
                share_method = 'number'
            except Exception as e:
                product_links, product_numbers, stores, product_img = get_ramdom_img()    
                flash('Product not found. Try with another number or store.')
                terminal.error(f'An error accured when extracting image with as input type {inputType}: {e}')
                return redirect('/') 
        try:
            gender = 'WOMEN'
            terminal.log(f'Programm started with given input')
            results = model.process(url, used_headers, 1)
            terminal.log(f'10 results found with input type: Share and with gender: {gender.upper()}')
            dev_mode(f'Results: {results}')
            files = os.listdir('uploads')
            uploaded_img_path = url
            model_img, product_img, product_links, stores, product_numbers, recommended_avaible = process_output(results, gender, userID)
            terminal.log(f'Programm ended succesfully in {(datetime.datetime.now() - start_time).total_seconds()} seconds')
            return render_template('pages/predict_page_1.html', share_method=share_method, share_store=share_store, share_content=share_content, recommend_avaible_1=recommended_avaible[0], recommend_avaible_2=recommended_avaible[1], recommend_avaible_3=recommended_avaible[2], recommend_avaible_4=recommended_avaible[3], recommend_avaible_5=recommended_avaible[4], recommend_avaible_6=recommended_avaible[5], recommend_avaible_7=recommended_avaible[6], recommend_avaible_8=recommended_avaible[7], recommend_avaible_9=recommended_avaible[8], recommend_avaible_10=recommended_avaible[9], UserID=userID, gender=gender.capitalize(), uploaded_img=uploaded_img_path, headers=used_headers, display_status='style=display:none', product_link_1=product_links[0], product_number_1=product_numbers[0], product_store_1=stores[0], product_model_img_1=model_img[0], product_img_1=product_img[0], product_link_2=product_links[1], product_number_2=product_numbers[1], product_store_2=stores[1], product_model_img_2=model_img[1], product_img_2=product_img[1], product_link_3=product_links[2], product_number_3=product_numbers[2], product_store_3=stores[2], product_model_img_3=model_img[2], product_img_3=product_img[2], product_link_4=product_links[3], product_number_4=product_numbers[3], product_store_4=stores[3], product_model_img_4=model_img[3], product_img_4=product_img[3], product_link_5=product_links[4], product_number_5=product_numbers[4], product_store_5=stores[4], product_model_img_5=model_img[4], product_img_5=product_img[4], product_link_6=product_links[5], product_number_6=product_numbers[5], product_store_6=stores[5], product_model_img_6=model_img[5], product_img_6=product_img[5], product_link_7=product_links[6], product_number_7=product_numbers[6], product_store_7=stores[6], product_model_img_7=model_img[6], product_img_7=product_img[6], product_link_8=product_links[7], product_number_8=product_numbers[7], product_store_8=stores[7], product_model_img_8=model_img[7], product_img_8=product_img[7], product_link_9=product_links[8], product_number_9=product_numbers[8], product_store_9=stores[8], product_model_img_9=model_img[8], product_img_9=product_img[8], product_link_10=product_links[9], product_number_10=product_numbers[9], product_store_10=stores[9], product_model_img_10=model_img[9], product_img_10=product_img[9])
        except Exception as e:    
            product_links, product_numbers, stores, product_img = get_ramdom_img()    
            flash('Product not found. Try with another input type.')
            terminal.error(f'An error accured when using input type {inputType}: {e}')
            return redirect('/')  
               
# This is called when you run `python app.py` from the terminal (THIS IS NOT USED ANYMORE, I LEFT IT HERE FOR REFERENCE)              
#parser = ArgumentParser()
#parser.add_argument('-dev', '--dev-mode', action='store_true', help='Enable dev mode')
#parser.add_argument('-reset', '--reset', action='store_true', help='Reset all users')
#args = parser.parse_args()
#dev_status = args.dev_mode
#if dev_status == True:
#    dev_mode('Dev mode enabled')
#    model.initialize_model(True)
#else:
#    model.initialize_model(False)
#reset_status = args.reset

# This is called when you run `python app.py` from the terminal (THIS IS NOT USED IN PRODUCTION)
if __name__ == '__main__':
    app.secret_key = 'FR6545'
    app.config['SESSION_TYPE'] = 'APPLICATION'
    if __name__ == '__main__':
        model.initialize_model(True)
    else:
        model.initialize_model(False)
        
    cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=['Access-Control-Allow-Origin'])
    app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    print('Server started')
    app.run(host="0.0.0.0", threaded=True, port=5000)