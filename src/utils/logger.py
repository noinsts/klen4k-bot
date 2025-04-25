import logging

def setup_logger():
    logger = logging.getLogger("discord_bot")
    logger.setLevel(logging.INFO)

    # Формат логів
    log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # 📂 Запис у файл `bot.log`
    file_handler = logging.FileHandler("bot.log", mode="a")
    file_handler.setFormatter(log_format)

    # 🖥️ Вивід у консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # Додаємо обидва хендлери
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
