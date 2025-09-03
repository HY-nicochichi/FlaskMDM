from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from extensions import db_orm

class Manager(db_orm.Model):
    pass_enc: Mapped[str] = mapped_column(nullable=False)
