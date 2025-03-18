FROM python:3.12-slim

WORKDIR /app
COPY . .

# Chrome 및 ChromeDriver 설치
RUN apt-get update && apt-get install -y chromium chromium-driver

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:10000", "oq_login:app"]
