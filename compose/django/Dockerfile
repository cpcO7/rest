FROM python:3

WORKDIR /app

COPY . /app

RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt

COPY /compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY /compose/django/start /start-django
RUN sed -i 's/\r$//g' /start-django
RUN chmod +x /start-django


CMD ["/entrypoint"]
