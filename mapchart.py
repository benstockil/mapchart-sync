import os
import time
import git

from selenium import webdriver
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from drivers.chrome import chromedriver
from drivers.firefox import firefoxdriver
from drivers.edge import edgedriver

MAP_DATA_PATH = "mapdata"
DOWNLOAD_PATH = "downloads"


# initialise git

if os.path.exists(MAP_DATA_PATH):
    mapRepo = git.Repo(MAP_DATA_PATH)
else:
    mapRepo = git.Repo.clone_from("https://github.com/benstockil/war-and-peace-mapchart", MAP_DATA_PATH)


# initialise webdriver

with open("BROWSER.txt") as browserConfig:
    browser = browserConfig.read()

    if browser == "FIREFOX":
        driver = firefoxdriver.create(DOWNLOAD_PATH)

    elif browser == "CHROME":
        driver = chromedriver.create(DOWNLOAD_PATH)

    elif browser == "EDGE":
        driver = edgedriver.create(DOWNLOAD_PATH)

    else:
        print("Please choose either EDGE, CHROME or FIREFOX are the browser set in \"BROWSER.txt\".")
        exit()


# load page

driver.get('https://mapchart.net/world-subdivisions.html')

print("Page loading...")

while True:
    try:
        downup = WebDriverWait(driver, 100000).until(
            EC.presence_of_element_located((By.ID, 'downup'))
        )
        break
    except TimeoutException:
        pass

time.sleep(2)

print("Page loaded.")


# wait for user input 
while True:
    try:

        userInput = input("Enter UPLOAD or DOWNLOAD to update the map: ").upper()
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", downup)
            downup.click()
        except:
            pass
        
        time.sleep(1)

        if userInput == "UPLOAD":
            print("Please wait...")

            # Click "download"
            driver.find_element_by_id("save-config").click()

            time.sleep(2)

            # Get latest download
            files = os.listdir(DOWNLOAD_PATH)
            latest = max([DOWNLOAD_PATH + "/" + f for f in files], key=os.path.getctime)

            # Replace the repo file with the new map data
            with open(latest) as downloadFile:
                mapData = downloadFile.read()
            with open(MAP_DATA_PATH + "/mapchart-data.txt", "w+") as repoFile:
                repoFile.write(mapData)

            os.remove(latest)

            # Upload to github
            mapRepo.index.add("mapchart-data.txt")
            mapRepo.index.commit("sync")
            try:
                mapRepo.remote().push()
                print("Success!")
            except:
                print(f"Upload failed. Please check you are authorised to upload. {e}")

            driver.find_element_by_class_name("icon-close").click()

        elif userInput == "DOWNLOAD":
            print("Please wait...")

            try:
                mapRepo.remote().pull()

                with open(MAP_DATA_PATH + "/mapchart-data.txt") as mapDataFile:
                    mapData = mapDataFile.read()

                driver.find_element_by_id("uploadData").send_keys(mapData)
                driver.find_element_by_id("upload-config").click()
            except Exception as e:
                print(f"Download failed. {e}")
                driver.find_element_by_class_name("icon-close").click()

        elif userInput == "EXIT":
            exit()

        else:
            print("Unknown command. Type EXIT to exit.")

    except Exception as e:
        print(f"\nAn error occurred. Please contact Ben with the following message:\n{e}\n")




