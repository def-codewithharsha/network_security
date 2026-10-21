import logging
from pathlib import Path
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_dir = Path.cwd() / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

logs_path = logs_dir / LOG_FILE

logging.basicConfig(
    filename = logs_path,
    level=logging.INFO,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
)