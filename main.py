import discord
from discord.ext import commands, tasks
from discord.utils import get
from math import *
import os
import json
import random
import asyncio
import aiocron

client = commands.Bot(command_prefix = "!")




#------------------------------------------------#
#                                                #
#                  LeaderBoard                   #
#                                                #
#------------------------------------------------#

@client.command(aliases = ["rank"])
async def leaderboard(ctx,x = 5):
  users = await get_bank_data()
  users.pop('798302007106338839')
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

  await ctx.send(embed = em)


#------------------------------------------------#
#                                                #
#                    Giveway                     #
#                                                #
#------------------------------------------------#


def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]


@client.command()
async def giveaway(ctx):

  users = await get_bank_data()

  await ctx.send("Le giveway commence !")
  questions = ["Sur quel channel ?", 
              "Quel est la durée de ton giveway ? (s|m|h|d) | Ex : *30m* pour 30 minutes.",
              "Quel est le prix du giveaway ?"]
  answers = []
  def check(m):
      return m.author == ctx.author and m.channel == ctx.channel 

  for i in questions:
      await ctx.send(i)

      try:
          msg = await client.wait_for('message', timeout=15.0, check=check)
      except asyncio.TimeoutError:
          await ctx.send('Tu n\'as pas répondu dans les temps! Recommence.')
          return
      else:
          answers.append(msg.content)
  try:
      c_id = int(answers[0][2:-1])
  except:
      await ctx.send(f"Vous n'avez pas renseigné le channel correctement. Il doit-être renseigné de cette façon : {ctx.channel.mention}, la prochaine fois.")
      return
  channel = client.get_channel(c_id)
  time = convert(answers[1])
  if time == -1:
      await ctx.send(f"Vous n'avez pas renseigné le temps avec la bonne unité. Utilisé (s|m|h|d) la prochaine fois !")
      return
  elif time == -2:
      await ctx.send(f"Le temps doit être un entier. Rentrer un entier la prochaine fois.")
      return            
  prize = answers[2]
  if int(prize) > users[str(ctx.author.id)]["wallet"]:
    await ctx.send(f'({ctx.author}) Tu n\'as pas assez de points pour lancer ton giveway. ({prize}/{users[str(ctx.author.id)]["wallet"]})!')
    return
  
  await ctx.send(f"Le giveway va être dans le salon {channel.mention} et va durer {answers[1]}!")


  embed = discord.Embed(title = "Giveaway!", description = f"{prize} Coins", color = ctx.author.color)
  embed.add_field(name = "Lancé par :", value = ctx.author.mention)
  embed.set_footer(text = f"Se termine dans {answers[1]} à partir de maintenant !")
  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("✅")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))
  winner = random.choice(users)

  await channel.send(f"Résultat du Giveaway lancé par {ctx.author}. Bravo à {winner.mention} qui a gagné {prize} Coins !")
  
  users = await get_bank_data()

  users[str(winner.id)]["wallet"] += int(prize)
  users[str(ctx.author.id)]["wallet"] -= int(prize)
  with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)

#------------------------------------------------#
#                                                #
#                      Bet                       #
#                                                #
#------------------------------------------------#

