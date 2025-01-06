import yaml
import subprocess
from mcstatus import JavaServer
import os
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load configuration from YAML
CONFIG_FILE = "config.yaml"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

# Load configuration
config = load_config()

SERVER_IP = config["server_ip"]
SERVER_PORT = config["server_port"]
SERVER_START_CMD = config["server_start_cmd"]
SERVER_STOP_CMD = config["server_stop_cmd"]
SERVER_DIR = config["server_dir"]
STATUS_CHECK_INTERVAL = config["status_check_interval"]
STATUS_TIMEOUT = config["status_timeout"]
BOT_API_TOKEN = config["bot_api_token"]

# Get public IP
def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception as e:
        return f"Error retrieving public IP: {e}"

# Check server status
def check_server_status():
    try:
        server = JavaServer(SERVER_IP, SERVER_PORT)
        server.status()  # Will throw an exception if unreachable
        return True
    except Exception:
        return False

def get_server_status_verbose():
    try:
        server = JavaServer(SERVER_IP, SERVER_PORT)
        status = server.status()
        public_ip = get_public_ip()
        return (
            f"✅ *Server is Online!*\n"
            f"👥 Players: {status.players.online}/{status.players.max}\n"
            f"🌍 Public IP: `{public_ip}`\n"
            f"🔌 Server Port: {SERVER_PORT}\n"
            f"📶 Ping: {status.latency:.2f} ms"
        )
    except Exception:
        public_ip = get_public_ip()
        return (
            f"❌ *Server is Offline or Unreachable!*\n"
            f"🌍 Public IP: `{public_ip}`"
        )

# Start server
def start_server_logic():
    if check_server_status():
        return "✅ *Server is already running.*\nNo need to start it again."
    os.chdir(SERVER_DIR)  # Change to server directory
    subprocess.run(SERVER_START_CMD, shell=True)
    if wait_for_status(True, "start"):
        return "✅ *Server started successfully!* 🚀"
    else:
        return "❌ *Failed to start the server.* Please check the logs for details."

# Stop server
def stop_server_logic():
    if not check_server_status():
        return "✅ *Server is already stopped.*\nNo need to stop it again."
    subprocess.run(SERVER_STOP_CMD, shell=True)
    if wait_for_status(False, "stop"):
        return "✅ *Server stopped successfully!* 🛑"
    else:
        return "❌ *Failed to stop the server.* Please check the logs for details."

# Restart server
def restart_server_logic():
    if not check_server_status():
        return start_server_logic()
    stop_server_logic()
    return start_server_logic()

# Wait for the server to reach the desired state
def wait_for_status(desired_status, action):
    start_time = time.time()
    while time.time() - start_time < STATUS_TIMEOUT:
        if check_server_status() == desired_status:
            return True
        time.sleep(STATUS_CHECK_INTERVAL)
    return False

# Telegram bot command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message."""
    welcome_message = (
        "👋 *Welcome to the Minecraft Server Control Bot!*\n\n"
        "Use `/help` to see available commands.\n"
        "Let's manage your server with ease! 🎮"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display available commands."""
    commands = (
        "🛠 *Available Commands:*\n\n"
        "👉 `/start` - Welcome message\n"
        "👉 `/help` - List available commands\n"
        "👉 `/start_server` - 🟢 Start the Minecraft server\n"
        "👉 `/stop_server` - 🔴 Stop the Minecraft server\n"
        "👉 `/restart_server` - 🔄 Restart the Minecraft server\n"
        "👉 `/status_server` - 📊 Show the status of the Minecraft server"
    )
    await update.message.reply_text(commands, parse_mode="Markdown")

async def start_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the Minecraft server."""
    await update.message.reply_text("🟢 *Starting the Minecraft server...*\nPlease wait. ⏳", parse_mode="Markdown")
    response = start_server_logic()
    await update.message.reply_text(response, parse_mode="Markdown")

async def stop_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop the Minecraft server."""
    await update.message.reply_text("🔴 *Stopping the Minecraft server...*\nPlease wait. ⏳", parse_mode="Markdown")
    response = stop_server_logic()
    await update.message.reply_text(response, parse_mode="Markdown")

async def restart_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Restart the Minecraft server."""
    await update.message.reply_text("🔄 *Restarting the Minecraft server...*\nPlease wait. ⏳", parse_mode="Markdown")
    response = restart_server_logic()
    await update.message.reply_text(response, parse_mode="Markdown")

async def status_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the status of the Minecraft server."""
    response = get_server_status_verbose()
    await update.message.reply_text(response, parse_mode="Markdown")

def main():
    """Main function to start the Telegram bot."""
    app = ApplicationBuilder().token(BOT_API_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start_server", start_server))
    app.add_handler(CommandHandler("stop_server", stop_server))
    app.add_handler(CommandHandler("restart_server", restart_server))
    app.add_handler(CommandHandler("status_server", status_server))

    # Start the bot with drop_pending_updates=True to ignore old updates
    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
