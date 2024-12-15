from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
from bs4 import BeautifulSoup
import os


### update the url and trails accordingly. name of trails can be found from looking at the HTML source
### this works on mac only (since it uses mac commands to notify when smth is available)

url="https://www.recreation.gov/permits/233262/registration/detailed-availability?type=overnight-permit"
trails=["AA07","AA09", "AA11","AA12", "AA13", "JM01" ]
startDate="Saturday, August 31, 2024"
groupsize=2

interval=30

_waittolad=5


options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

def checkStatus(driver):
    found=False
    while not found:
        print("checking...")

        
        try:    
            driver.get(url)
            driver.implicitly_wait(5)
            driver.find_element(By.ID,"prompt-answer-no1").click()
            select_element = driver.find_element(By.ID, 'permit-type')
            select = Select(select_element)
            select.select_by_value("overnight-permit")
            driver.find_element(By.CLASS_NAME,"toggle-calendar-button").click()
            driver.find_element(By.XPATH,"//div[@aria-label='"+startDate+"']").click()
            driver.find_element(By.ID,"guest-counter").click()
            driver.find_element(By.ID,"guest-counter-number-field-People").send_keys("2")
            driver.find_element(By.ID,"guest-counter").click()
            time.sleep(_waittolad)
            page=repr(driver.page_source.encode("utf-8"))
            # with open('out.html', 'w') as output:
            #     output.write(page)


            soup=BeautifulSoup(page,"html.parser")
            for t in trails:
                freeSpots=soup.find("div",string=t).next_sibling.next_sibling.next_sibling.find("span", class_="sarsa-button-content").text
                if int(freeSpots)>groupsize-1:
                    msg=str(t)+" has open spots!"
                    print(msg)
                    os.system("say "+ msg)

                    # os.system("osascript -e 'tell application \"Messages\" to send \""+msg+"\" to buddy \""+phoneNumber+"\"'")    
                    # os.system("osascript sendSMS.applescript")
                    found=True

            if found==False:
                print("not found. cheking in "+str(interval)+"s")
            else:
                return
            
            time.sleep(interval-_waittolad)
        except WebDriverException:
            driver = webdriver.Chrome(options=options)
            print("something went wrong, trying again...")

checkStatus(driver)
driver.quit()