from ast import Break
from cgi import print_arguments
from gettext import find
from lib2to3.pgen2.driver import Driver
from sre_constants import BRANCH
from attr import attr, attrs
from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
import json
import re
import time
import loginTest

def generateFacom():
    loginBrowser = loginTest.doLogin()

    facomUrl = "https://facom.ufu.br/facom/equipe/corpo-docente"
    driver = webdriver.Firefox()
    driver.get(facomUrl)
    time.sleep(10)

    professors = {}

    htmlContent = driver.page_source
    soup = BeautifulSoup(htmlContent) # parse html content into tree

    divs = soup.findAll('div', attrs={'class': ['views-row-odd views-row-first separar-thumb', 'views-row-even separar-thumb', 'views-row-odd separar-thumb', 'views-row-odd views-row-last separar-thumb']})

    for div in divs:
        nameContainer = div.find('a')

        infos = "None"
        infosContainer = div.find('div', attrs={'class': 'field field-name-field-curso field-type-taxonomy-term-reference field-label-hidden'})
        if(infosContainer):
            infos = infosContainer.text

        googleUrl = "None"
        googleContainer = div.find('a', href=re.compile("google"))
        if(googleContainer):
            googleUrl = googleContainer.attrs["href"]

        linkedinUrl = "None"
        linkedinContainer = div.find('a', href=re.compile("linkedin"))
        imgUrl = ""
        if(linkedinContainer):
            linkedinUrl = linkedinContainer.attrs['href']
            linkedInUserName = ""

            # gerar link p/ img atraves do href
            # https://www.linkedin.com/in/user-name/overlay/photo/
            # pega apenas 'user-name' da url
            # 
            for i in range(28, len(linkedinUrl)):
                if linkedinUrl[i] != '/':
                    linkedInUserName += linkedinUrl[i]
                else:
                    break

            # linkedInUserName = "kaio-souza"
            imgUrl = loginTest.getImgTagSrc(linkedInUserName, loginBrowser)
            print(f'User: {imgUrl}')

        professors[nameContainer.text] = {
            "info": infos,
            "google": googleUrl,
            "linkedin": linkedinUrl,
            "picture": imgUrl
        }
    driver.close()
    loginBrowser.close()

    # parse 'professors' into JSON
    with open("facom.json", 'w') as profJsonFile:
        profJson = json.dumps(professors, indent = 3) # parse PY dict to JSON
        profJsonFile.write(profJson)

generateFacom()