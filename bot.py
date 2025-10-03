import json
import os
import discord
import random
from random import randint
from discord.ext import commands
from discord.commands import Option
from dotenv import load_dotenv


#########
# CONNECTS GUILD ID AND BOT TOKEN THROUGH ENV VARIABLES
#########
load_dotenv()
GUILD = str(os.getenv('DUNGEON_GUILD'))
bot = commands.Bot(intents=discord.Intents.all(), command_prefix=str(os.getenv('DUNGEON_PREFIX')))


#########
# LISTS
#########
#########
MOB_TYPE = ["Ogre", "Slime", "Skeleton", "Goblin", "Zombie", "Bandit"]

#########
# BASE CLASSES
#########
#########
class item:
   def __init__(self):
       self.cost = 0
       self.hands = 0
       self.type = "Unknown"
       self.enchantments = []
       self.damage = 0
       self.protection = 0
       self.durability = 1  

class player:
   def __init__(self):
       self.health
       self.head
       self.hands = 2
       self.extra_hand

class Mob:
   def __init__(self, lvl: int):
       self.level = lvl
       self.type = random.choice(MOB_TYPE)
       self.health = randint(50, 100)
       self.damage = randint(5, 15)
       self.protection = randint(5, 10)

#########
# GAME
#########
#########
@bot.slash_command(guild_ids=[GUILD], name="raid", description="Enter the dungeon and fight monstuhs")
async def raid(ctx):
    pass

    ## INITIATES PLAYER DATA BY LOADING THEIR EXISTING ASSOCIATED JSON FILE, OR IF ONE ISNT FOUND LOADS THE USER TEMPLATE AS THEIR DATA
    if os.path.exists(f"{ctx.author.id}.json"):
        with open(f"{ctx.author.id}.json", "r") as f: # r = read mode, w = write mode
            player = json.load(f) # data is now a dict
        print("--- AUTHOR USER DATA LOADED ---")
    else:
        with open("UserTemplate.json", "r") as f: # r = read mode, w = write mode
            player = json.load(f) # data is now a dict
        print("--- USER TEMPLATE DATA LOADED FOR AUTHOR ---")

    ## GENERATES ENEMY TEAM
    enemyTeam = []
    enemyCount = randint(1, 3)
    EncounterText = f"You initiated combat!\n"
    for i in range(enemyCount):
        mob = Mob(1)
        enemyTeam.append(mob)
        EncounterText += f"{mob.type}: {mob.health}hp\n"

    await ctx.respond(EncounterText)

#########
# RUN
#########
#########
bot.run(os.getenv('DUNGEON_TOKEN'))
