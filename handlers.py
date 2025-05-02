import logging
import asyncio
from typing import Optional
from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler
)
from .utils import (
    is_admin,
    is_bot_message,
    should_delete_message,
    delete_message_with_delay,
    log_action,
    notify_admin
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages in the target channel."""
    config = context.bot_data["config"]
    
    # Skip if not the target channel
    if str(update.message.chat_id) != config.TARGET_CHANNEL_ID and \
       update.message.chat.username != config.TARGET_CHANNEL_ID.lstrip("@"):
        return
    
    # Skip if message is from admin or bot
    if await is_admin(update, context) or await is_bot_message(update, context):
        return
    
    # Check if message should be deleted
    if should_delete_message(update.message.text or update.message.caption, config):
        deletion_reason = "blacklisted content"
        success = await delete_message_with_delay(
            update.message,
            config.AUTO_DELETE_DELAY,
            context,
            reason=deletion_reason
        )
        
        status = "success" if success else "failed"
        log_action(
            update.message,
            "message_deletion",
            status,
            config,
            {"reason": deletion_reason}
        )
        
        if success:
            await notify_admin(
                context,
                config,
                f"Deleted message in {update.message.chat.title or update.message.chat_id}:\n"
                f"From: @{update.message.from_user.username or update.message.from_user.id}\n"
                f"Content: {update.message.text or update.message.caption or '[media]'}\n"
                f"Reason: {deletion_reason}"
            )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command to show bot status."""
    config = context.bot_data["config"]
    
    # Only respond to admin
    if update.effective_user.id != config.ADMIN_USER_ID:
        return
    
    status_msg = (
        "🤖 Bot Status:\n"
        f"• Channel: {config.TARGET_CHANNEL_ID}\n"
        f"• Blacklist: {len(config.BLACKLIST)} words\n"
        f"• Whitelist: {len(config.WHITELIST)} words\n"
        f"• Auto-delete delay: {config.AUTO_DELETE_DELAY} seconds\n"
        f"• Log file: {config.LOG_FILE or 'Not configured'}"
    )
    
    await update.message.reply_text(status_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command to show available commands."""
    config = context.bot_data["config"]
    
    # Only respond to admin
    if update.effective_user.id != config.ADMIN_USER_ID:
        return
    
    help_msg = (
        "🛠 Available Commands:\n"
        "/status - Show bot status\n"
        "/help - Show this help message\n\n"
        "Bot will automatically moderate messages in the configured channel."
    )
    
    await update.message.reply_text(help_msg)

def setup_handlers(application) -> None:
    """Set up all handlers for the bot."""
    # Message handler for the target channel
    application.add_handler(MessageHandler(
        filters.ChatType.CHANNELS & ~filters.COMMAND,
        handle_message
    ))
    
    # Command handlers
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("help", help_command))
