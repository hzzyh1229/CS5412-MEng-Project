from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

driver = webdriver.Chrome(ChromeDriverManager().install())
# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")
time.sleep(2)
# entering username
username = driver.find_element(By.ID, "username")
username.send_keys("hzzbsch@gmail.com")
# entering password
pword = driver.find_element(By.ID, "password")
pword.send_keys("cs5412")
# Clicking on the log in button
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Opening job's page
job_url = "https://www.linkedin.com/jobs/"
driver.get(job_url)
time.sleep(2)
# entering search keywords
search = driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-keyword-id-ember')]")
search.send_keys("software engineer")
time.sleep(2)
search.send_keys(Keys.RETURN)
time.sleep(2)

# scroll to load whole page
def scroll():
    print("start scrolling", end = ' ')
    left_panel = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
    time.sleep(1)
    verical_ordinate = 100
    for i in range(0, 10):
        print(".", end = ' ')
        driver.execute_script("arguments[0].scrollTop = arguments[1]", left_panel, verical_ordinate)
        verical_ordinate += 1000
        time.sleep(1)
    print("done scrolling")

# process jobs on one page
def process_page():
    job_src = driver.page_source
    #soup = BeautifulSoup(job_src, 'lxml')
    soup = BeautifulSoup(job_src, "html.parser")
    # get the list of job titles
    jobs_html = soup.find_all('a', {'class': 'job-card-list__title'})
    
    # loop through jobs on this page
    for title in jobs_html:
        try:
            job_data = {}
            print("processing position: " + title.text.strip())
            job_data["position"] = title.text.strip()

            # click on each job to get detailed information
            driver.find_element(By.LINK_TEXT, title.text.strip()).click()
            time.sleep(2)
            detail_src = driver.page_source
            soup = BeautifulSoup(detail_src, 'html.parser')
            detail = soup.find('section', {'class': 'scaffold-layout__detail'})

            # get job id
            url = driver.current_url
            index_start = url.find('currentJobId=') + 13
            index_end = url.find('&keywords=')
            info_id = url[index_start:index_end] if (index_start != -1 and index_end != -1) else ""
            job_data["job_id"] = info_id

            # get company name
            info_company = soup.find('span', {'class': 'jobs-unified-top-card__company-name'})
            job_data["company"] = info_company.text.strip() if info_company is not None else ""

            # get date posted
            info_date = soup.find('span', {'class': 'jobs-unified-top-card__posted-date'})
            job_data["date"] = info_date.text.strip() if info_date is not None else ""

            # get type and level
            info_type = soup.find('li', {'class': 'jobs-unified-top-card__job-insight'})
            job_data["type"] = info_type.text.strip() if info_type is not None else ""

            # get description
            info_description = soup.find('div', {'class': 'jobs-description-content'})
            job_data["description"] = info_description.text.strip() if info_description is not None else ""
            data.append(job_data)
        except:
            print("something wrong here :(")

# loop through the pages
page_lst = driver.find_element(By.CLASS_NAME, "artdeco-pagination__pages")
pages = page_lst.find_elements(By.TAG_NAME, "li")
start = int(pages[0].text)
end = int(pages[-1].text)
end = max(20, end)
data = []
time.sleep(2)

for page in range(start, end+1):
    driver.find_element(By.XPATH, "//button[@aria-label='Page " + str(page) + "']").click()
    time.sleep(2)
    print("currently on page: " + str(page))
    try:
        scroll()
        print("after scroll")
        process_page()
        print("after process")
        print("================================================")
    except:
        print("something wrong here :(")


# dump into json file
json_object = json.dumps(data)
with open(("LinkedIn" + datetime.today().strftime('%Y%m%d%H%M') + ".json"), "w") as outfile:
    outfile.write(json_object)