import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(30)
    #    request.addfinalizer(wd.quit)
    return wd


def test_add_product(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("http://localhost/litecard/admin/?app=catalog&doc=catalog&category_id=1")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))

    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='dataTable']")))

    list_products = driver.find_elements_by_xpath("//table[@class='dataTable']//input[contains(@name, 'products')]/../../td[3]/a")
    page_products = []
    browser_logs = {}

    for i in list_products:
        page_products.append(i.get_attribute("href"))

    for i in range(len(page_products)):
        driver.get("%s" % page_products[i])
        time.sleep(1)

        if len(driver.get_log("browser")) > 0:
            browser_logs.update({page_products[i] : driver.get_log("browser")})

    assert len(browser_logs.keys()) == 0, browser_logs
