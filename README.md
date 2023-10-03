# Image-api
Django REST framework  - Image API

## Set Up
Project is supposed to run via docker compose. To local use please use docker-compose.yml Run following commands in /app directory:

Build image:

        docker build .
        docker compose build   or   docker compose -f docker-compose.yml build
Run app:

        docker compose up      or   docker compose -f docker-compose.yml up

To create a superuser:

        docker compose run --rm app sh -c "python manage.py createsuperuser"

if **docker compose** doesn't run use **docker-compose**

## Links
* **Live preview on AWS:** http://ec2-52-90-180-102.compute-1.amazonaws.com/admin/