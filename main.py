import discord
from discord.ext import commands, tasks
from discord.utils import get
from math import *
import os
import json
import random

client = commands.Bot(command_prefix = "!")

#------------------------------------------------#
#                                                #
#           Timer point + Reset BEG              #
#                                                #
#------------------------------------------------#

client.checkReset = False
@tasks.loop(seconds=86000)
async def reset():
  if client.checkReset == False :
    client.checkReset = True
  else:
    print("reset")
    users = await get_bank_data()
    for user in users:
      users[str(user)]["beg"] = 0
      users[str(user)]["give"] = 0
      users[str(user)]["pitier"] = 0
    with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)

client.checkFree = False
@tasks.loop(seconds=3600)
async def freePoint():
  if client.checkFree == False :
    client.checkFree = True
  else:
    print("freePoint")
    users = await get_bank_data()
    for user in users:
      users[str(user)]["wallet"] += 5
    with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)

client.checkInterest = False
@tasks.loop(seconds=86000)
async def interest():
  if client.checkInterest == False :
    client.checkInterest = True
  else:
    print("interest")
    users = await get_bank_data()
    for user in users:
      users[str(user)]["bank"] =  ceil(users[str(user)]["bank"]*1.01)
    with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)

#------------------------------------------------#
#                                                #
#                  LeaderBoard                   #
#                                                #
#------------------------------------------------#

<<<<<<< HEAD
@client.command(aliases = ["rank"])
async def leaderboard(ctx,x = 5):
=======
@client.command()
async def rank(ctx, param:int):
>>>>>>> aff0b5409e2525d0b8d847d5f81d82d6b0d0ccd4
  users = await get_bank_data()
  leader_board = {}
  total = []
  for user in users:
      name = int(user)
      total_amount = users[user]["wallet"] + users[user]["bank"]
      leader_board[total_amount] = name
      total.append(total_amount)

  total = sorted(total,reverse=True)    

  em = discord.Embed(title = f"Nique La Bac top {x}" , description = "Classement fait sur le total de Coins contenu dans la banque et dans le wallet de chacun.",color = discord.Color(0x053599))
  index = 1
  for amt in total:
      id_ = leader_board[amt]
      member = await client.fetch_user(id_)
      em.add_field(name = f"{index}. {member.name}" , value = f"{amt}",  inline = False)
      if index == x:
          break
      else:
          index += 1

<<<<<<< HEAD
  await ctx.send(embed = em)
=======
  for u in users:
    pass
>>>>>>> aff0b5409e2525d0b8d847d5f81d82d6b0d0ccd4


#------------------------------------------------#
#                                                #
#                      Bet                       #
#                                                #
#------------------------------------------------#
<<<<<<< HEAD
"""
=======

>>>>>>> aff0b5409e2525d0b8d847d5f81d82d6b0d0ccd4

@client.command()
async def bet(ctx, param:int):

  user = ctx.author
  users = await get_bank_data()
  react = await get_reaction_data()
  userWallet = users[str(user.id)]["wallet"]

  if userWallet < param:
    await ctx.send(f"({user.name}) | Vous n'avez pas assez de Coins. ({userWallet}/{param})")
  else:
    await ctx.send(f"({user.name}) | Quel pari voulez-vous faire ?")

  def checkMessage(message):
    return message.author == ctx.message.author

  try:
    pari = await client.wait_for("message", timeout = 60, check = checkMessage)
    message = await ctx.send(f"**{pari.content}** | Veuillez votez en réagissant avec ✅ ou avec ❌ | Somme pour parier ({param})")
    
    react["reaction_message"] = {}
    react["reaction_message"]["id"] = message.id
    with open(os.getenv('REACT_JSON'),"w") as f:
      json.dump(react,f)

    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkEmoji(reaction, user):
      return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

    try:
      reaction, user = await client.wait_for("reaction_add", timeout = 60, check = checkEmoji)
      if reaction.emoji == "✅":
        await ctx.send(f"Fin du vote ! Résultat : ✅")
      else:
        await ctx.send(f"Fin du vote ! Résultat : ❌")
    except:
      await ctx.send("Le pari est fermé.")

  except:
    await ctx.send("Veuillez réitérer la commande.")
    return

@client.event
async def on_reaction_add(reaction, user):
  react = await get_reaction_data()
  bet = await get_bet_data()

  channel = react["reaction_message"]["id"]
  print(channel)
  if reaction.message.channel.id != channel:
    print("False")
    return False
  else:
    if reaction.emoji == "✅":
      print("testBET")
      bet[str(user.id)]["name"] = user.name
      with open(os.getenv('BET_JSON'),"w") as f:
        json.dump(bet,f)
      await ctx.send(f"Nouveau vote : ✅")
<<<<<<< HEAD
    """      
