import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <h3> tags with the class 'post-title entry-title'
        h3_tags = soup.find_all('h3', class_='post-title entry-title')

        # Extract the href and text from <a> tags within these <h3> tags
        links_and_texts = [(a.get('href'), a.get_text(strip=True)) for h3 in h3_tags for a in h3.find_all('a') if a.get('href')]

        # Write the links and texts to a text file
        with open('game-list.txt', 'w') as file:
            if links_and_texts:
                print("Game totals: ", len(links_and_texts))
                for href, text in links_and_texts:
                    file.write(f"Name: {text}\nLink: {href}\n")
                    file.write("\n")
                    print(f"Name: {text}\nLink: {href}\n")
            else:
                file.write('No games found.')
                print('No games found.')
    else:
        print('Failed to fetch the webpage')

def main():
    while True:
        choice = int(input('Made specially for heaven12bluesky.blogspot.com\n 1. Pre-made URL\n 2. Custom URL\n 3. Exit \n Option : '))
        match choice:      
            case 3:
                break
            case 1:
                base_year = input("Find based on year (e.g., 2024): ")
                base_month = input("Find based on month (e.g., 06): ")
                print("\n")
                url = f"https://heaven12bluesky.blogspot.com/{base_year}/{base_month}/"
                scrape_website(url)
            case 2:
                custom_url = input("Enter the custom URL: ")
                scrape_website(custom_url)
            case _:
                print("Invalid choice. Please enter '1', '2', or '3'.")

if __name__ == "__main__":
    main()
