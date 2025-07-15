# Import necessary libraries
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from keep_alive import keep_alive  # KeepAlive file you'll create below

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Import necessary libraries
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# IMPORTANT: Replace these with your actual IDs
REVIEW_CHANNEL_ID = 1391080977371238400  # Channel where reviews and vouches are posted
VOUCH_SERVER_ID = 1390254693107892264   # Server where !vouch is allowed
MAIN_SERVER_ID = 1394568009217081405    # Your main Discord server ID (primarily for context)

# --- Bot Setup ---
# Define Discord Intents.
intents = discord.Intents.default()
intents.message_content = True  # Required for auto-responder and prefix commands
intents.members = True          # Required for on_member_join
intents.guilds = True           # Required for guild-specific operations

# Initialize the bot client with a command prefix and intents.
# All commands will now use the '!' prefix.
# Set help_command=None to disable the default help command and allow custom one.
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# --- Event: Bot is Ready ---
@bot.event
async def on_ready():
    """
    Called when the bot is ready and connected to Discord.
    Prints a confirmation message to the console.
    """
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Invite URL: https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8') # No 'applications.commands' scope needed for prefix commands

    print("Bot is ready. Prefix commands are active.")

# --- Event: New Member Joins ---
@bot.event
async def on_member_join(member):
    """
    Sends a personalized, cooler welcome DM to new members.
    """
    print(f'New member joined: {member.name} ({member.id})')
    try:
        welcome_embed = discord.Embed(
            title=f"🚀 Welcome to McFleet MarketPlace, {member.name}! 🚀",
            description=(
                "We're absolutely thrilled to have you join our thriving community! "
                "This is the premier destination for **IRL Trading** within the "
                "**McFleet.net Minecraft Server** ecosystem.\n\n"
                "Whether you're looking to buy, sell, or simply explore, we aim to provide "
                "a secure, transparent, and user-friendly environment for all your "
                "in-game item trading needs."
            ),
            color=0x3498db # A vibrant blue for a fresh look
        )
        welcome_embed.add_field(
            name="🌟 Get Started - Important Steps:",
            value=(
                "• **Read the Rules:** Crucial for a safe experience! [Click Here to Read Rules](YOUR_RULES_CHANNEL_LINK_HERE)\n" # TODO: User to add actual link
                "• **How to Trade:** Learn the ropes of buying and selling. [Trading Guide](YOUR_TRADING_GUIDE_LINK_HERE)\n" # TODO: User to add actual link
                "• **Need Help?** Our support team is ready! [Contact Support](YOUR_SUPPORT_CHANNEL_LINK_HERE)" # TODO: User to add actual link
            ),
            inline=False
        )
        welcome_embed.add_field(
            name="✨ Our Features:",
            value=(
                "• **`!rating`**: Share your experience with sellers.\n"
                "• **`!vouch`**: Give a shout-out to trusted traders.\n"
                "• **Auto-Responders**: Type `qr`, `buy`, or `offers` for quick info!\n"
                "• **`!help`**: Get a list of all commands."
            ),
            inline=False
        )
        welcome_embed.set_thumbnail(url="https://placehold.co/128x128/3498db/ffffff?text=McFleet") # Blue themed placeholder
        welcome_embed.set_image(url="https://placehold.co/600x200/2ecc71/ffffff?text=Welcome+to+McFleet+MarketPlace") # Banner image
        welcome_embed.set_footer(text="Your journey to epic trades starts now! | McFleet MarketPlace")
        welcome_embed.timestamp = discord.utils.utcnow()

        await member.send(embed=welcome_embed)
        print(f'Sent enhanced welcome DM to {member.name}.')
    except discord.Forbidden:
        print(f"Could not send DM to {member.name}. They might have DMs disabled.")
    except Exception as e:
        print(f"An error occurred while sending welcome DM to {member.name}: {e}")

