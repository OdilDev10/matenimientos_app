import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from apps.computers.router import router_computers
from apps.matenimientos.router import router_mantenimiento
from apps.users.router import router_users
from config.config import DEBUG


app = FastAPI(
    title="Mi API",
    description="Una API de ejemplo con FastAPI",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/redocumentation",
    openapi_url="/myapi/openapi.json",
    debug=DEBUG,
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        # print_exception(error)
        return JSONResponse(status_code=500, content=f"Internal server ${error}")


app.middleware("http")(catch_exceptions_middleware)


@app.get("/", tags=["Home routes"])
def home(request: Request):
    client_headers = request.headers.get("authorization")
    return {"message": "Welcome to the api server.", "headers": client_headers}


app.include_router(router_computers, prefix="/api/v1")
app.include_router(router_mantenimiento, prefix="/api/v1")
app.include_router(router_users, prefix="/api/v1")
