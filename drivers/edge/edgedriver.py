import os
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

def create(downloadPath):
    driverPath = os.path.dirname(os.path.realpath(__file__)) + "\\msedgedriver.exe"

    edgeOptions = EdgeOptions()
    prefs = {"download.default_directory" : os.getcwd() + "\\" + downloadPath}
    edgeOptions.add_experimental_option("prefs",prefs)

    return Edge(executable_path=driverPath, options=edgeOptions)