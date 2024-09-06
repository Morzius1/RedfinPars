# задаем базовый образ (вместо 3.8 можно указать другую версию Python)
FROM python:3.12

# устанавливаем google-chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# выставляем нужный порт дисплея
ENV DISPLAY=:99

WORKDIR  /app

COPY  .  /app

RUN  pip  install  -r  requirements.txt

CMD  ["python",  "aiogram_run.py"]