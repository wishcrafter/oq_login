from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess

app = Flask(__name__)

# ✅ ChromeDriver 경로 확인 API (테스트용)
@app.route('/find_chromedriver', methods=['GET'])
def find_chromedriver():
    try:
        result = subprocess.run(['which', 'chromedriver'], capture_output=True, text=True)
        if result.stdout.strip():
            return f"✅ ChromeDriver Path Found: {result.stdout.strip()}"
        else:
            return "❌ ChromeDriver not found!"
    except Exception as e:
        return f"❌ Error finding ChromeDriver: {str(e)}"

# ✅ 기본 라우팅 (Render 배포 확인용)
@app.route('/')
def home():
    return "OQ Login Service is running!"

# ✅ 오더퀸 자동 로그인 기능
@app.route('/login', methods=['GET'])
def login():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드로 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ✅ Chrome 브라우저 경로 추가 (Render에서는 필수)
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    # ✅ ChromeDriver 경로 설정 (이 경로는 `/find_chromedriver` 실행 후 확인한 값 사용)
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 🔐 오더퀸 로그인 페이지 접속
        url = "https://www.orderqueen.kr/backoffice_admin/login.itp"
        driver.get(url)

        # ✅ 로그인 정보 입력
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userId"))).send_keys("yummar")
        driver.find_element(By.NAME, "pw").send_keys("12345678")

        # ✅ 로그인 버튼 클릭
        driver.find_element(By.ID, "btnLoginNew").click()

        # ✅ 성공적으로 이동할 때까지 대기
        WebDriverWait(driver, 10).until(EC.url_contains("backoffice_admin"))

        # ✅ 세션 쿠키 반환
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
