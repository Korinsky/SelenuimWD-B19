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

    driver.get("http://localhost/litecard/admin")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    top_menu_list = driver.find_elements_by_xpath("//li[@id='app-']")

    for top_menu_num in range(1, len(top_menu_list) + 1):
        driver.find_element_by_xpath("//li[@id='app-'][%i]" % top_menu_num).click()

        assert EC.presence_of_element_located((By.XPATH, "//h1")), "Menu has no title"

        if not EC.presence_of_element_located((By.XPATH, "//ul[@class='docs']")):
            continue

        sub_menu_list = driver.find_elements_by_xpath("//li/ul/li")

        for sub_menu_num in range(1, len(sub_menu_list) + 1):
            driver.find_element_by_xpath("//li/ul/li[%i]" % sub_menu_num).click()

            assert EC.presence_of_element_located((By.XPATH, "//h1")), "Menu has no title"
