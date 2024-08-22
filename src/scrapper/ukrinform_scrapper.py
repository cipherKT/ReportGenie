import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
import dateutil.parser

def fetch_article_content(article_url):
    """Fetch the full content of an article from its URL, based on the provided HTML structure."""
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the main article content
    article_section = soup.find('article')  # Assuming the content is within an <article> tag
    if article_section:
        content = []
        # Extract the title
        title = article_section.find('h2').get_text() if article_section.find('h2') else 'No Title'
        content.append(f"Title: {title}")

        # Extract publication date/time
        time_tag = article_section.find('time')
        publication_date = time_tag.get_text() if time_tag else 'No Date'
        content.append(f"Published on: {publication_date}")

        # Extract main article text
        paragraphs = article_section.find_all('p')
        article_text = "\n\n".join(p.get_text() for p in paragraphs)
        content.append(f"\nArticle Content:\n{article_text}")

        # Extract image URL
        image_tag = article_section.find('img')
        image_url = image_tag['src'] if image_tag else 'No Image'
        content.append(f"\nImage URL: {image_url}")

        return "\n".join(content)
    else:
        return "Article content not found"

def fetch_ukrinform_articles(days=1):
    """Fetch articles from Ukrinform and retrieve their full content."""
    url = 'https://www.ukrinform.net/rubric-ato'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get today's and yesterday's date
    current_time = datetime.now()
    date_limit = current_time - timedelta(days=days)

    articles = []
    for article in soup.find_all('article', {'data-id': True}):
        date = dateutil.parser.parse(article.find('time')['datetime'])
        
        # Make both date and date_limit offset-naive by removing timezone information
        if date.tzinfo is not None:
            date = date.replace(tzinfo=None)

        if date < date_limit:
            continue  # Skip articles older than the date limit

        title = article.find('h2').get_text()
        link = article.find('h2').find('a')['href']
        full_link = 'https://www.ukrinform.net' + link
        image_tag = article.find('img')
        image_url = image_tag['src'] if image_tag else None
        summary = article.find('p').get_text()

        # Fetch the full article content
        full_content = fetch_article_content(full_link)

        articles.append({
            'title': title,
            'link': full_link,
            'date': date.isoformat(),
            'image_url': image_url,
            'summary': summary,
            'full_content': full_content
        })

    return articles

def save_articles_to_json(articles, filename="ukrinform_articles.json"):
    """Save articles to a JSON file."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Fetch articles from the last two days
    articles = fetch_ukrinform_articles(days=2)

    # Save the articles to a JSON file
    save_articles_to_json(articles)
    
    print(f"Scraped and saved {len(articles)} articles from Ukrinform")
