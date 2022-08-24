import requests
import re


def find_infos_in_amazon_page(url):
    #Part 1 : Get the http code and find the price of the product thanks to the display price pattern
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    response = requests.get(url, headers=headers)

    code_http = response.text
    pattern_product_price = r'"priceAmount":([\d\.]*)'
    result_product_price = re.search(pattern_product_price, code_http)

    #Part 2 : Find the name of the product
    pattern_product_name = r'<meta name="title" content="(.*)" />'
    result_product_name = re.search(pattern_product_name, code_http)

    # On checke d'abord qu'on est bien sur une page produit
    if result_product_name == None or result_product_price == None:
        return "Error"
    else:
        return [result_product_price[1],result_product_name[1]]
