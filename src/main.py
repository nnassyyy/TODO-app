import uvicorn
import logging
from pathlib import Path
import sys

# Добавляем путь к src в sys.path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

if __name__ == "__main__":
    # Получаем абсолютный путь к папке src
    src_path = Path(__file__).parent.resolve()

    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        reload_dirs=[str(src_path)],  # Указываем текущую директорию
        reload_includes=["*.py"]
    )