# --- Event: Message Received (for auto-responder and prefix commands) ---
@bot.event
async def on_message(message):
    """
    Handles auto-responder triggers and prefix commands.
    """
    if message.author == bot.user:
        return

    msg_content = message.content.lower()

    # --- Auto-Responder ---
    if msg_content == 'qr':
        qr_embed = discord.Embed(
            title="QR Code Information 📸",
            description="Here's the QR code for quick and secure payments!",
            color=0x3498db # Blue color
        )
        qr_embed.set_image(url="https://i.ibb.co/zhJC96PS/image.webp")
        qr_embed.set_footer(text="Scan for Payments! | McFleet MarketPlace")
        await message.channel.send(embed=qr_embed)
        print(f'Sent QR embed in {message.channel.name}.')
    elif msg_content == 'buy':
        buy_embed = discord.Embed(
            title="How to Buy on McFleet MarketPlace 🛒",
            description="Ready to make a purchase? Our comprehensive guide will walk you through every step!",
            color=0xe67e22 # Orange color
        )
        buy_embed.add_field(name="Buying Guide:", value="[Click here to view our detailed buying guide!](https://discord.com/channels/1390254693107892264/1391080986745376889)", inline=False)
        buy_embed.set_footer(text="Happy shopping! | McFleet MarketPlace")
        await message.channel.send(embed=buy_embed)
        print(f'Sent Buy embed in {message.channel.name}.')
    elif msg_content == 'offers':
        offers_embed = discord.Embed(
            title="Looking for an Offer! 💰",
            description="Explore exciting offers and learn how to negotiate your best deals. Stay wise and trade smart!",
            color=0xf1c40f # Yellow color
        )
        offers_embed.add_field(name="Offers Guide:", value="[Click here to learn about making offers!](https://discord.com/channels/1390254693107892264/1391080956454113490)", inline=False)
        offers_embed.set_footer(text="Negotiate your best deal! | McFleet MarketPlace")
        await message.channel.send(embed=offers_embed)
        print(f'Sent Offers embed in {message.channel.name}.')

    # This line is crucial for commands.Bot to process commands defined with decorators
    # and also for handling prefix commands defined directly in on_message.
    await bot.process_commands(message)

# --- Prefix Command: !rating ---
@bot.command(name="rating", description="Rate a service or experience from 1 to 5 stars.")
async def rating_command(ctx, stars: int):
    """
    Handles the !rating prefix command.
    """
    review_channel = bot.get_channel(REVIEW_CHANNEL_ID)
    if not review_channel:
        await ctx.send("Error: The review channel is not configured correctly. Please contact an admin.", ephemeral=True)
        return

    if 1 <= stars <= 5:
        star_emojis = "⭐" * stars
        rating_embed = discord.Embed(
            title="New Service Rating! ⭐",
            description=f"{ctx.author.mention} rated a service {star_emojis}",
            color=0x2ecc71
        )
        rating_embed.add_field(name="Rating:", value=f"{stars}/5 Stars", inline=True)
        rating_embed.set_footer(text=f"Rating by {ctx.author.display_name} | McFleet MarketPlace")
        rating_embed.timestamp = discord.utils.utcnow()

        await review_channel.send(embed=rating_embed)
        await ctx.send(
            f"Thank you for your rating, {ctx.author.mention}! Your rating has been posted in {review_channel.mention}.",
            delete_after=10 # Delete message after 10 seconds for cleanliness
        )
        print(f'{ctx.author.name} submitted a {stars}-star rating via prefix command.')
    else:
        await ctx.send("Please provide a rating between 1 and 5 stars. Example: `!rating 5`")

# --- Prefix Command: !vouch ---
@bot.command(name="vouch", description="Vouch for a seller for a successful trade.")
async def vouch_command(ctx, seller: discord.Member, *, item_description: str):
    """
    Handles the !vouch prefix command.
    `*` before item_description makes it capture all remaining arguments as one string.
    """
    # Check if the command is being used in the designated vouch server
    if ctx.guild and ctx.guild.id != VOUCH_SERVER_ID:
        await ctx.send(
            f"The `!vouch` command can only be used in the designated server for vouches.",
            delete_after=10
        )
        print(f"Vouch command attempted outside designated server by {ctx.author.name}.")
        return

    review_channel = bot.get_channel(REVIEW_CHANNEL_ID)
    if not review_channel:
        await ctx.send("Error: The review channel is not configured correctly. Please contact an admin.", delete_after=10)
        return

    vouch_embed = discord.Embed(
        title="New Vouch! ✅",
        description=f"{ctx.author.mention} vouches for {seller.mention}!",
        color=0x9b59b6
    )
    vouch_embed.add_field(name="Seller:", value=seller.mention, inline=True)
    vouch_embed.add_field(name="Item/Service:", value=item_description, inline=False)
    vouch_embed.set_footer(text=f"Vouch by {ctx.author.display_name} | McFleet MarketPlace")
    vouch_embed.timestamp = discord.utils.utcnow()

    await review_channel.send(embed=vouch_embed)
    await ctx.send(
        f"Thank you for your vouch, {ctx.author.mention}! Your vouch for {seller.mention} has been posted in {review_channel.mention}.",
        delete_after=10
    )
    print(f'{ctx.author.name} vouched for {seller.display_name} for "{item_description}" via prefix command.')

