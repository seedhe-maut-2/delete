import logging
from typing import Optional, Dict, Any
from telegram import Update, Message, ChatMember
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the message sender is an admin in the channel."""
    if not update.message or not update.message.from_user:
        return False
    
    try:
        chat_member = await context.bot.get_chat_member(
            chat_id=update.message.chat_id,
            user_id=update.message.from_user.id
        )
        return chat_member.status in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]
    except Exception as e:
        logging.error(f"Error checking admin status: {e}")
        return False

async def is_bot_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the message was sent by the bot itself."""
    if not update.message or not update.message.from_user:
        return False
    return update.message.from_user.id == context.bot.id

def should_delete_message(text: str, config) -> bool:
    """
    Determine if a message should be deleted based on content.
    
    Returns:
        bool: True if message should be deleted, False otherwise
    """
    if not text:
        return False
    
    text_lower = text.lower()
    
    # First check whitelist - if any whitelist word exists, preserve message
    for word in config.WHITELIST:
        if word in text_lower:
            return False
    
    # Then check blacklist - if any blacklist word exists, delete message
    for word in config.BLACKLIST:
        if word in text_lower:
            return True
    
    return False

async def delete_message_with_delay(
    message: Message,
    delay: int,
    context: ContextTypes.DEFAULT_TYPE,
    reason: str = "auto-deletion"
) -> bool:
    """Delete a message with optional delay."""
    try:
        if delay > 0:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f"Message will be deleted in {delay} seconds ({reason})...",
                reply_to_message_id=message.message_id
            )
            await asyncio.sleep(delay)
        
        await message.delete()
        return True
    except Exception as e:
        logging.error(f"Failed to delete message {message.message_id}: {e}")
        return False

def log_action(
    message: Message,
    action: str,
    status: str,
    config,
    additional_info: Optional[Dict[str, Any]] = None
) -> None:
    """Log moderation actions."""
    log_entry = {
        "timestamp": message.date.isoformat() if message.date else "",
        "message_id": message.message_id,
        "chat_id": message.chat_id,
        "user_id": message.from_user.id if message.from_user else "",
        "username": message.from_user.username if message.from_user else "",
        "content_preview": message.text[:50] + "..." if message.text else "[media]",
        "action": action,
        "status": status,
        "additional_info": additional_info or {}
    }
    
    # Log to console
    logging.info(f"{action.upper()} - {status}: {log_entry}")
    
    # Log to file if configured
    if config.LOG_FILE:
        try:
            with open(config.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"{log_entry}\n")
        except Exception as e:
            logging.error(f"Failed to write to log file: {e}")

async def notify_admin(
    context: ContextTypes.DEFAULT_TYPE,
    config,
    message: str
) -> None:
    """Send a notification to the admin user."""
    try:
        await context.bot.send_message(
            chat_id=config.ADMIN_USER_ID,
            text=message
        )
    except Exception as e:
        logging.error(f"Failed to notify admin: {e}")
