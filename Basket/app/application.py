from pages.main_page import *
from pages.cart_page import *

def add_items_to_cart(driver):
    for i in range(1, 4):
        open_site(driver)
        choose_product(driver)
        choose_size_if_needed(driver)
        add_product(driver)
        check_count_cart(driver, i)

def open_cart(driver):
    quantity_products = open_cart_site(driver)
    return quantity_products

def clear_cart(driver, i):
    for product in range(i):
        remove_product(driver)