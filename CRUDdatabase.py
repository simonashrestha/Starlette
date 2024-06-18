from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import uvicorn
from starlette.requests import Request

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Middleware for handling CORS
middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
]

# Models
class Item(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity= Column(Integer, index=True)
    category= Column(String, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Routes
async def list_items(request: Request):
    session = SessionLocal()
    items = session.query(Item).all()
    session.close()
    return JSONResponse([{"id": item.id, "name": item.name, "quantity": item.quantity, "category": item.category} for item in items])

async def get_item(request: Request):
    item_id = request.path_params['item_id']
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    session.close()
    if item:
        return JSONResponse({"id": item.id, "name": item.name, "quantity": item.quantity, "category": item.category})
    return JSONResponse({'error': 'Item not found'}, status_code=404)

async def create_item(request: Request):
    data = await request.json()
    item = Item(name=data['name'], quantity=data['quantity'], category=data['category'])
    session = SessionLocal()
    session.add(item)
    session.commit()
    session.refresh(item)
    session.close()
    return JSONResponse({"id": item.id, "name": item.name, "quantity": item.quantity, "category": item.category}, status_code=201)

async def update_item(request: Request):
    item_id = request.path_params['item_id']
    data = await request.json()
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        item.name = data['name']
        session.commit()
        session.refresh(item)
        session.close()
        return JSONResponse({"id": item.id, "name": item.name, "quantity": item.quantity, "category": item.category})
    session.close()
    return JSONResponse({'error': 'Item not found'}, status_code=404)

async def delete_item(request: Request):
    item_id = request.path_params['item_id']
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        session.delete(item)
        session.commit()
        session.close()
        return JSONResponse({'message': 'Item deleted'})
    session.close()
    return JSONResponse({'error': 'Item not found'}, status_code=404)

routes = [
    Route('/items', list_items, methods=['GET']),
    Route('/items', create_item, methods=['POST']),
    Route('/items/{item_id}', get_item, methods=['GET']),
    Route('/items/{item_id}', update_item, methods=['PUT']),
    Route('/items/{item_id}', delete_item, methods=['DELETE']),
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=2000)
