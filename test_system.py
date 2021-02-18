import os
import pytest
import app
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import dotenv
import requests
import db_items
 
@pytest.fixture(scope='module')
def test_app():
    # construct the new application   
    application = app.create_app()   

    # start the app in its own thread.  
    thread = Thread(target=lambda: application.run(use_reloader=False))  
    thread.daemon = True  
    thread.start()   
    yield app   

    # Tear Down     
    thread.join(1)  
    test_item = db_items.get_item("TestItem")
    if test_item is not None:
        id = test_item["_id"]
        db_items.delete_item(id)



@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.headless = True     
    with webdriver.Firefox(options=opts) as driver:
        yield driver 

def test_adding_new_task(driver, test_app):    
    driver.get('http://localhost:5000/')  
        
    input_field = driver.find_element_by_id('title')
    input_field.send_keys("TestItem")
    add_item = driver.find_element_by_id('new_item')
    add_item.click()    
    page_source = driver.page_source    
    assert "TestItem" in page_source
        
