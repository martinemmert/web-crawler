import requests
from bs4 import BeautifulSoup
import zipfile
import os
import sys
import inquirer
import html2text
from playwright.sync_api import sync_playwright, TimeoutError
from urllib.parse import urlparse


def load_config(config_file):
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


def save_to_file(directory, filename, content):
    with open(os.path.join(directory, filename), 'w', encoding='utf-8') as file:
        file.write(content)
        print(f"Saved file: {os.path.join(directory, filename)}")

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def fetch_website_content(url, use_playwright, wait_condition=None, timeout=30000):
    if use_playwright:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            try:
                if wait_condition:
                    if 'selector' in wait_condition:
                        page.wait_for_selector(wait_condition['selector'], timeout=timeout)
                    elif 'function' in wait_condition:
                        page.wait_for_function(wait_condition['function'], timeout=timeout)
            except TimeoutError:
                print(f"Timeout while waiting for condition at {url}")

            content = page.content()
            browser.close()
            return content
    else:
        response = requests.get(url)
        response.raise_for_status()
        return response.text



def extract_external_links(html_content, external_link_patterns, full_url):
    base_url = get_base_url(full_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.find('body')
    links = []
    for link in body_content.find_all('a', href=True):
        href = link['href']
        if href.startswith('/'):
            href = base_url + href
        if any(pattern in href for pattern in external_link_patterns):
            links.append(href)
    return links


def file_exists(directory, filename):
    return os.path.exists(os.path.join(directory, filename))


def convert_html_to_markdown(html_content):
    return html2text.html2text(html_content)


def process_website(url, external_link_patterns, use_playwright, wait_condition):
    try:
        print(f"Accessing URL: {url}")
        html_content = fetch_website_content(url, use_playwright, wait_condition)
        # Adjust link extraction process
        external_links = extract_external_links(html_content, external_link_patterns, url)
        markdown_content = convert_html_to_markdown(html_content)
        return markdown_content, external_links
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None, []


def choose_job():
    jobs = [f for f in os.listdir('jobs') if os.path.isfile(os.path.join('jobs', f))]
    questions = [inquirer.List('job', message="Choose a job", choices=jobs)]
    answers = inquirer.prompt(questions)
    return answers['job']


def main():
    try:
        job_name = sys.argv[1] if len(sys.argv) > 1 else choose_job()
        config_file = os.path.join('jobs', job_name)
        config = load_config(config_file)

        job_base_name = os.path.splitext(job_name)[0]
        output_dir = os.path.join('out', job_base_name)
        txt_subfolder = 'txt'
        external_link_patterns = config.get('external_link_patterns', '').split(',')
        use_playwright = config.get('use_playwright', 'False').lower() == 'true'
        wait_condition = None
        if 'wait_selector' in config:
            wait_condition = {'selector': config['wait_selector']}
        elif 'wait_function' in config:
            wait_condition = {'function': config['wait_function']}

        ensure_directory_exists(output_dir)
        ensure_directory_exists(os.path.join(output_dir, txt_subfolder))

        main_website_url = config['main_url']
        main_filename = os.path.basename(main_website_url) + ".md"

        files_to_zip = []

        if not file_exists(os.path.join(output_dir, txt_subfolder), main_filename):
            markdown_content, external_links = process_website(main_website_url, external_link_patterns, use_playwright,
                                                               wait_condition)
            if markdown_content:
                save_to_file(os.path.join(output_dir, txt_subfolder), main_filename, markdown_content)
                files_to_zip = [os.path.join(txt_subfolder, main_filename)]
                for link in external_links:
                    filename = os.path.basename(link) + ".md"
                    if not file_exists(os.path.join(output_dir, txt_subfolder), filename):
                        content, _ = process_website(link, external_link_patterns, use_playwright, wait_condition)
                        if content:
                            save_to_file(os.path.join(output_dir, txt_subfolder), filename, content)
                            files_to_zip.append(os.path.join(txt_subfolder, filename))
                    else:
                        print(f"File already exists: {os.path.join(txt_subfolder, filename)}")

        zip_path = os.path.join(output_dir, f'{job_base_name}_resources.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files_to_zip:
                zipf.write(os.path.join(output_dir, file), file)
                print(f"Added to zip: {file}")

        print(f"Zip file created: {zip_path}")

    except KeyboardInterrupt:
        print("Aborted by the user.")


if __name__ == "__main__":
    main()
