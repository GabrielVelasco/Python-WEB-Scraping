from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json
import re
import time
import login_service
import requests
import os

def download_and_save_image(url, filename):
    # baixa imagem da 'url' e salva como 'filename'

    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded and saved as {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def get_user_name_from_linkedin_url(linkedin_url):
    # pega o 'user_name' do perfil do linkedin (href)

    linkedin_user_name = ""
    for i in range(28, len(linkedin_url)):
        if linkedin_url[i] != '/':
            linkedin_user_name += linkedin_url[i]
        else:
            break

    return linkedin_user_name

def generateFacom():
    professors = []

    try:
        download_linkedin_img = False
        if download_linkedin_img:
            logged_browser = login_service.doLogin()    # login in linkedin and return browser (to be able to download profile pictures)

        facom_url = "https://facom.ufu.br/facom/equipe/corpo-docente"

        os.environ['MOZ_HEADLESS'] = '1' # hide firefox execution
        driver = webdriver.Firefox()

        driver.get(facom_url)
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete') # wait for page to load

        html_content = driver.page_source
        soup = BeautifulSoup(html_content) # parse html content into tree

        divs = soup.findAll('div', attrs={'class': ['views-row-odd views-row-first separar-thumb', 'views-row-even separar-thumb', 'views-row-odd separar-thumb', 'views-row-odd views-row-last separar-thumb']})

        for div in divs:
            name_div = div.find('a')

            infos = "None"
            infos_div = div.find('div', attrs={'class': 'field field-name-field-curso field-type-taxonomy-term-reference field-label-hidden'})
            if infos_div:
                infos = infos_div.text

            google_url = "None"
            google_profile_div = div.find('a', href=re.compile("google"))
            if google_profile_div:
                google_url = google_profile_div.attrs["href"]

            linkedin_profile_url = "None"
            linkedin_profile_div = div.find('a', href=re.compile("linkedin"))
            linkedin_prof_img_url = ""
            if linkedin_profile_div:
                linkedin_profile_url = linkedin_profile_div.attrs['href']

                if download_linkedin_img:
                    # baixar a imagem do perfil do linkedin, caso queira
                    # pega o 'user_name' do perfil do linkedin (href)
                    linkedin_user_name = get_user_name_from_linkedin_url(linkedin_profile_url)

                    # Ex: linkedin_user_name = "kaio-souza"
                    linkedin_prof_img_url = login_service.get_img_url_from_profile(linkedin_user_name, logged_browser)
                    print(f'User: {linkedin_prof_img_url}')

                    # search substring 'media' (means that linkedIn prof has a picture) in imgUrl, if found run function download_and_save_image
                    if linkedin_prof_img_url.find('media') != -1: 
                        download_and_save_image(linkedin_prof_img_url, f'facom/{name_div.text}.jpg')

            # create a new professor dict
            professor = {}
            professor["name"] = name_div.text
            professor["infos"] = infos
            professor["google"] = google_url
            professor["linkedin"] = linkedin_profile_url

            professors.append(professor)
    
    except Exception as e:
        print("An error occurred... closing browser")

    driver.close()
    # if download_linkedin_img:
    #     loginBrowser.close()

    with open("facom.json", 'w') as profJsonFile:
        profJson = json.dumps(professors, indent = 3, ensure_ascii=False) 
        profJsonFile.write(profJson)

generateFacom()