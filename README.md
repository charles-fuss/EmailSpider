# EmailSpider

# Email Crawler

This Python script is designed to crawl and extract email addresses from a given website. The script navigates through the website's pages, extracting email addresses and saving them into a list. It uses the `requests` library to fetch web pages and the `lxml` library to parse the HTML content.

## Features

- Crawl through a given website to find email addresses
- Save email addresses to a list
- Skip URLs with specified file extensions (images, videos, etc.)
- Customizable email extraction and URL filtering

## Requirements

- Python 3.x
- requests
- lxml
- validators

## Installation

1. Clone the repository or download the provided code snippet.
2. Install the required Python libraries by running the following command:

```bash
pip install requests lxml validators
```

## Usage
Import the EmailCrawler class from the script.
Instantiate an EmailCrawler object with the desired website URL and a name.
Call the crawl() method on the object to start the crawling process and obtain the results.

Example:
```python
from email_crawler import EmailCrawler

crawler = EmailCrawler("example", "https://www.example.com")
name, email_count, emails = crawler.crawl()

print(f"Website: {name}")
print(f"Total emails found: {email_count}")
print("Email addresses:", emails)
```

I also added the file, ExcelReader, to read each entry from a predefined column to pass into the crawler. This is helpful for lead generation if you have a large list of company URL leads from an excel sheet, the script will read in the URLs and return the same excel sheet, except with a new column,  . At least that's what I wrote the script for anyways.

## Customization
You can customize the script by modifying the URL filtering, email extraction, or output formatting as needed.

## Disclaimer
Please note that web crawling and email extraction may be against the terms of service for some websites. This script is provided for educational purposes only. Use at your own risk and ensure you have permission to access and crawl the websites in question.