@client.command()
async def bet(ctx):

  user = ctx.author
  users = await get_bank_data()
  userWallet = users[str(user.id)]["wallet"]

  questions = ["Sur quel channel ?", 
              "Quel est la durée de ton bet ? (s|m|h|d) | Ex : *30m* pour 30 minutes.",
              "Quel est le prix pour participer ?",
              "Quel pari voulez vous faire ?"]
  answers = []
  def check(m):
      return m.author == ctx.author and m.channel == ctx.channel 

  for i in questions:
      await ctx.send(i)

      try:
          msg = await client.wait_for('message', timeout=60.0, check=check)
      except asyncio.TimeoutError:
          await ctx.send('Tu n\'as pas répondu dans les temps! Recommence.')
          return
      else:
          answers.append(msg.content)
  try:
      c_id = int(answers[0][2:-1])
  except:
      await ctx.send(f"Vous n'avez pas renseigné le channel correctement. Il doit-être renseigné de cette façon : {ctx.channel.mention}, la prochaine fois.")
      return
  channel = client.get_channel(c_id)
  time = convert(answers[1])
  if time == -1:
      await ctx.send(f"Vous n'avez pas renseigné le temps avec la bonne unité. Utilisé (s|m|h|d) la prochaine fois !")
      return
  elif time == -2:
      await ctx.send(f"Le temps doit être un entier. Rentrer un entier la prochaine fois.")
      return            
  prize = answers[2]
  if int(prize) > users[str(ctx.author.id)]["bank"]:
    await ctx.send(f'({ctx.author}) Tu n\'as pas assez de points pour lancer ton giveway. ({prize}/{users[str(ctx.author.id)]["bank"]})!')
    return

  pari = answers[3]

  embed = discord.Embed(title = "Bet !", description = f"**{pari}**", color = 15844367)
  embed.add_field(name = "Coins", value = prize, inline=True)
  embed.add_field(name = "Lancé par : ", value = ctx.author.mention, inline=True)
  embed.set_footer(text = f"Se termine dans {answers[1]} à partir de maintenant !")
  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("✅")
  await my_msg.add_reaction("❌")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  usersTrue = await new_msg.reactions[0].users().flatten()
  usersTrue.pop(usersTrue.index(client.user))
  for u in usersTrue:
    if users[str(u.id)]["bank"] < int(prize) :
      usersTrue.pop(usersTrue.index(u))

  usersFalse = await new_msg.reactions[1].users().flatten()
  usersFalse.pop(usersFalse.index(client.user))
  for u in usersFalse:
    if users[str(u.id)]["bank"] < int(prize) :
      usersFalse.pop(usersFalse.index(u))

  message = await channel.send(f"{ctx.author} | Le bet est finit, quel était le bon choix ?")
  await message.add_reaction("✅")
  await message.add_reaction("❌")

  def checkEmoji(reaction, user):
      return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")

  reaction, user = await client.wait_for("reaction_add", check = checkEmoji)
  if reaction.emoji == "✅":
    countT=0
    countF=0
    for u in usersTrue:
      countT += 1
    for u in usersFalse:
      countF += 1
    
    if countT == 0:
      await ctx.send(f"Personne ne gagne le Bet.")
      for user in usersFalse:
        users[str(user.id)]["bank"] -= int(prize)
      with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)
      return False
    else:
      count = countT+countF
      gain = (int(prize)*count)/countT
      await channel.send(f"Fin du vote ! Résultat : ✅")
      for user in usersTrue:
        await channel.send(f"Bravo à {user} qui a gagné {gain} Coins !")
        users[str(user.id)]["bank"] -= int(prize)
        users[str(user.id)]["bank"] += int(gain)
      for user in usersFalse:
        users[str(user.id)]["bank"] -= int(prize)
      with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)


  else:
    countT=0
    countF=0
    for user in usersTrue:
      countT += 1
    for user in usersFalse:
      countF += 1

    if countF == 0:
      await ctx.send(f"Personne ne gagne le Bet.")
      for user in usersTrue:
        users[str(user.id)]["bank"] -= int(prize)
      with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)
      return False
    else:    
      count = countT+countF
      gain = (int(prize)*count)/countF
      await channel.send(f"Fin du vote ! Résultat : ❌")
      for user in usersTrue:
        users[str(user.id)]["bank"] -= int(prize)
      for user in usersFalse:
        await channel.send(f"Bravo à {user} qui a gagné {gain} Coins !")
        users[str(user.id)]["bank"] -= int(prize)
        users[str(user.id)]["bank"] += int(gain)
      with open(os.getenv('USER_JSON'),"w") as f:
        json.dump(users,f)  


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
#                    LootBox                     #
#                                                #
#------------------------------------------------#

