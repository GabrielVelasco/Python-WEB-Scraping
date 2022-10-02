##################################################################################
#										 #
#				THIS IS A MODEL TO BE EDITED                     #	
#										 #
##################################################################################

from ast import Break
from cgi import print_arguments
from sre_constants import BRANCH
from attr import attr
from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
import json
# import panda as pd

driver = webdriver.Firefox()

def generateFacom():
    facomUrl = "file:///home/gabriel1908/OneDrive/Documents/Prog/WEB/webScrap/simple.html"
    driver.get(facomUrl)
    professors = {}

    htmlContent = driver.page_source
    soup = BeautifulSoup(htmlContent) # parse html content into html tree
    # print(f'RESULTS == {soup.prettify()}')

    divs = soup.findAll('div', attrs={'class': ['profData1', 'profData2']})

    for div in divs:
        nameContainer = div.find('h2', attrs={'class': 'name'})
        depatContainer = div.find('p', attrs={'class': 'depart'})
        photoContainer = div.find('img', attrs={'class': 'photo'})
        emailContainer = div.find('p', attrs={'class': 'email'})

        professors[nameContainer.text] = {
            "email": emailContainer.text,
            "department": depatContainer.text,
            "photo": photoContainer.attrs['src']
        }

    # parse 'professors' into JSON
    with open("facom.json", 'w') as profJsonFile:
        profJson = json.dumps(professors, indent = 3) # aprse PY dict to JSON
        profJsonFile.write(profJson)

generateFacom()
