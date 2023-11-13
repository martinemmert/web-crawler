# Web Crawler Script

This Python script is designed to crawl websites and extract content, optionally using Playwright for JavaScript-heavy pages. It's configurable to handle different crawling jobs, each with its own set of rules and targets.

## Features

- Crawl static and dynamic web pages.
- Configurable for different crawling tasks.
- Option to use Playwright for JavaScript-rendered content.
- Extract and convert content to Markdown.
- Handle relative links correctly by appending them to the base URL.
- Graceful handling of keyboard interruptions.

## Prerequisites

To use this script, you will need:
- Python 3.8 or higher.
- [Playwright](https://playwright.dev/python/docs/intro) for Python, if you intend to crawl JavaScript-heavy pages.
- Other Python dependencies: `requests`, `beautifulsoup4`, `html2text`, `inquirer`.

## Installation

1. **Install Python Dependencies**:

`pip install requests beautifulsoup4 html2text inquirer playwright`

2. **Install Playwright Browsers**:

`playwright install`

3. **Clone or Download This Script**:
- Clone this repository or download the script to your local machine.

## Configuration

Create job configuration files in the `jobs` directory with the following format:

```
main_url=<URL to crawl>
external_link_patterns=<comma-separated domains or patterns to follow>
use_playwright=<True/False to use Playwright>
wait_selector=<CSS selector to wait for (optional)>
wait_function=<JavaScript condition to wait for (optional)>
```

For example:

```
main_url=https://example.com
external_link_patterns=example.com,relateddomain.com
use_playwright=True
wait_selector=.content
```

## Usage

Run the script from the command line:

`python crawler_script.py [job configuration file]`


If you don't specify a job configuration file, the script will prompt you to choose one from the `jobs` directory.

## Notes

- Make sure to respect the terms of service and robots.txt of the websites you are crawling.
- The script can be stopped at any time by pressing Ctrl+C, and it will exit with the message "Aborted by the user."

## Contributing

Feel free to fork this repository or submit pull requests with improvements.

# Job Configuration Generator CLI
In addition to the main crawler script, a separate CLI tool is provided to simplify the creation of job configuration files.

## Usage
Run the job configuration generator script from the command line:

```
python create-job.py
```
The script will prompt you with a series of questions:

1. **Main URL:** The URL of the website you want to crawl.
2. **External Link Patterns:** Comma-separated list of domains or patterns for external links that the crawler should follow.
3. **Use Playwright:** Specify whether to use Playwright for JavaScript-rendered content. Choose 'True' or 'False'.
4. **Wait Selector (optional):** A CSS selector to wait for before crawling the page. Leave blank if not needed.
5. **Wait Function (optional):** A JavaScript condition to wait for before crawling the page. Leave blank if not needed.
6. **Filename:** The name for the new job configuration file.

After answering these questions, the script will create a new job configuration file in the jobs directory with your specified settings.

## Example
When you run the script, it will look like this:

```
Enter the main URL to crawl: https://example.com
Enter comma-separated domains or patterns to follow: example.com,relateddomain.com
Use Playwright for JavaScript-rendered content? (True/False): True
Enter a CSS selector to wait for (optional, press enter to skip): .content
Enter a JavaScript condition to wait for (optional, press enter to skip): 
Enter the filename for this job configuration: example_job.txt
Job configuration saved as example_job.txt
```

This process creates a job configuration file named example_job.txt in the jobs directory based on your inputs.

## License

This script is released under [MIT License](https://opensource.org/licenses/MIT).
