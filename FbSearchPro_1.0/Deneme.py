
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from get_profil import temizle_metin ,ara_telefon_numarası

def user_login():

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--log-level=3")  # 3 seviyesi sadece hataları gösterir
    # chrome_options.add_argument("--headless")  # Headless modunu etkinleştirin
    chrome_options.add_argument("--disable-gpu")  # GPU kullanımını devre dışı bırakın (bazı durumlarda gereklidir)
    chrome_options.add_argument("--window-size=1920x1080")  # Pencere boyutunu ayarlayın
    chrome_options.add_argument('--disable-extensions')
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,  # Görselleri yüklemeyi engeller
        }
    }
    chrome_options.add_experimental_option("prefs",prefs)
    service = Service('chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(45)  # Sayfa yükleme zaman aşımı süresini arttırma
    driver.set_script_timeout(45)     # Script çalıştırma zaman aşımı süresini arttırma
    
    driver.get('https://www.facebook.com/')
    time.sleep(2)


    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    password_input = driver.find_element(By.ID, 'pass')

    email_input.send_keys('fscraping5@gmail.com')
    password_input.send_keys('t.n.f.24')
    password_input.send_keys(Keys.RETURN)
    time.sleep(2)
    return driver 

def kaydır(driver):
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def deneme ():
    driver = user_login()


    driver.get("https://www.facebook.com/mahir.buyukbayram/")
    time.sleep(2)

    kaydır(driver)

    while True:
        try:
            daha_fazlasi_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Daha fazlasını gör')]"))
            )
            driver.execute_script("arguments[0].click();", daha_fazlasi_button)
        except Exception as e:
            break
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_text = soup.get_text()
    page_text = temizle_metin(page_text)
    phone_numbers = ara_telefon_numarası(page_text)
    print(f"telefon numarası: {phone_numbers}")

    driver.close()
    driver.quit()

