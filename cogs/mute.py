import discord
from discord.ext import commands
from discord import app_commands
from config import TEST_GUILDS_ID, GUILDS_ID
from main import client
from datetime import datetime, timedelta, timezone


class Mute(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="mute", description="An axe straight to their head!")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.guilds(*TEST_GUILDS_ID)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: app_commands.Range[int, 1, 40320], reason: str = None):
        # This commands is use to timeout a user with maximum 28 days 
        
        # If the member try to mute the bot, it backfire 
        if member.id == client.user.id:
            await interaction.response.send_message("You shall not mute me, all joke on you!")
            
            return
        
        # If they are already muted
        if member.is_communication_disabled():
            await interaction.response.send_message(f"**{member.display_name}** is already got sent to jail.")
            return 
        
        try: 
            timeout_duration = timedelta(minutes=minutes)
            until_date = datetime.now(timezone.utc) + timeout_duration
            
            await member.edit(timeout=until_date, reason=reason)
            
            await interaction.response.send_message(
                f"{member.mention} has been send to jail " 
                + (f"for {reason}." if reason else ".")                
            )
        except discord.Forbidden: 
            await interaction.response.send_message("")
            
    
async def setup(client):
    await client.add_cog(Mute(client))