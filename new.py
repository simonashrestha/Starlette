from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse
 
# Define an asynchronous function to handle the homepage route
async def homepage(request):
    # Return a plain text response with the message "Hello, World!"
    return PlainTextResponse("Hello, World!")
 
# Create a Starlette application and define a route for the homepage
app = Starlette(routes=[
    Route("/simona", homepage)
])
