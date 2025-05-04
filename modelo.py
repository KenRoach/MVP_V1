
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base() 
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    orden = Column(String(50), unique=True, nullable=False)
    franquicia = Column(String(100))
    tipo_orden = Column(String(50))
    subtotal = Column(Float)
    tax = Column(Float)
    total = Column(Float)
    item_discount = Column(Float)
    fecha_apertura = Column(DateTime)
    fecha_cierre = Column(DateTime)
    empleado_abre = Column(String(100))
    empleado_cierra = Column(String(100))
    discountname = Column(String(100))
    
    # Relaciones
    items = relationship("TicketItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")
    cash_returns = relationship("CashReturn", back_populates="order")

class TicketItem(Base):
    __tablename__ = "ticket_items"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200))
    cantidad = Column(Integer)
    precio = Column(Float)
    impuesto = Column(Float)
    
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="items")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    metodo = Column(String(50))
    monto = Column(Float)
    descripcion = Column(String(200))
    
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="payments")

class CashReturn(Base):
    __tablename__ = "devoluciones"
    
    id = Column(Integer, primary_key=True)
    monto = Column(Float)
    moneda = Column(String(50))
    descripcion = Column(String(200))
    
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="cash_returns")