# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
import anilist

import discord

import os

import json

#globals
animes_select_message =discord.message.Message
reactionstr = [":one:", ":two:", ":three:", ":four:", ":five:"]
lolnick = "none"
options =list()

anilistapi = anilist.Anilist()

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

with open('users.json', 'r') as usersfile:
  users = json.loads(usersfile.read())


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('&ola'):
    if message.author.name == "kaniroba":
      await message.channel.send('Olá papai!')
    else:
      await message.channel.send('Ola ' + message.author.name)

  if message.content.startswith('&animes'):

    if message.author.name not in users.keys():
      users[message.author.name] = {'animes': []}
      await message.channel.send("Você não tem nenhum anime adicionado.")
      print(users)
      with open('users.json', 'w') as usersfile:
        json.dump(users, usersfile)
    else:
      conteudo = message.content.split(' ')
      if len(conteudo) >2:
        action = conteudo[1]
        search = ''.join(conteudo[2:])
        
        if action == 'adicionar':
          options = anilistapi.busca(search)
          
          optionmessage =""
          i = -1
          
          for option in options:
            optionmessage += reactionstr[i:=i+1] + (option["title"]["romaji"] + "\n")
          
          animes_select_message = await message.channel.send(optionmessage)
          
        
        elif action == 'remover':
           users[message.author.name]['animes'].remove(search)
        
        elif action == 'listar':
            response = "Lista de animes de " + message.author.name + "/n"
            response += '\n'.join(users[message.author.name]['animes'])
            await message.channel.send(response)
        
        

      else:
        await message.channel.send(
            """Você precisa digitar uma ação e o nome do anime.
        Ex: &animes <acao> <anime>
        ações disponivels:
        adicionar
        remover
        listart""")

  if message.content.startswith('&help'):
    await message.channel.send(
        "Sou um bot criado pelo Kani Roba Cunha, qualquer duvida dirija-se a ele."
    )
  if message.content.startswith('&lol'):
    await message.channel.send("Função sendo trabalhada")


@client.event
async def on_reaction_add(reaction, user):
    if user != client.user and reaction.message == animes_select_message:
      try:
        emoji = str(reaction)
        index = reactionstr.index(emoji)  # Obtém o índice da reação na lista reactionstr
        selected_anime = options[index]  # Obtém o anime correspondente à reação

        # Adicione o anime à lista do usuário
        user_animes = users.get(user.name, {'animes': []})
        user_animes['animes'].append(selected_anime["title"]["romaji"])
        users[user.name] = user_animes

        # Atualize o arquivo JSON
        with open('users.json', 'w') as usersfile:
            json.dump(users, usersfile)

        # Envie uma mensagem de confirmação
        await reaction.message.channel.send(f'{user.mention}, você adicionou "{selected_anime["title"]["romaji"]}" à sua lista de animes.')
      except Exception as e:
        await reaction.message.channel.send(f'{user.mention}, houve um erro: '+ str(e))

token = os.getenv("TOKEN") or ""
if token == "":
  raise Exception("Please add your token to the Secrets pane.")
client.run(token)
