import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from new import command, speak

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument(r"--user-data-dir=C:\Users\aramb\AppData\Local\Google\Chrome\User Data\Default")
    chrome_options.add_argument("--profile-directory=Default")
    service = Service(r"C:\Users\aramb\OneDrive\Desktop\chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)

def login(driver):
    driver.get("https://foodmandu.com/")
    driver.maximize_window()
    sleep(3)
    driver.find_element(By.XPATH, '/html/body/header/div[2]/div/div[3]/ul/li[3]/span').click()#login ko face
    sleep(2)

def select_restaurant(driver, restaurant_xpath):
    driver.find_element(By.XPATH, restaurant_xpath).click()
    sleep(2)

def add_item_to_cart(driver, item_xpath, quantity=1):
    driver.find_element(By.XPATH, item_xpath).click()
    sleep(2)
    
    for _ in range(quantity - 1):  # Adjusting quantity if more than 1
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[4]/div/div[1]/div/div[2]/button/span[3]").click()
        sleep(1)
    
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[4]/div/div[2]/button').click()#adding to bag
    sleep(2)

def proceed_to_checkout(driver):
    speak("Do you want to place your order?")
    query_order = command().lower()
    if "yes" in query_order:
        driver.find_element(By.XPATH, '/html/body/div[3]/section[3]/div[2]/div[1]/div/div[4]/div/div/div[2]/div[9]/div/button').click()
        sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[2]/section[2]/div/div[1]/div[1]/div[6]/button').click()
        sleep(2)
        # driver.find_element(By.XPATH, '/html/body/div[1]/div/div/section/div[2]/div[1]/div/div/div[1]/div[2]/button[1]').click()
        speak("Order has been successfully placed")
    else:
        speak("Order cancelled.")

def pizza():
    driver = setup_driver()
    login(driver)
    speak("Do you want to order from your favourites?")
    query_fav = command().lower()
    speak("okay opening your favourites")
    if "yes" in query_fav or "s" in query_fav or "ok" in query_fav or "okay" in query_fav or "sure" in query_fav or "ok order" in query_fav or "from" in query_fav or "favourite" in query_fav:
        try:
            driver.find_element(By.XPATH, '/html/body/header/div[2]/div/div[3]/div[2]/div/div/div/div[2]/ul/li[2]/a/span[2]').click()#logging to facourites
            sleep(2)
            speak("From which restaurant do you want to order?")
            query_fav = command().lower()

            if "biryani" in query_fav or "lazeez" in query_fav:
                speak("Opening Lazeez Biryani House and ordering Chicken Dum Biryani")
                select_restaurant(driver, '/html/body/section[2]/div/div/div[2]/div/div[1]/ul/li[1]/div/div/a')# lazzez biryan ko pasal
                
                speak("How many servings do you want?")
                try:
                    quantity = int(command())
                except ValueError:
                    quantity = 1
                
                add_item_to_cart(driver, '/html/body/div[3]/section[3]/div[2]/div[1]/div/div[2]/div[3]/div[8]/ul/li[1]', quantity)#adding chicken biryani to cart
                proceed_to_checkout(driver)
            
            elif "momo" in query_fav or "narayan dai" in query_fav:
                speak("Opening Narayan Dai Ko Famous Momo")
                select_restaurant(driver, '/html/body/section[2]/div/div/div[2]/div/div[1]/ul/li[2]/div/div/a')
                
                speak("Do you want Veg Cheese or Chicken Momo?")
                momo_type = command().lower()
                item_xpath = "/html/body/div[3]/section[3]/div[2]/div[1]/div/div[2]/div[3]/div[2]/ul/li[3]" if "veg" in momo_type else "/html/body/div[3]/section[3]/div[2]/div[1]/div/div[2]/div[3]/div[2]/ul/li[2]"
                
                speak("How many servings do you want?")
                try:
                    quantity = int(command())
                except ValueError:
                    quantity = 1
                
                add_item_to_cart(driver, item_xpath, quantity)
                proceed_to_checkout(driver)

        except Exception as e:
            print(f"Error occurred: {e}")
    
    driver.quit()
    print("Successful completion")

if __name__ == "__main__":
    pizza()