@client.command(aliases = ["box"])
async def lootBox(ctx):
  user = ctx.author
  users = await get_bank_data()

  embed = discord.Embed(title = "Loot Disponible", description = "Coût de la LootBox : **250 Coins**", color = 3426654)
  embed.add_field(name = "100 Coins", value = "33.5%", inline=True)
  embed.add_field(name = "0 Coins", value = "20%", inline=True)
  embed.add_field(name = "500 Coins", value = "15%", inline=True)
  embed.add_field(name = "1 000 Coins", value = "5%", inline=True)
  embed.add_field(name = "Random Coins [0 - 2500]", value = "3%", inline=True)
  embed.add_field(name = "Random Coins [0 - 10000]", value = "1%", inline=True)
  embed.add_field(name = "10 000 Coins", value = "1%", inline=True)
  
  embed.add_field(name = "Banque x1.05", value = "5%", inline=True)
  embed.add_field(name = "Banque x1.1", value = "2.5%", inline=True)
  embed.add_field(name = "Banque x1.25", value = "1%", inline=True)
  embed.add_field(name = "Banque x0.8", value = "5%", inline=True)
  embed.add_field(name = "Banque x0.5", value = "2.5%", inline=True)
  embed.add_field(name = "Banque = 0", value = "0.5%", inline=True)
  embed.add_field(name = "FreeLoot Box", value = "5%", inline=True)
  embed.set_footer(text = f"Cocher ✅ pour jouer !")
  message = await ctx.send(embed = embed)
  await message.add_reaction("✅")

  def checkEmoji(reaction, user):
      return ctx.message.author == user and message.id == reaction.message.id and str(reaction.emoji) == "✅"
  
  def check(m):
      return m.author == ctx.author and m.channel == ctx.channel

  reaction, user = await client.wait_for("reaction_add", check = checkEmoji)
  if reaction.emoji == "✅":
    userWallet = users[str(user.id)]["wallet"]
    if userWallet < 250:
      await ctx.send(f"({user.name}) | Vous n'avez pas assez de Coins. ({userWallet}/250)")
    else:

      number = random.randrange(1000)
      number += 1

      users[str(user.id)]["wallet"] -= 250
      with open(os.getenv('USER_JSON'),"w") as f:
            json.dump(users,f)

      if 1 <= number < 335:  # 100 Coins
        await ctx.send(f"({user.name}) | Vous avez gagné **100  Coins**.")
        users[str(user.id)]["wallet"] += 100
      elif 335 <= number < 535: # 0 Coins
        await ctx.send(f"({user.name}) | Vous avez gagné **0  Coins**.")
      elif 535 <= number < 685: # 500 Coins
        await ctx.send(f"({user.name}) | Vous avez gagné **500  Coins**.")
        users[str(user.id)]["wallet"] += 500
      elif 685 <= number < 735: # 1 000 Coins
        await ctx.send(f"({user.name}) | Vous avez gagné **1 000  Coins**.")
        users[str(user.id)]["wallet"] += 1000
      elif 735 <= number < 745: # random [0 - 10 000] Coins
        rand = random.randrange(10000)
        rand += 1
        await ctx.send(f"({user.name}) | Vous avez gagné un nombre random **[0 - 10 000] Coins**.")
        await ctx.send(f"Résultat : **{rand} Coins**.")
        users[str(user.id)]["wallet"] += int(rand)
      elif 745 <= number < 775: # random [0 - 2 500] Coins
        rand = random.randrange(2500)
        rand += 1
        await ctx.send(f"({user.name}) | Vous avez gagné un nombre random **[0 - 2 500] Coins**.")
        await ctx.send(f"Résultat : **{rand} Coins**.")
        users[str(user.id)]["wallet"] += int(rand)
      elif 775 <= number < 785: # 10 000 Coins
        await ctx.send(f"({user.name}) | Vous avez gagné **10 000  Coins**.")
        users[str(user.id)]["wallet"] += 10000
      elif 785 <= number < 835: # Banque x 1.05
        await ctx.send(f"({user.name}) | Votre banque a été multipliée par **1.05**.")
        users[str(user.id)]["wallet"] += 250
        users[str(user.id)]["bank"] =  ceil(users[str(user.id)]["bank"]*1.05)
      elif 835 <= number < 860: # Banque x 1.1
        await ctx.send(f"({user.name}) | Votre banque a été multipliée par **1.1**.")
        users[str(user.id)]["wallet"] += 250
        users[str(user.id)]["bank"] =  ceil(users[str(user.id)]["bank"]*1.1)
      elif 860 <= number < 870: # Banque x 1.25
        await ctx.send(f"({user.name}) | Votre banque a été multipliée par **1.25**.")
        users[str(user.id)]["wallet"] += 250
        users[str(user.id)]["bank"] =  ceil(users[str(user.id)]["bank"]*1.25)
      elif 870 <= number < 875: # Banque x 0
        await ctx.send(f"({user.name}) | Votre banque a été multipliée par **0**.")
        users[str(user.id)]["wallet"] += 250
        users[str(user.id)]["bank"] =  ceil(users[str(user.id)]["bank"]*0)
      elif 875 <= number < 900: # Banque x 0.5
        await ctx.send(f"({user.name}) | Votre banque a été multipliée par **0.5**.")
        users[str(user.id)]["wallet"] += 250
        users[str(user.id)]["bank"] =  int(users[str(user.id)]["bank"]/2)
      elif 900 <= number < 950: # Banque x 0.8
        await ctx.send(f"({user.name}) | Votre banque a été multipliée par **0.8**.")
        users[str(user.id)]["wallet"] += 250
        users[str(user.id)]["bank"] =  int(users[str(user.id)]["bank"]/1.25)
      elif 950 <= number < 1000: #FreeLoot Box
        await ctx.send(f"({user.name}) | LootBox free.")
        users[str(user.id)]["wallet"] += 250
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
#                     Admin                      #
#                                                #
#------------------------------------------------#

