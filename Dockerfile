FROM python:3.8.5

WORKDIR /
COPY ["fabfile.py", "requirements.txt", "config.py", "docker/app_entrypoint.sh", "application.py", "manage.py", "./"]
COPY ["feed", "./feed"]

RUN pip3 install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

ENTRYPOINT ["./app_entrypoint.sh"]
