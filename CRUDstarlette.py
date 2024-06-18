from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

# In-memory storage for items
items = {}

# Middleware for handling CORS
middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
]

async def list_items(request):
    return JSONResponse(list(items.values()))

async def get_item(request):
    item_id = request.path_params['item_id']
    item = items.get(item_id)
    if item:
        return JSONResponse(item)
    return JSONResponse({'error': 'Item not found'}, status_code=404)

async def create_item(request):
    data = await request.json()
    item_id = str(len(items) + 1)
    items[item_id] = {'id': item_id, 'name': data['name']}
    return JSONResponse(items[item_id], status_code=201)

async def update_item(request):
    item_id = request.path_params['item_id']
    if item_id not in items:
        return JSONResponse({'error': 'Item not found'}, status_code=404)
    data = await request.json()
    items[item_id]['name'] = data['name']
    return JSONResponse(items[item_id])

async def delete_item(request):
    item_id = request.path_params['item_id']
    if item_id in items:
        del items[item_id]
        return JSONResponse({'message': 'Item deleted'})
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

