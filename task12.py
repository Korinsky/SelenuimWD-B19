import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import time


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(10)
    request.addfinalizer(wd.quit)
    return wd


def test_add_product(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost/litecard/admin/?app=catalog&doc=catalog")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    time.sleep(1)

    driver.find_element_by_xpath("//td[@id='content']//a[contains(., 'Add New Product')]").click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(., 'General')]")))
    time.sleep(1)

# General tab
    mark_if_not(driver, "//strong[contains(., 'Status')]/..//label[contains(., 'Enabled')]/input")
    driver.find_element_by_xpath("//strong[contains(., 'Name')]/..//input").send_keys("SuperDuck")
    driver.find_element_by_xpath("//strong[contains(., 'Code')]/..//input").send_keys("777")
    mark_if_not(driver, "//strong[contains(., 'Categories')]/..//input[@data-name='Rubber Ducks']")
    mark_if_not(driver, "//strong[contains(., 'Gender')]/../../..//td[contains(., 'Unisex')]//..//input[@type='checkbox']")
    clear_enter(driver, "//strong[contains(., 'Quantity')]/..//input", '50')
    driver.find_element_by_xpath("//strong[contains(., 'Upload Images')]/..//input").send_keys(os.getcwd()+"/utka.png")
    driver.find_element_by_xpath("//strong[contains(., 'Date Valid From')]/..//input").send_keys('01012020')
    driver.find_element_by_xpath("//strong[contains(., 'Date Valid To')]/..//input").send_keys('31122020')

# Information tab
    driver.find_element_by_xpath("//div[@class='tabs']//a[contains(., 'Information')]").click()
    time.sleep(1)
    Select(driver.find_element_by_xpath("//select[@name='manufacturer_id']")).select_by_visible_text("ACME Corp.")
    driver.find_element_by_xpath("//strong[contains(., 'Keywords')]/..//input").send_keys('test')
    driver.find_element_by_xpath("//strong[contains(., 'Short Description')]/..//input").send_keys('SuperDuck')
    driver.find_element_by_xpath("//strong[contains(., 'Description')]/..//div[@class='trumbowyg-editor']").send_keys('SuperDuck', Keys.RETURN, 'code - 777')
    driver.find_element_by_xpath("//strong[contains(., 'Head Title')]/..//input").send_keys('ACME')
    driver.find_element_by_xpath("//strong[contains(., 'Meta Description')]/..//input").send_keys('some text')

# Information tab
    driver.find_element_by_xpath("//div[@class='tabs']//a[contains(., 'Prices')]").click()
    time.sleep(1)

    clear_enter(driver, "//strong[contains(., 'Purchase Price')]/..//input", '1.99')
    Select(driver.find_element_by_xpath("//select[@name='purchase_price_currency_code']")).select_by_visible_text("US Dollars")
    clear_enter(driver, "//input[@name='prices[USD]']", '5')
    clear_enter(driver, "//input[@name='prices[EUR]']", '6')
    driver.find_element_by_xpath("//button[@name='save']").click()

# Check product
    driver.get("http://localhost/litecard/admin/?app=catalog&doc=catalog")
    assert EC.presence_of_element_located((By.XPATH, "//table[@class='dataTable']//a[contains(., 'SuperDuck')]")),\
        "new product not in catalog"


def clear_enter(driver, locator, text):
    el = driver.find_element_by_xpath("%s" % locator)
    el.click()
    el.send_keys(Keys.CONTROL, 'a')
    el.send_keys('%s' % text)


def mark_if_not(driver, locator):
    el = driver.find_element_by_xpath("%s" % locator)
    if not el.get_attribute("checked"):
        el.click()
