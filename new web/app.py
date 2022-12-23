from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup as bs
application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("hello.html")

@application.route("/input")
def trans():
    kor = request.args.get("santance")
    
    chrome_driver = ChromeDriverManager().install()
    service = Service(chrome_driver)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)
    
    URL = "https://papago.naver.com/"
    driver.get(URL)
    time.sleep(3)

    form = driver.find_element(By.CSS_SELECTOR, "textarea#txtSource")
    form.send_keys(kor)

    button = driver.find_element(By.CSS_SELECTOR, "button#btnTranslate")
    button.click()
    time.sleep(2)

    result = driver.find_element(By.CSS_SELECTOR, "div#txtTarget")
    en = result.text
    driver.close()

    print(en)
    result = ""
    eng = en.split()
    for en_word in eng:
        page = requests.get(f"https://dict-navi.com/en/dictionary/list/?type=search&search_term={en_word}&search_language=3")
        soup = bs(page.text, "html.parser") 
        wow = soup.find_all("td", "n")
        if wow == []:
            result += en_word + ' '
        else:
            nabi_text = wow[0].text.strip()
            word = ""
            for i in nabi_text:
                if i == '[': break
                word += i
            result += word + ' '
    print(result)
    return render_template("result.html", info = result)

@application.route("/back")
def back():
    return render_template("hello.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port = 5000)
