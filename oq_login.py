import streamlit as st
import requests
import hashlib

# ✅ SHA-256 해시 함수
def sha256_hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ✅ 자동 로그인 및 세션 쿠키 획득
def get_session_cookie():
    login_url = "https://www.orderqueen.kr/backoffice_admin/loginChk.itp"
    
    # 🔑 로그인 데이터
    data = {
        "userId": "yummar",
        "encryptPw": sha256_hash("12345678")
    }

    # 🟢 로그인 요청 및 세션 획득
    with requests.Session() as session:
        response = session.post(login_url, data=data)
        
        # 성공 시 세션 쿠키 반환
        if response.status_code == 200 and "SESSION" in session.cookies:
            return session.cookies.get("SESSION")
        else:
            return None

# 🔥 Streamlit 인터페이스
st.title("OQ Auto Login")

if 'trigger' in st.query_params:
    st.write("🔄 자동 로그인 진행 중...")
    session_cookie = get_session_cookie()
    if session_cookie:
        st.success(f"✅ 로그인 성공! 세션 값: {session_cookie}")
    else:
        st.error("❌ 로그인 실패! 다시 시도하세요.")
else:
    st.markdown(f"[🚀 자동 로그인 실행](?trigger=true)")
