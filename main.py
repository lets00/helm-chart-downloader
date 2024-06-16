import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://artifacthub.io/packages/search?kind=0&sort=relevance&page=1")

with open('links.txt', 'a') as file:
   for x in range(599):
        WebDriverWait(driver, 20).until(
           EC.presence_of_element_located((By.XPATH, "//a[contains(@role, 'link') and contains(@href, 'helm')]")))
       
        elements = driver.find_elements(By.XPATH, "//a[contains(@role, 'link') and contains(@href, 'helm')]")

        for element in elements:
            file.write(element.get_attribute("href") + "\n")

        next_button = driver.find_element(By.XPATH,
                            "//button[contains(@class, 'page-link text-primary')]/span[contains(text(), 'Next')]")

        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        time.sleep(2)

        next_button.click()

        time.sleep(5)

driver.quit()

# Reabre o navegador
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

with open('links.txt', 'r') as file:
    links = file.readlines()

with open('links_download.txt', 'a') as file:
    for link in links:
        link = link.strip()
        if link:
            driver.get(link)
            time.sleep(3)
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'ExternalLink_link') and contains(text(), 'link')]")))
                link_download_element = driver.find_element(By.XPATH, "//a[contains(@class, 'ExternalLink_link') and contains(text(), 'link')]")
                file.write(link_download_element.get_attribute("href") + "?modal=install" + "\n")
            except TimeoutException:
                print("Não encontrei o href em: "+ link)
driver.quit()
