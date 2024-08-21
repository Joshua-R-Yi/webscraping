import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json
import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, Float





product_array = []
price_array = []
model_array = []

def login(email, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')

    driver = webdriver.Chrome()
    driver.get("https://www.hardwareworld.com/")

    # Locate and click button to go to login page
    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "My Account")))
    login_button.click()

    # Locate and fill email field
    email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "_ctl0_body_topEmailEdit")))
    email_field.send_keys(email)
    
    # Locate and fill password field
    password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "_ctl0_body_topPasswordEdit")))
    password_field.send_keys(password)

    # Submit login form
    submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "_ctl0_body_topSubmitButton")))
    submit_button.click()

    # Traverse to Automotive Engine Oil page
    go_to_automotive = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Automotive")))
    go_to_automotive.click()
    go_to_engineoil = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Engine Oil & Hydraulics Fluids")))
    go_to_engineoil.click()

    # Scrape all product names and price 
    products = driver.find_elements(By.CLASS_NAME, "product-box")
    for product in products:
        product_header= product.find_element(By.TAG_NAME, "h2")
        product_title = product_header.find_element(By.TAG_NAME, "a")
        product_text = product_title.text
        product_array.append(product_text)

        price = product.find_element(By.CLASS_NAME, "price")
        price_text = price.text
        price_array.append(price_text[2:])

        model_number = product.find_element(By.CLASS_NAME, "model-no")
        model_text = model_number.text
        model_array.append(model_text[9:])


    print(product_array, price_array, model_array)

    # Write to excel
    data = {'model_number': model_array, 'product': product_array, 'price': price_array}
    df = pd.DataFrame(data)
    df.to_excel('HardwareWorld_EngineOil.xlsx', index=False)
    df.to_csv('HardwareWorld_EngineOil.csv', index=False, header=True)

    time.sleep(10)

    driver.close()


email = "xxxxxxxx@gmail.com"
password = "xxxxxxxx"
login(email, password)



####################################################################################################



# Adding to databse
DATABASE_URL = "mysql://username:password@host:port/database"

engine = create_engine(DATABASE_URL)

df = pd.read_csv('./HardwareWorld_EngineOil.csv')

dtype_dict = {
    'model': String(255),
    'product': String(255),
    'price': Float,
}
df.to_sql(name='hardware_world', con=engine, if_exists='replace', index=False, dtype=dtype_dict)

engine.dispose()
