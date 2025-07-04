import requests
from bs4 import BeautifulSoup
import re
from gtts import gTTS
import os

def setopati():
    url = "https://www.setopati.com/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract breaking news headlines
        headlines = soup.find_all(class_="breaking-news-item")
        
        # Extract news descriptions
        descriptions = soup.find_all(class_="description")

        # Prepare text for speech
        text_to_speak = "ताजा समाचार हेडलाइन: \n"

        print("Breaking News Headlines:")
        for headline in headlines:
            text = headline.get_text(strip=True)
            text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
            print("-", text)
            text_to_speak += text + ".\n"

        text_to_speak += "\nसमाचार विवरण:\n"
        print("\nNews Descriptions:")
        for desc in descriptions:
            text = desc.get_text(strip=True)
            text = re.sub(r'\s+', ' ', text)  # Remove extra spaces

            # Filter out unwanted contact information
            if "setopati@gmail.com" in text or any(char.isdigit() for char in text[:15]):
                continue  # Skip descriptions with contact details

            print("-", text)
            text_to_speak += text + ".\n"

        # Convert text to speech in Nepali
        tts = gTTS(text=text_to_speak, lang="ne", slow=False)
        tts.save("news.mp3")

        # Play the generated audio file
        os.system("start news.mp3")  # Windows
        # os.system("mpg321 news.mp3")  # Linux
        # os.system("afplay news.mp3")  # macOS

    else:
        error_message = "Failed to retrieve the page. Status code: " + str(response.status_code)
        print(error_message)
        tts = gTTS(text=error_message, lang="ne")
        tts.save("error.mp3")
        os.system("start error.mp3")
if __name__ == "main":
    setopati()
