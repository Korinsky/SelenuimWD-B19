import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(10)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    file = open("report.txt", "w")
    wait = WebDriverWait(driver, 10)
    driver.get("http://localhost/litecard")
    wait.until(EC.presence_of_element_located((By.ID, "box-most-popular")))

    item_list = driver.find_elements_by_css_selector(".middle>.content>.box li")

    for item in item_list:
        sticker = item.find_elements_by_css_selector(".sticker")

        if len(sticker) != 1:
            name = item.find_element_by_css_selector(".name")
            file.write("Product '%s' has no one sticker\n" % name.text)

    file.close()
    size = os.path.getsize("report.txt")
    if size == 0:
        file = open("report.txt", "a")
        file.write("all products have one sticker")
        file.close()
