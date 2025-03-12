import asyncio
from dotenv import load_dotenv
from bot import create_bot, register_handlers
from telegram import Update
import logging
import sys

def main():
    # Load environment variables
    load_dotenv()
    
    try:
        # Buat dan setup bot
        application = create_bot()
        register_handlers(application)
        
        print("Bot started! Press Ctrl+C to stop")
        
        # Jalankan bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except KeyboardInterrupt:
        print("\nBot stopped!")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Set event loop policy untuk Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    main() 