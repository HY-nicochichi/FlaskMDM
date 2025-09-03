from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from extensions import AppModel
if TYPE_CHECKING: from .manager import Manager

class Enterprise(AppModel):
    __tablename__ = 'enterprises'
    enroll_qrcode: Mapped[str] = mapped_column(nullable=False)
    manager_id: Mapped[str] = mapped_column(ForeignKey('managers.id'), nullable=False)
    manager: Mapped['Manager'] = relationship('Manager', back_populates='enterprises')
