import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
import dateutil.parser

def fetch_bbc_article_content(article_url):
    """Fetch the full content of an article from its URL, based on the provided HTML structure."""
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the main article content
    article_section = soup.find('article')  # Assuming the content is within an <article> tag
    if article_section:
        content = []
        # Extract the title
        title = article_section.find('h1').get_text() if article_section.find('h1') else 'No Title'
        content.append(f"Title: {title}")

        # Extract publication date/time
        time_tag = article_section.find('time')
        publication_date = time_tag.get('datetime') if time_tag else 'No Date'
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

def fetch_bbc_articles(days=1):
    """Fetch articles from BBC and retrieve their full content."""
    url = 'https://www.bbc.com/news/war-in-ukraine'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get today's and yesterday's date
    current_time = datetime.now()
    date_limit = current_time - timedelta(days=days)

    articles = []
    for article in soup.find_all('a', href=True):
        if '/news/' in article['href']:
            link = article['href']
            full_link = 'https://www.bbc.com' + link

            # Send a request to the article page to get more details
            article_response = requests.get(full_link)
            article_soup = BeautifulSoup(article_response.content, "html.parser")
            
            # Extract article date
            time_tag = article_soup.find('time')
            if time_tag:
                article_date = dateutil.parser.parse(time_tag.get('datetime'))
                if article_date.tzinfo is not None:
                    article_date = article_date.replace(tzinfo=None)
                
                if article_date < date_limit:
                    continue  # Skip articles older than the date limit
            else:
                article_date = None
            
            # Extract headline
            title = article.get_text(strip=True)
            
            # Fetch the full article content
            full_content = fetch_bbc_article_content(full_link)

            articles.append({
                'title': title,
                'link': full_link,
                'date': article_date.isoformat() if article_date else 'No Date',
                'full_content': full_content
            })

    return articles

def save_articles_to_json(articles, filename="bbc_articles.json"):
    """Save articles to a JSON file."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Fetch articles from the last two days
    articles = fetch_bbc_articles(days=2)

    # Save the articles to a JSON file
    save_articles_to_json(articles)
    
    print(f"Scraped and saved {len(articles)} articles from BBC")
