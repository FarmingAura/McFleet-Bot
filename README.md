McFleet MarketPlace Discord Bot
This Discord bot is designed to enhance the trading experience on the McFleet MarketPlace Discord server. It provides a welcoming system for new members, a robust review and vouch system, and helpful auto-responders for common queries.

Features
DM Welcome Message: Sends a personalized, professional welcome message to new members upon joining the server, including important links and bot features.

Review System (!rating): Allows users to rate services or trades from 1 to 5 stars, with ratings posted to a designated review channel.

Vouch System (!vouch): Enables users to publicly vouch for trusted sellers after successful trades, with vouches posted to the same designated review channel. This command is restricted to a specific server.

Auto-Responders: Automatically provides information via embeds when specific keywords are typed in any channel:

qr: Displays a QR code for payments.

buy: Provides a link to the buying guide.

offers: Provides a link to the offers guide.

Help Menu (!help): Offers a comprehensive list of all bot commands and auto-responder keywords with their usage.

Commands
All commands use the ! prefix.

!rating <1-5>

Description: Rate a service or experience with a star rating.

Usage: !rating 5 (rates 5 stars)

!vouch @seller <item_description>

Description: Publicly vouch for a seller after a successful trade. This command is restricted to the main trading server.

Usage: !vouch @ExampleUser Diamond Pickaxe Legit Trade

!help

Description: Displays this help menu with all available commands and auto-responder keywords.

Usage: !help

Auto-Responder Keywords
Simply type these keywords in any channel to trigger a response:

qr

buy

offers

Setup and Installation
Follow these steps to get your McFleet MarketPlace Discord Bot up and running.

1. Prerequisites
Python 3.8+ installed on your system.

A Discord account with permissions to create and manage bot applications.

2. Create a Discord Bot Application
Go to the Discord Developer Portal.

Click on "New Application".

Give your application a name (e.g., "McFleet MarketPlace Bot") and click "Create".

Navigate to the "Bot" tab on the left sidebar.

Click "Add Bot" and confirm.

Under "Privileged Gateway Intents", enable the following:

MESSAGE CONTENT INTENT

SERVER MEMBERS INTENT

PRESENCE INTENT (though not explicitly used for presence status, it's often good to have for member-related events)

Click "Reset Token" and copy your bot token. Keep this token absolutely secret!

3. Invite Your Bot to Your Server
In the Discord Developer Portal, go to the "OAuth2" > "URL Generator" tab for your bot application.

Under "SCOPES", select bot.

Under "BOT PERMISSIONS", select Administrator for easy setup. You can refine these permissions later if you prefer.

Copy the generated URL.

Paste the URL into your web browser, select your Discord server from the dropdown, and click "Authorize".

4. Project Setup
Create a new directory for your bot project (e.g., mcfleet_bot).

Inside this directory, create the following files:

bot.py (your main bot code)

keep_alive.py (for hosting services like Render.com)

.env (for storing your bot token securely)

requirements.txt (for managing Python dependencies)

5. Configuration Files
requirements.txt
Create a file named requirements.txt with the following content:

discord.py
python-dotenv
Flask

.env
Create a file named .env with the following content. Replace YOUR_ACTUAL_BOT_TOKEN_HERE with the token you copied from the Discord Developer Portal.

DISCORD_BOT_TOKEN=YOUR_ACTUAL_BOT_TOKEN_HERE

keep_alive.py
Create a file named keep_alive.py with the following content:

from flask import Flask
from threading import Thread
import os # Import os for environment variables

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))

def keep_alive():
    server = Thread(target=run)
    server.start()

bot.py
Place your main bot code (provided previously) into bot.py. Ensure you have the following lines at the top and bottom of your bot.py file, respectively:

# At the top of bot.py, with other imports:
from keep_alive import keep_alive

# ... (your bot code) ...

# At the very end of bot.py, before bot.run(TOKEN):
if TOKEN:
    keep_alive() # Call this to start the web server for hosting
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN not found. Please set it in your .env file or directly in the script.")

6. Configure IDs in bot.py
Open bot.py and replace the placeholder IDs with your actual Discord IDs:

REVIEW_CHANNEL_ID: The ID of the channel where you want !rating and !vouch messages to be posted.

How to get it: In Discord, enable Developer Mode (User Settings > Advanced). Right-click the channel and select "Copy ID".

VOUCH_SERVER_ID: The ID of your main Discord server where the !vouch command is allowed to be used.

How to get it: Right-click on your server icon in Discord and select "Copy ID".

MAIN_SERVER_ID: The ID of your main Discord server (used for general context in the bot).

How to get it: Right-click on your server icon in Discord and select "Copy ID".

Also, remember to update the placeholder links in the welcome_embed within the on_member_join event with your actual server's rule, trading guide, and support channel links.

7. Install Dependencies
Open your terminal or command prompt, navigate to your bot project directory, and run:

pip install -r requirements.txt

8. Run the Bot
From your bot project directory in the terminal, run:

python bot.py

Your bot should now connect to Discord and be ready to use!

Deployment (e.g., Render.com)
For continuous hosting on platforms like Render.com, the keep_alive.py file is essential.

Create a new Web Service on Render.com.

Connect your GitHub repository (if your code is there) or manually upload your files.

Build Command: pip install -r requirements.txt

Start Command: python bot.py

Render will automatically detect the PORT environment variable and ping your web service to keep it alive.

Note: If you encounter any issues, double-check your IDs, bot token, and ensure all necessary intents are enabled in the Discord Developer Portal.