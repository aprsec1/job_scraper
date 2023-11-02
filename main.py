from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import datetime
import os
import time


def extract_data(job_elements):
    companies = [comp.find("p", class_="job-company").get_text(strip=True) for comp in job_elements]
    job_titles = [job.find("p", class_="job-title").get_text(strip=True) for job in job_elements]
    links = [job.find("p", class_="job-title").find("a")["href"] for job in job_elements]
    return companies, job_titles, links


current_date = datetime.datetime.now().strftime("%Y-%m-%d")
folder_path = "C:\\Users\\Antonio\\PycharmProjects\\pythonProject\\web_scraper_project\\"
combined_data = []

# Set up Chrome WebDriver
service = Service('D:\\Tools\\Chrome_driver\\chromedriver.exe')  # Set the path to your ChromeDriver executable
driver = webdriver.Chrome(service=service)

# Start from the first page
base_url = "https://www.moj-posao.net/Pretraga-Poslova/?searchWord=&keyword=&job_title=&job_title_id=&skill=&skill_id=&area=2&category=11&page=1"
driver.get(base_url)
page_num = 1

try:
    while True:
        # Wait for the page to load
        time.sleep(3)  # Adjust the sleep time as needed

        doc = BeautifulSoup(driver.page_source, "html.parser")

        job_data_divs = doc.find_all("div", class_="job-data")
        test_csv = []

        for job_data_div in job_data_divs:
            logo = job_data_div.find_previous("img", class_="logo")
            if logo is not None:
                company_name = logo.get("title", "No Title Found")  # Use .get() method with a default value
            else:
                company_name = "No Company Name Found"  # Provide a default value when the logo is not found
            job_postings = job_data_div.find_all("a", attrs={"data-id": True})

            for posting in job_postings:
                if posting is not None:
                    job_position = posting.find("span", class_="job-position").get_text(strip=True)
                    job_link = posting["href"]
                    test_csv.append((company_name, job_position, job_link))

        job_name_1 = doc.find_all("div", class_="job type-5")
        companies_1, job_titles_1, links_1 = extract_data(job_name_1)
        job_name_2 = doc.find_all("div", class_="job type-4")
        companies_2, job_titles_2, links_2 = extract_data(job_name_2)
        job_name_3 = doc.find_all("div", class_="job type-3")
        companies_3, job_titles_3, links_3 = extract_data(job_name_3)
        job_name_4 = doc.find_all("div", class_="job type-1")
        companies_4, job_titles_4, links_4 = extract_data(job_name_4)

        datasets = [
            {
                'title': "Job Position",
                'data': test_csv
            },
            {
                'title': "Title",
                'data': list(zip(companies_1, job_titles_1, links_1))
            },
            {
                'title': "Title",
                'data': list(zip(companies_2, job_titles_2, links_2))
            },
            {
                'title': "Title",
                'data': list(zip(companies_3, job_titles_3, links_3))
            },
            {
                'title': "Title",
                'data': list(zip(companies_4, job_titles_4, links_4))
            }
        ]

        combined_data.extend(datasets)

        # Find the "Sljedeća stranica" (Next page) link and click it
        next_page_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Sljedeća stranica")

        if next_page_link and next_page_link.get_attribute("href"):
            next_page_link.click()
            page_num += 1
        else:
            break

    # After the loop, write the combined data to a single CSV file
    csv_filename = os.path.join(folder_path, f"combined_job_data_{current_date}.csv")

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";")
        csv_writer.writerow(["Title", "Job Position", "Link"])  # Write header row
        for dataset in combined_data:
            header = dataset['title']
            data = dataset['data']
            for row in data:
                csv_writer.writerow(row)

    print("CSV export completed.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    driver.quit()  # Quit the Selenium WebDriver when done
