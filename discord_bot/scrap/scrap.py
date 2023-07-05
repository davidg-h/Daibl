import json
import os
import re
import time
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sys


def get_links():
    print(sys.path)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.google.com")
    links = driver.find_elements(By.CSS_SELECTOR, "a")
    print(links)

def urls_to_array(path):
    urls=[]
    with open(path, "r") as file:
        count = 0
        while True:
            count += 1
        
            line = file.readline()
            if not line:
                break
            urls.append(line)
    return urls

def sort_urls():
    urls= urls_to_array("discord_bot/scrap/allUrls.txt")

    urls = [url for url in urls if url.startswith("https://www.th-nuernberg.de")]
    urls = [url.replace("\n", "") for url in urls]
    urls = [url.split("#")[0] for url in urls]
    urls.sort()
    # remove dublicates
    urls = list(dict.fromkeys(urls))

    with open("discord_bot/scrap/allUrlsFiltered.txt", "w") as file:
        for url in urls:
            file.write(url+"\n")


def download_pages(urls):
    path = "discord_bot/scrap/htmlfiles/"
    with requests.Session() as session:
    
        for url in urls:
            
            url = url.replace("\n", "")
            filename = url.replace("https://www.th-nuernberg.de/", "file_")
            filename = filename.replace("/", ">")
            filename = path + filename
            print(filename)
            # check, if file exists
            if not os.path.isfile(filename):
                response = session.get(url)
                if response.ok: 
                    with open(filename, "w+", encoding="utf-8") as file:
                        file.write(response.text)
                else:
                    print(f"Error reading {url}")
            else:
                print(f"File already exists: {filename}")
                pass
            
            # add grace period in seconds, if necessary
            time.sleep(0.2)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_content(file):
    soup = BeautifulSoup(file,"lxml")
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def create_content_json(path_html_files, outfile_name):
    html_contents = []
    for html_file in os.listdir(path_html_files):
        try: 
            html_file = "discord_bot/scrap/htmlfiles/" + html_file
            print(html_file)
            with open(html_file, "r", encoding="utf-8") as file:
                html_contents.append(get_content(file))
        except:

            html_contents.append("")

            
            
    
    with open(outfile_name, "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(html_contents)) 

# urls= urls_to_array("discord_bot/scrap/allUrlsFiltered.txt")          
# download_pages(urls=urls)

create_content_json("discord_bot/scrap/htmlfiles", "discord_bot/scrap/html_contents.json")

# with requests.Session() as session:
#     response = session.get("https://www.th-nuernberg.de/")
#     print(response.text)