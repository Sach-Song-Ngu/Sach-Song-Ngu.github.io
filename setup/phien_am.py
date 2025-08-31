import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
import tkinter as tk
from tkinter import filedialog
import pandas as pd

options = uc.ChromeOptions()
options.add_argument("--password-store=basic")
options.add_experimental_option(
    "prefs",
    {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    },
)

# options.add_argument("--disable-notifications")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-popup-blocking")

driver = uc.Chrome(options=options, driver_executable_path="chromedriver")

span_texts = []

    
# try:
driver.get("https://translate.google.com/?sl=ko&tl=vi&op=translate") ########## tiếng nhật
# driver.get("https://translate.google.com/?sl=zh-CN&tl=vi&op=translate") ########## tiếng trung

file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
print(file_path)
# Đọc tệp Excel
df = pd.read_excel(file_path)

# Lấy các đoạn text từ cột "text"
texts = df["text"]
# In ra các đoạn text
for text in texts:
    print(text)
    # driver.find_element(By.XPATH,"/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/span/span/div/textarea").clear()
    driver.get("https://translate.google.com/?sl=ko&tl=vi&op=translate") ########## tiếng nhật
    # driver.get("https://translate.google.com/?sl=zh-CN&tl=vi&op=translate") ########## tiếng trung
    time.sleep(2)
    textbox = EC.presence_of_element_located((By.XPATH, "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/div/c-wiz/span/span/div/textarea"))
    textbox_input = WebDriverWait(driver, 5).until(textbox)
    driver.find_element(By.XPATH,"/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/div/c-wiz/span/span/div/textarea").send_keys(text)
    # time.sleep(4)
    condition = EC.presence_of_element_located((By.XPATH, "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/div/c-wiz/div[2]/div[1]/span"))

    # Chờ cho đến khi thẻ span xuất hiện (tối đa 10 giây)
    try:
        span_element = WebDriverWait(driver, 5).until(condition)
        # Lấy nội dung của thẻ span
        span_text = span_element.text
        # In ra nội dung
        print( span_text)
        span_texts.append(span_text)
    except Exception as e:
        span_texts.append(" ")
        pass
# time.sleep(10000)
# Lấy tên file gốc
original_filename = os.path.basename(file_path)
# Tạo tên file kết quả
output_filename = "KETQUA_" + original_filename
# Ghi file Excel
df = df.assign(phien_am=span_texts)
df.to_excel(output_filename, index=False)
driver.quit()
