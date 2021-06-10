FROM python:3.9
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
CMD exec gunicorn --preload  cyclone:app -c gconfig.py
