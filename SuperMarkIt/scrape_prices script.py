import requests as re
from bs4 import BeautifulSoup
import sqlite3


def sort_name(name):
    name_list = name.split()
    return " ".join(name_list)


conn = sqlite3.connect("db.sqlite3")
conn.row_factory = lambda c, row: row[0]
c = conn.cursor()
c.execute("SELECT url_morrisons from products_product")
x = c.fetchall()
y = [url for url in x]
# print(y[0])
link1 = y[0]
page = re.get(link1)
page_text = page.text
soup = BeautifulSoup(page_text, "html.parser")
product_info = soup.find("div", class_="related-search-ribbon-enabled")
product_info_title = product_info.find(class_="productTitle").getText()
name = sort_name(product_info_title)
try:
    product_info_price = product_info.find(class_="nowPrice").getText()
    price = product_info_price.strip()[1:]
except AttributeError:
    product_info_price = product_info.find(class_="typicalPrice").getText()
    price = product_info_price.strip()[1:]
print(name, price)
c.execute("UPDATE products_product SET price_morrisons = ? WHERE url_morrisons=?", (price, link1))

conn.commit()
c.close()
conn.close()
