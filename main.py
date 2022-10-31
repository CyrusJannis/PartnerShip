from cgitb import grey
from math import perm
from nextcord.ext import commands
import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import json
import asyncio
import random

client = commands.Bot(
  command_prefix = "!",
  intents = nextcord.Intents.all()
)


@client.event
async def on_guild_remove(guild):
  with open("data.json", "r") as f:
    data = json.load(f)
  if str(guild.id) in data:
    del data[str(guild.id)]
  with open("data.json", "w") as f:
    json.dump(data, f, indent=4)


@client.event
async def on_ready():
  print("BOT READY!")
  x = []
  for guild in client.guilds:
    x.append(guild.member_count)
  users = sum(x)
  await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing, name=f"Guilds: {len(client.guilds)}\nUsers: {users}"))
  while True:
    with open("data.json", "r") as f:
      data = json.load(f)
    for ids in data:
      name = data[str(ids)]["name"]
      msg = data[str(ids)]["message"]
      inv = data[str(ids)]["link"]
      premium = data[str(ids)]["premium"]
      if premium == "true":
        for test in data:
          if test != ids:
            id = data[str(test)]["channel"]
            c = client.get_channel(int(id))
            embed = nextcord.Embed(title=name, description=f"{msg}\n{inv}")
            try:
              await c.send(f"{name}\n{msg}\n{inv}")
            except Exception as e:
              print(int(id))
              print(e)
      else:
        x = random.randint(1,100)
        print(x)
        if x <= 50:
          for test in data:
            if test != ids:
              id = data[str(test)]["channel"]
              c = client.get_channel(int(id))
              embed = nextcord.Embed(title=name, description=f"{msg}\n{inv}")
              try:
                await c.send(f"{name}\n{msg}\n{inv}")
              except Exception as e:
                print(int(id))
                print(e)
        else:
          continue
      await asyncio.sleep(4000)




class Modal1(nextcord.ui.Modal):
  def __init__(self):
    super().__init__(
      "Don't specify your link in the message"
      )
    self.name = nextcord.ui.TextInput(label="Name", min_length=2, max_length=100, required=True, placeholder="Enter your Server's name", style=nextcord.TextInputStyle.short) # Kleine Box durch den Style
    self.add_item(self.name)
    self.message = nextcord.ui.TextInput(label="Message", min_length=2, max_length=4000, required=True, placeholder="Enter your Advertising message", style=nextcord.TextInputStyle.paragraph) # Große Box durch den Style
    self.add_item(self.message)
  async def callback(self, interaction: nextcord.Interaction) -> None:
    message = self.message.value
    if "@everyone" in self.message.value or "@here" in self.message.value:
      message = "Don't join"
    overwrites = {
      interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel=True, send_messages=False, read_message_history=True),
      client.get_user(1035912997006233753): nextcord.PermissionOverwrite(send_messages=True)
    }
    cat = await interaction.guild.create_category("Partners", overwrites=overwrites)
    channel = await cat.create_text_channel("partners")
    invite = await interaction.channel.create_invite()
    with open("data.json", "r") as f:
        data = json.load(f)
    if str(interaction.guild.id) in data:
        await interaction.response.send_message("You are already registered", ephemeral=True)
    else:
        data[str(interaction.guild.id)] = {

        }
        data[str(interaction.guild.id)]["name"] = str(self.name.value)
        data[str(interaction.guild.id)]["message"] = str(message)
        data[str(interaction.guild.id)]["link"] = str(invite)
        data[str(interaction.guild.id)]["channel"] = channel.id
        data[str(interaction.guild.id)]["premium"] = "true"
        with open("data.json", "w") as f:
          json.dump(data, f, indent=4)
        await interaction.response.send_message("You successfully set up Partners Bot", ephemeral=True)

@client.slash_command(name="start", description="Start your journey with many partners")
@commands.has_permissions(administrator=True)
async def start(interaction: Interaction):
  await interaction.response.send_modal(Modal1())


@client.slash_command(name="stats", description="Get the Bot's stats")
async def stats(interaction: Interaction):
  x = []
  for guild in client.guilds:
    x.append(guild.member_count)
  users = sum(x)
  await interaction.response.send_message(f"Guilds: {len(client.guilds)}\nUsers: {users}")

client.run("MTAzNTkxMjk5NzAwNjIzMzc1Mw.GTLsCx.73G7C9IqijGLSWMrsjtViH1iWHeVK9HfrrJiJA")