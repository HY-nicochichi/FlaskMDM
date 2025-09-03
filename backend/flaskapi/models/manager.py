from typing import (
    Self,
    TYPE_CHECKING
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from extensions import AppModel
if TYPE_CHECKING: from .enterprise import Enterprise

class Manager(AppModel):
    __tablename__ = 'managers'
    pass_enc: Mapped[str] = mapped_column(nullable=False)
    enterprises: Mapped[list['Enterprise']] = relationship(
        'Enterprise', back_populates='manager', cascade='all, delete-orphan'
    )

    @classmethod
    def create(cls, id: str, password: str) -> Self|None:
        return super().create(
            id=id, pass_enc=generate_password_hash(password)
        )

    def is_password_matched(self, password: str) -> bool:
        return check_password_hash(self.pass_enc, password)
