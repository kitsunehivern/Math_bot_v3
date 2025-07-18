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