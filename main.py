import requests
import xml.etree.ElementTree as ET

# Configuration
SITEMAP_URL = "https://trovit.tn/news/sitemap.xml"  # Replace with your sitemap URL
INDEXNOW_ENDPOINT = "https://indexnow.yep.com/indexnow"
API_KEY = ""  # Replace with your API key

def fetch_sitemap_urls(sitemap_url):
    """Fetch and parse URLs from the sitemap."""
    response = requests.get(sitemap_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch sitemap: {response.status_code}")
    
    root = ET.fromstring(response.content)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]
    return urls

def submit_to_indexnow(urls, api_key):
    """Submit URLs to the IndexNow API."""
    payload = {
        "host": SITEMAP_URL.split('/')[2],  # Extract host from sitemap URL
        "key": api_key,
        "keyLocation": f"https://{SITEMAP_URL.split('/')[2]}/indexnow-key.txt",  # Update if needed
        "urlList": urls
    }
    
    response = requests.post(INDEXNOW_ENDPOINT, json=payload)
    if response.status_code == 200:
        print("URLs submitted successfully!")
    else:
        print(f"Failed to submit URLs: {response.status_code} - {response.text}")

# Main Execution
try:
    urls = fetch_sitemap_urls(SITEMAP_URL)
    print(f"Fetched {len(urls)} URLs from the sitemap.")
    submit_to_indexnow(urls, API_KEY)
except Exception as e:
    print(f"Error: {e}")
