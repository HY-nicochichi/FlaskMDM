FROM node:25.4.0-trixie-slim AS builder

ARG API_URL_BASE
ENV API_URL_BASE=${API_URL_BASE}

COPY . .
WORKDIR /nuxtapp

RUN npm install
RUN npm run generate



FROM nginx:1.29.4-alpine3.23-slim AS runner

RUN addgroup -g 1000 app && \
    adduser -D -u 1000 -G app -s /sbin/nologin app

COPY --from=builder /nginx.conf /etc/nginx
COPY --from=builder /nuxtapp/.output/public /usr/share/nginx/html

USER app

CMD ["nginx", "-g", "daemon off;"]
