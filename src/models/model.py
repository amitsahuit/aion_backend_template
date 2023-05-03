from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"

    id = Column(Integer, primary_key=True, index=True)
    shopping_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    product = relationship("Product", back_populates="shopping_cart")
    owner = relationship("User", back_populates="shopping_cart")


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    shopping_cart = relationship("ShoppingCart", back_populates="product")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    projects_handled = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    married_status = Column(Boolean, nullable=True)
    password = Column(String, nullable=False)
    phone_number = Column(String(10))
    createdtime = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    shopping_cart = relationship("ShoppingCart", back_populates="owner")
