import streamlit as st
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# SHA-256 해시 함수
def sha256_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Selenium 실행 함수
def run_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver_path = "C:/path/to/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        login_url = "https://www.orderqueen.kr/backoffice_admin/login.itp"
        driver.get(login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userId")))

        driver.find_element(By.NAME, "userId").clear()
        driver.find_element(By.NAME, "userId").send_keys("yummar")

        password_plain = "12345678"
        hashed_pw = sha256_hash(password_plain)
        driver.find_element(By.NAME, "pw").clear()
        driver.find_element(By.NAME, "pw").send_keys(password_plain)

        encrypt_input = driver.find_element(By.NAME, "encryptPw")
        driver.execute_script("arguments[0].value = arguments[1];", encrypt_input, hashed_pw)

        driver.find_element(By.ID, "btnLoginNew").click()
        WebDriverWait(driver, 10).until(lambda d: d.current_url != login_url)

        # 세션 쿠키 가져오기
        cookies = driver.get_cookies()
        session_cookie = next(cookie['value'] for cookie in cookies if cookie['name'] == 'SESSION')

        return session_cookie
    except Exception as e:
        return f"오류 발생: {e}"
    finally:
        driver.quit()

# Streamlit UI 구성
st.title("🔐 OrderQueen 자동 로그인")
if st.button("로그인 실행"):
    with st.spinner("로그인 중... 잠시만 기다려 주세요"):
        session_cookie = run_selenium()
        st.success(f"✅ 세션 쿠키: {session_cookie}")
