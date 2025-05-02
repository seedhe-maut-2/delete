#!/usr/bin/env python3
import asyncio
import logging
from telegram.ext import Application
from .config import load_config, validate_config
from .handlers import setup_handlers

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application) -> None:
    """Perform post-initialization tasks."""
    await application.bot.send_message(
        chat_id=application.bot_data["config"].ADMIN_USER_ID,
        text="🤖 Bot started and ready to moderate!"
    )

def main() -> None:
    """Start the bot."""
    try:
        # Load configuration
        config = load_config()
        validate_config(config)
        
        # Create the Application
        application = Application.builder().token(config.BOT_TOKEN).build()
        
        # Store config in bot_data for access in handlers
        application.bot_data["config"] = config
        
        # Set up handlers
        setup_handlers(application)
        
        # Run the bot
        logger.info("Starting bot...")
        application.run_polling(
            post_init=post_init,
            close_loop=False
        )
    except Exception as e:
        logger.error(f"Bot failed: {e}")
        raise

if __name__ == "__main__":
    main()
