import streamlit as st
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import hashlib

# ✅ Chrome 설치 설정 (Streamlit Cloud 전용)
def install_chrome():
    os.system("apt-get update")
    os.system("apt-get install -y chromium-browser")
    os.system("apt-get install -y chromium-chromedriver")
    os.environ["PATH"] += ":/usr/lib/chromium-browser/"

# ✅ SHA-256 해시 함수
def sha256_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ✅ 자동 로그인 처리
def get_session_cookie():
    install_chrome()  # Chrome 설치 추가

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        login_url = "https://www.orderqueen.kr/backoffice_admin/login.itp"
        driver.get(login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userId")))

        driver.find_element(By.NAME, "userId").send_keys("yummar")

        password_plain = "12345678"
        hashed_pw = sha256_hash(password_plain)
        driver.find_element(By.NAME, "pw").send_keys(password_plain)

        encrypt_input = driver.find_element(By.NAME, "encryptPw")
        driver.execute_script("arguments[0].value = arguments[1];", encrypt_input, hashed_pw)

        driver.find_element(By.ID, "btnLoginNew").click()
        WebDriverWait(driver, 10).until(lambda d: d.current_url != login_url)

        cookies = driver.get_cookies()
        session_cookie = next(cookie['value'] for cookie in cookies if cookie['name'] == 'SESSION')

        return session_cookie

    except Exception as e:
        return None

    finally:
        driver.quit()

# 🔥 Streamlit 인터페이스
st.title("오더퀸 자동화 시스템")

if 'trigger' in st.query_params:
    st.write("🔄 자동 로그인 진행 중...")
    session_cookie = get_session_cookie()
    if session_cookie:
        st.success(f"✅ 로그인 성공! 세션 값: {session_cookie}")
    else:
        st.error("❌ 로그인 실패! 다시 시도하세요.")
else:
    st.markdown(f"[🚀 자동 로그인 실행](?trigger=true)")
