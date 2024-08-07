import requests
from bs4 import BeautifulSoup

url = 'https://edition.cnn.com/?refresh=1'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find and save headlines and links
    articles = soup.find_all('span', class_='container__headline-text')

    with open('news_articles.txt', 'w') as file:
        if articles:
            print(f'Found {len(articles)} articles.')
        else:
            print('No articles found.')

        # Find all img tags
        img_tags = soup.find_all('img')

        # Create a dictionary to map article headlines to image URLs
        img_dict = {}
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                # Convert relative URLs to absolute URLs
                if not img_url.startswith('http'):
                    img_url = requests.compat.urljoin(url, img_url)
                # For simplicity, just use the first image found for each article
                img_dict[img_url] = img_url  # In practice, you might need a more sophisticated mapping

        # Write article titles, links, and images to the file
        for article in articles:
            title = article.text.strip()
            link = article.find_parent('a')['href']
            full_link = 'https://edition.cnn.com' + link if link.startswith('/') else link

            # Get an image URL if available
            img_url = list(img_dict.values())[0] if img_dict else 'No image found'

            file.write(f'Title: {title}\n')
            file.write(f'Link: {full_link}\n')
            file.write(f'Image: {img_url}\n\n')

    print('Scraping complete.')
else:
    print('Failed to fetch the webpage')
