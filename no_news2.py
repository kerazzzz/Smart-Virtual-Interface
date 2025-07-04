import requests
from bs4 import BeautifulSoup

url = "https://www.setopati.com/"

response = requests.get(url)
print(response)
if response.status_code == 200:
    soup = BeautifulSoup(response.content,'html.parser')
    headlines = soup.find_all(class_ = 'breaking-news-item' )

    for headline in headlines:
        print(headline.get_text(strip=True))
else:
        print('Article cannot be found')