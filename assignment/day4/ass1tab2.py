import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_internship_info(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(5)

    internships = []
    internships_elements = driver.find_element(By.CLASS_NAME,"table-responsive")
    internships_elements_ele = internships_elements.find_element(
    By.CSS_SELECTOR, "table.table-bordered.table-striped")

    table_body = internships_elements_ele.find_element(By.TAG_NAME,"tbody")
    table_rows = table_body.find_elements(By.TAG_NAME,"tr")
    for row in table_rows:
        cols = row.find_elements(By.TAG_NAME,"td")
        if len(cols) < 5:
            continue
        internship = {
            "Sr.No":cols[0].text,
            "Batch":cols[1].text,
            "Start Date":cols[2].text,
            "End Date":cols[3].text,
            "Time":cols[4].text,
            "Fees":cols[5].text,
            "Download Brochure":cols[6].text
        }
        
        internships.append(internship)
    driver.quit()
    return internships

if __name__== "_main_":
    url = "https://www.sunbeaminfo.in/internship"
    intrnships = scrape_internship_info(url)
    for intrn in intrnships:
        print(intrn)