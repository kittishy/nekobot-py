import random
from discord.ext import commands,tasks
import discord
from discord import app_commands
from datetime import datetime,timedelta
import time

from database.boosts import addBoost, changeBoost
from database.roles import get_role_id, set_role_id

class Boost(commands.Cog, name="boost"):
    def __init__(self, bot):
        self.bot = bot
            
    lastfirstbooster = None
    @commands.Cog.listener()
    async def on_member_update(self, before,after):
        servidor =  after.guild
        onebooster = servidor.premium_subscriber_role
        doublebooster = servidor.get_role(get_role_id())

        if onebooster in before.roles and onebooster not in after.roles:
            await after.remove_roles(doublebooster)  
            canal = after.guild.system_channel
            await canal.send(f"{after.mention} não é mais Booster")
            await changeBoost(after,0)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild == None:
            return
        
        if message.guild.system_channel == None:
            return
        
        if message.channel.id == message.guild.system_channel.id:
            if message.type in [discord.MessageType.premium_guild_subscription,discord.MessageType.premium_guild_tier_1,discord.MessageType.premium_guild_tier_2,discord.MessageType.premium_guild_tier_3]:
                
                usuariobooster = message.author

                boosts = await addBoost(usuariobooster)

                if boosts >= 2:
                    servidor = message.guild
                    doublebooster = servidor.get_role(get_role_id())
                    await message.author.add_roles(doublebooster)
                    await message.channel.send(f"{message.author.mention} virou 2x booster")
                else:
                    await message.channel.send(f"{message.author.mention} virou 1x booster")

        
    @commands.hybrid_command(name="configurar",description='Configure seu bot de impulsos')
    @app_commands.default_permissions(administrator=True)
    async def configurar(self, interaction: discord.Interaction):
        await interaction.send(content="Carregando...", ephemeral=True)
        try:
            doubleboosterrole = await interaction.guild.create_role(name="Double Booster")
            set_role_id(doubleboosterrole.id)

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
            }
            created_channel = await interaction.guild.create_text_channel(name="notificações-boosts", overwrites=overwrites)

            await interaction.guild.edit(
                system_channel=created_channel,
                system_channel_flags=discord.SystemChannelFlags(premium_subscriptions=True)
            )

            for member in interaction.guild.members:
                if member.premium_since is not None:
                    await changeBoost(member, 1)
        except Exception as e:
            await interaction.send(content=f"Não foi possível finalizar a ação, erro:{e}", ephemeral=True)
        else:
            await interaction.send(
                content=f"🎉 Operação concluída! Você pode agora editar os cargos e canais usados na configuração:\n> Cargo {doubleboosterrole.mention} criado.\n> Canal {created_channel.mention} criado.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Boost(bot))