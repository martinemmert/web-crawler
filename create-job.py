import inquirer
import os


def create_job_config():
    questions = [
        inquirer.Text('main_url', message="Enter the main URL to crawl"),
        inquirer.Text('external_link_patterns', message="Enter comma-separated domains or patterns to follow"),
        inquirer.List('use_playwright', message="Use Playwright for JavaScript-rendered content?",
                      choices=['True', 'False']),
        inquirer.Text('wait_selector', message="Enter a CSS selector to wait for (optional, press enter to skip)",
                      default=""),
        inquirer.Text('wait_function',
                      message="Enter a JavaScript condition to wait for (optional, press enter to skip)", default=""),
        inquirer.Text('filename', message="Enter the filename for this job configuration", default="new_job.txt")
    ]

    answers = inquirer.prompt(questions)

    config_content = (
        f"main_url={answers['main_url']}\n"
        f"external_link_patterns={answers['external_link_patterns']}\n"
        f"use_playwright={answers['use_playwright']}\n"
    )

    if answers['wait_selector']:
        config_content += f"wait_selector={answers['wait_selector']}\n"
    if answers['wait_function']:
        config_content += f"wait_function={answers['wait_function']}\n"

    with open(os.path.join('jobs', answers['filename']), 'w') as config_file:
        config_file.write(config_content)

    print(f"Job configuration saved as {answers['filename']}")


if __name__ == "__main__":
    create_job_config()
