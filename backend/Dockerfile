FROM python:3.13.11-slim-trixie AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_CONCURRENCY=15

WORKDIR /src



FROM base AS builder

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

COPY service_account.json .
COPY cmd.sh .
COPY flaskapi .
COPY swagger.yaml .



FROM base AS runner

RUN groupadd -g 1000 app && \
    useradd -u 1000 -g app -s /sbin/nologin app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /src .

USER app

CMD ["sh", "cmd.sh"]
