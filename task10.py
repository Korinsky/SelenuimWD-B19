import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


@pytest.fixture(params=['Chrome', 'Firefox', 'IE'])
def driver(request):
    wd = webdriver.Chrome()
    wd.set_page_load_timeout(10)
    request.addfinalizer(wd.quit)
    return wd


def test_country_order(driver):
    wait = WebDriverWait(driver, 10)

    driver.get("http://localhost/litecard")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))

    main_data = driver.find_element_by_xpath("//*[@id='box-campaigns']//li/a[@class='link']")

    mp_name = main_data.find_element_by_xpath(".//div[@class='name']").text
    mp_base_price = main_data.find_element_by_xpath(".//s").text
    mp_reg_color = main_data.find_element_by_xpath(".//s").value_of_css_property("color")
    mp_reg_font = main_data.find_element_by_xpath(".//s").value_of_css_property("font-size")
    mp_reg_text = main_data.find_element_by_xpath(".//s").value_of_css_property("text-decoration")
    mp_action_price = main_data.find_element_by_xpath(".//strong").text
    mp_action_color = main_data.find_element_by_xpath(".//strong").value_of_css_property("color")
    mp_action_font = main_data.find_element_by_xpath(".//strong").value_of_css_property("font-size")
    mp_action_text = main_data.find_element_by_xpath(".//strong").value_of_css_property("font-weight")

    reg_color = re.compile(r'\d+').findall(mp_reg_color)
    if not reg_color[0] == reg_color[1] == reg_color[2]:
        assert "base price color on the main page is not gray"

    if re.compile(r'line-through').match(mp_reg_text) is None:
        assert "base price on the main is not crossed out"

    action_color = re.compile(r'\d+').findall(mp_action_color)
    if not action_color[1] == action_color[2] == 0:
        assert "action price color on the main is not red"

    if int(mp_action_text) < 700:
        assert "action price on the main is not bold"

    if float(mp_reg_font.replace("px", "")) >= float(mp_action_font.replace("px", "")):
        assert "action price on the main is no more than base"

    main_data.click()
    prod_page = driver.find_element_by_xpath("//div[@class='price-wrapper']")

    name = driver.find_element_by_xpath("//h1[@class='title']").text
    base_price = prod_page.find_element_by_xpath(".//s").text
    reg_color = prod_page.find_element_by_xpath(".//s").value_of_css_property("color")
    reg_font = prod_page.find_element_by_xpath(".//s").value_of_css_property("font-size")
    reg_text = prod_page.find_element_by_xpath(".//s").value_of_css_property("text-decoration")
    action_price = prod_page.find_element_by_xpath(".//strong").text
    action_color = prod_page.find_element_by_xpath(".//strong").value_of_css_property("color")
    action_font = prod_page.find_element_by_xpath(".//strong").value_of_css_property("font-size")
    action_text = prod_page.find_element_by_xpath(".//strong").value_of_css_property("font-weight")

    reg_color = re.compile(r'\d+').findall(reg_color)
    if not reg_color[0] == reg_color[1] == reg_color[2]:
        assert "base price color on the product page is not gray"

    if re.compile(r'line-through').match(reg_text) is None:
        assert "base price on the product page is not crossed out"

    action_color = re.compile(r'\d+').findall(action_color)
    if not action_color[1] == action_color[2] == 0:
        assert "action price color on the product page is not red"

    if int(action_text) < 700:
        assert "action price on the product page is not bold"

    if float(reg_font.replace("px", "")) >= float(action_font.replace("px", "")):
        assert "action price on the product page is no more than base"

    if mp_name != name:
        assert "names do not match"

    if (mp_base_price != base_price) or (mp_action_price != action_price):
        assert "prices do not match"