# --- Prefix Command: !help ---
@bot.command(name="help", description="Displays all available commands and their usage.")
async def help_command(ctx):
    """
    Handles the !help prefix command, providing a detailed help menu.
    """
    help_embed = discord.Embed(
        title="📚 McFleet MarketPlace Bot Help Menu 📚",
        description="Here's a list of all commands and how to use them. We're here to make your trading experience seamless!",
        color=0xffa500 # Gold/Orange color for help menu
    )

    help_embed.add_field(
        name="⭐ `!rating <stars>`",
        value="`stars`: A number from 1 to 5.\n"
              "Rate a service or a trade you've experienced. Your rating will be posted publicly.",
        inline=False
    )
    help_embed.add_field(
        name="✅ `!vouch @seller <item_description>`",
        value="`seller`: Mention the Discord user you are vouching for (e.g., `@phyzer`).\n"
              "`item_description`: A brief description of the item or service you received.\n"
              "Publicly vouch for a trusted seller. This command is restricted to the main trading server.",
        inline=False
    )
    help_embed.add_field(
        name="💬 Auto-Responder Keywords",
        value="Simply type these keywords in any channel for quick information:\n"
              "• `qr`: Get the QR code for payments.\n"
              "• `buy`: Learn how to buy items on the marketplace.\n"
              "• `offers`: Understand how to make and receive offers.",
        inline=False
    )
    help_embed.set_footer(text="Your ultimate trading companion! | McFleet MarketPlace")
    help_embed.timestamp = discord.utils.utcnow()

    await ctx.send(embed=help_embed)
    print(f'{ctx.author.name} requested the help menu.')

# --- Run the Bot ---
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN not found. Please set it in your .env file or directly in the script.")

# --- Bot Setup ---
# Define Discord Intents.
intents = discord.Intents.default()
intents.message_content = True  # Required for auto-responder and prefix commands
intents.members = True          # Required for on_member_join
intents.guilds = True           # Required for guild-specific operations

# Initialize the bot client with a command prefix and intents.
# All commands will now use the '!' prefix.
# Set help_command=None to disable the default help command and allow custom one.
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# --- Event: Bot is Ready ---
@bot.event
async def on_ready():
    """
    Called when the bot is ready and connected to Discord.
    Prints a confirmation message to the console.
    """
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Invite URL: https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8') # No 'applications.commands' scope needed for prefix commands

    print("Bot is ready. Prefix commands are active.")

