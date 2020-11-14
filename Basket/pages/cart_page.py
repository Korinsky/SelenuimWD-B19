from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def remove_product(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='content']/table")))
    table = driver.find_element_by_xpath("//div[@class='content']/table")
    wait.until(EC.visibility_of(driver.find_element_by_xpath("//div[@class='viewport']//button[contains(., 'Remove')]")))
    time.sleep(0.5)
    driver.find_element_by_xpath("//div[@class='viewport']//button[contains(., 'Remove')]").click()
    wait.until(EC.staleness_of(table))