from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Define an asynchronous function to handle the homepage route
async def homepage(request):
    # Return a plain text response with the message "Hello, World!"
    return PlainTextResponse("Hello, World!")

# Define the middleware
middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"])
]

# Create a Starlette application and define a route for the homepage
app = Starlette(routes=[
    Route("/simona", homepage)
], middleware=middleware)
