# db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    
class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    __tablename__ = 'sale_items'
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")

# Código para probar la creación de tablas
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///database.db")
    Base.metadata.create_all(engine)
    print("Tablas creadas exitosamente.")
