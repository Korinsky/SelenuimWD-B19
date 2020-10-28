import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(10)
    request.addfinalizer(wd.quit)
    return wd


def test_add_product(driver):
    wait = WebDriverWait(driver, 10)

    for i in range(1, 4):
        driver.get("http://localhost/litecard")
        wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='title']")))
        driver.find_element_by_xpath("//div[@id='box-most-popular']//ul/li[1]/a[1]").click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//form[@name='buy_now_form']//strong[contains(., 'Quantity')]")))

        option = driver.find_elements_by_xpath("//form[@name='buy_now_form']//strong[contains(., 'Size')]")
        if len(option) != 0:
            Select(driver.find_element_by_xpath("//form[@name='buy_now_form']//select")).select_by_visible_text('Small')
        driver.find_element_by_xpath("//form[@name='buy_now_form']//button[contains(., 'Add To Cart')]").click()

        count = False
        for p in range(10):
            if int(driver.find_element_by_xpath("//div[@id='cart']/a[@class='content']/span[@class='quantity']").text) == i:
                count = True
                continue
            time.sleep(0.5)
        assert count, "the number of items in the cart has not changed"

    driver.find_element_by_xpath("//div[@id='cart']/a[@class='link']").click()
    product_count = len(driver.find_elements_by_xpath("//div[@class='content']/table//tr/td[@class='item']"))

    for i in range(product_count):
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content']/table")))
        table = driver.find_element_by_xpath("//div[@class='content']/table")
        wait.until(EC.visibility_of(driver.find_element_by_xpath("//div[@class='viewport']//button[contains(., 'Remove')]")))
        time.sleep(0.5)
        driver.find_element_by_xpath("//div[@class='viewport']//button[contains(., 'Remove')]").click()
        wait.until(EC.staleness_of(table))

