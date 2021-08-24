from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

driver = webdriver.Chrome(executable_path='./chromedriver.exe')

driver.get("https://www.mvideo.ru/")
close = driver.find_element_by_xpath('//div[contains(@class, "c-popup__close")]').click()
goods_new = driver.find_element_by_xpath("//div[@data-holder='#loadSubMultiGalleryblock8552369']")

actions = ActionChains(driver)
actions.move_to_element(goods_new)
actions.perform()

button = goods_new.find_element_by_xpath(".//a[contains(@class, 'next-btn')]")
while 'disabled' not in button.get_attribute('class').split():
    button.click()

    goods_new_1 = goods_new.find_element_by_xpath(".//a[@data-product-info]")
    goods_new_2 = goods_new_1.get_attribute('data-product-info')

    client = MongoClient('127.0.0.1', 27017)
    db = client['ai_1054_goods']

    mvideo_goods = db.mvideo_goods
    mvideo_goods.insert_one(goods_new_2)

driver.close()
