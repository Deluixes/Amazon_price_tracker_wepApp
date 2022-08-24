from celery import shared_task
from .models import *
from datetime import date
from .FunctionFindInfosinPage import *
#
# @background(schedule=10)
# def update_price_amazon_pages():
#     today_date = date.today().strftime('%Y-%m-%d')
#     set_old_date_amazonpage = set()
#     error = 0
#     id_value = 0
#
#     while error < 10:
#         try:
#             set_old_date_amazonpage.add(
#                 ProductInstance.objects.exclude(day_of_check=today_date).get(pk=id_value).product_id)
#             id_value += 1
#         except:
#             error += 1
#             id_value += 1
#
#     for id_value in set_old_date_amazonpage:
#         amazonpage = AmazonPage.objects.get(pk=id_value)
#         list_infos = find_infos_in_amazon_page(amazonpage.url)
#         price = list_infos[0]
#         new_product_instance = ProductInstance(product=amazonpage.id, product_price=price,
#                                                day_of_check=today_date)
#         new_product_instance.save()

@shared_task
def send_notifiction():
     print("‘Here I\’m")



@shared_task(name="add_new_products_datas")
def update_price_amazon_pages():
    today_date = date.today().strftime('%Y-%m-%d')
    set_old_date_amazonpage = set()
    error = 0
    id_value = 0

    while error < 10:
        try:
            set_old_date_amazonpage.add(
                ProductInstance.objects.exclude(day_of_check=today_date).get(pk=id_value).product_id)
            id_value += 1
        except:
            error += 1
            id_value += 1

    for id_value in set_old_date_amazonpage:
        amazonpage = AmazonPage.objects.get(pk=id_value)
        list_infos = find_infos_in_amazon_page(amazonpage.url)
        price = list_infos[0]
        new_product_instance = ProductInstance(product=amazonpage, product_price=price,
                                               day_of_check=today_date)
        new_product_instance.save()





