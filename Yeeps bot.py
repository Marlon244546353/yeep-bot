import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import random
import asyncio

# Set up your bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# List of Yeeps characters
yeeps = [
    {"name": "JB", "image_url": "https://cdn.discordapp.com/attachments/1339583617512243230/1346104446337159189/IMG_0398.png"},
    {"name": "Puffbros", "image_url": "https://cdn.discordapp.com/attachments/1339583617512243230/1346104446672965642/IMG_0396.png"},
    {"name": "Plushy yeep", "image_url": "https://cdn.discordapp.com/attachments/1321264208918085672/1346107849285046302/Yeeps-Hide-Seek-Plush-Toys.png"},
    {"name": "Colebits", "image_url": "https://cdn.discordapp.com/attachments/1339583617512243230/1346174573409865750/IMG_0400.png"},
    {"name": "Arafax", "image_url": "https://cdn.discordapp.com/attachments/1339583617512243230/1346175393367064717/IMG_0402.png"},
    {"name": "Mak_Vr", "image_url": "https://cdn.discordapp.com/attachments/1339583617512243230/1346176571156987924/IMG_0404.png"},
    {"name": "Pirate yeep", "image_url": "https://cdn.discordapp.com/attachments/1321264208918085672/1346177348411854989/pirateyeep.png"},
    {"name": "School yeep", "image_url": "https://cdn.discordapp.com/attachments/1321264208918085672/1346177348634148926/schoolyeep.png"},
    {"name": "Yeti yeep", "image_url": "https://cdn.discordapp.com/attachments/1321264208918085672/1346177348864577547/yetiyeep.png"},
    {"name": "War yeep", "image_url": "https://cdn.discordapp.com/attachments/1321264208918085672/1346177349179281463/waryeep.png"},
    {"name": "Cheese yeep", "image_url": "https://cdn.discordapp.com/attachments/1321264208918085672/1346177349451776062/yoshiyepp.png"},
    {"name": "British Bagel", "image_url": "https://cdn.discordapp.com/attachments/1339583617512243230/1346242773061210194/IMG_0411.png"},
    {"name": "Loafff", "image_url": "https://cdn.discordapp.com/attachments/1339583617512243230/1346242773375909970/IMG_0409.png"},
]

user_captures = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # Sync commands
    await bot.tree.sync()
    print("Slash commands synced!")

    # Removed unregistering old slash commands
    await spawn_yeep_periodically()

async def spawn_yeep_periodically():
    channel = bot.get_channel(1303188158397153366)
    await asyncio.sleep(10)
    while True:
        await asyncio.sleep(random.choice([600, 1200, 300, 600, 1300, 400, 700, 1111, 666, 20, 5, 100, 500]))
        await send_random_yeep(channel)

async def send_random_yeep(channel):
    yeep = random.choice(yeeps)
    embed = discord.Embed(title="A Yeep has appeared!", description="Guess the Yeep's name to catch it!")
    embed.set_image(url=yeep["image_url"])

    button = Button(label="Guess!", style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        modal = Modal(title="Enter Yeep Name")
        text_input = TextInput(label="Yeep Name", placeholder="Type the Yeep's name here...")
        modal.add_item(text_input)

        async def modal_callback(modal_interaction):
            guessed_name = text_input.value.strip()
            if guessed_name.lower() == yeep["name"].lower():
                user_id = modal_interaction.user.id
                if user_id not in user_captures:
                    user_captures[user_id] = []
                if yeep["name"] not in user_captures[user_id]:
                    user_captures[user_id].append(yeep["name"])
                    button.disabled = True  # Disable the button
                    await interaction.message.edit(view=view)  # Update the view
                    await modal_interaction.response.send_message(f"Correct! {modal_interaction.user.name} You caught  {yeep['name']}!")
                else:
                    await modal_interaction.response.send_message(f"{yeep['name']} has already been caught!")
            else:
                await modal_interaction.response.send_message(f"Wrong name! {modal_interaction.user.name}, try again next time.")

        modal.on_submit = modal_callback
        await interaction.response.send_modal(modal)

    button.callback = button_callback
    view = View()
    view.add_item(button)
    await channel.send(embed=embed, view=view)

@bot.tree.command(name="yeep_progress", description="Show your Yeep progress")
async def yeep_progress(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in user_captures and user_captures[user_id]:
        progress = "\n".join(user_captures[user_id])
        await interaction.response.send_message(f"**Your Yeep Progress:**\n{progress}")
    else:
        await interaction.response.send_message("You haven't caught any Yeeps yet!")

@bot.tree.command(name="spawn_yeep", description="Spawn a Yeep (requires Yeep Spawner role)")
async def spawn_yeep(interaction: discord.Interaction):
    role_name = "Yeep Spawner"
    has_role = any(role.name == role_name for role in interaction.user.roles)
    if has_role:
        await send_random_yeep(interaction.channel)
        await interaction.response.send_message("A Yeep has been spawned!")
    else:
        await interaction.response.send_message("You need the 'Yeep Spawner' role to use this command.")

@bot.tree.command(name="give_yeep", description="Give a Yeep to another user (requires Yeep Giver role)")
async def give_yeep(interaction: discord.Interaction, user: discord.User):
    role_name = "Yeep Giver"
    has_role = any(role.name == role_name for role in interaction.user.roles)
    if has_role:
        if user.id not in user_captures:
            user_captures[user.id] = []
        yeep = random.choice(yeeps)
        if yeep["name"] not in user_captures[user.id]:
            user_captures[user.id].append(yeep["name"])
            await interaction.response.send_message(f"{interaction.user.name} has given {yeep['name']} to {user.name}!")
        else:
            await interaction.response.send_message(f"{user.name} already has {yeep['name']}.")
    else:
        await interaction.response.send_message("You need the 'Yeep Giver' role to use this command.")

bot.run('MTM0NjI3MTU0NTgxOTE0MDE2Ng.GEkScK.HCP_TlLDVJaR33Z1IVeE1h0wp2a5YkUNzjitFk')
