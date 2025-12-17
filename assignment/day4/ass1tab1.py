from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_internship_info(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 30)
    internships = []

    try:
        # Wait until at least one row is present
        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tr")))

        rows = driver.find_elements(By.XPATH, "//table//tr")

        if len(rows) <= 1:
            print("Table found but no data rows.")
            return []

        for row in rows[1:]:  # skip header
            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) >= 5:
                internships.append({
                    "Technology": cols[0].text,
                    "Aim": cols[1].text,
                    "Prerequisite": cols[2].text,
                    "Learning": cols[3].text,
                    "Location": cols[4].text
                })

    except Exception as e:
        print("Error:", e)

    driver.quit()
    return internships


if __name__ == "__main__":
    url = "https://www.sunbeaminfo.in/internship"
    data = scrape_internship_info(url)

    if not data:
        print("No data found!")
    else:
        for d in data:
            print(d)
