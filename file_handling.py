import os
import time
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


# todo: add logs for user
# todo: Ensure that the file content is legal to scrape.
# todo: Ensure the path/file is valid before processing
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def parse_job_listing(job, base_url="https://mockwebsite.com"):
    title = job.find(class_='title').text.strip() if job.find(class_='title') else 'Not Available'
    company = job.find('p', class_='company').text.strip() if job.find('p', 'company') else 'Not Available'
    location = job.find('p', class_='location').text.strip() if job.find('p', 'location') else 'Not Available'
    apply_link = job.find('a', class_='apply')['href'].strip() if job.find('a', class_='apply') else 'Not Available'

    # Convert relative URLs to absolute URLs
    if apply_link != 'Not Available':
        apply_link = urljoin(base_url, apply_link)

    print(f"Job Title: {title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print(f"Apply Link: {apply_link}")
    print('-' * 60)

    return {
        'Title': title,
        'Company': company,
        'Location': location,
        'Apply Link': apply_link
    }


# todo: Consider adding functionality to process all HTML files in a selected directory,
#  generating a CSV for each file automatically or one file for all of them.
def process_html_file(filepath):
    html_content = read_file(filepath)
    parsed_html = BeautifulSoup(html_content, 'html.parser')
    job_listings = parsed_html.find_all('div', class_='job')
    jobs = [parse_job_listing(job) for job in job_listings]

    return jobs


# todo: Consider adding a check to limit the number of CSV files in the directory (for example 1000)
#  to avoid excessive storage usage, after the maximum number of files is reached, the oldest file in the directory
#  will be replaced with the new one. Or maybe you can save them in db
def save_to_csv(jobs, directory='jobs_csv'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    # todo: give name base on the file name and other distinct variables
    # Generate a unique filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(directory, f'jobs_{timestamp}.csv')

    # Save the jobs list to the CSV file
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False, encoding='utf-8')
    # todo: print(f"CSV file created: {filename}")