# --- Event: New Member Joins ---
@bot.event
async def on_member_join(member):
    """
    Sends a personalized, cooler welcome DM to new members.
    """
    print(f'New member joined: {member.name} ({member.id})')
    try:
        welcome_embed = discord.Embed(
            title=f"🚀 Welcome to McFleet MarketPlace, {member.name}! 🚀",
            description=(
                "We're absolutely thrilled to have you join our thriving community! "
                "This is the premier destination for **IRL Trading** within the "
                "**McFleet.net Minecraft Server** ecosystem.\n\n"
                "Whether you're looking to buy, sell, or simply explore, we aim to provide "
                "a secure, transparent, and user-friendly environment for all your "
                "in-game item trading needs."
            ),
            color=0x3498db # A vibrant blue for a fresh look
        )
        welcome_embed.add_field(
            name="🌟 Get Started - Important Steps:",
            value=(
                "• **Read the Rules:** Crucial for a safe experience! [Click Here to Read Rules](https://discord.com/channels/1390254693107892264/1390255535164493905)\n" # TODO: User to add actual link
                "• **How to Trade:** Learn the ropes of buying and selling. [Price's](https://discord.com/channels/1390254693107892264/1391080947952259102)\n" # TODO: User to add actual link
                "• **Need Help?** Our support team is ready! [Contact Support](https://discord.com/channels/1390254693107892264/1391080986745376889)" # TODO: User to add actual link
            ),
            inline=False
        )
        welcome_embed.add_field(
            name="✨ Our Features:",
            value=(
                "• **`!rating`**: Share your experience with sellers.\n"
                "• **`!vouch`**: Give a shout-out to trusted traders.\n"
                "• **Auto-Responders**: Type `qr`, `buy`, or `offers` for quick info!\n"
                "• **`!help`**: Get a list of all commands."
            ),
            inline=False
        )
        welcome_embed.set_thumbnail(url="https://placehold.co/128x128/3498db/ffffff?text=McFleet") # Blue themed placeholder
        welcome_embed.set_image(url="https://placehold.co/600x200/2ecc71/ffffff?text=Welcome+to+McFleet+MarketPlace") # Banner image
        welcome_embed.set_footer(text="Your journey to epic trades starts now! | McFleet MarketPlace")
        welcome_embed.timestamp = discord.utils.utcnow()

        await member.send(embed=welcome_embed)
        print(f'Sent enhanced welcome DM to {member.name}.')
    except discord.Forbidden:
        print(f"Could not send DM to {member.name}. They might have DMs disabled.")
    except Exception as e:
        print(f"An error occurred while sending welcome DM to {member.name}: {e}")

# --- Event: Message Received (for auto-responder and prefix commands) ---
@bot.event
async def on_message(message):
    """
    Handles auto-responder triggers and prefix commands.
    """
    if message.author == bot.user:
        return

    msg_content = message.content.lower()

    # --- Auto-Responder ---
    if msg_content == 'qr':
        qr_embed = discord.Embed(
            title="QR Code Information 📸",
            description="Here's the QR code for quick and secure payments!",
            color=0x3498db # Blue color
        )
        qr_embed.set_image(url="https://i.ibb.co/zhJC96PS/image.webp")
        qr_embed.set_footer(text="Scan for Payments! | McFleet MarketPlace")
        await message.channel.send(embed=qr_embed)
        print(f'Sent QR embed in {message.channel.name}.')
    elif msg_content == 'buy':
        buy_embed = discord.Embed(
            title="How to Buy on McFleet MarketPlace 🛒",
            description="Ready to make a purchase? Our comprehensive guide will walk you through every step!",
            color=0xe67e22 # Orange color
        )
        buy_embed.add_field(name="Buying Guide:", value="[Click here to view our detailed buying guide!](https://discord.com/channels/1390254693107892264/1391080986745376889)", inline=False)
        buy_embed.set_footer(text="Happy shopping! | McFleet MarketPlace")
        await message.channel.send(embed=buy_embed)
        print(f'Sent Buy embed in {message.channel.name}.')
    elif msg_content == 'offers':
        offers_embed = discord.Embed(
            title="Looking for an Offer! 💰",
            description="Explore exciting offers and learn how to negotiate your best deals. Stay wise and trade smart!",
            color=0xf1c40f # Yellow color
        )
        offers_embed.add_field(name="Offers Guide:", value="[Click here to learn about making offers!](https://discord.com/channels/1390254693107892264/1391080956454113490)", inline=False)
        offers_embed.set_footer(text="Negotiate your best deal! | McFleet MarketPlace")
        await message.channel.send(embed=offers_embed)
        print(f'Sent Offers embed in {message.channel.name}.')

    # This line is crucial for commands.Bot to process commands defined with decorators
    # and also for handling prefix commands defined directly in on_message.
    await bot.process_commands(message)

