
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Set up Chrome options 
def pizza():
    from new import command, speak
    chrome_options = Options()
    chrome_options.add_argument(r"--user-data-dir=C:\Users\aramb\AppData\Local\Google\Chrome\User Data\Default")  # Your Chrome user data
    chrome_options.add_argument("--profile-directory=Default")  # Use your default Chrome profile

# Set up the WebDriver Service
    service = Service(r"C:\Users\aramb\OneDrive\Desktop\chromedriver.exe")  # Path to chromedriver.exe
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Start WebDriver
# Open Google and maximize the window
    driver.get("https://www.google.com")
    driver.maximize_window()
    speak("opening Foodmandu")
    driver.get('https://foodmandu.com/')
    sleep(3)
    driver.find_element(By.XPATH,'/html/body/header/div[2]/div/div[3]/ul/li[3]/span').click() #login ko face
    sleep(1)
    speak("Do you want to order from your favourites?")
    query_fav = command().lower()
    speak("opening your favourites")
    if 'yes' in query_fav or 'okay' in query_fav or 'ok' in query_fav:
        try:
            driver.find_element(By.XPATH,'/html/body/header/div[2]/div/div[3]/div[2]/div/div/div/div[2]/ul/li[2]/a/span[2]').click()#going to favourites
            sleep(2)
            speak("From which resturant you want to order")
            query_fav = command().lower()
            if ("biryani" in query_fav) or ('lazeez' in query_fav) or ('lazeez biryani' in query_fav):
                speak("opening lazeez biryani house and Resturant and ordering the chicken dum biryani")
                driver.find_element(By.XPATH,'/html/body/section[2]/div/div/div[2]/div/div[1]/ul/li[1]/div/div/a').click() # lazzez biryan ko pasal
                sleep(2)
                driver.find_element(By.XPATH,'/html/body/div[3]/section[3]/div[2]/div[1]/div/div[2]/div[3]/div[8]/ul/li[1]').click()#adding chicken Dum Biryani-Half
                sleep(3)
                driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[4]/div/div[2]/button').click()#Adding to Bag
                sleep(2) 
                driver.find_element(By.XPATH,'/html/body/div[3]/section[3]/div[2]/div[1]/div/div[4]/div/div/div[2]/div[9]/div/button').click() #proceed to checkout of lazzez biryani
                driver.find_element(By.XPATH,'/html/body/div[3]/section[3]/div[2]/div[1]/div/div[2]/div[3]/div[3]/ul/li').click()
                sleep(2)
                driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/div/div[1]/div[1]/div[6]/button').click()#continue button of lazeez biryani
                sleep(2)
                driver.find_element(By.XPATH,'/html/body/div[1]/div/div/section/div[2]/div[1]/div/div/div[1]/div[2]/button[1]').click()#place order
                speak("order has been successfully placed")
            elif ("narayan dai" in query_fav) or ("famous" in query_fav) or ("momo" in query_fav) or ("ek" in query_fav) or ("dai" in query_fav) or ("ko" in query_fav):
                speak("Opening naryan dai ko famous momo")
                sleep(3)
                driver.find_element(By.XPATH,'/html/body/section[2]/div/div/div[2]/div/div[1]/ul/li[2]/div/div/a').click()#naryan dai ko famous momo
                sleep(2)
                speak("which momo do you want to order veg_cheese or chicken")
                query_fav = command().lower()
                if ("veg" in query_fav) or ("bej" in query_fav) or ("cheese" in query_fav) or ("veg cheese" in query_fav) or ("veg momo" in query_fav):
                    driver.find_element(By.XPATH,'/html/body/div[3]/section[3]/div[2]/div[1]/div/div[2]/div[3]/div[2]/ul/li[3]').click()#clicking veg momo
                    sleep(2)
                    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[4]/div/div[2]/button').click()#Adding to bag
                    sleep(2)
                    driver.find_element(By.XPATH,'/html/body/div[3]/section[3]/div[2]/div[1]/div/div[4]/div/div/div[2]/div[9]/div/button').click()#proceed to checkout
                    sleep(2)
                    driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/div/div[1]/div[1]/div[6]/button').click()#continue to checkout
                    sleep(2)
                    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/section/div[2]/div[1]/div/div/div[1]/div[2]/button[1]').click()#placeing the order
                    sleep(2)
                    speak("order has been succesfully placed")
                else: 
                    driver.find_element(By.XPATH,"/html/body/div[3]/section[3]/div[2]/div[1]/div/div[2]/div[3]/div[2]/ul/li[2]").click()#clicking chicken momo
                    sleep(2)
                    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[4]/div/div[2]/button').click()#adding to bag
                    sleep(2)
                    driver.find_element(By.XPATH,'/html/body/div[3]/section[3]/div[2]/div[1]/div/div[4]/div/div/div[2]/div[9]/div/button').click()#proceed to checkout
                    sleep(2)
                    driver.find_element(By.XPATH,'/html/body/div[2]/section[2]/div/div[1]/div[1]/div[6]/button').click()#continue to checkout
                    sleep(2)
                    # driver.find_element(By.XPATH,'/html/body/div[1]/div/div/section/div[2]/div[1]/div/div/div[1]/div[2]/button[1]').click()#placeing the order
                    # sleep(2)
                    speak("order has been succesfully placed")
        except:
            exit()
    print("sucessful completion")

if __name__ == "__main__":
    pizza()