@client.command()
async def adminAdd(ctx, param:int, person : discord.Member = None):
  await ctx.message.delete()
  user = ctx.author
  users = await get_bank_data()
  print("----------------")
  print(user.id)
  print(user.id==211153408709754880)
  print("----------------")
  if ((user.id == 211153408709754880) or (user.id == 798302007106338839)):
    if person == None :
      await ctx.send(f"({user.name}) | Vous devez renseigner une personne.")
    else: 
      users[str(person.id)]["bank"] += param
      await ctx.send(f"(**ADMIN COMMAND**) | {param} Coins ont été ajoutés à {person}.")
      with open(os.getenv('USER_JSON'),"w") as f:
            json.dump(users,f)
  else:
    await ctx.send(f"({user.name}) | Vous n'avez pas les droits pour exécuter cette commande.")
  

@client.command()
async def adminDel(ctx, param:int, person : discord.Member = None):
  await ctx.message.delete()
  user = ctx.author
  users = await get_bank_data()
  print("----------------")
  print(user.id)
  print("----------------")
  if user.id == 211153408709754880:
    if person == None :
      await ctx.send(f"({user.name}) | Vous devez renseigner une personne.")
    else: 
      if users[str(person.id)]["wallet"] < param:
        if users[str(person.id)]["bank"] < param:
          total = users[str(person.id)]["wallet"] + users[str(person.id)]["bank"]
          if total < param :
            await ctx.send(f"({user.name}) | L'utilisateur n'a pas assez de points.")
          else :
            total -= param
            users[str(person.id)]["bank"] = total
            users[str(person.id)]["wallet"] = 0
            await ctx.send(f"(**ADMIN COMMAND**) | {param} Coins ont été retirés à {person}.")
            with open(os.getenv('USER_JSON'),"w") as f:
              json.dump(users,f)
        else:
          users[str(person.id)]["bank"] -= param
          await ctx.send(f"(**ADMIN COMMAND**) | {param} Coins ont été retirés à {person}.")
          with open(os.getenv('USER_JSON'),"w") as f:
              json.dump(users,f)
      else:
        users[str(person.id)]["wallet"] -= param
        await ctx.send(f"(**ADMIN COMMAND**) | {param} Coins ont été retirés à {person}.")
        with open(os.getenv('USER_JSON'),"w") as f:
          json.dump(users,f)
  else:
    await ctx.send(f"({user.name}) | Vous n'avez pas les droits pour exécuter cette commande.")
  
    



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

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 200
    users[str(user.id)]["beg"] = 0
    users[str(user.id)]["give"] = 0
    users[str(user.id)]["pitier"] = 0

  with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)


