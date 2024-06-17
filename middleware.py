from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
 
# Create a Starlette application
app = Starlette()
 
# Add CORS middleware to allow all origins
app.add_middleware(CORSMiddleware, allow_origins=["*"])
 
# Define a route for the homepage using a decorator
@app.route("/simona")
async def homepage(request):
    # Respond with a plain text message
    return PlainTextResponse("Hello, It's an example of middleware implementation!")