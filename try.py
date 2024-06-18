from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

async def homepage (request):
    return PlainTextResponse("Hello my name is Simona.")

app= Starlette(routes=[
    Route("/simona", homepage)

], middleware=CORSMiddleware)