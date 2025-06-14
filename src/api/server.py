from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from .tasks import router as tasks_router
from .projects import router as projects_router
from . import tasks, projects  # Импортируем модули с роутерами

app = FastAPI(
    title="Todo API",
    description="Clean Architecture Todo App",
    version="1.0.0",
)

# Настройка логирования
logger = logging.getLogger(__name__)

# Обработчики ошибок
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)},
    )

# Подключаем роутеры
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo API"}