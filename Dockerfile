FROM python:3.7.3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 FLASK_ENV=development

WORKDIR /
COPY ["fabfile.py", "requirements.txt", "config.py", "entrypoint.sh", "wsgi.py", "manage.py", "./"]
COPY ["feed", "./feed"]

RUN pip3 install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

ENTRYPOINT ["./entrypoint.sh"]