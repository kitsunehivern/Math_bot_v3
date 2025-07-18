import discord
from discord.ext import commands
from discord import app_commands
from config import TEST_GUILDS_ID, GUILDS_ID
import random


class RollDices(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    dice_faces = [
        "", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"
    ]

    class DiceRerollButton(discord.ui.View):
        def __init__(self, amount, sides):
            super().__init__()
            self.amount = amount
            self.sides = sides
            self.reroll_count = 0
            self.dice_faces = ["", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"] # funny code
        @discord.ui.button(label="Reroll!", style=discord.ButtonStyle.red, emoji="🎲")
        async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
            rolls = [random.randint(1, self.sides) for _ in range(self.amount)]
            total = sum(rolls)
            faces = " ".join(self.dice_faces[r] if self.sides <= 6 and r <= 6 else str(r) for r in rolls)
            embed = discord.Embed(title=f"🎲 Let roll {self.amount} (1-{self.sides})dices!", color=discord.Colour.blue())
            embed.add_field(name="Results", value=faces)
            embed.add_field(name="Total", value=str(total))
            self.reroll_count += 1
            embed.set_footer(text=f"Rerolled {self.reroll_count} times!")
            await interaction.response.edit_message(embed=embed, view=self)
            # await interaction.response.send_message(f" {self.amount}, {self.sides}", embed=embed)

    @app_commands.command(name="roll", description="Roll dices")
    @app_commands.describe(amount="Number of dices (default: 1, min: 1, max: 100)", sides="Number of sides (default: 6, min: 1, max: 100)")
    @app_commands.guilds(*GUILDS_ID)
    async def roll(self, interaction: discord.Interaction, amount: int = 1, sides: int = 6):
        if amount < 1 or amount > 100 or sides < 1 or sides > 100:
            embed = discord.Embed(title=":bangbang: Limit exceeded! Please request again with a proper amount.", description="The values for `amount` and `sides` are only allow in the range of `1` to `100`.", color=discord.Colour.blue())  
            await interaction.response.send_message(embed=embed)
            return
            
        rolls = [random.randint(1, sides) for _ in range(amount)]
        total = sum(rolls)
        faces = " ".join(self.dice_faces[r] if sides <= 6 and r <= 6 else str(r) for r in rolls)
        embed = discord.Embed(title=f"🎲 Let roll {amount} (1-{sides})dices!", color=discord.Colour.blue())
        embed.add_field(name="Results", value=faces)
        embed.add_field(name="Total", value=str(total))
        await interaction.response.send_message(embed=embed, view=self.DiceRerollButton(amount=amount, sides=sides))
    
async def setup(client):
    await client.add_cog(RollDices(client))