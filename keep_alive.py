# Import necessary libraries for the web server
from flask import Flask
from threading import Thread

# Create a Flask web application instance
app = Flask('')

# Define a route for the root URL ('/')
@app.route('/')
def home():
    """
    This function is called when the web server receives a request to the root URL.
    It returns a simple message to indicate the server is alive.
    """
    return "Bot is alive!"

def run():
    """
    This function starts the Flask web server.
    It will listen on all available network interfaces (0.0.0.0) on port 8080.
    Render.com will typically ping this port.
    """
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080)) # Use PORT env var if available, else 8080

def keep_alive():
    """
    This function starts the web server in a separate thread.
    This is crucial because the main thread needs to be free to run the Discord bot.
    """
    # Create a new thread that will run the 'run' function
    server = Thread(target=run)
    # Start the thread. This makes the web server run concurrently with your bot.
    server.start()

# Example of how you would use it in your main bot.py file:
# from keep_alive import keep_alive
#
# # Call keep_alive() before bot.run(TOKEN)
# keep_alive()
# bot.run(TOKEN)
