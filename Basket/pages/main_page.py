from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


def open_site(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("http://localhost/litecard")
    wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='title']")))

def choose_product(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element_by_xpath("//div[@id='box-most-popular']//ul/li[1]/a[1]").click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//form[@name='buy_now_form']//strong[contains(., 'Quantity')]")))

def choose_size_if_needed(driver):
    option = driver.find_elements_by_xpath("//form[@name='buy_now_form']//strong[contains(., 'Size')]")
    if len(option) != 0:
        Select(driver.find_element_by_xpath("//form[@name='buy_now_form']//select")).select_by_visible_text('Small')

def add_product(driver):
    driver.find_element_by_xpath("//form[@name='buy_now_form']//button[contains(., 'Add To Cart')]").click()

def check_count_cart(driver, count):
    check = False
    for p in range(10):
        if int(driver.find_element_by_xpath("//div[@id='cart']/a[@class='content']/span[@class='quantity']").text) == count:
            check = True
            continue
        time.sleep(0.5)
    assert check, "the number of items in the cart has not changed"

def open_cart_site(driver):
    driver.find_element_by_xpath("//div[@id='cart']/a[@class='link']").click()
    return len(driver.find_elements_by_xpath("//div[@class='content']/table//tr/td[@class='item']"))