import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(10)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("http://localhost/litecard")
    wait.until(EC.presence_of_element_located((By.ID, "box-most-popular")))

    item_list = driver.find_elements_by_css_selector(".product")

    for item in item_list:
        sticker = item.find_elements_by_css_selector(".sticker")

        assert len(sticker) == 1, "not one sticker"