=======
          
>>>>>>> aff0b5409e2525d0b8d847d5f81d82d6b0d0ccd4


#------------------------------------------------#
#                                                #
#                 Kick Server                    #
#                                                #
#------------------------------------------------#

@client.command()
async def kick(ctx, person :discord.Member = None):

  if person is None:
    await ctx.send(f"({user.name}) | Vous devez renseigner le pseudo de la personne | Ex : **!kick @Ursule**")
    return
  else :

    user = ctx.author
    users = await get_bank_data()
    userWallet = users[str(user.id)]["wallet"]

    if userWallet >= 5000:
      await ctx.send(f"{person.name} a été kick du serveur par {user.name}, pour 5000 Coins")
      await person.kick()
      users[str(user.id)]["wallet"] -= 5000
      with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)
    else:
      await ctx.send(f"({user.name}) | Vous ne posséder pas assez de Coins. ({userWallet}/5000)")


#------------------------------------------------#
#                                                #
#                 Mute Server                    #
#                                                #
#------------------------------------------------#

@client.command()
async def mute(ctx, person : discord.Member = None):

  if person is None:
    await ctx.send(f"({user.name}) | Vous devez renseigner le pseudo de la personne | Ex : **!mute @Ursule**")
    return
  else :
    user = ctx.author
    users = await get_bank_data()
    userWallet = users[str(user.id)]["wallet"]

    if userWallet < 2000:
      await ctx.send(f"({user.name}) | Vous n'avez pas assez de Coins. ({userWallet}/2000)")
      return
    else:
      await person.edit(mute = True)
      await ctx.send(f"{person} a été mute par {user.name} pour **2000 Coins**.")
      users[str(user.id)]["wallet"] -= 2000
      with open(os.getenv('USER_JSON'),"w") as f:
              json.dump(users,f)
"""
@client.command()
async def muteText(ctx, person : discord.Member = None):

  role = ctx.guild.get_role(799999674072694805)
  print(" AZERTY ROLE : ")
  print(role)
  if person is None:
    await ctx.send("Vous devez renseigner le pseudo de la personne | Ex : **!muteText @Ursule**")
  else :
    user = ctx.author
    users = await get_bank_data()
  
    await person.add_roles(role)
    await ctx.send(f"{person} a été mute par {user.name}.")
"""

#------------------------------------------------#
#                                                #
#                Unmute Server                   #
#                                                #
#------------------------------------------------#

@client.command()
async def unmute(ctx):

  user = ctx.author
  users = await get_bank_data()
  userWallet = users[str(user.id)]["wallet"]

  if userWallet < 1500:
    await ctx.send(f"({user.name}) | Vous n'avez pas assez de Coins. ({userWallet}/2000)")
    return
  else:
    await user.edit(mute = False)
    await ctx.send(f"{user.name} s'est Unmute pour **1500 Coins**.")
    users[str(user.id)]["wallet"] -= 1500
    with open(os.getenv('USER_JSON'),"w") as f:
            json.dump(users,f)


#------------------------------------------------#
#                                                #
#               Voleur de Coins                  #
#                                                #
#------------------------------------------------#

@client.command()
async def ludoVoleur(ctx, param : int, person : discord.Member = None):
  if person == None :
    await ctx.send(f"({user.name}) | Veuillez renseigner la personne à voler.")
  else:
    
    user = ctx.author
    users = await get_bank_data()
    userWallet = users[str(user.id)]["wallet"]
    
    if userWallet < param:
      await ctx.send(f"({user.name}) | Vous n'avez pas assez de points. ({userWallet}/{param})")
    else : 
      userWalletPoint = users[str(person.id)]["wallet"]
      if userWalletPoint < param:
        await ctx.send(f"({user.name}) | Votre cible n'a pas assez de points. ({userWalletPoint}/{param})")
      else:
        rand = random.uniform(0, 1)
        print(rand)
        if rand >= 0.65:
          users[str(person.id)]["wallet"] -= param
          users[str(user.id)]["wallet"] += param
          await ctx.send(f'({user.name}) | {param} Coins ont été retirés du Wallet de {person} et ont été ajoutés au vôtre.' )
          with open(os.getenv('USER_JSON'),"w") as f:
            json.dump(users,f)
        else:
          users[str(person.id)]["wallet"] += param
          users[str(user.id)]["wallet"] -= param
          await ctx.send(f"({user.name}) | {param} Coins ont été retirés de votre Wallet et ont été ajoutés au Wallet d'{person}." )
          with open(os.getenv('USER_JSON'),"w") as f:
            json.dump(users,f)
      
        

