import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(10)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("https://software-testing.ru/")
