import os
from selenium import webdriver
from selenium.webdriver import ChromeOptions

def create(downloadPath):
    driverPath = os.path.dirname(os.path.realpath(__file__)) + "\\chromedriver.exe"

    chromeOptions = ChromeOptions()
    prefs = {"download.default_directory" : os.getcwd() + "\\" + downloadPath}
    chromeOptions.add_experimental_option("prefs",prefs)

    return webdriver.Chrome(executable_path=driverPath, chrome_options=chromeOptions)