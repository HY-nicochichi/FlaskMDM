from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

class Base(DeclarativeBase):
    __abstract__ = True
    id : Mapped[str] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

db_orm = SQLAlchemy(model_class=Base)
jwt_manager = JWTManager()
cross_origin = CORS()

amapi_client = build(
    serviceName = 'androidmanagement',
    version = 'v1',
    credentials = Credentials.from_service_account_file(
        '/service_account.json', scopes=['https://www.googleapis.com/auth/androidmanagement']
    )
)
