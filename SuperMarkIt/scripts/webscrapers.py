import requests as req
from bs4 import BeautifulSoup


def sort_name(name):
    """ removes whitespace from product name"""
    name_list = name.split()
    sorted_name = " ".join(name_list)
    return sorted_name


def create_soup_page(url):
    webpage = req.get(url)
    webpage_text = webpage.text
    soup = BeautifulSoup(webpage_text, "html.parser")
    return soup


def sainsburys_scrape(url):
    """returns the item price for a sainsburys product"""
    soup = create_soup_page(url)
    try:
        price_units = soup.find("p", class_="pricePerUnit").getText().strip()
        product_price = price_units.partition("/")[0]
        if "p" in product_price:
            product_price_pence = product_price.replace("p", "")
            product_price_final = float(product_price_pence)/100
        else:
            product_price_final = price_units.partition("/")[0][1:]

        return product_price_final

    except AttributeError:
        print("Failed- investigate: {}".format(url))


def morrisons_scrape(url):
    """returns the item price for a morrisons product"""
    soup = create_soup_page(url)
    try:
        product_description = soup.find("div", class_="related-search-ribbon-enabled")

        try:
            product_price_raw = product_description.find(class_="nowPrice").getText()
            product_price = product_price_raw.strip()[1:]
        except AttributeError:
            # If the nowPrice isn't available it means the product is on offer.
            product_price_raw = product_description.find(class_="typicalPrice").getText()
            product_price = product_price_raw.strip()[1:]

        return product_price
    except AttributeError:
        print("Failed- investigate: {}".format(url))


def tesco_scrape(url):
    """returns the item price for a morrisons product"""
    soup = create_soup_page(url)
    try:
        product_price = soup.find(class_="value").getText()
        return product_price

    except AttributeError:
        print("Failed- investigate: {}".format(url))
