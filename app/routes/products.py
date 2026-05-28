from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.utils.security import decode_token
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

def get_current_user_id(request: Request) -> str:
    auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")
    
    token = auth_header.split(" ")[1]
    
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    return payload["sub"]

@router.get("/", response_model=List[ProductResponse])
def get_products(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(request)
    return db.query(Product).filter(Product.owner_id == user_id).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(request)
    product = db.query(Product).filter(
        Product.id == product_id, Product.owner_id == user_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    payload: ProductCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(request)
    product = Product(**payload.model_dump(), owner_id=user_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    payload: ProductUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(request)
    product = db.query(Product).filter(
        Product.id == product_id, Product.owner_id == user_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(request)
    product = db.query(Product).filter(
        Product.id == product_id, Product.owner_id == user_id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(product)
    db.commit()