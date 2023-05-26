FROM python:3.9

WORKDIR /api

ARG DATABASE_URL
ARG MAIL_USERNAME
ARG MAIL_PASSWORD
ARG OAUTH2_CLIENT_ID
ARG OAUTH2_CLIENT_SECRET
ARG OAUTH2_AUTH_URL
ARG OAUTH2_TOKEN_URL
ARG OAUTH2_CERTS_URL
ARG ADMIN_ID

ARG PORT

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN alembic upgrade head

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", ${PORT}]