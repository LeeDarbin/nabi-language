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
    time.sleep(1)

    form = driver.find_element(By.CSS_SELECTOR, "textarea#txtSource")
    form.send_keys(kor)

    button = driver.find_element(By.CSS_SELECTOR, "button#btnTranslate")
    button.click()
    time.sleep(1)

    result = driver.find_element(By.CSS_SELECTOR, "div#txtTarget")
    en = result.text
    driver.close()

    print(en)
    result = ""
    eng = en.split()
    count = 0
    e_count = 0
    # jom = ['.' , ',', '?', '!', "@", "#", "$" ,"%", "^", "&" ,"*" ,"(", ")", "-", "+", "_", "="]
    if eng == []:
        result = "다빈이 화났어요"
        return render_template("result.html", info = result)
    for i in range(len(eng)):
        if "'" in eng[i]:
            j = eng[i].find("'")
            if i == len(eng) - 1:
                temp = []
                if i == 0:
                    temp = [eng[i][:j]]
                else:
                    temp = eng[:i]
                    temp += [eng[i][:j]]
                eng = temp
            else:
                temp = []
                if i == 0:
                    temp = [eng[i][:j]]
                    temp += eng[i+1:]
                else:
                    temp = eng[:i]
                    temp += [eng[i][:j]]
                    temp += eng[i + 1:]
                eng = temp            
    # for i in eng:
    #     if i in jom:
    #         result = "다빈이 화났어요"
    #         return render_template("result.html", info = result)
    for i in eng:
        for j in i:
            if ord('가') <= ord(j) <= ord('힣'):
                count+=1
                if count:break
            if ord('a') <= ord(j) <= ord('z') or ord('A') <= ord(j) <= ord('Z'):
                e_count += 1
    if count or e_count == 0:
        result = "다빈이가 한국어 쓰라고 했죠!!!"
        return render_template("result.html", info = result)
    for en_word in eng:
        if en_word == '':
            continue
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
    if result == '':
        result = "다빈이 화났어요"
    return render_template("result.html", info = result)

@application.route("/back")
def back():
    return render_template("hello.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port = 6001)
