import praw
# import pandas as pd

import os
import discord
from discord.ext import commands
from discord.ext import tasks
import random
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get('TOKEN')


bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())


# client = discord.Client()
# client = discord.Bot()

@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))
    scrape.start()

reddit_read_only = praw.Reddit(client_id="***REMOVED***",
                               client_secret="***REMOVED***",
                               user_agent="r/ucla scraper")

reddit = praw.Reddit(
    client_id="***REMOVED***",
    client_secret="***REMOVED***",
    password="***REMOVED***",
    user_agent="r/ucla scraper",
    username="***REMOVED***",
)

read_only_subreddit = reddit_read_only.subreddit("ucla")
subreddit = reddit.subreddit("ucla")

@tasks.loop(hours=1)
async def scrape():
    await bot.wait_until_ready()
    channel = bot.get_channel(785293912083791922)
    for post in subreddit.top(time_filter="week"):
        if post.score > 300 and not post.saved: 
            print("title:", post.title)
            print("upvotes:", post.score)
            # print(post.permalink)
            post.save()
            await channel.send("NEW banger Reddit post with " + str(post.score) + " upvotes just dropped!\nhttps://www.reddit.com" + post.permalink)
    

bot.run(token)



