# https://www.linkedin.com/in/gabriel-velasco-078457103/overlay/photo/
# https://www.linkedin.com/in/kaio-souza/overlay/photo/
# https://www.linkedin.com/in/user-name/overlay/photo/

from ast import Break
from cgi import print_arguments
from gettext import find
from sre_constants import BRANCH
from attr import attr, attrs
from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
from selenium.webdriver.common.keys import Keys
import time
import json
import re

# used to get someones Linked-in profile pic

def doLogin():
    browser = webdriver.Firefox()
    browser.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin");
    time.sleep(10)

    # login with your account
    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")

    username.send_keys("user@email.com")
    password.send_keys("userPass")

    submitBtn = browser.find_element_by_xpath("//*[@type='submit']")
    submitBtn.submit()
    time.sleep(10)

    browser.get("https://www.linkedin.com/in/gabriel-velasco-078457103/")
    time.sleep(10)

    return browser

def getImgTagSrc(linkedinUserName, browser):
    # ja logado, posso visitar perfis q tiver linkedin
    
    browser.get(f'https://www.linkedin.com/in/{linkedinUserName}/overlay/photo/')
    time.sleep(10)

    htmlContent = browser.page_source
    soup = BeautifulSoup(htmlContent)

    imgUrl = "None"
    imgCont = soup.find('img', id=re.compile("ember"))
    if(imgCont):
        imgUrl = imgCont.attrs['src']

    return imgUrl
