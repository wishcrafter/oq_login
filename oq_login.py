from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/')
def home():
    return "OQ Login Service is running!"

@app.route('/login', methods=['GET'])
def login():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ✅ ChromeDriver & Chromium 경로 설정
    chrome_options.binary_location = "/usr/bin/google-chrome"
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://www.orderqueen.kr/backoffice_admin/login.itp"
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userId"))).send_keys("yummar")
        driver.find_element(By.NAME, "pw").send_keys("12345678")

        driver.find_element(By.ID, "btnLoginNew").click()

        WebDriverWait(driver, 10).until(EC.url_contains("backoffice_admin"))

        cookies = driver.get_cookies()
        session_cookie = next(cookie['value'] for cookie in cookies if cookie['name'] == 'SESSION')

        return jsonify({
            "result": "로그인 성공",
            "session_cookie": session_cookie
        })

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