# --- Prefix Command: !rating ---
@bot.command(name="rating", description="Rate a service or experience from 1 to 5 stars.")
async def rating_command(ctx, stars: int):
    """
    Handles the !rating prefix command.
    """
    review_channel = bot.get_channel(REVIEW_CHANNEL_ID)
    if not review_channel:
        await ctx.send("Error: The review channel is not configured correctly. Please contact an admin.", ephemeral=True)
        return

    if 1 <= stars <= 5:
        star_emojis = "⭐" * stars
        rating_embed = discord.Embed(
            title="New Service Rating! ⭐",
            description=f"{ctx.author.mention} rated a service {star_emojis}",
            color=0x2ecc71
        )
        rating_embed.add_field(name="Rating:", value=f"{stars}/5 Stars", inline=True)
        rating_embed.set_footer(text=f"Rating by {ctx.author.display_name} | McFleet MarketPlace")
        rating_embed.timestamp = discord.utils.utcnow()

        await review_channel.send(embed=rating_embed)
        await ctx.send(
            f"Thank you for your rating, {ctx.author.mention}! Your rating has been posted in {review_channel.mention}.",
            delete_after=10 # Delete message after 10 seconds for cleanliness
        )
        print(f'{ctx.author.name} submitted a {stars}-star rating via prefix command.')
    else:
        await ctx.send("Please provide a rating between 1 and 5 stars. Example: `!rating 5`")

# --- Prefix Command: !vouch ---
@bot.command(name="vouch", description="Vouch for a seller for a successful trade.")
async def vouch_command(ctx, seller: discord.Member, *, item_description: str):
    """
    Handles the !vouch prefix command.
    `*` before item_description makes it capture all remaining arguments as one string.
    """
    # Check if the command is being used in the designated vouch server
    if ctx.guild and ctx.guild.id != VOUCH_SERVER_ID:
        await ctx.send(
            f"The `!vouch` command can only be used in the designated server for vouches.",
            delete_after=10
        )
        print(f"Vouch command attempted outside designated server by {ctx.author.name}.")
        return

    review_channel = bot.get_channel(REVIEW_CHANNEL_ID)
    if not review_channel:
        await ctx.send("Error: The review channel is not configured correctly. Please contact an admin.", delete_after=10)
        return

    vouch_embed = discord.Embed(
        title="New Vouch! ✅",
        description=f"{ctx.author.mention} vouches for {seller.mention}!",
        color=0x9b59b6
    )
    vouch_embed.add_field(name="Seller:", value=seller.mention, inline=True)
    vouch_embed.add_field(name="Item/Service:", value=item_description, inline=False)
    vouch_embed.set_footer(text=f"Vouch by {ctx.author.display_name} | McFleet MarketPlace")
    vouch_embed.timestamp = discord.utils.utcnow()

    await review_channel.send(embed=vouch_embed)
    await ctx.send(
        f"Thank you for your vouch, {ctx.author.mention}! Your vouch for {seller.mention} has been posted in {review_channel.mention}.",
        delete_after=10
    )
    print(f'{ctx.author.name} vouched for {seller.display_name} for "{item_description}" via prefix command.')

# --- Prefix Command: !help ---
@bot.command(name="help", description="Displays all available commands and their usage.")
async def help_command(ctx):
    """
    Handles the !help prefix command, providing a detailed help menu.
    """
    help_embed = discord.Embed(
        title="📚 McFleet MarketPlace Bot Help Menu 📚",
        description="Here's a list of all commands and how to use them. We're here to make your trading experience seamless!",
        color=0xffa500 # Gold/Orange color for help menu
    )

    help_embed.add_field(
        name="⭐ `!rating <stars>`",
        value="`stars`: A number from 1 to 5.\n"
              "Rate a service or a trade you've experienced. Your rating will be posted publicly.",
        inline=False
    )
    help_embed.add_field(
        name="✅ `!vouch @seller <item_description>`",
        value="`seller`: Mention the Discord user you are vouching for (e.g., `@phyzer`).\n"
              "`item_description`: A brief description of the item or service you received.\n"
              "Publicly vouch for a trusted seller. This command is restricted to the main trading server.",
        inline=False
    )
    help_embed.add_field(
        name="💬 Auto-Responder Keywords",
        value="Simply type these keywords in any channel for quick information:\n"
              "• `qr`: Get the QR code for payments.\n"
              "• `buy`: Learn how to buy items on the marketplace.\n"
              "• `offers`: Understand how to make and receive offers.",
        inline=False
    )
    help_embed.set_footer(text="Your ultimate trading companion! | McFleet MarketPlace")
    help_embed.timestamp = discord.utils.utcnow()

    await ctx.send(embed=help_embed)
    print(f'{ctx.author.name} requested the help menu.')

# --- Run the Bot ---
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN not found. Please set it in your .env file or directly in the script.")
