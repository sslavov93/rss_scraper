echo "Stopping docker containers..."
docker stop nginx scraper postgres rabbitmq

echo "Removing containers, images and volumes..."
docker rm nginx scraper postgres rabbitmq
docker rmi rss_nginx:1.0.0 nginx:1.17-alpine rss_scraper:1.0.0 rss_rabbitmq:1.0.0 rabbitmq:3.8.8 python:3.8.5 postgres:12.4
docker volume rm rss_scraper_stor_vol
echo "Done."
