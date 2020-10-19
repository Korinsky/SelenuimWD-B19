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


def test_country_order(driver):
    countries_list = []
    countries_with_zones_list = []
    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost/litecard/admin/?app=countries&doc=countries")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait.until(EC.presence_of_element_located((By.ID, "box-apps-menu")))

    row_list = driver.find_elements_by_css_selector(".dataTable tr.row")

    for row in row_list:
        countries_list.append(row.find_element_by_css_selector("a").text)

        if row.find_element_by_css_selector("td:nth-of-type(6)").text != '0':
            countries_with_zones_list.append(row.find_element_by_css_selector("a").get_attribute("href"))

    assert list(countries_list) == sorted(countries_list), "list of countries not in alphabetical order"

    for i in range(0, len(countries_with_zones_list)):
        zones_list = []
        driver.get("%s" % countries_with_zones_list[i])
        wait.until(EC.presence_of_element_located((By.ID, "table-zones")))
        row_list = driver.find_elements_by_css_selector("#table-zones tr:not(.header)")

        for i in range(0, len(row_list)-1):
            zone = row_list[i]
            zones_list.append(zone.find_element_by_css_selector("td:nth-child(3)").text)

        assert list(zones_list) == sorted(zones_list), "list of zones not in alphabetical order"
