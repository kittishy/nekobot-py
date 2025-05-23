import random
from discord.ext import commands, tasks
import discord
from discord import app_commands
from datetime import datetime, timedelta
import time

from database.boosts import addBoost, changeBoost
from database.roles import get_role_id, set_role_id

class Boost(commands.Cog, name="boost"):
    def __init__(self, bot):
        self.bot = bot
        
    lastfirstbooster = None
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        servidor = after.guild
        onebooster = servidor.premium_subscriber_role
        doublebooster = servidor.get_role(get_role_id())

        if onebooster in before.roles and onebooster not in after.roles:
            await after.remove_roles(doublebooster)
            
            canal = after.guild.system_channel
            await canal.send(f"{after.mention} não é mais Booster")
            await changeBoost(after, 0)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild == None:
            return
            
        if message.guild.system_channel == None:
            return
            
        if message.channel.id == message.guild.system_channel.id:
            if message.type in [discord.MessageType.premium_guild_subscription, discord.MessageType.premium_guild_tier_1, discord.MessageType.premium_guild_tier_2, discord.MessageType.premium_guild_tier_3]:
                
                usuariobooster = message.author
                
                boosts = await addBoost(usuariobooster)
                
                if boosts >= 2:
                    servidor = message.guild
                    doublebooster = servidor.get_role(get_role_id())
                    await message.author.add_roles(doublebooster)
                    await message.channel.send(f"{message.author.mention} virou 2x booster")
                else:
                    await message.channel.send(f"{message.author.mention} virou 1x booster")

    @commands.hybrid_command(name="configurar", description='Configure seu bot de impulsos')
    @app_commands.default_permissions(administrator=True)
    async def configurar(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Carregando...", ephemeral=True)
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
            await interaction.followup.send(content=f"Não foi possível finalizar a ação, erro:{e}", ephemeral=True)
        else:
            await interaction.followup.send(
                content=f"🎉 Operação concluída! Você pode agora editar os cargos e canais usados na configuração:\n> Cargo {doubleboosterrole.mention} criado.\n> Canal {created_channel.mention} criado.",
                ephemeral=True
            )

    @commands.hybrid_command(name="boost", description='Mostra informações sobre boost')
    async def boost(self, interaction: discord.Interaction):
        # Criando a embed baseada no JSON fornecido
        embed = discord.Embed(
            title="Seja neko booster!",
            description="<a:emoji_61:1362870476195758290> Por que impulsionar o Neko Café? <a:emoji_61:1362870476195758290>\n\nAo impulsionar o Neko Café, você contribui diretamente para que nosso cantinho continue cada vez mais ativo, acolhedor e cheio de conteúdos especiais. E, como forma de agradecimento, você recebe mimos exclusivos pensados com muito carinho!\n\nConfira os benefícios que preparamos para nossos queridos Boosters:\n\n<a:emoji_60:1362870461859369051> Cargo exclusivo de Booster com cor personalizada\n<a:emoji_60:1362870461859369051> Acesso antecipado a eventos, sorteios e canais secretos\n<a:emoji_60:1362870461859369051> Prioridade em jogos, eventos e demais atividades do servidor\n<a:emoji_60:1362870461859369051> Espaço especial para divulgar suas redes sociais ou comissões\n<a:emoji_60:1362870461859369051> Direito a solicitar um cargo personalizado com nome e cor à sua escolha\n<a:emoji_60:1362870461859369051> Pessoa que impulsionarem nosso serv 1 vez eram ganhar 100k de sonhos por semana, as que impulsionar 2 irão ganhar 250k por semana como agradecimento!\n<a:emoji_60:1362870461859369051> E, claro, muito carinho da staff e da comunidade!\n\nImpulsionar o Neko Café é mais do que apoiar o servidor — é fazer parte de algo mágico.\nAgradecemos de coração por todo o apoio!",
            color=0x0FFF  # 4095 em hexadecimal
        )
        
        # Adicionando a imagem
        embed.set_image(url="https://cdn.discordapp.com/attachments/1334474182049796131/1373811365273141358/seja_booster_by_aishy_.png?ex=6831b3c9&is=68306249&hm=8855acce0a23379ca9dd045958db1067ec13f02e0db50e31d71a6621509245eb&")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Boost(bot))