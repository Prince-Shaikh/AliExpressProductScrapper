import csv,time
from requests_html import HTMLSession
session = HTMLSession()

products_list = []
#page_url = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=headphones'

def request(requests_url):
    r = session.get(requests_url)
    r.html.render(scrolldown=5,timeout=30,sleep=3)
    products = r.html.find('.list-items',first=True)
    return products

def extract_data(items):
    indivisual_items = items.find('.list-item')

    for list_item in indivisual_items:
        product_title = list_item.find('.item-title-wrap',first=True).text
        product_url = ""
        for link in list_item.find('.item-title-wrap',first=True).absolute_links:
            product_url = link
            break

        product_price = list_item.find('.price-current',first=True).text

        try:
            product_rating = float(list_item.find('.rating-value',first=True).text)
        except:
            product_rating = 0

        try:
            pieces_sold = list_item.find('.sale-value-link',first=True).text
            pieces_sold = pieces_sold.replace(" sold","")
            pieces_sold = int(pieces_sold)
        except:
            pieces_sold = 0

        store_name = list_item.find('.store-name',first=True).text
        store_url = ""
        for link in list_item.find('.item-store-wrap',first=True).absolute_links:
            store_url = link
            break
        
        data = {'product_title': product_title, 'product_url': product_url, 'price': product_price, 'rating': product_rating, 'pieces_sold':pieces_sold,'store_name':store_name,'store_url':store_url }
        products_list.append(data)


def create_csv():
    csv_columns = ['product_title', 'product_url', 'price', 'rating', 'pieces_sold','store_name','store_url']
    csv_file = "products.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in products_list:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    

page_url = input("Enter Aliexpress search page url: ")
print("Extracting Data...")
page = 1
while True:
    try:
        page_url = page_url+f'&page={page}'
        products_data = request(page_url)
        extract_data(products_data)
        page = +1
        time.sleep(3)
        print(str(len(products_list))+" items extracted!")
    except:
        break

create_csv()


