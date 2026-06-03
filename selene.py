from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://exemplo.com/login")

time.sleep(2)

driver.find_element(By.ID, "username").send_keys("meu_usuario")
driver.find_element(By.ID, "password").send_keys("minha_senha")
driver.find_element(By.ID, "login").click()

time.sleep(5)
driver.quit()