#------------------------------------------------#
#                                                #
#           Récupération des données             #
#                                                #
#------------------------------------------------#

async def get_bank_data():
  with open(os.getenv('USER_JSON'),"r") as f:
    users = json.load(f)
  return users

async def get_bet_data():
  with open(os.getenv('BET_JSON'),"r") as f:
    bet = json.load(f)
  return bet

@client.event
async def on_ready():
  print('Bot NLB est prêt !' )
  asyncio.get_event_loop().run_forever()
  

#------------------------------------------------#
#                                                #
#                  Timer Action                  #
#                                                #
#------------------------------------------------#


@aiocron.crontab('0 0 * * *')
async def reset():
 
  print("reset")
  users = await get_bank_data()
  for user in users:
    users[str(user)]["beg"] = 0
    users[str(user)]["give"] = 0
    users[str(user)]["pitier"] = 0
  with open(os.getenv('USER_JSON'),"w") as f:
    json.dump(users,f)

client.checkFree = False
@aiocron.crontab('0 * * * *')
async def freePoint():
  
  print("freePoint")
  users = await get_bank_data()
  for user in users:
    users[str(user)]["wallet"] += 5
  with open(os.getenv('USER_JSON'),"w") as f:
    json.dump(users,f)

@aiocron.crontab('0 23 * * *')
async def interest():
  
  print("interest")
  users = await get_bank_data()
  for user in users:
    users[str(user)]["bank"] =  ceil(users[str(user)]["bank"]*1.01)
  with open(os.getenv('USER_JSON'),"w") as f:
    json.dump(users,f)


@aiocron.crontab('0 22 * * *')
async def giveW():
  users = await get_bank_data()

  duree = "30m"

  channel = client.get_channel(637209521202266124)
  time = convert(duree)      
  prize = "500"

  embed = discord.Embed(title = "Giveaway journalier!", description = f"{prize} Coins", color = 1752220)
  embed.set_footer(text = f"Se termine dans {duree} à partir de maintenant !")
  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("✅")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))
  winner = random.choice(users)

  await channel.send(f"Résultat du Giveaway : Bravo à {winner.mention} qui a gagné {prize} Coins !")
  
  users = await get_bank_data()

  users[str(winner.id)]["wallet"] += int(prize)
  with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)

@aiocron.crontab('0 21 * * 0')
async def giveWeek():
  users = await get_bank_data()

  duree = "59m"

  channel = client.get_channel(637209521202266124)
  time = convert(duree)      
  prize = "1000"

  embed = discord.Embed(title = "Giveaway Dominical !", description = f"{prize} Coins", color = 1752220)
  embed.set_footer(text = f"Se termine dans {duree} à partir de maintenant !")
  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("✅")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))
  winner = random.choice(users)

  await channel.send(f"Résultat du Giveaway : Bravo à {winner.mention} qui a gagné {prize} Coins !")
  
  users = await get_bank_data()

  users[str(winner.id)]["wallet"] += int(prize)
  with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)

@aiocron.crontab('0 20 1 * *')
async def giveMouth():
  users = await get_bank_data()

  duree = "59m"

  channel = client.get_channel(637209521202266124)
  time = convert(duree)      
  prize = "5000"

  embed = discord.Embed(title = "Giveaway Mensuel !", description = f"{prize} Coins", color = 1752220)
  embed.set_footer(text = f"Se termine dans {duree} à partir de maintenant !")
  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("✅")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))
  winner = random.choice(users)

  await channel.send(f"Résultat du Giveaway : Bravo à {winner.mention} qui a gagné {prize} Coins !")
  
  users = await get_bank_data()

  users[str(winner.id)]["wallet"] += int(prize)
  with open(os.getenv('USER_JSON'),"w") as f:
      json.dump(users,f)



client.run(os.getenv('TOKEN'))
