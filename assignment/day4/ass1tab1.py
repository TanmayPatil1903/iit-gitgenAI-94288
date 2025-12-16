#1. Scrape Internship information and batches from Sunbeam website.
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_internship_info(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)

    internships = []
    internships_elements = driver.find_element(By.CLASS_NAME,"list_style")
    table_body = internships_elements.find_element(By.TAG_NAME,"tbody")
    table_rows = table_body.find_elements(By.TAG_NAME,"tr")
    for row in table_rows:
        cols = row.find_elements(By.TAG_NAME,"td")
        if len(cols) < 5:
            continue
        internship = {
            "Technology":cols[0].text,
            "Aim":cols[1].text,
            "Prerequisite":cols[2].text,
            "Learning":cols[3].text,
            "Location":cols[4].text
        }
        
        internships.append(internship)
    driver.quit()
    return internships


if __name__ == "__main__":
    url = "https://www.sunbeaminfo.in/internship"
    intrnships = scrape_internship_info(url)
    for intrn in intrnships:
        print(intrn)