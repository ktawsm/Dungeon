import json
import os
import discord
import random
import enum
from random import randint
from discord.ext import commands
from discord.commands import Option
from dotenv import load_dotenv

# CONNECTS GUILD ID AND BOT TOKEN THROUGH ENV VARIABLES
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
class Item:
   def __init__(self):
       self.cost = 0
       self.hands = 0
       self.type = "Unknown"
       self.enchantments = []
       self.damage = 0
       self.protection = 0
       self.durability = 1  

class Mob:
   def __init__(self, lvl: int):
       self.level = lvl
       self.type = random.choice(MOB_TYPE)
       self.health = randint(50, 100)
       self.damage = randint(5, 15)
       self.protection = randint(5, 10)

class Player:
   def __init__(self, user: discord.Member):
        data = loadPlayerData(user)
        self.level = data["player"]["level"]
        self.experience
        self.equipped = []

#########
# FUNCTIONS
#########
#########

# Load player
def loadPlayerData(player: discord.Member):
    if os.path.exists(f"{player.id}.json"):
        print("Loading player data: " + str({player.id}))
        with open(f"{player.id}.json", 'r') as f:
            playerDictionary = json.load(f)
    else:
        print("Loading player data as template: " + str({player.id}))
        with open(f"UserTemplate.json", 'r') as f:
            playerDictionary = json.load(f)
    return playerDictionary

# Save player
def savePlayerData(player:discord.Member, dictionary: dict):
    print("Saving player data: " + str({player.id}))
    with open(f"Users\\{player.id}.json", 'w') as f:
        f = json.dump(dictionary, f, indent=2)


#########
# GAME
#########
#########

# RAID COMMAND 
@bot.slash_command(guild_ids=[GUILD], name="raid", description="Enter the dungeon and fight monstuhs")
async def raid(ctx):
  #  ## (remaking as its own function) INITIATES PLAYER DATA BY LOADING THEIR EXISTING ASSOCIATED JSON FILE, OR IF ONE ISNT FOUND LOADS THE USER TEMPLATE AS THEIR DATA
  #  if os.path.exists(f"{ctx.author.id}.json"):
  #      with open(f"{ctx.author.id}.json", "rw") as f: # r = read mode, w = write mode
  #          player = json.load(f) # data is now a dict
  #          json.dump(player, f, indent = 4)
  #      print("--- AUTHOR USER DATA LOADED ---")
  #  else:
  #      with open("UserTemplate.json", "r") as f: # r = read mode, w = write mode
  #          player = json.load(f) # data is now a dict
  #      print("--- USER TEMPLATE DATA LOADED FOR AUTHOR ---")
    playerData = loadPlayerData(ctx.author)

    ## GENERATES ENEMY TEAM
    enemyTeam = []
    enemyCount = randint(1, 3)
    EncounterText = f"You initiated combat!\n"
    for i in range(enemyCount):
        mob = Mob(1)
        enemyTeam.append(mob)
        EncounterText += f"{mob.type}: {mob.health}hp\n"
    print(f"Generated player data: " + str(EncounterText))
    savePlayerData(ctx.author, playerData)
    await ctx.respond(EncounterText)


#########
# RUN
#########
#########
bot.run(os.getenv('DUNGEON_TOKEN'))
