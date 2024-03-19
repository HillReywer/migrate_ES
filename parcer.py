import requests
from bs4 import BeautifulSoup
import re
import os

def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)

def fetch_and_save_article(url):
    print(f"Processing: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "Title Not Found"
    title = sanitize_filename(title)
    print(f"Title: {title}")
    
    content = ""
    notion_elements = soup.find_all(class_=re.compile("^notion"))
    for element in notion_elements:
        content += str(element) + "\n\n"
    
    if not content:
        content = "Content Not Found"
        print("Content Not Found")
    
    os.makedirs('articles', exist_ok=True)
    file_path = os.path.join('articles', f"{title}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_article_links(url):
    links = []
    domain = urlparse(url).netloc
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/') or domain in href:
            full_url = requests.compat.urljoin(url, href)
            links.append(full_url)
    
    return links

def main():
    url = 'https://exil-solidaire.fr'
    article_links = get_article_links(url)
    for link in article_links:
        fetch_and_save_article(link)

if __name__ == "__main__":
    main()
