from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hashlib

app = Flask(__name__)

def sha256_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/run-selenium', methods=['GET'])
def run_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver_path = "/usr/bin/chromedriver"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        login_url = "https://www.orderqueen.kr/backoffice_admin/login.itp"
        driver.get(login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userId")))

        driver.find_element(By.NAME, "userId").send_keys("yummar")
        driver.find_element(By.NAME, "pw").send_keys("12345678")

        hashed_pw = sha256_hash("12345678")
        encrypt_input = driver.find_element(By.NAME, "encryptPw")
        driver.execute_script("arguments[0].value = arguments[1];", encrypt_input, hashed_pw)

        driver.find_element(By.ID, "btnLoginNew").click()
        WebDriverWait(driver, 10).until(lambda d: d.current_url != login_url)

        session_cookie = next(cookie['value'] for cookie in driver.get_cookies() if cookie['name'] == 'SESSION')
        return jsonify({"session_cookie": session_cookie})

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
