# Telegram Auto-Moderation Bot

A bot that automatically moderates messages in a Telegram channel based on configurable rules.

## Features

- Automatically delete messages containing blacklisted keywords
- Whitelist support to preserve important messages
- Role-based moderation (admins/bot messages are preserved)
- Configurable deletion delay
- Detailed logging
- Admin notifications

## Setup

### 1. Prerequisites

- Python 3.8+
- Telegram bot token (get from @BotFather)
- Admin rights in the target channel

### 2. Configuration

1. Copy `.env.example` to `.env` and fill in your details:
   - `BOT_TOKEN`: From @BotFather
   - `TARGET_CHANNEL_ID`: Channel username (e.g., `@yourchannel`) or ID (e.g., `-1001234567890`)
   - `ADMIN_USER_ID`: Your Telegram user ID (get from @userinfobot)
   - Optionally configure blacklist, whitelist, and deletion delay

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
