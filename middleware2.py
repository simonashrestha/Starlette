from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Define an asynchronous function to handle the homepage route
async def homepage(request):
    return PlainTextResponse("Hello, World with Advanced CORS!")

# Create a Starlette application with advanced CORS middleware configuration
app = Starlette(routes=[
    Route("/simona", homepage)
], middleware=[
    Middleware(CORSMiddleware, allow_origins=["https://example.com"], allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])
])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
