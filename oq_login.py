from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "OQ Login Service is running!"

@app.route('/login', methods=['POST'])
def login():
    # Chrome Driver 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless 모드로 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Chrome Driver 실행 (Render 환경 경로)
    driver_path = "/usr/bin/chromedriver"  # Render 배포시 ChromeDriver 경로
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 오더퀸 로그인 페이지 접속
        url = "
