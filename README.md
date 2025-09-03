## FlaskMDM
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-blue.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-red?style=flat&logo=google-cloud&logoColor=white)](https://cloud.google.com/)

Flask & Nuxt Android device management app using AMAPI  

Flask: API (http://localhost:8000)  
Nuxt: SPA (http://localhost:8080)  

## How to Run
STEP1: Prepare ./database.env & ./backend.env
```
# ./database.env
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"
POSTGRES_DB="db"
```
```
# ./backend.env
SQLALCHEMY_DATABASE_URI="postgresql+psycopg://user:password@database:5432/db"
JWT_SECRET_KEY="secret"
GOOGLE_CLOUD_PROJECT_ID="Your-Google-Cloud-Project-ID"
```
STEP2: Run `$ docker compose up -d --build`
