import discord
from os import getenv
import traceback

class MyClient(discord.Client):
  async def on_ready(self):
    self.user_list = {}
    print(f'Logged on as {self.user}!')
    print("------")

  async def on_message(self, message):
    if message.author.id == self.user.id:
        return

    guildId = str(message.guild.id)

    if guildId not in self.user_list:
      self.user_list[guildId] = []

    if message.content.startswith('n.join'):
      self.user_list[guildId].append(message.author.id)

    if message.content.startswith('n.leave'):
      self.user_list[guildId].remove(message.author.id)

    msg = f'Message from **{message.author}** in {message.channel.name}:\n{message.content}'

    for id in self.user_list[guildId]:
      mem = message.guild.get_member(id)
      if not mem:
        print(f'user {id} was not found')
        continue
      await mem.send(msg)

intents = discord.Intents.all()
client = MyClient(intents=intents)

token = getenv('DISCORD_BOT_TOKEN')
client.run(token)
