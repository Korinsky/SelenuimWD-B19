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

    driver.get("http://localhost/litecard/admin/?app=countries&doc=countries")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//td[@id='content']//a[contains(., 'Add New Country')]")))
    driver.find_element_by_xpath("//td[@id='content']//a[contains(., 'Add New Country')]").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//form[@method='post']//a[@target='_blank']")))
    url_list = driver.find_elements_by_xpath("//form[@method='post']//a[@target='_blank']")

    for i in range(0, len(url_list)):
        main_window = driver.current_window_handle
        old_windows = driver.window_handles
        button = url_list[i]
        button.click()
        new_window = there_is_window_other_than(driver, old_windows)
        driver.switch_to_window(new_window[0])
        print(str(i) + " - " + driver.title)
        driver.close()
        driver.switch_to_window(main_window)


def there_is_window_other_than(driver, old):
    for count in range(10):
        new = driver.window_handles
        for i in old:
            new.remove(i)
        if len(new) > 0:
            return new
        time.sleep(1)
    assert True, "new window didn't open in 10 seconds"