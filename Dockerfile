FROM python:3.11-slim

COPY . /app
WORKDIR /app


RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x /app/acme-auth-hook.sh

CMD [ "certbot", "renew", "--non-interactive", "--preferred-challenges", "dns-01", "--manual-auth-hook", "/app/acme-auth-hook.sh" ]
