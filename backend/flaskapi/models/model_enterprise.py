from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from extensions import db_orm

class Enterprise(db_orm.Model):
    enroll_qrcode: Mapped[str] = mapped_column(nullable=False)
    manager_id: Mapped[str] = mapped_column(nullable=False)
