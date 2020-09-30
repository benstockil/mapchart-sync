import os
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

def create(downloadPath):
    driverPath = os.path.dirname(os.path.realpath(__file__)) + "\\geckodriver.exe"

    fxProfile = FirefoxProfile()

    fxProfile.set_preference("browser.download.folderList",2)
    fxProfile.set_preference("browser.download.manager.showWhenStarting", False)
    fxProfile.set_preference("browser.download.dir", os.getcwd() + "\\" + downloadPath)
    fxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk","text/plain")

    return webdriver.Firefox(executable_path=driverPath, firefox_profile=fxProfile)