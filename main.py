import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import random
import asyncio

load_dotenv()

GUILDS_ID = [
    discord.Object(id=1066207532374294558), #test guild
    discord.Object(id=1354771751527256115)
]

TEST_GUILDS_ID = discord.Object(id=1066207532374294558)

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        try:
            for guild in GUILDS_ID:
                synced = await self.tree.sync(guild=guild)
                print(f'Synced {len(synced)} commands to guild {guild.id}')
            
        except Exception as e:
            print(f'Error syncing commands: {e}')
    
    # async def on_message(self, message):
    #     if message.author == self.user:
    #         return
    #     if message.content.startswith('hello'):
    #         await message.channel.send(f'Hi there {message.author}')
    
    # async def on_reaction_add(self, reaction, user):
    #     await reaction.message.channel.send('You reacted!')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


commands_list = [
    r"`\info` - Information about the bot",
    r"`\roll` - Roll dices"
]

@client.tree.command(name="info", description="Information about the bot", guilds=GUILDS_ID)
async def mathBot(interaction: discord.Interaction):
    embed = discord.Embed(title="Hi! I am Math Bot!", description="A version 2.0 of a bot developed by _HDH", color=discord.Colour.blue());
    embed.add_field(name="List of commands", value="\n".join(commands_list))
    embed.set_footer(text="The bot is currently in development, more commands is on the way!")
    await interaction.response.send_message(embed=embed)

dice_faces = [
    "", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"
]

class DiceRerollButton(discord.ui.View):
    def __init__(self, amount, sides):
        super().__init__()
        self.amount = amount
        self.sides = sides
        self.reroll_count = 0
    @discord.ui.button(label="Reroll!", style=discord.ButtonStyle.red, emoji="🎲")
    async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
        rolls = [random.randint(1, self.sides) for _ in range(self.amount)]
        total = sum(rolls)
        faces = " ".join(dice_faces[r] if self.sides <= 6 and r <= 6 else str(r) for r in rolls)
        embed = discord.Embed(title=f"🎲 Let roll {self.amount} (1-{self.sides})dices!", color=discord.Colour.blue())
        embed.add_field(name="Results", value=faces)
        embed.add_field(name="Total", value=str(total))
        self.reroll_count += 1
        embed.set_footer(text=f"Rerolled {self.reroll_count} times!")
        await interaction.response.edit_message(embed=embed, view=self)
        # await interaction.response.send_message(f" {self.amount}, {self.sides}", embed=embed)

@client.tree.command(name="roll", description="Roll dices", guilds=GUILDS_ID)
@app_commands.describe(amount="Number of dices (default: 1, min: 1, max: 100)", sides="Number of sides (default: 6, min: 1, max: 100)")
async def roll(interaction: discord.Interaction, amount: int = 1, sides: int = 6):
    if amount < 1 or amount > 100 or sides < 1 or sides > 100:
        embed = discord.Embed(title=":bangbang: Limit exceeded! Please request again with a proper amount.", description="The values for `amount` and `sides` are only allow in the range of `1` to `100`.", color=discord.Colour.blue())  
        await interaction.response.send_message(embed=embed)
        return
          
    rolls = [random.randint(1, sides) for _ in range(amount)]
    total = sum(rolls)
    faces = " ".join(dice_faces[r] if sides <= 6 and r <= 6 else str(r) for r in rolls)
    embed = discord.Embed(title=f"🎲 Let roll {amount} (1-{sides})dices!", color=discord.Colour.blue())
    embed.add_field(name="Results", value=faces)
    embed.add_field(name="Total", value=str(total))
    await interaction.response.send_message(embed=embed, view=DiceRerollButton(amount=amount, sides=sides))


# @client.tree.command(name="hello", description="Say hello!", guild=TEST_GUILDS_ID)
# async def sayHello(interaction: discord.Interaction):
#     await interaction.response.send_message("Hi there!")
    
@client.tree.command(name="print", description="I will print whatever you give me!", guild=TEST_GUILDS_ID)
async def printer(interaction: discord.Interaction, print: str):
    await interaction.response.send_message(print) 

@client.tree.command(name="guess", description="Guess a number from 1-10!", guild=TEST_GUILDS_ID)
async def guessNumber(interaction: discord.Interaction, number: int):
    random_number = random.randint(1, 10)
    if random_number == number:
        await interaction.response.send_message(f"✅ You are correct! The number are {random_number}.")
    else: 
        await interaction.response.send_message(f"❌ You are incorrect! The number are {random_number}.") 

@client.tree.command(name="embed", description="Embed demo!", guild=TEST_GUILDS_ID)
async def printer(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a Title", url="https://youtu.be/ESx_hy1n7HA?si=t3AgQTi75Bap1202", description="I am a description", color=discord.Colour.blue())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1066207532839874592/1391697862080856114/Screenshot_2025-07-07_at_15.30.18.png?ex=686cd722&is=686b85a2&hm=48c91d1bae6a10794be9451cd730a2c834c2a34efdd0b134b54760d5b6f257db&")
    embed.add_field(name="Field 1", value="aahhhhh", inline=False)
    embed.add_field(name="Field 2", value="aahhhhh 2")
    embed.set_footer(text="This song is fire!")
    embed.set_author(name=interaction.user.name, url="https://youtu.be/ESx_hy1n7HA?si=t3AgQTi75Bap1202", icon_url=interaction.user.image)
    await interaction.response.send_message(embed=embed)
    
class View(discord.ui.View):
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.red, emoji="🎲")
    async def button_callback(self, button, interaction):
        await button.response.send_message("you have clicked the button!")
    
    @discord.ui.button(label="Click meeeee!", style=discord.ButtonStyle.blurple, emoji="🎲")
    async def button_callback_2(self, button, interaction):
        await button.response.send_message("you have clicked the buttonnnnn!")
        
    @discord.ui.button(label="Click meeee!", style=discord.ButtonStyle.green, emoji="🎲")
    async def button_callback_3(self, button, interaction):
        await button.response.send_message("you have clicked the buttomnnnnn!")
        
@client.tree.command(name="button", description="Displaying a button!", guild=TEST_GUILDS_ID)
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())
    
class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Option 1",
                description="This is option 1",
                emoji="🔥"
            ),
            
            discord.SelectOption(
                label="Option 2",
                description="This is option 2",
                emoji="💀"
            ),
            
            discord.SelectOption(
                label="Option 3",
                description="This is option 3",
                emoji="😋"
            )
        ]
        
        super().__init__(placeholder="Please choose an option: ", min_values=1, max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Option 1":
            await interaction.response.send_message(f" YAY ! You picked {self.values[0]}")

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())
    
@client.tree.command(name="menu", description="Displaying a dropdown menu!", guild=TEST_GUILDS_ID)
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view=MenuView())

async def main():
    initial_extensions = []

    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            initial_extensions.append("cogs." + file_name[:-3])
            
        for extension in initial_extensions:
            await client.load_extension(extension)
        
if __name__ == "__main__":
    asyncio.run(main())
client.run(os.getenv("TOKEN"))