#------------------------------------------------#
#                                                #
#                    Random                      #
#                                                #
#------------------------------------------------#

@client.command()
async def rand(ctx, param:int):

    user = ctx.author
    users = await get_bank_data()
    userWalletoint = users[str(user.id)]["wallet"]

    if users[str(user.id)]["wallet"] < param:
      await ctx.send(f"({user.name}) | Vous n'avez pas assez de Coins. ({userWalletoint}/{param})" )
      return False
    else:
      rand = random.uniform(0, 1)
      print(rand)
      if rand <= 0.5:
        users[str(user.id)]["wallet"] -= param
        await ctx.send(f"({user.name}) | {param} Coins ont été retirés de votre Wallet." )
        with open(os.getenv('USER_JSON'),"w") as f:
          json.dump(users,f)
      else:
        users[str(user.id)]["wallet"] += param
        await ctx.send(f"({user.name}) | {param} Coins ont été ajoutés à votre Wallet." )
        with open(os.getenv('USER_JSON'),"w") as f:
          json.dump(users,f)
      return True


#------------------------------------------------#
#                                                #
#                     Give                       #
#                                                #
#------------------------------------------------#

@client.command()
async def give(ctx, param: int, person : discord.Member = None):
  if person == None :
    await ctx.send(f"({user.name}) | Vous devez renseigner à qui vous voulez donner vos Coins.")
  else:
    user = ctx.author
    users = await get_bank_data()
    userWalletoint = users[str(user.id)]["wallet"]

    if users[str(user.id)]["wallet"] < param:
      await ctx.send(f"({user.name}) | Vous n'avez pas assez de points. ({userWalletoint}/{param})" )
      return False
    else:
      if users[str(user.id)]["give"] > 0:
        await ctx.send(f"({user.name}) | Vous avez déjà give une fois aujourd'hui." )
        return False
      else:
        users[str(user.id)]["wallet"] -= param
        users[str(user.id)]["give"] += 1
        users[str(person.id)]["wallet"] += param
        await ctx.send(f"({user.name}) | {param} coins ont été transférés à {person.name}" )
        with open(os.getenv('USER_JSON'),"w") as f:
          json.dump(users,f)
        return True
        
      

#------------------------------------------------#
#                                                #
#               Pitier monsieur                  #
#                                                #
#------------------------------------------------#

@client.command()
async def pitierMonsieur(ctx):

    user = ctx.author
    users = await get_bank_data()
    pitier = users[str(user.id)]["pitier"]

    if pitier > 4:
      await ctx.send(f"({user.name}) | Vous avez atteint la limite de PitierMonsieur. (Attendez demain)" )
    else:
      if (users[str(user.id)]["wallet"] <= 10 and users[str(user.id)]["bank"] <= 10):
        users[str(user.id)]["pitier"] += 1
        pitier += 1
        await ctx.send(f"({user.name}) | Il s'agirait d'arrêter de parier monsieur ! Voici 50 coins pour vous refaire ({pitier}/5)" )
        users[str(user.id)]["wallet"] += 50
        with open(os.getenv('USER_JSON'),"w") as f:
          json.dump(users,f)
      else:
        await ctx.send(f"({user.name}) | Vous avez encore assez de points sur votre compte." )
        
        

#------------------------------------------------#
#                                                #
#                    Balance                     #
#                                                #
#------------------------------------------------#

@client.command()
async def balance(ctx, person : discord.Member = None):
  
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  if person == None:
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"Coins : {ctx.author.name}",color = discord.Color.red())
    em.add_field(name = "Wallet", value = wallet_amt)
    em.add_field(name = "Bank", value = bank_amt)
    await ctx.send(embed = em)
  else:
    wallet_amt = users[str(person.id)]["wallet"]
    bank_amt = users[str(person.id)]["bank"]

    em = discord.Embed(title = f"Coins : {person.name}",color = discord.Color.red())
    em.add_field(name = "Wallet", value = wallet_amt)
    em.add_field(name = "Bank", value = bank_amt)
    await ctx.send(embed = em)


