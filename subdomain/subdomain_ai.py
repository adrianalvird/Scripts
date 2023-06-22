import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse

def get_subdomains_ai(url):
    subdomains = set()

    # Make a request to the given URL
    response = requests.get(url)
    if response.status_code == 200:
        # Extract the domain from the URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the anchor tags in the HTML
        anchor_tags = soup.find_all('a')

        # Extract subdomains from the anchor tags' href attributes
        for tag in anchor_tags:
            href = tag.get('href')
            if href:
                # Check if the href attribute contains a subdomain
                subdomain = urlparse(href).netloc
                if subdomain:
                    subdomains.add(subdomain)

    return subdomains

def get_subdomains_google_dork(url):
    subdomains = set()

    # Use Google Dorking to find subdomains
    google_url = f"https://www.google.com/search?q=site:{url}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(google_url, headers=headers)
    if response.status_code == 200:
        # Use regex to extract subdomains from Google search results
        subdomains_list = re.findall(r'\b(?:https?://|www\.)\S+\b', response.text)
        for subdomain in subdomains_list:
            parsed_url = urlparse(subdomain)
            domain = parsed_url.netloc
            if domain:
                subdomains.add(domain)

    return subdomains

def main():
    parser = argparse.ArgumentParser(description='Find subdomains of a website using AI and Google Dorking.')
    parser.add_argument('-u', '--url', type=str, help='URL of the website')
    args = parser.parse_args()

    if args.url:
        url = args.url
        subdomains_ai = get_subdomains_ai(url)
        subdomains_google_dork = get_subdomains_google_dork(url)

        subdomains = subdomains_ai.union(subdomains_google_dork)

        if subdomains:
            print("Subdomains found:")
            for subdomain in subdomains:
                print(subdomain)
        else:
            print("No subdomains found.")
    else:
        print("Please provide the URL using -u or --url argument.")

if __name__ == '__main__':
    main()

