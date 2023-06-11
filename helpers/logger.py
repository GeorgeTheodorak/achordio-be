from loguru import logger as log

# Configure Loguru logger
log.add("logs/runtime.log", rotation="500 MB", compression="zip", serialize=True)
