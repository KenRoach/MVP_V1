from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from modelo import Base, Order, TicketItem, Payment, CashReturn  
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Order API", description="API para gestionar órdenes", version="1.0.0")

# Pydantic Schemas
class TicketItemSchema(BaseModel):
    nombre: str
    cantidad: int
    precio: float
    impuesto: float

    class Config:
        orm_mode = True

class PaymentSchema(BaseModel):
    metodo: str
    monto: float
    descripcion: str

    class Config:
        orm_mode = True

class CashReturnSchema(BaseModel):
    monto: float
    moneda: str
    descripcion: str

    class Config:
        orm_mode = True

class OrderSchema(BaseModel):
    orden: str
    franquicia: str
    tipo_orden: str
    subtotal: float
    tax: float
    total: float
    item_discount: float
    fecha_apertura: str
    fecha_cierre: str
    empleado_abre: str
    empleado_cierra: str
    discountname: str

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.post("/orders/", response_model=OrderSchema)
def create_order(order: OrderSchema, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/", response_model=List[OrderSchema])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Order).offset(skip).limit(limit).all()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
