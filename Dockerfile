FROM python:3.9-slim-buster
 
# 사용자 지정
USER root


ADD . /app

# 작업 디렉토리로 이동
WORKDIR /app

COPY requirements.txt .

RUN \
	python -m pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 29573


CMD python app.py
#CMD ["/bin/sh"]