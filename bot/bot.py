from telegram.ext import Application
from os import getenv
import logging

def create_bot() -> Application:
    """Membuat instance bot Telegram."""
    # Konfigurasi logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Membuat aplikasi bot
    token = getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di environment variables")
    
    application = Application.builder().token(token).build()
    return application 