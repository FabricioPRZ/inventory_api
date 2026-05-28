from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.database import engine, Base
from app.routes import auth, products

Base.metadata.create_all(bind=engine)

security = HTTPBearer()

app = FastAPI(
    title="Inventory API",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Inventory API corriendo 🚀"}