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
    menu_dict = {'Appearence': ('Template', 'Logotype'), 'Catalog': ('Catalog', 'Product Groups', 'Option Groups', 'Manufacturers', 'Suppliers', 'Delivery Statuses', 'Sold Out Statuses', 'Quantity Units', 'CSV Import/Export'), 'Countries': [], 'Currencies': [], 'Customers': ('Customers', 'CSV Import/Export', 'Newsletter'), 'Geo Zones': [], 'Languages': ('Languages', 'Storage Encoding'), 'Modules': ('Background Jobs', 'Customer', 'Shipping', 'Payment', 'Order Total', 'Order Success', 'Order Action'), 'Orders': ('Orders', 'Order Statuses'), 'Pages': [], 'Reports': ('Monthly Sales', 'Most Sold Products', 'Most Shopping Customers'), 'Settings': ('Store Info', 'Defaults', 'General', 'Listings', 'Images', 'Checkout', 'Advanced', 'Security'), 'Slides': [], 'Tax': ('Tax Classes', 'Tax Rates'), 'Translations': ('Search Translations', 'Scan Files', 'CSV Import/Export'), 'Users': [], 'vQmods': ['vQmods']}

    driver.get("http://localhost/litecard/admin")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    for top_menu_num in range(1, len(menu_dict.keys())+1):
        top_menu = driver.find_element_by_xpath("//ul[@id='box-apps-menu']/li[%i]" % top_menu_num)
        top_menu.click()

        if driver.find_elements_by_xpath("//h1") == []:
            file.write("Menu '%s' has no title\n" % top_menu_num)

        top_menu = list(menu_dict.keys())[top_menu_num-1]
        sub_menu = menu_dict.get(top_menu)

        if len(sub_menu) == 0:
            continue

        sub_menu_list = len(menu_dict.get(top_menu))
        for sub_menu_num in range(1, sub_menu_list+1):
            wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='docs']/li[%i]" % sub_menu_num)))
            sub_menu = driver.find_element_by_xpath("//ul[@class='docs']/li[%i]" % sub_menu_num)
            sub_menu.click()

            if driver.find_elements_by_xpath("//h1") == []:
                file.write("Sub-menu '%s' in menu '%s' hase no title\n" % (sub_menu, top_menu))

    size = os.path.getsize("report.txt")
    if size == 0:
        file.write("all headers are present")
    file.close()


