from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id           = Column(String(36), primary_key=True, default=gen_uuid)
    name         = Column(String(100), nullable=False)
    email        = Column(String(150), unique=True, nullable=False, index=True)
    password     = Column(String(255), nullable=False)
    created_at   = Column(DateTime, server_default=func.now())

    products     = relationship("Product", back_populates="owner")


class Product(Base):
    __tablename__ = "products"

    id         = Column(String(36), primary_key=True, default=gen_uuid)
    name       = Column(String(150), nullable=False)
    price      = Column(Float, nullable=False)
    stock      = Column(Integer, default=0)
    date       = Column(DateTime, server_default=func.now())
    owner_id   = Column(String(36), ForeignKey("users.id"), nullable=False)

    owner      = relationship("User", back_populates="products")