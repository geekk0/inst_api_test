import json
import os
import re
import time
import webbrowser

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
# res = requests.get(url="https://www.instagram.com/0_litvinenko/?__a=1")
base_path = os.getcwd()
driver_path = os.path.join(base_path, "chromedriver_linux64")
print(driver_path)

"""params = {"client_id": 426225215926994,
          "redirect_uri": "https://ya.ru",
          "response_type": "code",
          "scope": "user_profile,user_media"}

auth_window_request = requests.request(url="https://www.instagram.com/oauth/authorize/", params=params, method="GET")"""

auth_url = "https://www.instagram.com/oauth/authorize?client_id=426225215926994" \
         "&redirect_uri=https://ya.ru/&scope=user_profile,user_media&response_type=code"

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
#options = webdriver.ChromeOptions()
# options.add_argument('--headless')

username = "*"
password = "*"


def catch_code_page(driver):
    if driver.current_url.startswith("https://ya.ru/"):
        return True
    else:
        return False


try:
    # with webdriver.Chrome(options=options) as browser:

        driver.get(auth_url)
        time.sleep(1)
        username_input = driver.find_element(By.NAME, "username").send_keys(username)
        password_input = driver.find_element(By.NAME, "password").send_keys(password)
        # submit_button = driver.find_element(By.TAG_NAME, "button").submit()
        # time.sleep(1)
        # save_info_button = driver.find_element(By.TAG_NAME, "button").submit()

        WebDriverWait(driver, timeout=60).until(catch_code_page)

        code = driver.current_url[20:][:-2]

        exchange_url = "https://api.instagram.com/oauth/access_token"
        data = {"client_id": 426225215926994,
                "client_secret": "49a1ef6b16cd94eee89272898affb66a",
                "code": str(code),
                "grant_type": "authorization_code",
                "redirect_uri": "https://ya.ru/",
                }
        exchanged_token_request = requests.post(exchange_url, data=data)  # Меняем код на токен
        token = exchanged_token_request.json()['access_token']

        print(token)

        """get_media_url = "https://graph.instagram.com/"                   # Запрос на "медиа" юзера

        params = {"access_token": token}

        get_media_request = requests.get(get_media_url, params=params)

        print(get_media_request.request)

        print(get_media_request.text)
        print(get_media_request.status_code)
        print(get_media_request.content)"""

        get_media_url = "https://graph.instagram.com/me/media?fields=id,media_type,media_url,permalink,thumbnail_url" \
                       "&access_token="+token

        get_user_media = requests.get(url=get_media_url)

        print(get_user_media.text)

        time.sleep(1)
except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()




"""auth_window = webbrowser



auth_window.open(url=auth_url)"""






# Instagram App Id 426225215926994
# Instagram App Secret 49a1ef6b16cd94eee89272898affb66a
# profilePage_48907685556
# 48907685556
# code=AQCO4VQ-zj_hRjMp3unRyHHN_zHHdaLguOAW0ETmzrCnEflKOwm5rDmKkWMnfILAa7U1GCqJ8wjvnQlpajWh2CbIDpG8gcntiIhe_gHbfeLxJDdiDKzSEbx6in7NXvp_LGaOFjJc13brPX0j4E_2l9hbLJdeNc5GilNbOvs6iltqA5STE93e_pWBNIf7B-_yTU5Ilrk58AwTG7CUAbp1UE04SjVRImPcJQLImWGMXWEdcg #_