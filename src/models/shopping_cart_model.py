from sqlalchemy import Column, ForeignKey, Integer, String
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
