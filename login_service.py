# https://www.linkedin.com/in/gabriel-velasco-078457103/overlay/photo/
# https://www.linkedin.com/in/kaio-souza/overlay/photo/
# https://www.linkedin.com/in/user-name/overlay/photo/

from bs4 import BeautifulSoup
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# used to get someones Linked-in profile pic
def doLogin():
    browser = webdriver.Firefox()
    browser.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

    # Wait for the login page to load
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # login with your account
    username = browser.find_element(By.ID, "username")
    password = browser.find_element(By.ID, "password")

    username.send_keys("sample@email.com")
    password.send_keys('samplePassWord')

    submitBtn = browser.find_element(By.XPATH, "//*[@type='submit']")
    submitBtn.click()

    # Wait for the LinkedIn profile page to load after login
    time.sleep(2.5)

    return browser

def get_img_url_from_profile(linkedin_user, browser):
    # browser esta logado
    # redireciona para foto do perfil de 'linkedin_user' 
    
    browser.get(f'https://www.linkedin.com/in/{linkedin_user}/overlay/photo/')
    time.sleep(2)

    htmlContent = browser.page_source
    soup = BeautifulSoup(htmlContent)

    imgUrl = "None"
    imgCont = soup.find('img', id=re.compile("ember"))
    if(imgCont):
        imgUrl = imgCont.attrs['src']

    return imgUrl