#------------------------------------------------#
#                                                #
#                 Beg aléatoire                  #
#                                                #
#------------------------------------------------#

@client.command()
async def beg(ctx):

    user = ctx.author
    users = await get_bank_data()

    if users[str(user.id)]["beg"] < 3:
      earnings = random.randrange(11)

      await ctx.send(f"({user.name}) | Quelqu'un t'a donné {earnings} Coins !")

      users[str(user.id)]["wallet"] += earnings
      users[str(user.id)]["beg"] += 1

      with open(os.getenv('USER_JSON'),"w") as f:
          json.dump(users,f)
      
    else:
      await ctx.send(f"({user.name}) | Tu as déjà utilisé trop de fois cette commande aujourd'hui ! Reviens demain.")




#------------------------------------------------#
#                                                #
#              Transfert to Bank                 #
#                                                #
#------------------------------------------------#


@client.command()
async def tC(ctx, param:int):
    user = ctx.author
    users = await get_bank_data()
    userWalletoint = users[str(user.id)]["wallet"]

    if users[str(user.id)]["wallet"] < param:
      await ctx.send(f"({user.name}) | Vous n'avez pas assez de points. ({userWalletoint}/{param})" )
      return False
    else:
      users[str(user.id)]["wallet"] -= param
      users[str(user.id)]["bank"] += param
      with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)
      await ctx.send(f"({user.name}) | {param} Coins ont été transférés à votre banque.")
      return True

@client.command()
async def tCAll(ctx):

    user = ctx.author
    users = await get_bank_data()

    users[str(user.id)]["bank"] += users[str(user.id)]["wallet"]
    users[str(user.id)]["wallet"] = 0
    with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)
    await ctx.send(f"({user.name}) | Tous vos Coins ont été transférés dans votre banque." )
    return True

#------------------------------------------------#
#                                                #
#             Transfert to Wallet                #
#                                                #
#------------------------------------------------#

@client.command()
async def gC(ctx, param:int):

    user = ctx.author
    users = await get_bank_data()
    userWalletoint = users[str(user.id)]["bank"]

    if users[str(user.id)]["bank"] < param:
      await ctx.send(f"({user.name}) | Vous n'avez pas assez de points. ({userWalletoint}/{param})" )
      return False
    else:
      users[str(user.id)]["bank"] -= param
      users[str(user.id)]["wallet"] += param
      with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)
      await ctx.send(f"({user.name}) | {param} Coins ont été transférés à votre Wallet." )
      return True

@client.command()
async def gCAll(ctx):

    user = ctx.author
    users = await get_bank_data()

    users[str(user.id)]["wallet"] += users[str(user.id)]["bank"]
    users[str(user.id)]["bank"] = 0
    with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)
    await ctx.send(f"({user.name}) | Tous vos Coins ont été transférés dans votre Wallet." )
    return True

#------------------------------------------------#
#                                                #
#              Création de compte                #
#                                                #
#------------------------------------------------#

async def open_account(user):
  users = await get_bank_data()

<<<<<<< HEAD
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 200
    users[str(user.id)]["beg"] = 0
    users[str(user.id)]["give"] = 0
    users[str(user.id)]["pitier"] = 0

  with open(os.getenv('RANK_JSON'),"w") as f:
      json.dump(rank,f)

  with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)
=======
    if str(user.id) in users:
      return False
    else:
      users[str(user.id)] = {}
      users[str(user.id)]["wallet"] = 0
      users[str(user.id)]["bank"] = 200
      users[str(user.id)]["beg"] = 0
      users[str(user.id)]["give"] = 0
      users[str(user.id)]["pitier"] = 0
>>>>>>> aff0b5409e2525d0b8d847d5f81d82d6b0d0ccd4


#------------------------------------------------#
#                                                #
#           Récupération des données             #
#                                                #
#------------------------------------------------#

async def get_bank_data():
  with open(os.getenv('USER_JSON'),"r") as f:
    users = json.load(f)
  return users

async def get_reaction_data():
  with open(os.getenv('REACT_JSON'),"r") as f:
    react = json.load(f)
  return react

async def get_bet_data():
  with open(os.getenv('BET_JSON'),"r") as f:
    bet = json.load(f)
  return bet

@client.event
async def on_ready():
  print('Bot NLB est prêt !' )
  reset.start()
  freePoint.start()
  interest.start()

client.run(os.getenv('TOKEN'))