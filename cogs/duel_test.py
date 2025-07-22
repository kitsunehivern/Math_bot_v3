import discord
from discord.ext import commands
from discord import app_commands
from config import TEST_GUILDS_ID, GUILDS_ID
import random

class DuelTest(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    current_duel = []
    
    

    @app_commands.command(name="duel_test", description="Test funny duel function")
    @app_commands.guilds(*GUILDS_ID)
    async def mathBot(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{interaction.user.display_name} challenges you to a dice duel!",
            description="A valiant duel of rolling dices to see the luckiest person!",
            color=discord.Colour.blurple()
        )
        
        class AcceptDuelButton(discord.ui.View):
            def __init__(self, challenger):
                super().__init__()
                self.challenger = challenger
                
            @discord.ui.button(
                label="Accept", 
                style=discord.ButtonStyle.red,
                emoji="⚔️"
            )
            async def accept(self, interaction: discord.Interaction, button: discord.ui.button):
                embed = discord.Embed(
                    title=f"⚔️ {interaction.user.display_name} accepted {self.challenger}'s duel!",
                    color=discord.Colour.blurple(),
                )
                
                dice_faces = [
                    "", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"
                ]
                
                A_roll = random.randint(1, 6)
                B_roll = random.randint(1, 6)
                reroll_count = 0
                while A_roll == B_roll:
                    A_roll = random.randint(1, 6)
                    B_roll = random.randint(1, 6)
                    
                embed.add_field(
                    name=f"{self.challenger}'s roll", 
                    value=dice_faces[A_roll],
                    inline=True
                    )
                embed.add_field(
                    name=f"{interaction.user.display_name}'s roll", 
                    value=dice_faces[B_roll],
                    inline=True
                    )
                
                winner = self.challenger if A_roll > B_roll else interaction.user.display_name
                embed.add_field(
                    name=f"{winner} emerged victory!!!", 
                    value="",
                    inline=False
                )
                
                embed.set_footer(text=f"Reroll total: {reroll_count}")
                
                
                await interaction.response.edit_message(
                    embed=embed,
                    view=None
                )
                
        await interaction.response.send_message(embed=embed, view=AcceptDuelButton(challenger=interaction.user.display_name))    
    
    
async def setup(client):
    await client.add_cog(DuelTest(client))