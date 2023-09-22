from bs4 import BeautifulSoup
import requests
import csv
import datetime
import os

def extract_data(job_elements):
    companies = [comp.find("p", class_="job-company").get_text(strip=True) for comp in job_elements]
    job_titles = [job.find("p", class_="job-title").get_text(strip=True) for job in job_elements]
    links = [job.find("p", class_="job-title").find("a")["href"] for job in job_elements]
    return companies, job_titles, links

try:
    url = "https://www.moj-posao.net/Pretraga-Poslova/?searchWord=&keyword=&job_title=&job_title_id=&skill=&skill_id=&area=2&category=11"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    job_data_divs = doc.find_all("div", class_="job-data")
    test_csv = []
    for job_data_div in job_data_divs:
        company_name = job_data_div.find_previous("img", class_="logo")["title"]
        job_postings = job_data_div.find_all("a", attrs={"data-id": True})

        for posting in job_postings:
            job_position = posting.find("span", class_="job-position").get_text(strip=True)
            job_link = posting["href"]
            test_csv.append((company_name, job_position, job_link))

    job_name_1 = doc.find_all("div", class_="job type-5")
    companies_1, job_titles_1, links_1 = extract_data(job_name_1)
    job_name_2 = doc.find_all("div", class_="job type-4")
    companies_2, job_titles_2, links_2 = extract_data(job_name_2)
    job_name_3 = doc.find_all("div", class_="job type-3")
    companies_3, job_titles_3, links_3 = extract_data(job_name_3)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    folder_path = "C:\\Users\\Antonio\\PycharmProjects\\pythonProject\\web_scraper_project\\"
    combined_data = []
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
        }
    ]

    csv_filename = os.path.join(folder_path, f"combined_job_data_{current_date}.csv")

    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";")
        csv_writer.writerow(["Title", "Job Position", "Link"])  # Write header row
        for dataset in datasets:
            header = dataset['title']
            data = dataset['data']

            for row in data:
                csv_writer.writerow(row)

    print("CSV export completed.")

except Exception as e:
    print(f"An error occurred: {str(e)}")