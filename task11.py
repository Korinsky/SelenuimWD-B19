import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import time
from selenium.webdriver.support.ui import Select


@pytest.fixture()
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(10)
    wd.set_script_timeout(1000)
    request.addfinalizer(wd.quit)
    return wd


def test_registration(driver):
    wait = WebDriverWait(driver, 10)
    mail = 'lol_' + str(random.randint(0, 1000)) + '@lol.org'

    driver.get("http://localhost/litecard")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

    driver.find_element_by_xpath("//form[@name='login_form']//a[contains(@href, 'create_account')]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//input[@name='tax_id']").send_keys("111-22-33333")
    driver.find_element_by_xpath("//input[@name='firstname']").send_keys("Seleniun")
    driver.find_element_by_xpath("//input[@name='lastname']").send_keys("Driver")
    driver.find_element_by_xpath("//input[@name='address1']").send_keys("street & house 1")
    driver.find_element_by_xpath("//input[@name='city']").send_keys("BigApple")
    driver.find_element_by_xpath("//input[@name='postcode']").send_keys("12345")
    Select(driver.find_element_by_xpath("//select[@name='country_code']")).select_by_visible_text("United States")
    driver.find_element_by_xpath("//select[@name='zone_code']").click()
    time.sleep(1)
    Select(driver.find_element_by_xpath("//select[@name='zone_code']")).select_by_value("AK")
    driver.find_element_by_xpath("//input[@name='email']").send_keys('%s' % mail)
    driver.find_element_by_xpath("//input[@name='phone']").send_keys("+12223334455")
    driver.find_element_by_xpath("//input[@name='password']").send_keys("pass1")
    driver.find_element_by_xpath("//input[@name='confirmed_password']").send_keys("pass1")
    driver.find_element_by_xpath("//button[@name='create_account']").click()
    assert EC.presence_of_element_located((By.XPATH, "//i[contains(., 'Your customer account has been created.')]")), "failed to create account"

    driver.find_element_by_xpath("//a[contains(., 'Logout')]").click()
    assert EC.presence_of_element_located((By.XPATH, "//a[@href, 'create_account']")), "failed to log out"

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
    driver.find_element_by_xpath("//input[@name='email']").send_keys('%s' % mail)
    driver.find_element_by_xpath("//input[@name='password']").send_keys('pass1')
    driver.find_element_by_xpath("//button[@name='login']").click()
    assert EC.presence_of_element_located((By.XPATH, "//a[contains., Edit Account]")), "failed to login"

    driver.find_element_by_xpath("//a[contains(., 'Logout')]").click()
    assert EC.presence_of_element_located((By.XPATH, "//input[@name='email']")), "failed to log out"
