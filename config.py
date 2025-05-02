import os
from dotenv import load_dotenv
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str
    TARGET_CHANNEL_ID: str
    ADMIN_USER_ID: int
    BLACKLIST: List[str]
    WHITELIST: List[str]
    AUTO_DELETE_DELAY: int
    LOG_FILE: Optional[str] = None

def load_config() -> Config:
    """Load configuration from environment variables."""
    load_dotenv()
    
    # Required configurations
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN is required in environment variables")
    
    target_channel = os.getenv("TARGET_CHANNEL_ID")
    if not target_channel:
        raise ValueError("TARGET_CHANNEL_ID is required in environment variables")
    
    admin_user_id = os.getenv("ADMIN_USER_ID")
    if not admin_user_id:
        raise ValueError("ADMIN_USER_ID is required in environment variables")
    
    # Optional configurations with defaults
    blacklist = os.getenv("BLACKLIST", "").split(",")
    whitelist = os.getenv("WHITELIST", "").split(",")
    
    # Clean up lists (remove empty strings and strip whitespace)
    blacklist = [word.strip().lower() for word in blacklist if word.strip()]
    whitelist = [word.strip().lower() for word in whitelist if word.strip()]
    
    auto_delete_delay = int(os.getenv("AUTO_DELETE_DELAY", "0"))
    log_file = os.getenv("LOG_FILE")
    
    return Config(
        BOT_TOKEN=bot_token,
        TARGET_CHANNEL_ID=target_channel,
        ADMIN_USER_ID=int(admin_user_id),
        BLACKLIST=blacklist,
        WHITELIST=whitelist,
        AUTO_DELETE_DELAY=auto_delete_delay,
        LOG_FILE=log_file
    )

def validate_config(config: Config) -> None:
    """Validate the loaded configuration."""
    if not config.BOT_TOKEN.startswith(""):
        raise ValueError("Invalid BOT_TOKEN format")
    
    if not (config.TARGET_CHANNEL_ID.startswith("-100") or 
            config.TARGET_CHANNEL_ID.startswith("@")):
        raise ValueError("TARGET_CHANNEL_ID must start with -100 or @")
    
    if config.AUTO_DELETE_DELAY < 0:
        raise ValueError("AUTO_DELETE_DELAY must be >= 0")
