import random
import logging
from discord.ext import commands, tasks
import discord
from discord import app_commands
from datetime import datetime, timedelta
import time

from database.boosts import addBoost, changeBoost, getBoosts
from database.roles import get_role_id, set_role_id
from helpers import checks

class Boost(commands.Cog, name="boost"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
    lastfirstbooster = None
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            servidor = after.guild
            onebooster = servidor.premium_subscriber_role
            doublebooster_role_id = get_role_id()
            
            if not doublebooster_role_id:
                return  # Sistema não configurado ainda
                
            doublebooster = servidor.get_role(doublebooster_role_id)
            
            if not doublebooster:
                self.logger.warning(f"Cargo Double Booster não encontrado (ID: {doublebooster_role_id})")
                return

            # Usuário perdeu o boost
            if onebooster in before.roles and onebooster not in after.roles:
                if doublebooster in after.roles:
                    await after.remove_roles(doublebooster, reason="Usuário não é mais booster")
                
                canal = after.guild.system_channel
                if canal:
                    embed = discord.Embed(
                        title="💔 Boost Removido",
                        description=f"{after.mention} não é mais Booster do servidor.",
                        color=0xFF6B6B
                    )
                    await canal.send(embed=embed)
                    
                await changeBoost(after, 0)
                self.logger.info(f"Usuário {after} perdeu o boost")
        except Exception as e:
            self.logger.error(f"Erro em on_member_update: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if not message.guild or not message.guild.system_channel:
                return
                
            if message.channel.id != message.guild.system_channel.id:
                return
                
            boost_message_types = [
                discord.MessageType.premium_guild_subscription,
                discord.MessageType.premium_guild_tier_1,
                discord.MessageType.premium_guild_tier_2,
                discord.MessageType.premium_guild_tier_3
            ]
            
            if message.type not in boost_message_types:
                return
                
            usuariobooster = message.author
            boosts = await addBoost(usuariobooster)
            
            servidor = message.guild
            doublebooster_role_id = get_role_id()
            
            if not doublebooster_role_id:
                embed = discord.Embed(
                    title="⚠️ Sistema não configurado",
                    description="O sistema de boosts não foi configurado ainda. Use `/configurar` para configurá-lo.",
                    color=0xFFB347
                )
                await message.channel.send(embed=embed)
                return
                
            doublebooster = servidor.get_role(doublebooster_role_id)
            
            if not doublebooster:
                self.logger.warning(f"Cargo Double Booster não encontrado (ID: {doublebooster_role_id})")
                return
            
            if boosts >= 2:
                await message.author.add_roles(doublebooster, reason="Usuário atingiu 2+ boosts")
                embed = discord.Embed(
                    title="🎉 Double Booster!",
                    description=f"{message.author.mention} agora é um **Double Booster**! Obrigado por impulsionar o servidor {boosts} vezes! 💜",
                    color=0x9B59B6
                )
                embed.set_thumbnail(url=message.author.display_avatar.url)
                await message.channel.send(embed=embed)
                self.logger.info(f"Usuário {message.author} virou Double Booster ({boosts} boosts)")
            else:
                embed = discord.Embed(
                    title="💜 Novo Booster!",
                    description=f"{message.author.mention} agora é um **Booster**! Obrigado por impulsionar o servidor! 🚀",
                    color=0xF368E0
                )
                embed.set_thumbnail(url=message.author.display_avatar.url)
                await message.channel.send(embed=embed)
                self.logger.info(f"Usuário {message.author} virou Booster ({boosts} boost)")
                
        except Exception as e:
            self.logger.error(f"Erro ao processar boost: {e}")

    @commands.hybrid_command(name="configurar", description='Configure o sistema de boosts do servidor')
    @app_commands.default_permissions(administrator=True)
    @checks.not_blacklisted()
    async def configurar(self, ctx: commands.Context):
        """Configura o sistema de boosts do servidor."""
        
        # Verificar se é uma interação ou comando de prefixo
        is_interaction = hasattr(ctx, 'interaction') and ctx.interaction
        
        if is_interaction:
            await ctx.interaction.response.send_message("⚙️ Configurando sistema de boosts...", ephemeral=True)
        else:
            await ctx.send("⚙️ Configurando sistema de boosts...")
            
        try:
            guild = ctx.guild
            
            # Verificar se já existe configuração
            existing_role_id = get_role_id()
            if existing_role_id:
                existing_role = guild.get_role(existing_role_id)
                if existing_role:
                    embed = discord.Embed(
                        title="⚠️ Sistema já configurado",
                        description=f"O sistema de boosts já está configurado com o cargo {existing_role.mention}.",
                        color=0xFFB347
                    )
                    if is_interaction:
                        await ctx.interaction.followup.send(embed=embed, ephemeral=True)
                    else:
                        await ctx.send(embed=embed)
                    return
            
            # Criar cargo Double Booster
            doublebooster_role = await guild.create_role(
                name="Double Booster",
                color=discord.Color.purple(),
                reason="Configuração automática do sistema de boosts"
            )
            set_role_id(doublebooster_role.id)
            self.logger.info(f"Cargo Double Booster criado: {doublebooster_role.name} (ID: {doublebooster_role.id})")

            # Configurar canal de notificações
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            
            notifications_channel = await guild.create_text_channel(
                name="notificações-boosts",
                overwrites=overwrites,
                reason="Canal para notificações de boost"
            )

            # Configurar canal do sistema
            await guild.edit(
                system_channel=notifications_channel,
                system_channel_flags=discord.SystemChannelFlags(premium_subscriptions=True),
                reason="Configuração do sistema de boosts"
            )
            
            self.logger.info(f"Canal de notificações criado: {notifications_channel.name} (ID: {notifications_channel.id})")

            # Sincronizar boosters existentes
            boosters_count = 0
            for member in guild.members:
                if member.premium_since is not None:
                    await changeBoost(member, 1)
                    boosters_count += 1
                    
            self.logger.info(f"Sincronizados {boosters_count} boosters existentes")
            
            # Enviar confirmação
            embed = discord.Embed(
                title="🎉 Sistema de Boosts Configurado!",
                description=(
                    "O sistema de boosts foi configurado com sucesso!\n\n"
                    f"**📋 Configurações:**\n"
                    f"• Cargo: {doublebooster_role.mention}\n"
                    f"• Canal: {notifications_channel.mention}\n"
                    f"• Boosters sincronizados: {boosters_count}\n\n"
                    "**ℹ️ Como funciona:**\n"
                    "• 1 boost = Cargo de Booster padrão\n"
                    "• 2+ boosts = Cargo Double Booster adicional"
                ),
                color=0x00FF00
            )
            embed.set_footer(text="Você pode editar os cargos e canais criados conforme necessário.")
            
            if is_interaction:
                await ctx.interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro de Permissão",
                description="Não tenho permissões suficientes para configurar o sistema. Verifique se tenho permissões de:",
                color=0xFF0000
            )
            embed.add_field(
                name="Permissões necessárias:",
                value="• Gerenciar Cargos\n• Gerenciar Canais\n• Gerenciar Servidor",
                inline=False
            )
            if is_interaction:
                await ctx.interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)
            
        except Exception as e:
            self.logger.error(f"Erro na configuração: {e}")
            embed = discord.Embed(
                title="❌ Erro na Configuração",
                description=f"Ocorreu um erro durante a configuração: `{str(e)}`",
                color=0xFF0000
            )
            if is_interaction:
                await ctx.interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

    @commands.hybrid_command(name="boost", description='Mostra informações sobre boost')
    @checks.not_blacklisted()
    async def boost(self, ctx: commands.Context):
        """Mostra informações sobre o sistema de boosts do servidor."""
        
        # Criando a embed baseada no JSON fornecido
        embed = discord.Embed(
            color=12428788,
            title="**<a:emoji_236:1375908714992767169> Benefícios Boost <a:emoji_236:1375908714992767169> **",
            description=(
                "**Um Boost:**\n"
                "<a:emoji_237:1375908735670554684> permissão para mandar mídias no chat-geral e em outros canais.\n"
                "<a:emoji_237:1375908735670554684> cargo destacado.\n"
                "<a:emoji_237:1375908735670554684> 5x entradas em drop e sorteios.\n"
                "<a:emoji_237:1375908735670554684> acesso a canais da categoria vip.\n"
                "<a:emoji_237:1375908735670554684> imunidade do AutoMod contra uso excessivo de mensagens repetidas.\n"
                "<a:emoji_237:1375908735670554684> imunidade a alguns requisitos de drops e sorteios.\n"
                "<a:emoji_237:1375908735670554684> prazo de 1 horas para resgatar prêmio de sorteios.\n"
                "<a:emoji_237:1375908735670554684> 6x mais xp na Loritta.\n"
                "<a:emoji_237:1375908735670554684> acesso de sorteios exclusivos.\n"
                "<a:emoji_237:1375908735670554684> 5x entradas em drop e sorteios.\n"
                "<a:emoji_237:1375908735670554684> permissão para usar efeito sonoro.\n"
                "<a:emoji_237:1375908735670554684> pode dar um <@&1361859905081966785> mensal para um amigo.\n"
                "<a:emoji_237:1375908735670554684> recebe um <@&1361860092450046092> até o Boost acabar.\n"
                "_\n"
                "**Dois Boost:**\n"
                "<a:emoji_237:1375908735670554684> todos os benefícios de um Boost.\n"
                "<a:emoji_237:1375908735670554684> prazo de 6 horas para resgatar prêmio de sorteios.\n"
                "<a:emoji_237:1375908735670554684> pode dar um <@&1361860092450046092> mensal para um amigo.\n"
                "<a:emoji_237:1375908735670554684> recebe um <@&1361860208304980048> até o Boost acabar."
            )
        )
        
        # Adicionando a imagem
        embed.set_image(url="https://cdn.discordapp.com/attachments/1334474182049796131/1373811365273141358/seja_booster_by_aishy_.png?ex=6835a849&is=683456c9&hm=c8da171df3ba1bc3df3c086ea5587d2a85a90176a3a7b9b9a4979751d56b04a8&")
        
        # Check if invoked as slash or prefix
        if hasattr(ctx, "interaction") and ctx.interaction is not None:
            await ctx.interaction.response.send_message(embed=embed)
        else:
            await ctx.send(embed=embed)
            
    @commands.hybrid_command(name="boosts", description='Mostra estatísticas de boosts do servidor')
    @checks.not_blacklisted()
    async def boosts_stats(self, ctx: commands.Context):
        """Mostra estatísticas de boosts do servidor."""
        
        if not ctx.guild:
            await ctx.send("Este comando só pode ser usado em servidores!", ephemeral=True)
            return
            
        try:
            guild = ctx.guild
            total_boosts = guild.premium_subscription_count or 0
            boost_tier = guild.premium_tier
            
            # Contar boosters únicos
            boosters = [member for member in guild.members if member.premium_since]
            unique_boosters = len(boosters)
            
            embed = discord.Embed(
                title=f"📊 Estatísticas de Boost - {guild.name}",
                color=0xF368E0
            )
            
            embed.add_field(
                name="🚀 Total de Boosts",
                value=f"**{total_boosts}** boosts",
                inline=True
            )
            
            embed.add_field(
                name="👥 Boosters Únicos",
                value=f"**{unique_boosters}** pessoas",
                inline=True
            )
            
            embed.add_field(
                name="⭐ Nível do Servidor",
                value=f"**Nível {boost_tier}**",
                inline=True
            )
            
            # Próximo nível
            next_level_boosts = {0: 2, 1: 7, 2: 14}.get(boost_tier, None)
            if next_level_boosts:
                remaining = next_level_boosts - total_boosts
                embed.add_field(
                    name="🎯 Próximo Nível",
                    value=f"Faltam **{remaining}** boosts para o nível {boost_tier + 1}",
                    inline=False
                )
            
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
                
            embed.set_footer(text="Use /boost para ver os benefícios de ser um booster!")
            
            if hasattr(ctx, "interaction") and ctx.interaction is not None:
                await ctx.interaction.response.send_message(embed=embed)
            else:
                await ctx.send(embed=embed)
                
        except Exception as e:
            self.logger.error(f"Erro ao buscar estatísticas de boost: {e}")
            await ctx.send("❌ Erro ao buscar estatísticas de boost.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Boost(bot))