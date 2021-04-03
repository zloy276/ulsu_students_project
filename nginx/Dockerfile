ARG SERVER_IMAGE
ARG CLIENT_IMAGE

FROM $SERVER_IMAGE AS server
RUN poetry run python3 manage.py collectstatic --no-input

FROM $CLIENT_IMAGE AS client

FROM broagency/nginx-le:1.17.1

COPY service.conf /etc/nginx/service.conf
COPY .htpasswd /etc/nginx/

COPY --from=client /app/user/dist /app/user
COPY yandex_75747403c231c335.html /app/user
COPY --from=client /app/user/src/static /app/user/static
COPY --from=server /home/python/app/staticfiles /app/user/static
