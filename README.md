# Minecraft Telegram Server Handler

A simple Python script to control a Minecraft server through a Telegram bot on a unix plateform. This script allows you to start, stop, restart, and check the status of your Minecraft server using commands sent through Telegram.

---

## Features

- Start, stop, restart, and check the status of a Minecraft server.
- Receive detailed status updates, including player count, server latency, and public IP.
- Interact with the server remotely using a Telegram bot.

---

## Installation Instructions

### Prerequisites

1. **Python**: Ensure you have Python 3.8+ installed on your system.
   - [Download Python](https://www.python.org/downloads/)

2. **Minecraft Server**:
   - Download the Minecraft server `.jar` file and documentation from the [official Minecraft website](https://www.minecraft.net/en-us/download/server).
   - Follow the instructions provided by Minecraft to set up your server.
   - Make sure to set the `server_dir` value in `config.yaml` to the directory where your Minecraft server is installed.

3. **Install Screen Utility**:
   - The script uses the `screen` command to manage the Minecraft server in a detached session. Install `screen` on your system:

     ```bash
     sudo apt update && sudo apt upgrade -y
     sudo apt install screen -y
     ```

---

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/YOUR-USERNAME/minecraft-tg-server-handler.git
cd minecraft-tg-server-handler
```

---

### Step 2: Set Up a Python Environment

1. Create a Python virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

     ```bash
     source venv/bin/activate
     ```

---

### Step 3: Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

### Step 4: Configure the Script

1. Open the `config.yaml` file located at the root of the project.
2. Set the following values:

   ```yaml
   server_ip: "127.0.0.1"  # Local or remote IP
   server_port: 25565
   server_start_cmd: "screen -dmS minecraft java -Xms1G -Xmx2G -jar minecraft_server.jar nogui"
   server_stop_cmd: "screen -S minecraft -p 0 -X stuff 'stop\n'"
   server_dir: "/path/to/your/minecraft/server"  # Replace with your server directory
   status_check_interval: 1  # Interval to check status in seconds
   status_timeout: 20  # Timeout for status confirmation in seconds
   bot_api_token: "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your Telegram bot token
   ```

---

### Step 5: Create a Telegram Bot

1. Open Telegram and search for `BotFather`.
2. Start a chat with `BotFather` and type `/newbot`.
3. Follow the prompts to create your bot and get your bot token.
4. Copy the bot token and paste it into the `bot_api_token` field in `config.yaml`.

---

### Step 6: Run the Script

Start the bot by running the script:

```bash
python mc_tg_server_handler.py
```

The bot is now running and waiting for commands on Telegram.

---

## Usage Instructions

### Telegram Commands

Once the bot is running, use the following commands in Telegram to interact with the Minecraft server:

1. **Start the Bot**:
   ```
   /start
   ```
   - Displays a welcome message.

2. **Help**:
   ```
   /help
   ```
   - Lists all available commands.

3. **Start the Server**:
   ```
   /start_server
   ```
   - Starts the Minecraft server.

4. **Stop the Server**:
   ```
   /stop_server
   ```
   - Stops the Minecraft server.

5. **Restart the Server**:
   ```
   /restart_server
   ```
   - Restarts the Minecraft server.

6. **Check Server Status**:
   ```
   /status_server
   ```
   - Displays the server status, including:
     - Player count
     - Server latency
     - Public IP address

---

### Notes

- Ensure the Minecraft server is properly set up and tested before using this script.
- The bot only processes new commands sent after it is started. Any commands sent while the bot was offline will be ignored.

---

## Troubleshooting

If you encounter any issues:
1. Verify the Python virtual environment is active.
2. Ensure all dependencies are installed using `pip install -r requirements.txt`.
3. Check that the `config.yaml` file is properly configured.
4. Make sure the Minecraft server is correctly installed and the `server_dir` points to its directory.

---

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features!

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
