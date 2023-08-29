from fastapi import FastAPI
from psycopg.errors import Error

from .db import db


def init_routers(app: FastAPI) -> None:
    from .routers import auth, jobs

    app.include_router(auth.router, prefix="/auth")
    app.include_router(jobs.router, prefix="/jobs")


def init_middlewares(app: FastAPI) -> None:
    from fastapi.middleware.cors import CORSMiddleware

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    app = FastAPI(
        on_shutdown=[db.close],
        exception_handlers={
            Error: db.exception_handler,
        },
    )
    init_routers(app)
    init_middlewares(app)

    return app
