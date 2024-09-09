import os
import discord
from discord.ext import commands, tasks
import random
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables
load_dotenv()
token = os.environ.get('TOKEN')

# Discord bot setup
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Reddit setup
import praw

reddit_read_only = praw.Reddit(client_id="your_client_id",
                               client_secret="your_client_secret",
                               user_agent="r/ucla scraper")

reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    password="your_password",
    user_agent="r/ucla scraper",
    username="your_username",
)

read_only_subreddit = reddit_read_only.subreddit("ucla")
subreddit = reddit.subreddit("ucla")

# Flask setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received data: {data}")
    return "Received", 200

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scrape.start()

@tasks.loop(hours=1)
async def scrape():
    await bot.wait_until_ready()
    channel = bot.get_channel(785293912083791922)
    for post in subreddit.top(time_filter="week"):
        if post.score > 300 and not post.saved: 
            print("title:", post.title)
            print("upvotes:", post.score)
            post.save()
            await channel.send(f"NEW banger Reddit post with {post.score} upvotes just dropped!\nhttps://www.reddit.com{post.permalink}")

def run_discord_bot():
    bot.run(token)

if __name__ == "__main__":
    # Run Flask server in a separate thread
    from threading import Thread

    flask_thread = Thread(target=lambda: app.run(host="0.0.0.0", port=5000))
    flask_thread.start()

    # Run Discord bot
    run_discord_bot()
