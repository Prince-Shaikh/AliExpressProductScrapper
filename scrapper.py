import csv,time
from requests_html import HTMLSession
session = HTMLSession()
products_list = []
import requests
import json
import re
target = ["imagePath"]
def request(requests_url):
    rr = session.get(requests_url)
    rr.html.render(scrolldown=5,timeout=30,sleep=3)
    products = rr.html.find('.list-items',first=True)
    return products
def extract_data(items):
    indivisual_items = items.find('.list-item')
    for list_item in indivisual_items:
        product_title = list_item.find('.item-title-wrap',first=True).text
        product_url = ""
        for link in list_item.find('.item-title-wrap',first=True).absolute_links:
            product_url = link
            r = requests.get(product_url)
            match = re.search(r'data: ({.+})', r.text).group(1)
            data = json.loads(match)
            goal = [data['pageModule'][x] for x in target]
            print(goal[0])
            break
        product_price = list_item.find('.price-current',first=True).text

        #url = goal.get('imagePath')
        data = {'product_title': product_title, 'product_url': product_url, 'price': product_price, 'url': goal[0]}
        products_list.append(data)
def create_csv():
    csv_columns = ['product_title', 'product_url', 'price', 'url']
    csv_file = "products.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in products_list:
                writer.writerow(data)
    except IOError:
        print("I/O error")
page_url = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=apple'
#page_url = input("Enter Aliexpress search page url: ")
print("Extracting data...")
page = 1
while True:
    try:
        page_url = page_url+f'&page={page}'
        products_data = request(page_url)
        extract_data(products_data)
        page = +1
        print(str(len(products_list))+" items extracted!")
        time.sleep(3)
    except:
        break
create_csv()
